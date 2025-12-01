"""
Agentic RAG Example
Agent decides IF retrieval is needed, WHICH source to query, and validates results
"""

import os
from openai import OpenAI
from typing import List, Dict, Optional

class AgenticRAG:
    """
    Agentic RAG implementation demonstrating:
    - LLM-based routing (decides if retrieval is needed)
    - Multi-source selection (web search, database, API)
    - Result validation
    - Context generation
    """
    
    def __init__(self):
        self.client = OpenAI()
        
        # Multiple knowledge sources
        self.sources = {
            "web_search": [
                {"text": "Latest AI news: GPT-5 announced with multimodal capabilities", "date": "2025-11-30"},
                {"text": "Breaking: New quantum computing breakthrough achieved", "date": "2025-11-29"}
            ],
            "database": [
                {"text": "Python is a high-level programming language", "category": "programming"},
                {"text": "Machine learning enables systems to learn from data", "category": "ai"}
            ],
            "api": [
                {"text": "Current weather: 72°F, Sunny", "location": "San Francisco"},
                {"text": "Stock price AAPL: $195.32", "symbol": "AAPL"}
            ]
        }
    
    def route_query(self, query: str) -> Dict:
        """
        Agent decides:
        1. Does this query need retrieval?
        2. Which source(s) should be queried?
        """
        routing_prompt = f"""Analyze this query and decide:
1. Does it need external information retrieval? (yes/no)
2. If yes, which source(s): web_search, database, or api?
3. Why?

Query: {query}

Respond in this format:
NEEDS_RETRIEVAL: yes/no
SOURCES: [source1, source2, ...]
REASONING: explanation"""

        response = self.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are a routing agent that decides if and where to retrieve information."},
                {"role": "user", "content": routing_prompt}
            ]
        )
        
        # Parse response (simplified)
        content = response.choices[0].message.content
        needs_retrieval = "yes" in content.split("NEEDS_RETRIEVAL:")[1].split("\n")[0].lower()
        
        # Extract sources
        sources = []
        if "web_search" in content:
            sources.append("web_search")
        if "database" in content:
            sources.append("database")
        if "api" in content:
            sources.append("api")
        
        return {
            "needs_retrieval": needs_retrieval,
            "sources": sources,
            "reasoning": content
        }
    
    def retrieve_from_sources(self, query: str, sources: List[str]) -> List[Dict]:
        """Retrieve information from selected sources"""
        results = []
        
        for source in sources:
            if source in self.sources:
                # In production, this would call actual APIs, databases, or search engines
                source_results = self.sources[source]
                results.extend([{**item, "source": source} for item in source_results])
        
        return results
    
    def validate_results(self, query: str, results: List[Dict]) -> Dict:
        """Agent validates if retrieved results are useful"""
        results_text = "\n".join([f"- {r.get('text', str(r))}" for r in results])
        
        validation_prompt = f"""Query: {query}

Retrieved results:
{results_text}

Are these results relevant and useful for answering the query?
Rate relevance (0-10) and explain why.

Format:
RELEVANCE_SCORE: X
EXPLANATION: ...
SHOULD_USE: yes/no"""

        response = self.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are a validation agent that assesses result quality."},
                {"role": "user", "content": validation_prompt}
            ]
        )
        
        content = response.choices[0].message.content
        should_use = "yes" in content.split("SHOULD_USE:")[1].lower() if "SHOULD_USE:" in content else True
        
        return {
            "should_use": should_use,
            "validation_response": content,
            "results": results if should_use else []
        }
    
    def generate_response(self, query: str) -> Dict:
        """
        Agentic RAG Pipeline:
        1. Route query (decide if/where to retrieve)
        2. Retrieve from selected sources
        3. Validate results
        4. Generate response
        """
        # Step 1: Route
        routing = self.route_query(query)
        
        if not routing["needs_retrieval"]:
            # Direct response without retrieval
            response = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": query}
                ]
            )
            return {
                "query": query,
                "routing": routing,
                "retrieval": None,
                "validation": None,
                "response": response.choices[0].message.content,
                "approach": "Agentic RAG - No retrieval needed"
            }
        
        # Step 2: Retrieve
        results = self.retrieve_from_sources(query, routing["sources"])
        
        # Step 3: Validate
        validation = self.validate_results(query, results)
        
        # Step 4: Generate
        if validation["should_use"]:
            context = "\n\n".join([f"[{r['source']}] {r.get('text', str(r))}" for r in validation["results"]])
            augmented_prompt = f"""Context from multiple sources:
{context}

Question: {query}

Answer based on the context provided."""
        else:
            augmented_prompt = query
        
        response = self.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": augmented_prompt}
            ]
        )
        
        return {
            "query": query,
            "routing": routing,
            "retrieval": results,
            "validation": validation,
            "response": response.choices[0].message.content,
            "approach": "Agentic RAG - Read-only via tool calls"
        }


def main():
    """Demonstrate Agentic RAG workflow"""
    print("=" * 60)
    print("Agentic RAG Example: Agent-Driven Retrieval")
    print("=" * 60)
    
    agent = AgenticRAG()
    
    # Example queries
    queries = [
        "What is machine learning?",
        "What's the latest AI news?",
    ]
    
    for query in queries:
        print(f"\n{'=' * 60}")
        print(f"Query: {query}")
        print("-" * 60)
        
        result = agent.generate_response(query)
        
        print(f"\nRouting Decision:")
        print(f"  Needs Retrieval: {result['routing']['needs_retrieval']}")
        if result['routing']['needs_retrieval']:
            print(f"  Sources Selected: {result['routing']['sources']}")
        
        if result['retrieval']:
            print(f"\nRetrieved Data:")
            for item in result['retrieval']:
                print(f"  [{item['source']}] {item.get('text', str(item))}")
        
        if result['validation']:
            print(f"\nValidation: {'Passed' if result['validation']['should_use'] else 'Failed'}")
        
        print(f"\nFinal Response:")
        print(f"  {result['response']}")
        
        print(f"\nApproach: {result['approach']}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
