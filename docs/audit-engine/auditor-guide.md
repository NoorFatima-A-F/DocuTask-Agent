# Enterprise Software Auditor Guide

## 1. Quick Verification Protocol for External Auditors

As an external auditor, due diligence consultant, or CTO review team, follow this 4-step protocol to independently verify the platform:

### Step 1: Verify Engine Attestation & Integrity
Check the immutable engine build metadata:
```bash
cat enterprise_audit_engine/BUILD_INFO.json
cat enterprise_audit_engine/ENGINE_MANIFEST.json
```

### Step 2: Test Audit Reproducibility
Execute the twin-run deterministic reproducibility test:
```bash
python -m enterprise_audit_engine.cli.main reproduce-test --repo-root .
```
Verify that `differences_count == 0` and Merkle roots match.

### Step 3: Run Full Certification
```bash
python -m enterprise_audit_engine.cli.main enterprise-certify --repo-root .
```
Inspect the output summary and check:
- `Certification Status: ENTERPRISE_CERTIFIED`
- `Evidence Coverage: 100.0%`
- `Engine Security: SECURE`

### Step 4: Verify Cryptographic Hashes & Proofs
Inspect `release_audit/audit_merkle_root.json` and verify individual evidence records in `release_audit/collector_results/`.
```bash
python -m enterprise_audit_engine.cli.main verify-integrity --output-dir audit_output
```
