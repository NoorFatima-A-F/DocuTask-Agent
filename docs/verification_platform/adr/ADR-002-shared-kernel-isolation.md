# ADR-002: Minimalist Framework-Independent Shared Kernel

## Status
Accepted

## Context
A monolithic shared utility folder frequently devolves into tight coupling and framework contamination.

## Decision
Establish `app/shared_kernel/` as a strictly minimal, framework-neutral library containing only universal primitives (`Result[T, E]`, `TypedId`, `TimeProvider`, `EventBus`, `Hasher`). Zero imports of FastAPI, SQLAlchemy, Redis, or cloud SDKs are permitted.

## Consequences
- Clean architecture dependency rule preserved.
- Static AST validator enforces zero illegal imports automatically in CI.
