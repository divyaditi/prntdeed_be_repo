# Design Notes and Implementation Choices

I built this assistant around a lightweight RAG pattern that keeps answers grounded in PrintFlow documentation instead of relying on the model to recall facts from memory. The core pieces are configured in [src/constant.py](src/constant.py), the retrieval pipeline is implemented in [src/utils/chunking_utils.py](src/utils/chunking_utils.py), and the tool-enabled agent is wired in [src/client/grok_client.py](src/client/grok_client.py).

---

## Why LangChain + Reason-and-Execute Architecture

A normal LLM call cannot reliably decide whether to invoke tools or retrieve documents based on user intent. The assistant needs to:

1. **Reason** about the query (Is this a feature question? A file format question?)
2. **Plan** a response strategy (Should I call `check_tier_feature`? Should I search documentation?)
3. **Execute** the chosen tools and compose the answer

LangChain's `create_tool_calling_agent` + `AgentExecutor` provides this orchestration layer. The agent receives the user query, evaluates available tools (`check_tier_feature` and `printflow_document_search`), and autonomously decides which tools to invoke. This is far more robust than hardcoding conditional logic in the application code.

### LangChain Abstractions Used

Beyond agent orchestration, LangChain provides key document-processing abstractions:

- **`MarkdownHeaderTextSplitter`**: Preserves document hierarchy by splitting on markdown headers (`#`, `##`, `###`). This ensures related sections stay together, critical for support docs where concepts span multiple levels.
- **`RecursiveCharacterTextSplitter`**: Falls back to character-level splitting when a chunk exceeds the threshold, using separators like `\n\n` and `\n`. This maintains paragraph cohesion better than naive line-based splitting.
- **`langchain_core.tools`**: The `@tool` decorator wraps functions as LLM-callable tools with auto-generated schemas. Both `check_tier_feature` and `printflow_document_search` are decorated this way, allowing the agent to invoke them with type-checked arguments.

This combination creates a linear, maintainable pipeline: load → split → embed → store → retrieve → reason → execute.

---

## Chunking Strategy: 250–400 Token Range

After analyzing the PrintFlow documentation, I chose a smaller chunk size than initially configured:

### Why 250–400 Tokens (vs. 1000)?

**Data Structure Analysis:**
- `policies.md`: Contains 15 structured subsections (Subscription Plans, Overage Policy, Storage Policy, etc.), each with 100–300 words
- `onboarding_faq.md`: Contains 20+ Q&A pairs, each 50–200 words
- `products.md`: Contains product specs organized by printing service (Offset, Digital, Wide Format) with tables and lists

**Problem with Larger Chunks (1000 tokens):**
- A 1000-token chunk spans multiple distinct topics (e.g., "Starter Plan" → "Pro Plan" → "Enterprise Plan" all in one chunk)
- When the LLM retrieves this, it wastes context on irrelevant plan details (e.g., retrieving Enterprise features when the user only asked about Starter)
- Increases noise in the prompt, making the model more prone to conflating plan benefits

**250–400 Token Sweet Spot:**
- Each chunk typically covers ONE coherent topic: a single plan, a single product type, a single FAQ answer
- For example, the "Pro Plan" features table is ~200 tokens—fits perfectly in a single chunk with its heading
- API rate limit info ("60 req/min" for Pro) is ~50 tokens—grouped with API access details
- Reduces retrieval ambiguity: when the user asks "What's the API rate limit?", the system retrieves the Pro/Enterprise API chunk, not an Enterprise-only feature chunk

**Alignment with Vector Search:**
- Smaller chunks improve recall precision. The embedding model (`BAAI/bge-m3`, 1024-dim) is designed for dense retrieval; it excels at matching semantic relevance within focused chunks
- A 250–400 token chunk is large enough to retain local context but small enough to avoid information dilution

**Practical Impact on Grounding:**
- The tool `check_tier_feature` returns exact feature availability (e.g., "VDP is available on Pro and Enterprise")
- The document retrieval then surfaces the supporting context from a single, focused chunk
- The LLM can confidently cite both the tool result and the retrieved documentation without contradiction

