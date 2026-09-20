# ADR-069 / ADR-966: Automated Rollback & Incident Recovery Architecture

## Status
Accepted

## Context
When a newly deployed release introduces errors or service degradations in production, manual intervention to identify and revert changes is slow and error-prone.

## Decision
We implement `RollbackExecutor` and `RollbackRecoveryManager`:
1. Automated tripping on metric anomalies, health check failures, governance policy violations, or AI model quality degradation.
2. Immediate halts to progressive rollouts and instant restoration of prior known good version.
3. Automated compilation of a post-rollback Root Cause Analysis (`PostRollbackRCAReport`) to guide engineering remediation.

## Consequences
- Mean Time to Recovery (MTTR) reduced from minutes to sub-second automated rollbacks.
- Comprehensive audit records capturing the failure cause, telemetry at failure, and recovery actions.
- Automatic prevention of subsequent promotion until remediation is verified.
