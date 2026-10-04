# ADR 0002: Deterministic Pydantic V2 Contracts for Agent Outputs

## Status
Accepted

## Context
LLM responses are inherently probabilistic and susceptible to hallucinated fields, schema drift, or invalid data types, which lead to downstream database integrity violations and API contract breakage.

## Decision
All agent and extraction operations must pass through strictly typed and validated Pydantic v2 schemas (`app/schemas/`). If validation fails:
1. An autonomous schema repair agent executes 1 targeted re-prompt providing the specific JSON validation error and expected schema signature.
2. If schema validation fails after the repair attempt, the task payload is routed to the Celery Dead-Letter Queue (`dlq.tasks`) for human-in-the-loop (HITL) audit and manual review.

## Consequences
- Prevents invalid or hallucinated data from persisting to PostgreSQL / SQLite.
- Guarantees downstream API contracts and frontend serializers remain deterministic and unbroken.
- Introduces minimal recovery latency during transient repair re-prompts.
