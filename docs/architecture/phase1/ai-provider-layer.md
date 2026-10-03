# AI Provider Abstraction & Model Mesh Specification

## 1. AI Provider Mesh Architecture

```mermaid
graph TD
    subgraph "Business & Agent Application Layer"
        AGENTS[Agents & Workflows]
        DOC_ENG[Document Extraction Engine]
        RAG_ENG[Hybrid RAG Engine]
    end

    subgraph "AI Mesh Router & Gateway"
        ROUTER[Multi-Tier Dynamic Model Router]
        CACHE[Semantic Prompt Cache (Redis Vector)]
        METER[Token & Cost Telemetry Meter]
    end

    subgraph "AI Provider Interface (IAIProvider)"
        IFACE[Standardized AIProvider Protocol]
    end

    subgraph "Provider Adapters"
        ADAPT_GEMINI[Google Gemini 1.5 / 2.0 Adapter]
        ADAPT_OPENAI[OpenAI GPT-4o / O3 Adapter]
        ADAPT_CLAUDE[Anthropic Claude 3.5 Sonnet Adapter]
        ADAPT_LOCAL[Local OSS vLLM / Ollama Adapter]
    end

    AGENTS & DOC_ENG & RAG_ENG --> ROUTER
    ROUTER --> CACHE
    CACHE -.->|Cache Hit| ROUTER
    CACHE -.->|Cache Miss| IFACE
    ROUTER --> METER
    IFACE --> ADAPT_GEMINI & ADAPT_OPENAI & ADAPT_CLAUDE & ADAPT_LOCAL
```

---

## 2. Standard AI Provider Protocol (`IAIProvider`)

```python
# app/domain/ai/interface.py
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, AsyncGenerator
from dataclasses import dataclass
from enum import Enum


class AIModelTier(str, Enum):
    TIER_1_REASONING = "TIER_1_REASONING"  # Complex planning, causal analysis (GPT-4o, Claude 3.5, Gemini 1.5 Pro)
    TIER_2_BALANCED = "TIER_2_BALANCED"    # Standard extraction, summarization (Gemini Flash, GPT-4o-mini)
    TIER_3_EDGE = "TIER_3_EDGE"            # Low-latency classification, local privacy (Local Llama-3, vLLM)


@dataclass
class CompletionRequest:
    prompt: str
    messages: List[Dict[str, str]]
    temperature: float = 0.0
    max_tokens: int = 4096
    structured_json_schema: Optional[Dict[str, Any]] = None
    tools: Optional[List[Dict[str, Any]]] = None
    stop_sequences: Optional[List[str]] = None


@dataclass
class UsageMetrics:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    estimated_cost_usd: float
    latency_ms: float


@dataclass
class CompletionResponse:
    content: str
    structured_data: Optional[Dict[str, Any]]
    tool_calls: Optional[List[Dict[str, Any]]]
    usage: UsageMetrics
    finish_reason: str
    model_version: str


class IAIProvider(ABC):
    """Universal abstraction layer for all LLM and embedding providers."""

    @abstractmethod
    async def complete(self, request: CompletionRequest) -> CompletionResponse:
        """Executes a chat completion or structured JSON extraction."""
        pass

    @abstractmethod
    async def complete_stream(self, request: CompletionRequest) -> AsyncGenerator[str, None]:
        """Streams token chunks in real-time for interactive user interfaces."""
        pass

    @abstractmethod
    async def embed(self, texts: List[str]) -> List[List[float]]:
        """Generates dense vector embeddings for semantic search and RAG."""
        pass
```

---

## 3. Dynamic Multi-Tier Routing & Cost Optimization Strategy

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                      MULTI-TIER ROUTING LOGIC                                   │
├────────────────────────────────┬──────────────────────────┬────────────────────┤
│ Task Complexity                │ Assigned Tier / Model    │ Cost / 1k Tokens   │
├────────────────────────────────┼──────────────────────────┼────────────────────┤
│ 1. Simple Classification / NER │ Tier 3: Gemini Flash / OSS│ $0.0001            │
│ 2. Standard Invoice Extraction │ Tier 2: Gemini 1.5 Flash │ $0.0005            │
│ 3. Complex Multi-Page Contract │ Tier 1: Claude 3.5 Sonnet│ $0.0030            │
│ 4. Strategic Causal Planning   │ Tier 1: GPT-4o / Pro     │ $0.0050            │
└────────────────────────────────┴──────────────────────────┴────────────────────┘
```

1. **Semantic Prompt Caching**: Queries with cosine similarity $\ge 0.96$ against recently processed document templates return cached completions instantly with 0 tokens spent.
2. **Automated Fallback Cascade**: If the primary provider returns HTTP 429 or 503, the router cascades in $< 200\text{ms}$ to the secondary provider without workflow disruption.
3. **Monthly Hard Quota Breakers**: If a workspace reaches 100% of its monthly token spend cap, the system automatically routes to local open-source models or pauses non-critical batch jobs.
