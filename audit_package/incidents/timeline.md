# Incident Timeline: INC-2026-DR-001
All timestamps in UTC.

| Time (UTC) | Action / Event | Actor | Status |
|---|---|---|---|
| 14:00:00 | Simulated network partition injected into Primary DB node (AZ-1) | Chaos Engine | Initialized |
| 14:00:32 | Prometheus heartbeat alert fired: `PostgresLeaderUnreachable` | Alertmanager | Firing |
| 14:00:45 | Patroni cluster detected leader loss; initiated election | Patroni DCS | In Progress |
| 14:01:10 | Standby node in AZ-2 elected new leader; promoted to primary | Patroni | Promoted |
| 14:01:45 | PgBouncer dynamic connection pool redirected client connections | PgBouncer | Diverted |
| 14:02:15 | Microservices reconnected; health check endpoints returned 200 OK | Platform SRE | Healthy |
| 14:04:12 | Verification suite validated 100% data integrity & zero lost transactions | Verification Agent | Certified |
