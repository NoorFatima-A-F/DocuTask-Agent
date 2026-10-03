# Enterprise Testing Strategy & Verification Methodology

DocuTask Agent enforces a deterministic, multi-tiered testing pyramid designed to ensure mission-critical reliability across multimodal extraction, multi-agent state machines, distributed GitOps controllers, and zero-trust supply chain pipelines.

---

## 1. Testing Pyramid Overview

```
                      / \
                     /   \
                    / E2E \       <-- Full Certification Scenarios (Gold Master & Auto-Rollback)
                   /-------\
                  /  Integ  \     <-- Service Meshes, Database Migrations, OCI Referrers
                 /-----------\
                /    Unit     \   <-- State Machines, DAG Schedulers, Pydantic Schema Parsers
               /---------------\
```

---

## 2. Test Suites Structure

The platform includes automated tests organized by architectural domain under `tests/`:

### Core Subsystem Suites
- **`tests/runtime/`**: Deterministic state transitions, multi-agent goal decomposition, and memory retention.
- **`tests/observability/`**: OpenTelemetry span propagation, Prometheus metric scrapers, and DORA telemetry calculators.
- **`tests/agents/`**: Multimodal OCR entity parsing, confidence scoring critics, and human-in-the-loop task routing.

### Platform Delivery OS Suites (`tests/platform_delivery/`)
1. **`test_control_plane.py`**: State machine DAG transitions, CQRS command bus, and idempotency key constraints.
2. **`test_builds_and_evidence.py`**: 11-stage build engine topological execution and cryptographic `TestEvidence` capture.
3. **`test_artifacts_and_oci.py`**: Content-addressed SHA-256 digests, OCI 1.1 referrers graph, and quarantine isolation.
4. **`test_sbom_provenance_signing.py`**: CycloneDX 1.5, SPDX 2.3, SLSA Level 3 attestations, and Sigstore/Cosign verification.
5. **`test_releases_and_compatibility.py`**: Multi-system SemVer matrix validation and immutable release manifests.
6. **`test_environments_and_promotion.py`**: Environment promotion path verification and exact artifact digest preservation.
7. **`test_gitops_and_drift.py`**: ArgoCD & Flux CD reconciliation, emergency drift classification, and auto-healing.
8. **`test_progressive_delivery_strategies.py`**: Rolling surge, Blue-Green atomic swap, Canary weighted traffic shift, and Shadow dark traffic traces.
9. **`test_rollout_and_automated_rollback.py`**: Telemetry quality gate evaluation, automated canary abort, and rapid rollback recovery.
10. **`test_database_expand_contract.py`**: Online database migration safety, blocking destructive DDL in expand phases.
11. **`test_governance_and_risk.py`**: Risk scoring engine, release freeze calendars, and multi-person dual-approval rules.
12. **`test_plugins_and_sandbox.py`**: Sandboxed plugin lifecycle, timeout limits, and unauthorized capability traps.
13. **`test_sdk_and_cli.py`**: `InfrastructureSDK` client calls and `doctaskctl` CLI subcommands.
14. **`test_platform_delivery_api.py`**: FastAPI REST endpoints with `Idempotency-Key` headers.
15. **`test_end_to_end_certification_scenario.py`**: End-to-end Gold Master release path and automated canary failure disaster recovery.

---

## 3. Running Test Suites

```bash
# Execute full platform test suite
pytest tests/ -v

# Execute Platform Delivery OS verification suite
pytest tests/platform_delivery/ -v

# Generate terminal and XML coverage reports
pytest --cov=app --cov-report=term-missing --cov-report=xml
```
