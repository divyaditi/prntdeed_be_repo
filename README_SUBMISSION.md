# Design Notes and Implementation Choices

I built this assistant around a lightweight RAG pattern that keeps the answers grounded in the PrintFlow documentation instead of relying on the model to recall facts from memory. The key pieces are configured in [src/constant.py](src/constant.py), the retrieval pipeline is implemented in [src/utils/chunking_utils.py](src/utils/chunking_utils.py), and the tool-enabled agent is wired in [src/client/grok_client.py](src/client/grok_client.py).

## Why LangChain

I used LangChain because a normal LLM call does not reliably decide when to invoke tools based on a user query. The project needs the model to route plan and feature questions to a tool like `check_tier_feature`, and to pull relevant documentation through a search tool when the answer is grounded in the onboarding materials. LangChain gives us that orchestration layer through `create_tool_calling_agent` and `AgentExecutor`, which makes the tool invocation reusable and easier to manage than writing custom function-calling logic from scratch.

It also gives us the abstractions we need for document processing. In this codebase, the split logic uses `MarkdownHeaderTextSplitter` and `RecursiveCharacterTextSplitter` to preserve heading structure while splitting long markdown sections into digestible chunks. This is the same general pattern LangChain uses for document chunking, and it is more robust than trivial line-based splitting.

## Chunking Strategy

The chunking configuration is intentionally moderate: `CHUNK_SIZE = 1000` and `CHUNK_OVERLAP = 100` in [src/constant.py](src/constant.py). This size keeps chunks large enough to retain useful context, but small enough to stay focused on a single topic. The overlap helps avoid losing information at boundaries, which matters in support documents where a concept might be split across sections.

The actual chunking implementation in [src/utils/chunking_utils.py](src/utils/chunking_utils.py) first preserves markdown headings, then recursively splits long blocks when they exceed a threshold. This makes retrieval more precise than storing each full file as a single large chunk and reduces context dilution in the answer-generation step.

## Embedding Model

The project uses `BAAI/bge-m3` as the embedding model, also configured in [src/constant.py](src/constant.py). I chose this model because it is a strong general-purpose embedding model for semantic retrieval over policy and support documentation. It works well for matching user questions to relevant passages like plan restrictions, file-format requirements, and retention policies.

## Trade-offs and Limitations

The main trade-off is that we avoid stuffing all documents into the prompt. Instead, the system retrieves only the most relevant chunks, which keeps the prompt focused and reduces hallucination risk. A limitation is that the current version does not include deep multi-turn memory or a fully optimized streaming pipeline, but the architecture is already set up for those improvements if needed.
