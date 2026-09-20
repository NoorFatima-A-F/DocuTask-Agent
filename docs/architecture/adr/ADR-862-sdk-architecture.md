# ADR-862: Governance SDK Architecture

## Context
Developers need ergonomic, typed, and resilient SDKs in Python and TypeScript to integrate governance checks into agent execution loops, LLM routers, and durable pipelines.

## Decision
Provide native Python and TypeScript SDKs featuring automated exponential backoff retries, type safety, rate-limit awareness, explicit domain models, and exception mapping (`PolicyDeniedError`, `AuthenticationError`, `RateLimitExceededError`).

## Status
Accepted

## Consequences
- Single line evaluation integration (`client.evaluate(...)`).
- Seamless local and cloud testing capabilities without network boilerplate.
