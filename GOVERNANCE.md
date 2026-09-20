# Enterprise Repository Governance & Engineering Policy

## 1. Architectural Philosophy
The DocuTask Agent Enterprise Verification Platform operates as a unified engineering system governed by Clean Architecture, Domain-Driven Design (DDD), and Hexagonal Architecture principles.

## 2. Bounded Context Isolation
- **Domain Independence**: Core domain logic in `app/platform_verification` has **zero** outward dependencies on infrastructure, databases, API frameworks, or deployment tools.
- **Dependency Rule**: Dependencies always point inward toward domain abstractions.
- **Shared Kernel Restraint**: `app/shared_kernel` contains only generic enterprise primitives (Result, Typed IDs, TimeProvider, BaseEntity). No business rules are allowed in the shared kernel.

## 3. Review & Promotion Requirements
1. **Architecture RFC / ADR**: Any cross-cutting architectural change requires an Architecture Decision Record in `docs/architecture/adr/`.
2. **Quality Gate Compliance**: All PRs must pass the 100% automated test suite (`tests/platform_verification/`) including static topology validation (`tooling/governance/repository_validator.py`).
3. **Dual Approval**: PRs modifying `/app/shared_kernel/` or `/app/platform_verification/` require approval from at least two members of `@platform-architects`.

## 4. Semantic Versioning & Release Strategy
We adhere to Semantic Versioning 2.0.0 (`MAJOR.MINOR.PATCH`):
- `MAJOR`: Incompatible public API or contract breaking changes.
- `MINOR`: Backwards-compatible functionality additions.
- `PATCH`: Backwards-compatible bug fixes and internal performance optimizations.
