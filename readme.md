# AI Onboarding Assistant for PrintFlow

An intelligent AI-powered assistant that answers customer onboarding questions using a Retrieval-Augmented Generation (RAG) pipeline. The assistant ingests PrintFlow documentation, retrieves relevant context, and uses an LLM with tool calling to provide accurate, grounded answers.

## Quick Start

### Prerequisites

- **Python:** 3.10 or higher
- **Groq API Key:** Sign up at [GroqCloud](https://console.groq.com) and get your API key
- **Embedding Model:** `BAAI/bge-m3` (downloads automatically on first run)

### Setup Instructions

1. **Navigate to the source directory:**
   ```bash
   cd src
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - **On Windows (Command Prompt):**
     ```bash
     venv\Scripts\activate
     ```
   - **On Windows (PowerShell):**
     ```bash
     .\venv\Scripts\Activate.ps1
     ```
   - **On macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure the Groq API Key:**
   - Open or create `src/.env` file
   - Add your Groq API key:
     ```
     GROQ_API_KEY=your_api_key_here
     ```
   - Get your key from: https://console.groq.com/keys

### Running the Application

```bash
python solution.py
```

This starts the FastAPI server on `http://localhost:8080` with automatic vector store initialization.

### API Endpoints

- **Health Check:** `GET /api/v1/health`
- **Chat:** `POST /api/v1/chat`
  ```json
  {
    "query": "What file formats do you support?"
  }
  ```

---

## Project Architecture

### Core Components

| Component | Purpose | Location |
|-----------|---------|----------|
| **Embedding Pipeline** | Chunks documents and creates embeddings | `service/embedding_service.py`, `utils/chunking_utils.py` |
| **Vector Store** | Stores and retrieves document chunks | ChromaDB in `chroma_db/` |
| **Groq Client** | LLM with tool calling | `client/grok_client.py` |
| **Chat Service** | Orchestrates retrieval + LLM response | `service/chat_service.py` |
| **Tools** | Implements business logic (e.g., `check_tier_feature`) | `tools/printflow_tools.py` |

### Data Flow

```
User Query
    ↓
Embedding Service (query embedding)
    ↓
Vector Store Retrieval (find relevant chunks)
    ↓
Groq Client with Tool Calling
    ├─ Decision: Use tool? → call check_tier_feature
    └─ Generate grounded response from retrieved docs
    ↓
Return Answer to User
```
## Troubleshooting

### "ModuleNotFoundError: No module named 'X'"

Ensure you've activated the virtual environment and installed dependencies:

```bash
pip install -r requirements.txt
```

### "GROQ_API_KEY not set"

Check your `.env` file in `src/` and verify the key format:

```
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxx
```

### Slow embedding generation on first run

Sentence-transformers downloads the embedding model (~500MB) on first use. This is normal.

### Windows multiprocessing issues

The `constant.py` file includes Windows-specific settings to prevent tokenizer parallelism errors:

```python
TOKENIZERS_PARALLELISM = "false"
OMP_NUM_THREADS = "1"
```

These are set automatically in `embedding_client.py`.

---

## Configuration

All settings are in `src/constant.py`:

| Setting | Value | Purpose |
|---------|-------|---------|
| `MODEL_NAME` | `llama-3.1-8b-instant` | Fast, reliable LLM with function calling |
| `EMBED_MODEL_NAME` | `BAAI/bge-m3` | Strong semantic embedding for support docs |
| `CHUNK_SIZE` | `1000` | Balanced chunk size for context retention |
| `CHUNK_OVERLAP` | `100` | Prevents information loss at boundaries |



## Project Structure

```
src/
├── solution.py                 # Main FastAPI app entry point
├── constant.py                 # Configuration and constants
├── .env                        # Environment variables (not in git)
├── requirements.txt            # Python dependencies
├── client/
│   ├── embedding_client.py     # Embedding model wrapper
│   └── grok_client.py          # Groq LLM client with tool calling
├── service/
│   ├── embedding_service.py    # Vector store initialization
│   └── chat_service.py         # Chat orchestration
├── router/
│   ├── chat_router.py          # /api/v1/chat endpoint
│   └── health_router.py        # /api/v1/health endpoint
├── tools/
│   └── printflow_tools.py      # Tool implementations
├── utils/
│   ├── chunking_utils.py       # Document chunking logic
│   ├── prompt_utils.py         # Prompt templates
│   └── v_db_utils.py           # Vector DB utilities
├── data/
│   ├── onboarding_faq.md       # FAQ documentation
│   ├── policies.md             # Policies documentation
│   └── products.md             # Product/features documentation
└── chroma_db/                  # Vector store (generated)
```

---

## Design Notes

For detailed design rationale and trade-offs, see [`README_SUBMISSION.md`](README_SUBMISSION.md).

Key highlights:
- **Chunking:** Moderate size (1000 tokens) with overlap for semantic coherence
- **Retrieval:** Vector similarity matching over raw embedding space
- **Tool Integration:** Function calling routed through LangChain agent
- **No Hallucination:** Answers grounded strictly in retrieved documents

---

## Next Steps

To extend this system, consider:

1. **Multi-turn Memory:** Need to Add conversation history tracking in chat service
2. **Streaming Responses:** Need to Use FastAPI `StreamingResponse` with LLM streaming
3. **Evaluation Harness:** Add ragas for answer quality and retrieval accuracy
4. **Caching:** Need to  add Redis layer for frequently asked questions
