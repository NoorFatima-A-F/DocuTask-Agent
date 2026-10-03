# ADR-811: Enterprise Prompt as Governed Software Artifact

## Status
Accepted

## Context
Prompts in AI systems are traditionally embedded as unstructured strings inside codebases, leading to untracked modifications, lack of ownership, absence of review gates, security vulnerabilities (prompt injection, secret leakage), and untracked production behavior.

## Decision
We establish prompts as first-class, versioned, evaluated, and governed enterprise software assets under `app/prompts/`:
- Every prompt is registered in a tenant-isolated `PromptRegistryRepository` with unique identification, ownership, department, purpose, category, risk level, and metadata.
- Prompts follow a strict 10-state lifecycle FSM (`DRAFT` $\to$ `VALIDATION` $\to$ `TESTING` $\to$ `REVIEW` $\to$ `APPROVED` $\to$ `PUBLISHED` $\to$ `ACTIVE` $\to$ `EXPERIMENTAL` $\to$ `DEPRECATED` $\to$ `ARCHIVED`).
- Prompts cannot be executed directly by agents without passing governance checks and resolving approved version snapshots.

## Consequences
- **Positive**: Complete auditability, explicit ownership, enforced review processes, eliminate rogue hardcoded strings.
- **Negative**: Requires formal registration and promotion workflow for new prompt assets.
