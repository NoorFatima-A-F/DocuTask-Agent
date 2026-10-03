# Incident Management Standard Operating Procedure (SOP)

## 1. Severity Classifications
- **CATASTROPHIC**: Multi-region outage, data loss risk, or platform-wide unavailability. Immediate executive paging.
- **CRITICAL**: Single region outage or loss of core document processing capability. On-call paged within 5 minutes.
- **MAJOR**: Subsystem degraded, elevated error rates ($> 5\%$). On-call notified within 15 minutes.
- **MINOR**: Non-critical background worker loss or minor latency increases.
- **WARNING**: Approaching capacity or SLA margins.
- **INFO**: Informational system event or planned maintenance.

## 2. Incident Lifecycle Stages
```
[DETECTED] ──> [INVESTIGATING] ──> [IDENTIFIED] ──> [MITIGATING] ──> [RESOLVED] ──> [POSTMORTEM] ──> [CLOSED]
```

## 3. Post-Incident Review (PIR) & Closure Invariant
An incident cannot be transitioned to `CLOSED` without completing the `POSTMORTEM` review, capturing root cause, mitigation effectiveness, and preventative architectural backlog items.
