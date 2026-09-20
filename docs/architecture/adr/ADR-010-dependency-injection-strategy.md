# Architecture Decision Record: ADR-010

## Title
Dependency Injection Strategy: Explicit Scopes, Circular Dependency Detection, and Zero Global Singletons

## Status
**ACCEPTED** (2026-03-24)

## Context
Global variable singletons (`db = Database()`, `ai_client = Gemini()`) introduce hidden couplings, impede unit testing, cause concurrency leaks across async request contexts, and violate Clean Architecture principles.

## Decision
We mandate the platform-wide use of **DependencyContainer** supporting three distinct lifetimes:
1. `SINGLETON`: Process-level lifecycle (e.g., Connection Pools, EventBus, Registries).
2. `SCOPED`: Request / Workflow execution lifecycle with tenant context isolation.
3. `TRANSIENT`: Ephemeral per-call instantiation (e.g., Command Handlers, Task Executors).
The container incorporates automated type-hint parameter resolution, recursion-based circular dependency cycle detection with explicit error reporting, and test override injection.

## Consequences
### Positive
- Subsystems are completely decoupled and mockable in unit test suites.
- Elimination of global mutable state and multithreaded contention bugs.
- Clear dependency graphs across all platform subsystems.
### Negative / Trade-Offs
- Requires developers to specify type annotations on class `__init__` methods.
