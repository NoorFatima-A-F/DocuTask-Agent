# Enterprise Repository Ownership Matrix

| Subsystem / Path | Primary Owner | Backup Owner | Review Authority | Criticality |
|---|---|---|---|---|
| `app/shared_kernel/` | Platform Architecture Team | Staff Backend Leads | Architecture Board | Tier 1 (Critical) |
| `app/contexts/verification/` | Verification Squad | QA Platform Architect | Lead Verifier | Tier 1 (Critical) |
| `app/contexts/execution/` | Execution Platform Squad | SRE Lead | Platform Lead | Tier 1 (Critical) |
| `app/contexts/datasets/` | Data Engineering Squad | MLOps Architect | Data Lead | Tier 2 (High) |
| `app/contexts/environments/` | Infrastructure Squad | DevOps Lead | Platform Lead | Tier 2 (High) |
| `app/contexts/configuration/` | Infrastructure Squad | Security Architect | Platform Lead | Tier 1 (Critical) |
| `app/contexts/evidence/` | Storage & Evidence Squad | Compliance Lead | Security Lead | Tier 1 (Critical) |
| `app/contexts/metrics/` | AI Evaluation Squad | Data Science Lead | AI Lead | Tier 2 (High) |
| `app/contexts/statistics/` | Data Science Squad | AI Evaluation Lead | Science Lead | Tier 2 (High) |
| `app/contexts/quality/` | QA Governance Squad | Release Lead | QA Lead | Tier 1 (Critical) |
| `app/contexts/certification/` | Compliance Squad | Security Architect | Compliance Officer | Tier 1 (Critical) |
| `app/contexts/audit/` | Audit & Security Squad | Compliance Lead | Chief Security Officer | Tier 1 (Critical) |
| `app/contexts/plugins/` | Extensibility Squad | Developer Experience Lead | Platform Lead | Tier 3 (Medium) |
