# AI Memory Evolution: From RAG to Continual Learning

This repository provides a hands-on demonstration of the evolution of AI memory, from simple Retrieval-Augmented Generation (RAG) to agentic systems with read-write memory capabilities. It includes Python code examples and an n8n workflow to illustrate the concepts visually.

![The Evolution of AI Memory](/home/ubuntu/ai-memory-evolution/assets/evolution-infographic.png)

## Overview

The journey from static information retrieval to adaptive AI systems is marked by three key milestones:

1.  **RAG (2020-2023):** The initial approach involved retrieving information once and generating a response. This was a read-only, one-shot process that often suffered from irrelevant context retrieval.

2.  **Agentic RAG:** The next step introduced an agent that could make decisions. The agent determines *if* retrieval is necessary, *which* data source to query, and *validates* the usefulness of the results. However, it remains a read-only architecture.

3.  **AI Memory:** The current frontier is AI Memory, where agents can both **read from and write to** an external knowledge base. This enables true personalization and continual learning, as the agent remembers past interactions, user preferences, and context.

This repository provides practical examples of each of these stages.

## Project Structure

```
/ai-memory-evolution
├── assets
│   └── evolution-infographic.png
├── docs
│   └── (additional documentation)
├── examples
│   ├── rag
│   │   └── rag_example.py
│   ├── agentic-rag
│   │   └── agentic_rag_example.py
│   └── ai-memory
│       ├── ai_memory_example.py
│       └── memory_store.json
├── n8n-workflows
│   └── ai-memory-evolution-workflow.json
├── requirements.txt
└── README.md
```

-   **`assets`**: Contains the infographic image.
-   **`docs`**: For any additional documentation.
-   **`examples`**: Contains standalone Python scripts for each of the three approaches.
-   **`n8n-workflows`**: Contains the JSON file for the n8n workflow.

## Getting Started with the Python Examples

### Prerequisites

-   Python 3.8+
-   An OpenAI API key

### Installation

1.  **Clone the repository:**

    ```bash
    gh repo clone <your-username>/ai-memory-evolution
    cd ai-memory-evolution
    ```

2.  **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up your OpenAI API Key:**

    Create a `.env` file in the root of the project and add your API key:

    ```
    OPENAI_API_KEY=\
your-api-key-here
    ```

### Running the Examples

Navigate to the respective directories and run the Python scripts:

-   **RAG Example:**

    ```bash
    python examples/rag/rag_example.py
    ```

-   **Agentic RAG Example:**

    ```bash
    python examples/agentic-rag/agentic_rag_example.py
    ```

-   **AI Memory Example:**

    ```bash
    python examples/ai-memory/ai_memory_example.py
    ```

## Using the n8n Workflow

The `n8n-workflows/ai-memory-evolution-workflow.json` file contains a workflow that visually represents the three approaches in parallel.

### How to Import and Use

1.  **Open your n8n instance.**
2.  Go to the **Workflows** page.
3.  Click on **Import from File** and select the `ai-memory-evolution-workflow.json` file.
4.  The workflow will be imported. You may need to configure your OpenAI credentials in the LLM nodes.
5.  Click **Test workflow** to run the demonstration.

### Workflow Logic

The workflow is structured with three parallel paths, one for each approach:

1.  **RAG Path:** A simple LLM call with hardcoded context to simulate one-shot retrieval.
2.  **Agentic RAG Path:** An LLM call with a more complex prompt that asks the agent to decide, retrieve, and validate (all simulated within the prompt).
3.  **AI Memory Path:** An LLM call that uses memory context (user preferences) and demonstrates how the agent can write back to memory.

All three paths merge at the end to display a comparison of the results.

## The Power of AI Memory

The key takeaway is that AI Memory, with its read-write capabilities, is what bridges the gap between static models and truly adaptive AI systems. By allowing agents to learn from every interaction, we can build systems that are personalized, context-aware, and continuously improving.

While this introduces new challenges like memory corruption and management, frameworks like [Graphiti](https://github.com/Graphiti-AI/graphiti) are emerging to solve these problems by providing robust infrastructure for building real-time knowledge graphs.

---

*This repository was created by Manus, an autonomous AI agent.*
