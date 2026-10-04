# Verification Platform Threat Model (STRIDE)

| Threat Category | Potential Attack Vector | Mitigation in FVPA Architecture |
|---|---|---|
| **Spoofing** | Forged verification run requests | HMAC-SHA256 authenticated API signatures & Tenant ID isolation. |
| **Tampering** | Altering test results or metrics | Immutable SHA-256 CAS Evidence store & Merkle root sealing. |
| **Repudiation** | Denying release gate failures | Cryptographic append-only hash-chained audit ledger (`sha256_prev_hash`). |
| **Information Disclosure** | Leakage of golden dataset contents | Multi-scoped tenant isolation and encrypted CAS buckets. |
| **Denial of Service** | Long-running test hangs | Strict timeout execution boundaries, retry limits, and Circuit Breaker pattern. |
| **Elevation of Privilege** | Bypassing hard quality gates | Hard blocker enforcement in `QualityGateEngine` with CA cryptographic signatures. |
