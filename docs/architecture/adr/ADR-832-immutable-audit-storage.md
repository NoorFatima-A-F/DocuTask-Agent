# ADR-832: Immutable Storage & Cryptographic Hash Chaining

## Status
Accepted

## Context
Audit records must be provably tamper-resistant to satisfy compliance audits and legal discovery. Any malicious or accidental alteration, deletion, or reordering of audit logs must be immediately detectable by auditors and automated verification tools.

## Decision
We implemented an append-only store with cryptographic hash chaining (`app/audit/integrity/` and `app/audit/storage/`):
1. **Hash Chaining**: Each audit record computes its SHA-256 integrity hash by combining its canonical JSON payload with the hash of the preceding event in the tenant's chain:
   $$H_n = \text{SHA256}(\text{canonical\_json}(E_n) + H_{n-1})$$
   where $H_0 = \text{"0000...0000"}$ (Genesis Hash).
2. **Digital Signatures**: Events are signed with HMAC-SHA256 signatures to ensure authenticity.
3. **Immutability Invariant**: Updates and direct deletions are strictly rejected.
4. **Verification Engine (`verify_audit_integrity()`)**: Traverses the sequential hash chain, re-computing each block hash to detect corrupted, modified, or omitted records.

## Consequences
### Positive
- Guarantees tamper-evidence and non-repudiation for all audit events.
- Immediate detection of any unauthorized database manipulation or missing events.