### Overlap Rationale

A `CHUNK_OVERLAP = 50` (updated from 100) bridges boundaries without creating redundancy:
- Feature tables in `policies.md` have headers like "### Pro — $199/month" followed by a table
- 50-token overlap ensures the next chunk includes the header and first few rows, maintaining context
- Prevents information loss at chunk boundaries where a concept spans two sections

---

## Embedding Model: BAAI/bge-m3

I chose `BAAI/bge-m3` over general-purpose models like `all-MiniLM-L6-v2` for several reasons:

### Higher Dimensionality
- **bge-m3**: 1024 dimensions
- **all-MiniLM-L6-v2**: 384 dimensions
- Higher dimensions allow more nuanced semantic capture, especially important for nuanced policy language (e.g., "Net-30 invoicing" vs. "Net-45 terms")

### Multi-Lingual & Dense Retrieval Optimization
- **bge-m3** is trained on a diverse corpus including technical documentation and Q&A pairs
- Excels at matching FAQ questions to support docs (dense retrieval task)
- Scores higher on BEIR benchmarks for similar retrieval tasks

### Lightweight & Local
- ~500MB model size; downloads once and runs locally
- No external API calls during inference
- Works reliably in offline environments

---

## Tool Calling: Two-Tool Architecture

### Tool 1: `check_tier_feature(feature: str, tier: str) → str`
Maps feature names (e.g., "api_access", "webhooks", "vdp") to subscription tiers. This tool is **deterministic** and always correct because it consults the hardcoded `FEATURE_PLAN_MAP` in [src/constant.py](src/constant.py). The LLM never hallucinates feature availability; it defers to the tool.

### Tool 2: `printflow_document_search(query: str) → str`
Searches the vector store for the top 3 most relevant document chunks. This bridges RAG with tool calling: the LLM can explicitly ask for documentation when it needs grounding for an answer.

**Why Two Tools?**
- **Separation of Concerns**: Feature availability is deterministic (tool 1); documentation is semantic (tool 2)
- **Agent Routing**: For queries like "Is API access on Starter?", the agent routes to tool 1. For "How do I add team members?", it routes to tool 2. For complex queries, it may call both.
- **Reduced Hallucination**: Tool 1 removes ambiguity; tool 2 ensures answers cite actual documentation.

---

## Trade-offs and Limitations

**Trade-off: Chunk Size vs. Retrieval Precision**
- Smaller chunks improve retrieval precision but increase the number of chunks to store (~150 chunks vs. ~30 with 1000-token size)
- This trade-off favors precision, reducing noise in the LLM's context window

**Trade-off: Multi-Turn Memory**
- The current implementation is stateless; each query is independent
- A production system would maintain conversation history, but this adds complexity without improving the core RAG quality
- Stateless design allows for easier horizontal scaling and debugging

**Limitation: No Fine-Tuned Reranker**
- The system uses raw vector similarity to rank chunks. A learned reranker (e.g., `cross-encoder/ms-marco-MiniLM-L-6-v2`) could improve ranking precision
- Trade-off: simplicity vs. marginal retrieval gains

**Limitation: No Streaming Response**
- Responses are generated synchronously and returned as complete text
- Streaming would improve perceived latency but adds complexity to the FastAPI response layer

---

## Why This Design Works for PrintFlow

PrintFlow's onboarding challenge is fundamentally about **accuracy under routing complexity**:
- Users ask about specific plans, file formats, SLAs, and features
- Wrong answers (e.g., "API is available on Starter") cause support escalations
- The RAG + tool-calling architecture eliminates guessing: the LLM retrieves facts from documentation and defers to tools for structured data

The 250–400 token chunk size ensures retrieval is precise enough to support this without drowning the LLM in irrelevant context. LangChain's abstractions make the pipeline maintainable and extensible for future features like streaming or multi-turn memory.
