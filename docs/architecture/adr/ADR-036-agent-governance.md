# ADR-036: Multi-Tier Agent Governance & Deterministic Provenance

## Status
Accepted

## Context
In regulated enterprise environments, every automated decision must be traceable, reproducible, and verifiable. If an invoice was processed or a legal agreement signed, auditors must know the exact agent version, prompt version, model version, policy set, memory namespace, and workflow context that generated the decision.

## Decision
We implement `AgentGovernanceManager` capturing immutable `AgentGovernanceRecord` snapshots before and during agent execution:
- `Agent Version`: Semantic version of agent capability definition.
- `Prompt Version`: Immutable prompt template version.
- `Model Version`: Foundational model identifier (e.g. `gemini-2.5-flash`).
- `Policy Version`: Active policy ruleset version.
- `Memory Namespace`: Tenant and workspace memory boundary.
- `Workflow Version`: Correlated Phase 3 workflow execution snapshot.
- `Checksum`: Cryptographic verification hash.

## Consequences
- Guaranteed deterministic reproducibility of historical agent runs.
- Full compliance with enterprise governance, SOC2, and ISO AI management standards.
