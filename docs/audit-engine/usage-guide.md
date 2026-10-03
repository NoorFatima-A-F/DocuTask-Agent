# Enterprise Audit Engine Usage Guide

## Commands

### 1. Run Complete Enterprise Due Diligence Audit
Executes all collectors, runs multi-dimensional strength analysis, tracks provenance, validates claims, and compiles the due diligence report suite:
```bash
python -m enterprise_audit_engine.cli.main verify-enterprise --repo-root . --output-dir audit_output
```

### 2. Verify Evidence Store Integrity (Tampering Detection)
Validates stored evidence records against the cryptographic SHA-256 hashes sealed in `manifest.json`:
```bash
python -m enterprise_audit_engine.cli.main verify-integrity --output-dir audit_output
```

### 3. CI/CD Release Gate Verification
Enforces release blocking in CI pipelines if evidence is insufficient or critical findings exist:
```bash
python -m enterprise_audit_engine.cli.main verify-gate --repo-root .
```

### 4. Run Standard Collection Pipeline
Collects raw evidence records into `audit_output/audit-evidence/`:
```bash
python -m enterprise_audit_engine.cli.main run-all --repo-root . --output-dir audit_output
```

### 5. Run Audit Engine Self-Verification Test Suite
```bash
pytest enterprise_audit_engine/tests/ -v
```
