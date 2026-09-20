# Standalone Zero-Dependency External Verifier

## Overview
To facilitate third-party audits, acquisition due diligence, and enterprise customer compliance reviews, the platform provides a **Zero-Dependency Standalone Verifier** (`enterprise_audit_engine/external_verifier/`).

## Minimal Trusted Computing Base (TCB)
- **Zero Engine Imports**: Does not import collectors, analyzers, or orchestrators from `enterprise_audit_engine`.
- **Pure Cryptographic Evaluation**: Uses standard Ed25519 public key verification to validate digital certificates against portable evidence packages.

## Standalone Usage
```bash
python -m enterprise_audit_engine.external_verifier.cli \
    --certificate release_audit/verification_certificate.json \
    --public-key release_audit/public_key.pem \
    --merkle-manifest release_audit/audit_merkle_root.json
```

## Exit Codes
- `0`: Certificate is cryptographically authentic, active (non-expired), and Merkle root verified.
- `1`: Signature invalid, Merkle hash mismatched, certificate expired, or certificate revoked.
