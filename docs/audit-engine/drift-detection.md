# Certification Drift Detection Engine

## Overview

The **Certification Drift Detection Engine** (`enterprise_audit_engine/drift_detection`) tracks divergence between the state of the codebase when a certificate was issued and its current state. It prevents "stale certificate masquerading" where an application evolves while claiming past certification validity.

---

## 1. Monitored Drift Vectors

```
┌────────────────────────────────────────────────────────────────────────┐
│                        DRIFT DETECTION MATRIX                          │
├────────────────────┬────────────────────┬──────────────────────────────┤
│     CODE DRIFT     │  DEPENDENCY DRIFT  │     INFRASTRUCTURE DRIFT     │
│ - Source SHA-256   │ - Lockfile Hash    │ - Dockerfile / OCI Digest    │
│ - Git Commit Diff  │ - Version Pinning  │ - Kubernetes Manifests       │
│ - Ast Complexity   │ - CVE Exposure     │ - Environment Variables      │
└─────────┬──────────┴─────────┬──────────┴──────────────┬───────────────┘
          │                    │                         │
          ▼                    ▼                         ▼
┌────────────────────────────────────────────────────────────────────────┐
│                    DRIFT REPORT & SEVERITY SCORING                     │
│  - Total Drift Percentage (0% - 100%)                                  │
│  - Critical Drift Indicators (e.g., Security Config Modification)      │
│  - Automated Revocation Trigger (> 25% or Critical Mutation)           │
└────────────────────────────────────────────────────────────────────────┘
```

### 1.1 Source Code Drift
- Measures AST structure, line additions/deletions, and SHA-256 tree hashes since certification issuance.
- **Threshold**: Changes to $> 15\%$ of audited source files or modifications to core auth/security modules trigger an invalidation alert.

### 1.2 Dependency Drift
- Tracks changes in lockfiles (`poetry.lock`, `Pipfile.lock`, `package-lock.json`, `requirements.txt`).
- Assesses newly introduced packages or unpinned version updates for known CVE disclosures.

### 1.3 Infrastructure & Configuration Drift
- Compares OCI container base image digests, Helm charts, Kubernetes YAMLs, and `.env` template definitions against the certified baseline.

---

## 2. Drift Impact on Certification Status

- **0% – 5% Drift**: `VALID` (Minor maintenance changes, no security impact).
- **5% – 20% Drift**: `NEEDS_REVALIDATION` (Notice issued, recertification recommended).
- **> 20% Drift or Critical Module Mutation**: `CERTIFICATION_REVOKED` (Automatic invalidation; certificate marked superseded or lapsed).
