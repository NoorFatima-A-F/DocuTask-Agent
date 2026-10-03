# ADR-010: Retention Architecture

## Status
Accepted

## Context
Corporate compliance standards (e.g. IRS tax records, GDPR storage limitation, HIPAA 6-year retention) mandate automatic retention enforcement while ensuring active legal holds override scheduled deletions.

## Decision
1. Implement `RetentionPolicy` definitions with configurable schedules and actions on expiry (`ARCHIVE`, `DELETE`, `REQUIRE_APPROVAL`).
2. Implement `RetentionAndLegalHoldEngine` supporting active legal holds (`LegalHold`) that immutably freeze target assets and block deletion or archival until formally released by authorized legal counsel.

## Consequences
- **Positive**: Strict regulatory retention adherence combined with ironclad legal hold preservation.
- **Trade-off**: Requires periodic background expiration scanning.
