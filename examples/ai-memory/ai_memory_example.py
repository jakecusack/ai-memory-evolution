"""
AI Memory Example
Read AND write to external knowledge, learns from interactions
Demonstrates continual learning and personalization
"""

import os
import json
from datetime import datetime
from openai import OpenAI
from typing import List, Dict, Optional

class AIMemorySystem:
    """
    AI Memory implementation demonstrating:
    - Search in memory (read)
    - Tools for memory operations
    - Store in memory (write)
    - Memory store with episodic, semantic, and procedural memory
    - Continual learning from interactions
    """
    
    def __init__(self, memory_file: str = "memory_store.json"):
        self.client = OpenAI()
        self.memory_file = memory_file
        
        # Initialize memory types
        self.memory = {
            "episodic": [],      # Past conversations and events
            "semantic": [],       # Facts and knowledge
            "procedural": []      # User preferences and patterns
        }
        
        self.load_memory()
    
    def load_memory(self):
        """Load memory from persistent storage"""
        if os.path.exists(self.memory_file):
            with open(self.memory_file, 'r') as f:
                self.memory = json.load(f)
    
    def save_memory(self):
        """Save memory to persistent storage"""
        with open(self.memory_file, 'w') as f:
            json.dump(self.memory, f, indent=2)
    
    def search_memory(self, query: str, memory_types: Optional[List[str]] = None) -> List[Dict]:
        """
        Search across memory types
        In production, this would use vector similarity search
        """
        if memory_types is None:
            memory_types = ["episodic", "semantic", "procedural"]
        
        results = []
        query_lower = query.lower()
        
        for mem_type in memory_types:
            if mem_type in self.memory:
                for item in self.memory[mem_type]:
                    # Simple keyword matching for demonstration
                    content = item.get("content", "").lower()
                    if any(word in content for word in query_lower.split()):
                        results.append({**item, "memory_type": mem_type})
        
        return results
    
    def store_memory(self, content: str, memory_type: str, metadata: Optional[Dict] = None) -> Dict:
        """
        Store new information in memory
        This is the key difference from RAG - we can WRITE to memory
        """
        memory_entry = {
            "id": len(self.memory[memory_type]) + 1,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        
        self.memory[memory_type].append(memory_entry)
        self.save_memory()
        
        return memory_entry
    
    def extract_learnings(self, conversation: str) -> Dict:
        """
        Extract what should be remembered from a conversation
        This enables continual learning
        """
        extraction_prompt = f"""Analyze this conversation and extract:
1. Facts to remember (semantic memory)
2. User preferences or patterns (procedural memory)
3. Important events or context (episodic memory)

Conversation:
{conversation}

Format your response as:
SEMANTIC: [fact1, fact2, ...]
PROCEDURAL: [preference1, preference2, ...]
EPISODIC: [event1, event2, ...]"""

        response = self.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are a memory extraction agent that identifies what to remember."},
                {"role": "user", "content": extraction_prompt}
            ]
        )
        
        return {
            "extraction": response.choices[0].message.content,
            "timestamp": datetime.now().isoformat()
        }
    
    def decide_memory_action(self, query: str) -> Dict:
        """
        Agent decides what memory operations to perform
        - Should we search memory?
        - Should we store something?
        - What memory types are relevant?
        """
        decision_prompt = f"""For this query, decide:
1. Should we search memory? (yes/no)
2. Which memory types to search? (episodic, semantic, procedural)
3. Will this interaction create new memories? (yes/no)

Query: {query}

Format:
SEARCH_MEMORY: yes/no
MEMORY_TYPES: [type1, type2, ...]
CREATE_MEMORY: yes/no
REASONING: explanation"""

        response = self.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are a memory management agent."},
                {"role": "user", "content": decision_prompt}
            ]
        )
        
        content = response.choices[0].message.content
        
        # Parse decision
        search_memory = "yes" in content.split("SEARCH_MEMORY:")[1].split("\n")[0].lower()
        create_memory = "yes" in content.split("CREATE_MEMORY:")[1].split("\n")[0].lower() if "CREATE_MEMORY:" in content else True
        
        memory_types = []
        if "episodic" in content:
            memory_types.append("episodic")
        if "semantic" in content:
            memory_types.append("semantic")
        if "procedural" in content:
            memory_types.append("procedural")
        
        return {
            "search_memory": search_memory,
            "memory_types": memory_types or ["episodic", "semantic", "procedural"],
            "create_memory": create_memory,
            "reasoning": content
        }
    
    def generate_response(self, query: str, user_id: str = "user_001") -> Dict:
        """
        AI Memory Pipeline:
        1. Decide memory actions
        2. Search memory if needed
        3. Generate response with memory context
        4. Extract and store learnings
        """
        # Step 1: Decide memory actions
        decision = self.decide_memory_action(query)
        
        # Step 2: Search memory
        memory_context = []
        if decision["search_memory"]:
            memory_context = self.search_memory(query, decision["memory_types"])
        
        # Step 3: Generate response
        if memory_context:
            context_text = "\n".join([
                f"[{m['memory_type']}] {m['content']} (from {m['timestamp']})"
                for m in memory_context
            ])
            augmented_prompt = f"""Relevant memories:
{context_text}

User query: {query}

Respond naturally, incorporating relevant memories to personalize your response."""
        else:
            augmented_prompt = query
        
        response = self.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant with memory. Use past context to personalize responses."},
                {"role": "user", "content": augmented_prompt}
            ]
        )
        
        response_text = response.choices[0].message.content
        
        # Step 4: Extract and store learnings
        new_memories = []
        if decision["create_memory"]:
            conversation = f"User: {query}\nAssistant: {response_text}"
            learnings = self.extract_learnings(conversation)
            
            # Store episodic memory of this interaction
            episodic_entry = self.store_memory(
                content=f"Conversation with {user_id}: {query[:100]}...",
                memory_type="episodic",
                metadata={"user_id": user_id, "query": query}
            )
            new_memories.append(episodic_entry)
        
        return {
            "query": query,
            "decision": decision,
            "memory_context": memory_context,
            "response": response_text,
            "new_memories": new_memories,
            "approach": "AI Memory - Read-write via tool calls with continual learning",
            "memory_stats": {
                "episodic_count": len(self.memory["episodic"]),
                "semantic_count": len(self.memory["semantic"]),
                "procedural_count": len(self.memory["procedural"])
            }
        }
    
    def add_user_preference(self, user_id: str, preference: str):
        """Manually add a user preference (procedural memory)"""
        return self.store_memory(
            content=preference,
            memory_type="procedural",
            metadata={"user_id": user_id, "type": "preference"}
        )
    
    def add_fact(self, fact: str, source: str = "user"):
        """Manually add a fact (semantic memory)"""
        return self.store_memory(
            content=fact,
            memory_type="semantic",
            metadata={"source": source}
        )


