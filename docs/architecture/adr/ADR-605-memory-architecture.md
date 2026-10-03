# ADR-605: Decoupled Memory Intelligence & Consolidation Architecture

## Status
Accepted

## Context
Many AI architectures conflate Knowledge ("What exists in documents and records") with Memory ("What happened during agent interactions and workflow runs"). Conflating these leads to bloated vector stores, context window exhaustion, and degradation of retrieval quality.

## Decision
We cleanly separate Knowledge Fabric from Memory Intelligence:
1. `MemoryIntelligencePlatform` manages 8 distinct tiers: `WORKING`, `SHORT_TERM`, `EPISODIC`, `SEMANTIC`, `PROCEDURAL`, `ORGANIZATION`, `WORKFLOW`, `AGENT`.
2. `MemoryConsolidationEngine` operates in the background to summarize old memories, score importance, promote valuable patterns to procedural/episodic stores, and evict expired TTL items.

## Consequences
- Clean conceptual and operational separation between static/ingested facts and dynamic execution history.
- Prevents memory bloat while preserving long-term agent learning and playbook synthesis.
