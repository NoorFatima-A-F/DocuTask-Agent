# Mutation Security & Adversarial Testing Suite

## Objective
To prove mathematically and empirically that the audit engine cannot be tricked into certifying a defective or tampered system, the engine includes a **50+ Synthetic Mutation Testing Suite**.

## Mutation Attack Categories

| Category | Count | Attack Vectors Simulated | Defense Mechanism |
| :--- | :--- | :--- | :--- |
| **Evidence Manipulation** | 15 | Payload tampering, hash forging, dropping referenced records, empty payloads | SHA-256 Content Hash Verification, Merkle Tree proofs |
| **Classification Attacks** | 15 | Claim promotion from INSUFFICIENT to VERIFIED, static-only execution claims | `ClaimValidator` contract checks, rule boundary enforcement |
| **Cryptographic Forgery** | 10 | Altering signed certificates, signature stripping, invalid public keys | Ed25519 digital signature cryptographic validation |
| **Policy Degradation** | 10 | Lowering EQI thresholds, removing required domains, unprovable claims | `PolicyRegressionDetector`, `ClaimEvidenceMatcher` |

## Execution
```bash
python -m enterprise_audit_engine.cli.main run-expanded-mutations
```
All 50 mutations must be blocked (100% defense rate) for release gating to pass.
