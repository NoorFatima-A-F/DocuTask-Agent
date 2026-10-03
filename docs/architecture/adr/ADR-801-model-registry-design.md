# ADR-801: Enterprise Model Registry & Asset Metadata Topology

## Status
Accepted

## Context
In previous phases, AI models were frequently referenced as static strings (e.g. `"gpt-4o"`, `"claude-3-5-sonnet"`, `"gemini-1.5-pro"`), creating security vulnerabilities, untracked operational costs, regulatory compliance risks, and preventing automated policy enforcement across multi-tenant workloads.

## Decision
We implement a unified, multi-tenant `ModelRegistryRepository` and `ModelRegistryService` that treat every AI model, embedding engine, and specialized classification network as a first-class enterprise asset.
Each registered model includes:
- Unique model identifiers, family versioning, and provider metadata.
- Operational properties: context window size, max output tokens, token pricing.
- Fine-grained capability sets (e.g. `structured_output`, `vision`, `function_calling`, `rag_reasoning`).
- Regulatory metadata: data residency regions, risk levels, approval state, and replacement pointers.

## Consequences
- **Positive**: Eliminates arbitrary model string references; enforces rigorous tenant boundaries; enables dynamic capability matching.
- **Negative**: Adds mandatory registration step before new third-party foundation models can be utilized in production workflows.
