# n8n Workflow Guide: AI Memory Evolution Demo

This guide will help you set up and run the AI Memory Evolution demonstration workflow in n8n.

## Prerequisites

- An active n8n instance (cloud or self-hosted)
- OpenAI API credentials configured in n8n
- Basic familiarity with n8n workflows

## Importing the Workflow

### Step 1: Download the Workflow File

The workflow file is located at: `n8n-workflows/ai-memory-evolution-workflow.json`

### Step 2: Import into n8n

1. Open your n8n instance
2. Click on **Workflows** in the left sidebar
3. Click the **Import from File** button (or use the menu: **Workflow** → **Import from File**)
4. Select the `ai-memory-evolution-workflow.json` file
5. The workflow will be imported and opened automatically

### Step 3: Configure Credentials

The workflow uses OpenAI's API for LLM calls. You need to configure your credentials:

1. Click on any of the LLM nodes (e.g., "LLM - RAG")
2. In the node settings, find the **Credentials** section
3. If you already have OpenAI credentials configured:
   - Select them from the dropdown
4. If not, click **Create New Credential**:
   - Enter your OpenAI API key
   - Give it a name (e.g., "OpenAI")
   - Click **Save**
5. Repeat for all three LLM nodes (RAG, Agentic RAG, AI Memory)

## Understanding the Workflow

### Workflow Structure

The workflow demonstrates three parallel execution paths, each representing a different approach to AI memory:

```
                    ┌─────────────────┐
                    │  Manual Trigger │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
        ┌─────────┐    ┌─────────┐    ┌─────────┐
        │   RAG   │    │ Agentic │    │   AI    │
        │  Query  │    │   RAG   │    │ Memory  │
        │         │    │  Query  │    │  Query  │
        └────┬────┘    └────┬────┘    └────┬────┘
             │              │              │
             ▼              ▼              ▼
        ┌─────────┐    ┌─────────┐    ┌─────────┐
        │   LLM   │    │   LLM   │    │   LLM   │
        │   RAG   │    │ Agentic │    │ Memory  │
        └────┬────┘    └────┬────┘    └────┬────┘
             │              │              │
             ▼              ▼              ▼
        ┌─────────┐    ┌─────────┐    ┌─────────┐
        │ Format  │    │ Format  │    │ Format  │
        │Response │    │Response │    │Response │
        └────┬────┘    └────┬────┘    └────┬────┘
             │              │              │
             └──────────────┼──────────────┘
                            ▼
                    ┌───────────────┐
                    │ Merge Results │
                    └───────────────┘
```

### Node Descriptions

**1. Manual Trigger**
- Starts the workflow when you click "Test workflow"
- Splits execution into three parallel paths

**2. Set Query Nodes** (3 nodes)
- `Set RAG Query`: Prepares input for the RAG path
- `Set Agentic RAG Query`: Prepares input for the Agentic RAG path
- `Set AI Memory Query`: Prepares input for the AI Memory path

Each sets the same query but labels it with the approach type.

**3. LLM Nodes** (3 nodes)
- `LLM - RAG`: Demonstrates simple context-based retrieval
- `LLM - Agentic RAG`: Demonstrates agent-driven decision-making
- `LLM - AI Memory`: Demonstrates read-write memory capabilities

Each node uses different prompts to simulate the respective approach.

**4. Format Response Nodes** (3 nodes)
- Format the LLM output with metadata about the approach
- Add characteristics that distinguish each method

**5. Merge All Results**
- Combines outputs from all three paths
- Enables side-by-side comparison

**6. Sticky Notes**
- Provide visual documentation within the workflow
- Explain each approach and its characteristics

## Running the Workflow

### Execute the Workflow

1. Click the **Test workflow** button in the top-right corner
2. The workflow will execute all three paths in parallel
3. Watch as each node processes and displays results

### Viewing Results

After execution, you can view the output of each node:

