# Deterministic Audit Reproducibility Engine

## 1. Principles of Deterministic Auditing
An enterprise audit must not depend on environmental nondeterminism, network fluctuations, or execution race conditions. Given identical repository state:
`Audit(Repo_t) == Audit(Repo_t)`

## 2. Twin-Run Verification Process
The `AuditReproducibilityVerifier` performs:
1. Spawns `Run A` in isolated sandbox directory `dir_a`.
2. Spawns `Run B` in isolated sandbox directory `dir_b`.
3. Validates:
   - **Evidence Count Match**: Identical number of `EV-` records collected.
   - **Category Mapping Match**: Categorical classification parity.
   - **Collector Manifest Match**: Every collector completion status is identical.
   - **Merkle Root Equivalence**: Root SHA-256 of `Run A` equals `Run B`.

## 3. CLI Execution
```bash
python -m enterprise_audit_engine.cli.main reproduce-test --repo-root .
```

Output:
```
[*] Testing Audit Reproducibility across twin runs for: /repo
[*] Reproducibility Verification Result:
    - Deterministic:     True
    - Status:            DETERMINISTIC_REPRODUCIBLE
    - Run A Merkle Root: a1b2c3...
    - Run B Merkle Root: a1b2c3...
    - Discrepancies:     0

[+] Audit Engine Proven Deterministic & Reproducible.
```
