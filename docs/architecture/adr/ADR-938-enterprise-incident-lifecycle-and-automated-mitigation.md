# ADR-938: Enterprise Incident Lifecycle & Automated Alert Mitigation

## Status
Accepted

## Context
During platform anomalies, fragmented alert streams overwhelm on-call engineers while lacking formal lifecycle progression, timeline auditing, and automated mitigation runbook linking.

## Decision
We implement `IncidentLifecycleStateMachine`, `IncidentManager`, and `IncidentNotifier` providing 6 severity classifications (`INFO` to `CATASTROPHIC`), 7 lifecycle states (`DETECTED`, `INVESTIGATING`, `IDENTIFIED`, `MITIGATING`, `RESOLVED`, `POSTMORTEM`, `CLOSED`), rate-limited multi-channel dispatch, and automated mitigation hooks.

## Consequences
- Deduplication and correlation of alerts to avoid notification storms.
- Mandatory postmortem tracking before an incident can be transitioned to CLOSED.
- Complete timeline audit trail capturing all actors, state changes, and automated remediation actions.
