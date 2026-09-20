# ADR-001: Hexagonal Architecture and 12 Bounded Contexts

## Status
Accepted

## Context
The Enterprise Verification Platform requires long-term scalability across multiple verification domains without tight coupling or monolith degradation.

## Decision
Organize the platform into 12 dedicated Bounded Contexts (`verification`, `execution`, `datasets`, `environments`, `configuration`, `evidence`, `metrics`, `statistics`, `quality`, `certification`, `audit`, `plugins`), each following the strict 4-layer Hexagonal architecture (`domain/`, `application/`, `infrastructure/`, `interfaces/`, `contracts.py`).

## Consequences
- High cohesion and strict domain isolation.
- Zero cross-context direct internal imports; communication strictly through published contracts and domain events.
