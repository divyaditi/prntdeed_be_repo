# Design Considerations and Implementation Choices

## System Overview

PrintFlow Assistant uses a lightweight retrieval-augmented generation (RAG) architecture to ground responses in the supplied PrintFlow documentation. The assistant combines document retrieval with two purpose-specific tools: one deterministic feature-to-plan lookup and one semantic document-search tool.


## Why LangChain and an Agent-Based Architecture

A direct language-model call would require the application to decide in advance whether a question needs a subscription-plan lookup, documentation retrieval, or both. The agent-based design delegates that decision to the model using the tools and their descriptions as available capabilities.

The agent follows a reason-and-execute pattern:

1. It receives the user's question.
2. It determines whether the question requires a deterministic feature lookup, document retrieval, or both.
3. It invokes the selected tool or tools.
4. It uses the returned results to compose the final answer.

This design avoids hardcoding every possible user-intent branch in application code. It also keeps the responsibilities separated: structured plan availability is handled by a deterministic mapping, while explanatory and procedural questions are handled through document retrieval.


## LangChain Abstractions

The document pipeline uses Markdown-aware and recursive text-splitting abstractions.

**MarkdownHeaderTextSplitter** uses Markdown headings to preserve document hierarchy. This is useful for the PrintFlow corpus because the documents organize information into sections such as subscription plans, printing services, API integration, billing, and support.

**RecursiveCharacterTextSplitter** is used after structural splitting when a section is larger than the configured target size. The splitter attempts to preserve larger text units before falling back to smaller separators. In this project, the configured chunk target is expressed in tokens, so the implementation uses a token-aware length function when calculating chunk size and overlap.

**@tool abstraction** exposes typed Python functions to the agent. The tool schema helps the model provide the expected arguments, while the tool implementation remains responsible for validating values and handling unknown features, tiers, or queries.

The system consists of two related flows:

```
Indexing flow: load documents → split into chunks → embed chunks → store vectors

Question flow: user query → agent selects tools → tool results → final answer
```

The question flow is agentic rather than strictly linear because the model may invoke one tool or both tools depending on the query.

## Chunking Strategy: 250–400 Tokens

The project uses a target chunk size of approximately 250–400 tokens. This range is selected to keep retrieved passages focused while retaining enough local context for plan descriptions, product requirements, policy rules, and FAQ answers.

The attached corpus contains three Markdown files:

| File | Approximate words | Main content |
|------|-------------------|--------------|
| onboarding_faq.md | 871 | 18 onboarding, job-submission, API, billing, and support questions |
| policies.md | 675 | Subscription plans and operational policies |
| products.md | 510 | Printing services, file submission, VDP, proofing, and finishing |

The data is organized into short sections and question-and-answer units. For example, the FAQ includes individual questions about team members, pre-flight failures, API access, rate limits, webhooks, billing, and support SLAs. The policies document contains separate plan tables for Starter, Pro, and Enterprise, while the products document separates offset, digital, and wide-format printing.

A 250–400-token target is therefore appropriate for keeping most retrieved passages centered on one question, one plan, one policy, or one product capability. It also reduces the likelihood that a result about one subscription tier will contain excessive information about unrelated tiers.

The chunk size is a configuration choice for this corpus, not a universal optimum. Its effectiveness should ultimately be evaluated with representative PrintFlow questions and retrieval metrics such as recall@k, precision@k, or mean reciprocal rank.

## Chunk Overlap

The configured overlap is 50 tokens. Its purpose is to preserve context when a section crosses a chunk boundary. This is especially relevant for Markdown tables and plan sections, where a heading or introductory sentence may otherwise be separated from the rows that follow it.

The overlap should remain smaller than the chunk size so that adjacent chunks share useful context without duplicating most of the same passage. The appropriate value can be adjusted if retrieval evaluation shows that headings, table rows, or policy conditions are frequently separated.

## Embedding Model: BAAI/bge-m3

The project uses BAAI/bge-m3 for local embeddings. BGE-M3 is a multilingual embedding model that supports dense, sparse, and multi-vector retrieval modes. Its dense embedding output is 1024-dimensional, which matches the vector-store configuration when dense retrieval is used.

