# ADR-710: Compliance Profile Architecture

## Status
Accepted

## Context
Different industries require distinct compliance postures (SOC2, ISO27001, GDPR, HIPAA, PCI DSS) with differing retention windows, audit logging rules, and PII anonymization mandates.

## Decision
1. Implement `ComplianceFramework` with configurable profiles: `STANDARD`, `SOC2`, `ISO27001`, `GDPR`, `HIPAA`, and `PCI_DSS`.
2. Map compliance profiles to explicit rule sets defining retention minimums (e.g. 6 years for HIPAA, 2 years for GDPR), mandatory immutable audit logging, cross-border transfer prohibitions, and PII redaction enforcement.
3. Automatically apply compliance constraints during request dispatch and background task execution.

## Consequences
- **Positive**: Declarative, automated regulatory adherence tailored to each tenant's compliance requirements.
- **Trade-off**: High-retention compliance tiers (e.g. HIPAA) increase long-term storage requirements.
