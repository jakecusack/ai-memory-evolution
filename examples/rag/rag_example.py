"""
RAG (Retrieval-Augmented Generation) Example
Read-only, one-shot retrieval and generation
"""

import os
from openai import OpenAI

class SimpleRAG:
    """
    Simple RAG implementation demonstrating:
    - Query input
    - Embedding generation
    - Vector DB search
    - Context retrieval
    - LLM generation
    """
    
    def __init__(self):
        self.client = OpenAI()
        self.knowledge_base = [
            {
                "id": 1,
                "text": "Python is a high-level programming language known for its simplicity and readability.",
                "metadata": {"category": "programming"}
            },
            {
                "id": 2,
                "text": "Machine learning is a subset of artificial intelligence that enables systems to learn from data.",
                "metadata": {"category": "ai"}
            },
            {
                "id": 3,
                "text": "Vector databases store and retrieve data based on semantic similarity using embeddings.",
                "metadata": {"category": "database"}
            }
        ]
        
    def generate_embedding(self, text: str) -> list:
        """Generate embeddings for text using OpenAI"""
        response = self.client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        return response.data[0].embedding
    
    def retrieve_context(self, query: str, top_k: int = 2) -> list:
        """
        Retrieve relevant context from knowledge base
        In production, this would use a vector database like Pinecone, Weaviate, or Qdrant
        """
        # Simplified retrieval - in production, use cosine similarity with embeddings
        query_lower = query.lower()
        relevant_docs = []
        
        for doc in self.knowledge_base:
            # Simple keyword matching for demonstration
            if any(word in doc["text"].lower() for word in query_lower.split()):
                relevant_docs.append(doc)
        
        return relevant_docs[:top_k]
    
    def generate_response(self, query: str) -> dict:
        """
        RAG Pipeline:
        1. Retrieve relevant context
        2. Augment prompt with context
        3. Generate response
        """
        # Step 1: Retrieve context
        context_docs = self.retrieve_context(query)
        context = "\n\n".join([doc["text"] for doc in context_docs])
        
        # Step 2: Augment prompt
        augmented_prompt = f"""Context information:
{context}

Question: {query}

Answer the question based on the context provided above."""
        
        # Step 3: Generate response
        response = self.client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that answers questions based on the provided context."},
                {"role": "user", "content": augmented_prompt}
            ]
        )
        
        return {
            "query": query,
            "context_used": context_docs,
            "response": response.choices[0].message.content,
            "approach": "RAG - Read-only, one-shot retrieval"
        }


def main():
    """Demonstrate RAG workflow"""
    print("=" * 60)
    print("RAG Example: Read-Only, One-Shot Retrieval")
    print("=" * 60)
    
    rag = SimpleRAG()
    
    # Example query
    query = "What is machine learning?"
    
    print(f"\nQuery: {query}")
    print("\n" + "-" * 60)
    
    result = rag.generate_response(query)
    
    print(f"\nContext Retrieved:")
    for doc in result["context_used"]:
        print(f"  - {doc['text']}")
    
    print(f"\nResponse:")
    print(f"  {result['response']}")
    
    print(f"\nApproach: {result['approach']}")
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
