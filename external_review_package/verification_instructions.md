# External Auditor Verification Instructions

## Overview
This package contains cryptographically signed audit evidence and certification for **DocuTask Agent (Release 1.0.0)**.
Third-party auditors can independently verify all claims, signatures, and evidence integrity without access to the source code repository.

## Step 1: Verify Digital Signature & Certificate Integrity
Run the standalone verifier CLI against the signed certificate and public key:
```bash
python -m enterprise_audit_engine.cli.main verify-certificate \
    --certificate certificate.json \
    --public-key public_key.pem \
    --merkle-manifest merkle_root.json
```

## Step 2: Validate Cryptographic Merkle Root
Verify that the `merkle_root` inside `certificate.json` matches the root calculated in `merkle_root.json`.

- **Expected Merkle Root**: `7d0cfac2ddd6a08cd3af75c74a288e7b18328fa27c43c35843b9b9fa5a35cb33`
- **Evidence Quality Index (EQI)**: `99.38 / 100`
- **Certification Status**: `VALID`
- **Expiry Date**: `2027-03-19T19:40:26.059776+00:00`

## Step 3: Inspect Raw Evidence & Findings
All individual evidence records supporting every report statement are archived in `selected_evidence/`.
Inspect the executive and technical due diligence reports in `reports/`.
