# ADR-012: Privacy Control Model

## Status
Accepted

## Context
Handling sensitive customer data, employee records, and confidential identifiers requires flexible privacy-preserving techniques: partial masking for UI presentation, full redaction for logs, and tokenization for secure processing.

## Decision
Implement `PrivacyMaskingEngine` supporting 4 distinct privacy transformations:
1. **Masking**: Partially obscures sensitive fields (e.g. `john@example.com` $\to$ `j***@example.com`, SSN `***-**-1234`).
2. **Redaction**: Completely strips sensitive matches with `[REDACTED]`.
3. **Tokenization**: Replaces sensitive values with deterministic cryptographic tokens (`TOK_...`) backed by a secure vault.
4. **Detokenization**: Reversible reconstruction from secure tokens when authorized.

## Consequences
- **Positive**: Complies with GDPR Article 32 (pseudonymization) and HIPAA Safe Harbor privacy guidelines.
- **Trade-off**: Requires maintaining a secure tokenization vault for reversible workflows.