1. Click on any node to see its output in the right panel
2. The **Merge All Results** node shows the combined output from all three approaches
3. Compare the responses to see the differences between RAG, Agentic RAG, and AI Memory

### Expected Output

Each path will return:

- **Approach**: The name of the method (RAG, Agentic RAG, or AI Memory)
- **Response**: The LLM's answer to the query
- **Characteristics**: Key features of that approach

## Customizing the Workflow

### Changing the Query

To test with different queries:

1. Click on any of the **Set Query** nodes
2. Find the `query` assignment
3. Change the value to your desired question
4. Repeat for all three paths (or use different queries for each)
5. Click **Test workflow** to see results with the new query

### Modifying Prompts

To adjust how each approach works:

1. Click on an **LLM** node
2. Find the **Messages** section
3. Edit the prompt content
4. You can:
   - Add more context
   - Change the instructions
   - Simulate different data sources
5. Save and test

### Adding Real Data Sources

To make the workflow more realistic, you can:

**For RAG:**
- Add a **Vector Store** node before the LLM
- Connect to Pinecone, Weaviate, or Supabase
- Perform actual vector similarity search

**For Agentic RAG:**
- Add **HTTP Request** nodes for web search
- Add **Database** nodes for structured data
- Use **IF** nodes for routing logic

**For AI Memory:**
- Add **Database** nodes to store/retrieve memories
- Use **Supabase** or **PostgreSQL** for persistence
- Implement read and write operations

## Advanced Configuration

### Using Different LLM Models

You can change the model used in each path:

1. Click on an LLM node
2. Find the **Model** dropdown
3. Select a different model (e.g., `gpt-4`, `gpt-4.1-nano`)
4. Different models may produce different results

### Adding Error Handling

To make the workflow more robust:

1. Add **Error Trigger** nodes
2. Implement retry logic with **Loop** nodes
3. Add **IF** nodes to handle edge cases

### Implementing Real Memory

To implement actual memory storage:

1. Add a **Supabase** or **PostgreSQL** node
2. Create tables for episodic, semantic, and procedural memory
3. Before the LLM node, add a **Database Query** to retrieve memories
4. After the LLM node, add a **Database Insert** to store new memories

Example memory table schema:

```sql
CREATE TABLE memories (
  id SERIAL PRIMARY KEY,
  user_id VARCHAR(255),
  memory_type VARCHAR(50), -- 'episodic', 'semantic', 'procedural'
  content TEXT,
  metadata JSONB,
  timestamp TIMESTAMP DEFAULT NOW()
);
```

## Troubleshooting

### Issue: "Credentials not found"

**Solution**: Make sure you've configured OpenAI credentials in all three LLM nodes.

### Issue: "Rate limit exceeded"

**Solution**: The workflow makes three LLM calls in parallel. If you hit rate limits:
- Wait a moment and try again
- Modify the workflow to execute paths sequentially instead of in parallel

### Issue: "Workflow execution failed"

**Solution**: 
- Check the error message in the failed node
- Verify your OpenAI API key is valid
- Ensure you have sufficient credits in your OpenAI account

### Issue: "Empty response from LLM"

**Solution**:
- Check that the prompt is properly formatted
- Verify the model name is correct
- Ensure the query is being passed correctly from the Set nodes

## Next Steps

After familiarizing yourself with the basic workflow:

1. **Extend the Examples**: Add more complex queries and scenarios
2. **Integrate Real Data**: Connect to actual databases and APIs
3. **Build a UI**: Create a frontend that calls this workflow via webhook
4. **Add Persistence**: Implement real memory storage for the AI Memory path
5. **Deploy**: Set up the workflow to run on a schedule or via webhook

## Resources

- [n8n Documentation](https://docs.n8n.io/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Graphiti Framework](https://github.com/Graphiti-AI/graphiti) - For production memory systems
- [Implementation Guide](./IMPLEMENTATION_GUIDE.md) - Detailed technical guide

---

*This guide was created by Manus AI as part of the AI Memory Evolution demonstration project.*
