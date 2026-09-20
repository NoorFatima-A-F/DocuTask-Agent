# ADR-006: Domain Plugin Registry and Contract Isolation

## Status
Accepted

## Context
The platform requires verification across diverse domains (OCR, AI Extraction, RAG, Multi-Agent Swarms, Security, Chaos). Hardcoding domain logic into the orchestrator creates tight coupling and inhibits extensibility.

## Decision
We designed a decoupled Plugin Architecture:
- Concrete plugins adhere to `VerificationPlugin` abstract protocol.
- The `PluginRegistry` manages registration, health checks, domain filtering, and execution dispatching.
- Shipped 6 default plugins: `ocr`, `ai_extraction`, `rag_eval`, `agent_orchestration`, `security_compliance`, `chaos_resilience`.

## Consequences
### Positive
- Open-Closed Principle: New domains (e.g. Speech, Video, Fine-Tuning) can be added with zero changes to the core orchestrator.
- Independent testability of domain-specific logic.

### Negative
- Plugins must strictly map outputs to `PluginVerificationResult`.