def main():
    """Demonstrate AI Memory workflow"""
    print("=" * 60)
    print("AI Memory Example: Read-Write Memory with Continual Learning")
    print("=" * 60)
    
    # Initialize memory system
    memory_system = AIMemorySystem(memory_file="/home/ubuntu/ai-memory-evolution/examples/ai-memory/memory_store.json")
    
    # Seed some initial memories
    print("\n[Setup] Adding initial memories...")
    memory_system.add_user_preference("user_001", "Prefers concise explanations")
    memory_system.add_user_preference("user_001", "Interested in AI and machine learning")
    memory_system.add_fact("Python is a popular programming language for AI", "knowledge_base")
    
    # Example interactions
    queries = [
        "What is machine learning?",
        "Can you remind me what I'm interested in?",
        "I prefer detailed explanations now, not concise ones"
    ]
    
    for i, query in enumerate(queries, 1):
        print(f"\n{'=' * 60}")
        print(f"Interaction {i}")
        print(f"Query: {query}")
        print("-" * 60)
        
        result = memory_system.generate_response(query)
        
        print(f"\nMemory Decision:")
        print(f"  Search Memory: {result['decision']['search_memory']}")
        print(f"  Memory Types: {result['decision']['memory_types']}")
        print(f"  Create Memory: {result['decision']['create_memory']}")
        
        if result['memory_context']:
            print(f"\nMemory Context Used:")
            for mem in result['memory_context']:
                print(f"  [{mem['memory_type']}] {mem['content']}")
        
        print(f"\nResponse:")
        print(f"  {result['response']}")
        
        if result['new_memories']:
            print(f"\nNew Memories Stored:")
            for mem in result['new_memories']:
                print(f"  [{mem['memory_type']}] {mem['content']}")
        
        print(f"\nMemory Stats:")
        print(f"  Episodic: {result['memory_stats']['episodic_count']}")
        print(f"  Semantic: {result['memory_stats']['semantic_count']}")
        print(f"  Procedural: {result['memory_stats']['procedural_count']}")
    
    print("\n" + "=" * 60)
    print("Key Difference: Memory grows over time through interactions!")
    print("=" * 60)


if __name__ == "__main__":
    main()
