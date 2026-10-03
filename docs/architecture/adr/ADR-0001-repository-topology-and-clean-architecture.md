# ADR-0001: Enterprise Repository Topology & Hexagonal Domain Boundary

## Status
**ACCEPTED** (2026-09-14)

## Context
As the DocuTask Agent verification platform scales across hundreds of verification modules, multiple engineering teams, distributed execution clusters, and future microservice extractions, organizing the repository around technical frameworks (e.g. `controllers/`, `models/`, `views/`) results in tight coupling, cognitive overload, and architecture drift.

## Decision
We adopt a capability-first, Clean/Hexagonal repository topology structured into 14 distinct root and sub-domain areas:
1. `app/platform_verification`: Pure core verification domain & 16 specialized components.
2. `app/shared_kernel`: Generic primitives (Result[T, E], Typed IDs, TimeProvider, BaseEntity).
3. `app/infrastructure`: External adapters (Storage CAS, SQLAlchemy DB, OpenTelemetry).
4. `app/interfaces`: Ingress boundaries (REST API routers, CLI commands, Workers).
5. `config/`: Multi-tier environment configurations and validation schemas.
6. `datasets/`: Immutable dataset manifests, golden sets, and benchmark corpora.
7. `evidence/`: Dedicated non-production artifact storage with gitignore seals.
8. `docs/`: Architecture specifications, ADRs, and operational runbooks.
9. `tooling/`: Repository linters, governance validators, and generators.
10. `deploy/`: Cloud-native deployment manifests and IaC assets.
11. `security/`: Threat models, IAM profiles, and compliance rules.
12. `observability/`: Dashboards, metric descriptors, and alert rules.
13. `tests/`: Multi-tier test suites (unit, integration, component, contract, chaos).

## Consequences
- **Positive**: Strict decoupling allows independent module evolution and seamless future microservice extraction.
- **Positive**: Zero accidental framework leaks into business evaluation algorithms.
- **Positive**: Machine-readable repository governance guarantees architectural compliance in CI/CD.