The choice is motivated by the nature of the PrintFlow corpus:

- The corpus consists of technical support, product, policy, and FAQ language.
- The model supports multilingual retrieval if the knowledge base is expanded beyond English.
- Local inference avoids a per-request dependency on a hosted embedding API after the model and dependencies have been installed.
- The model supports long inputs, although this project intentionally creates much smaller chunks for retrieval precision.


## Two-Tool Architecture

### Tool 1: check_tier_feature(feature: str, tier: str) -> str

This tool checks whether a feature is available for a subscription tier using the hardcoded FEATURE_PLAN_MAP in `src/constant.py`.

It is appropriate for questions such as:

- Is API access available on Starter?
- Does Pro include webhooks?
- Which plans support variable data printing?
- Is physical proofing available on Enterprise?

The tool is deterministic for valid, normalized inputs because it reads from a fixed mapping rather than asking the language model to recall the answer. However, deterministic lookup does not automatically make the result complete or current. The mapping must be maintained when plans or features change, and the implementation should handle unknown feature and tier names explicitly.

### Tool 2: printflow_document_search(query: str) -> str

This tool performs semantic search over the embedded PrintFlow documentation and returns the configured top results. It is appropriate for questions that require procedural or explanatory context, such as:

- How do I add team members?
- What should I do when pre-flight returns ERR_BLEED?
- What file formats are accepted for wide-format printing?
- How long are uploaded files retained?

The search tool provides documentation evidence to the agent. Retrieval does not by itself guarantee that the final answer will cite the evidence or remain faithful to it, so the system prompt should instruct the agent to prioritize retrieved content and acknowledge when the documentation does not answer the question.

### Why Two Tools?

The two-tool design separates two different types of knowledge:

| Knowledge type | Tool | Retrieval behavior |
|---|---|---|
| Subscription feature availability | check_tier_feature | Deterministic lookup |
| Procedures, specifications, policies, and FAQs | printflow_document_search | Semantic vector search |

For a simple plan-feature question, the agent can use the deterministic tool. For a procedural question, it can search the documentation. For a question that combines both, such as whether a plan supports a feature and how that feature is configured, it can invoke both tools.

The architecture reduces the amount of information the model must infer from its pretrained knowledge, but it does not eliminate all hallucination risk. The model may choose an inappropriate tool, misunderstand an input, or misstate a returned result. Tool outputs should therefore be treated as evidence that constrains the answer, not as a substitute for validation and monitoring.

## Runtime Characteristics

### Stateless Requests

The current implementation is stateless. Each invocation receives the current user query and does not persist conversation history, session memory, or prior tool results between requests.

This means that every request must contain the context required to answer it. A follow-up such as "What about Enterprise?" may be ambiguous if the previous question is not included in the same request. The stateless design simplifies deployment, horizontal scaling, testing, and debugging because requests do not depend on server-side conversational state.

If multi-turn conversations are added later, the application will need a history store, a conversation identifier, or another explicit state-management mechanism.

### Non-Streaming Responses

The current implementation does not use streaming. It invokes the agent asynchronously and returns the completed final message after the agent has finished its model and tool calls.

This keeps the API layer simple and makes error handling straightforward. The trade-off is that users do not receive partial output while retrieval and generation are in progress. Streaming can be added later through the appropriate asynchronous streaming interface if perceived latency becomes a priority.


## Why This Design Fits PrintFlow

PrintFlow questions are often specific and operational. They refer to subscription tiers, API limits, file formats, pre-flight requirements, turnaround times, support SLAs, storage policies, and production options. These topics benefit from grounding in a controlled corpus rather than relying only on general model knowledge.

The design addresses this need with two complementary mechanisms. The feature tool handles structured plan availability, while the document-search tool provides supporting context for policies, procedures, and product specifications. The 250–400-token chunk target keeps retrieved evidence focused, the stateless runtime keeps request handling predictable, and the non-streaming response path keeps the initial implementation simple.

The design is intentionally extensible. Future improvements can include retrieval evaluation, query normalization, reranking, citation enforcement, structured answer schemas, conversation memory, or streaming responses without changing the basic separation between deterministic feature lookup and semantic document retrieval.
