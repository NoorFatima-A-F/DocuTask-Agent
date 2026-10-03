# ADR-835: Retention Policies, Lifecycle Automation & Legal Holds

## Status
Accepted

## Context
Enterprise data regulations require balancing data minimization (e.g. GDPR storage limitation) with statutory retention mandates (e.g. 7-year retention for financial records, HIPAA 6-year requirements). Additionally, ongoing litigation requires immutable legal holds that prevent automated or manual deletion of relevant audit records.

## Decision
We implemented a retention policy engine under `app/audit/retention/`:
1. **Configurable Retention Policies (`RetentionPolicy`)**:
   - `DELETE_AFTER_PERIOD`: Automated purge after retention window expires.
   - `ARCHIVE`: Move historical audit blocks to immutable cold storage.
   - `PERMANENT_RETENTION`: Indefinite preservation for foundational records.
2. **Legal Hold Engine (`LegalHold`)**:
   - Allows compliance officers to place legal hold locks on a tenant, case, or specific set of event IDs.
   - Active legal holds strictly override retention expiration rules, preventing premature deletion or archiving.

## Consequences
### Positive
- Automated compliance with data minimization and statutory retention periods.
- Bulletproof defense against spoliation of evidence during legal investigations.
