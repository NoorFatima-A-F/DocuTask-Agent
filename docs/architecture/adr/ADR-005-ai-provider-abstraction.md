# Architecture Decision Record: ADR-005

## Title
AI Provider Abstraction & Model Mesh: Multi-Tier Dynamic Routing, Semantic Caching, and Vendor-Agnostic LLM Protocol

## Status
**ACCEPTED** (2026-03-24)

## Context
DocuTask Agent relies heavily on Large Language Models (LLMs), Vision-Language Models (VLMs), and specialized document intelligence models for OCR extraction, unstructured entity recognition, semantic reasoning, agent deliberation, and workflow synthesis.

Enterprise AI platform operations face critical commercial and architectural challenges:
1. **Vendor Lock-In & Commercial Volatility**: Direct dependencies on a single proprietary AI provider (e.g., OpenAI, Anthropic, Google Gemini, AWS Bedrock) expose enterprises to price hikes, regional outages, API deprecations, and regulatory compliance issues.
2. **Economic Inefficiency**: Routing simple entity classification tasks to flagship foundation models (e.g., GPT-4o, Claude 3.5 Sonnet) causes runaway operational costs.
3. **Data Sovereignty & Privacy Mandates**: Specific enterprise workloads (HIPAA PHI, GDPR EU-only, defense classified data) require strictly on-premise or sovereign cloud model execution (e.g., vLLM / Ollama with Llama 3 / Mistral).
4. **Latency & Reliability Vulnerability**: External LLM API rate limits (HTTP 429), regional outages (HTTP 503), and unpredictable latency spikes directly impair workflow SLAs.

DocuTask Agent requires a unified, vendor-agnostic AI provider layer that decouples application logic from underlying model vendors while providing dynamic routing, automated fallback, cost optimization, and semantic caching.

---

## Decision

We adopt a **Unified AI Provider Abstraction & Dynamic Model Mesh** governed by the `IAIProvider` protocol:

### 1. Vendor-Agnostic Protocol (`IAIProvider`)
Core agent and document processing logic shall exclusively interact with the unified `IAIProvider` abstract protocol:
- `generate_text(prompt, options) -> CompletionResponse`
- `generate_structured(prompt, response_schema, options) -> StructuredResponse`
- `stream_text(prompt, options) -> AsyncIterator[CompletionChunk]`
- `generate_embeddings(texts, model_override) -> EmbeddingBatch`
- `analyze_multimodal(images, prompt, options) -> MultimodalResponse`

All vendor SDKs (Google GenAI, OpenAI SDK, Anthropic SDK, AWS Bedrock SDK, Azure OpenAI, vLLM) are encapsulated inside isolated adapter implementations in `app/infrastructure/ai/`.

### 2. 4-Tier Model Classification & Dynamic Routing
Workloads are assigned to semantic model tiers based on task complexity, accuracy requirements, and latency constraints:
- **Tier 1 (Fast & Economical)**: Sub-100ms classification, routing, preliminary entity extraction (e.g., Gemini 1.5 Flash, GPT-4o-mini, Claude 3.5 Haiku, local Llama 3 8B).
- **Tier 2 (Standard Reasoning)**: Multi-page document extraction, validation rules, structured JSON parsing (e.g., Gemini 1.5 Pro, Claude 3.5 Sonnet, GPT-4o).
- **Tier 3 (Deep Cognitive & Strategic)**: Complex exception resolution, cross-document reconciliation, high-stakes verification (e.g., Claude 3 Opus, OpenAI o1/o3-mini, Gemini Ultra).
- **Tier 4 (Sovereign & Local)**: Air-gapped, zero-data-retention, on-premise execution (vLLM, TensorRT-LLM, HuggingFace TGI).

The **Dynamic AI Router** evaluates incoming requests against workspace tier policies, budget thresholds, provider health scores, and real-time p99 latency metrics to select the optimal model.

### 3. Automated Resilience & Circuit Breaking
- **Cascading Fallbacks**: If a primary provider experiences rate limits (429), timeouts (>5000ms), or 5xx server errors, the router instantly and transparently switches to the secondary configured provider within the same tier.
- **Circuit Breakers**: Providers experiencing >5% error rates over a 1-minute sliding window are temporarily marked unhealthy and placed into a cooling state.

### 4. Semantic Embedding & Prompt Caching
- Exact-match prompts and system instructions are cached in Redis with cryptographic hash keys.
- Semantic vector similarity caching (Qdrant / Milvus) detects recurring document patterns and resolves identical extraction queries with sub-5ms latency and zero LLM token costs.

### 5. AI Governance & Token Metering
Every AI call is logged with prompt/completion token counts, estimated dollar cost, model latency, and tenant attribution for precise enterprise cost allocation and chargeback.

---

## Consequences

### Positive
- **Zero Vendor Lock-In**: The platform can switch from one LLM provider to another with a single configuration change or automatically based on cost/latency.
- **Substantial Cost Reduction**: Intelligent tier routing and semantic caching reduce LLM token expenditure by an estimated 45%–70% across production workloads.
- **High Availability**: Cascading multi-provider failover guarantees 99.99% availability for mission-critical document processing workflows even during major third-party AI outages.
- **Regulatory Compliance**: Enterprises can enforce sovereign model routing for sensitive data categories without altering business logic.

### Negative / Trade-Offs
- **Prompt Sensitivity Variations**: Different LLM families (e.g., OpenAI vs. Anthropic vs. Gemini) interpret edge-case prompt instructions slightly differently; standard structured output schemas (JSON Schema / Pydantic) are required to normalize outputs.
- **Embedding Incompatibility**: Switching embedding models requires re-indexing historical vector databases unless dual-embedding pipelines are configured.

---

## Alternatives Considered

1. **Direct Vendor SDK Integration (OpenAI SDK throughout app)**: Rejected due to catastrophic vendor lock-in, inability to support sovereign on-premise deployments, and lack of resilient failover.
2. **Generic Third-Party Gateways (LiteLLM, LangChain, Portkey)**: Evaluated; while conceptually similar, DocuTask Agent requires deep native integration with our 7-tier tenant metering, PostgreSQL RLS contexts, and specialized document bounding-box multimodal schemas. A lightweight native adapter pattern (`IAIProvider`) maintains zero external gateway dependencies.
