# ADR-707: Provisioning Workflow

## Status
Accepted

## Context
Tenant onboarding must be automated, fast (< 1 second for core provisioning), idempotent, and resilient against partial failures.

## Decision
Implement a multi-step orchestrated `TenantProvisioningEngine`:
1. Register Organization entity in `REGISTERED` state.
2. Advance to `PROVISIONING` state.
3. Provision default workspace (`Default Workspace`).
4. Provision default execution environments (`Production`, `Development`).
5. Assign primary owner membership with `OWNER` role.
6. Initialize default quotas, policies, and telemetry.
7. Advance state to `INITIALIZED` and then `ACTIVE`.

## Consequences
- **Positive**: Complete out-of-the-box tenant readiness with zero manual operational intervention.
- **Trade-off**: Requires transactional consistency across multiple sub-managers.
