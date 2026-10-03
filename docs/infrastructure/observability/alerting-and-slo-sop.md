# Alerting Platform & SLO Burn Rate Standard Operating Procedure (SOP)

## 1. Alert Severity Levels & Response Protocols
- `EMERGENCY`: Direct page on-call SRE and engineering leads. Immediate service impact or catastrophic multi-region outage. Target ACK: < 5 mins.
- `CRITICAL`: Page on-call primary engineer. 1h SLO fast burn rate or major subsystem degradation. Target ACK: < 15 mins.
- `ERROR`: High priority ticket and Slack/Teams notification. Partial degradation with automated fallback operational. Target ACK: < 1 hour.
- `WARN`: Ticket logged for daytime triage. Emerging capacity bottleneck or slow burn rate. Target ACK: < 24 hours.
- `INFO`: Recorded for trend analysis and automated reporting.

## 2. Multi-Window SLO Burn Rate Alerting Rules
Following Google SRE best practices:
| Window | Consumption Threshold | Burn Rate Multiplier | Alert Severity | Action |
|---|---|---|---|---|
| 1 Hour | 2% Error Budget | 14.4x | CRITICAL | PagerDuty Page |
| 6 Hours | 5% Error Budget | 6.0x | CRITICAL | PagerDuty Page |
| 24 Hours | 10% Error Budget | 3.0x | ERROR | Slack Alert & Incident Ticket |
| 3 Days | 10% Error Budget | 1.0x | WARN | Engineering Backlog Item |

## 3. Dynamic Alert Routing & Deduplication
`AlertRouter` and `AlertDispatcher` evaluate rule labels against team ownership, region, and tenant tier, applying a configurable cooldown window to prevent notification storms.
