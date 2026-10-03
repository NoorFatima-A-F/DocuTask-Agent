# External Benchmark Methodology & Archetype Calibration

## Overview

The **External Benchmark Suite** (`enterprise_audit_engine/benchmark`) validates the audit engine's discriminatory power by executing full audit pipelines against standardized reference archetypes. This guarantees that the audit engine reliably awards high marks to well-engineered codebases and unerringly fails vulnerable, incomplete, or misleading systems.

---

## 1. Reference Archetypes

| Archetype | Expected Result | Expected Score | Description & Key Characteristics |
| :--- | :---: | :---: | :--- |
| **Archetype A: Golden Enterprise System** | `CERTIFIED` | **90.0 – 100.0** | Full test coverage ($> 85\%$), pinned dependencies, zero known CVEs, authenticated APIs, verified DB rollback, complete provenance. |
| **Archetype B: Intentionally Vulnerable System** | `REJECTED` | **< 60.0** | Hardcoded secrets, unauthenticated admin routes, SQL injection risks, permissive CORS (`*`), unpinned outdated libraries. |
| **Archetype C: Misleading / High-Test Façade** | `REJECTED` | **< 65.0** | High static test pass count ($99\%+$) but assertions are mocks or empty `pass`, reality probes fail on runtime endpoints and persistence. |

---

## 2. 250+ Adversarial Mutation Test Matrix

The benchmark includes an active automated battery of **250 adversarial mutation attacks** across 5 distinct domains (50 attacks per domain):

```
┌────────────────────────────────────────────────────────────────────────┐
│                   250 ADVERSARIAL MUTATION VECTORS                     │
├──────────────────┬──────────────────┬──────────────────────────────────┤
│ EVIDENCE ATTACKS │ CERT. ATTACKS    │ AI PIPELINE ATTACKS              │
│ (50 Attacks)     │ (50 Attacks)     │ (50 Attacks)                     │
│ - Hash tampering │ - Expired cert   │ - Unprovable capability claims   │
│ - Merkle pruning │ - Bit-flip sig   │ - Mock/static masquerade         │
│ - Null payload   │ - Revoked cert   │ - Prompt-override injection      │
├──────────────────┴──────────────────┴──────────────────────────────────┤
│ SECURITY ATTACKS (50 Attacks)       │ SUPPLY-CHAIN ATTACKS (50 Attacks)│
│ - Mass assignment role escalation   │ - Dependency lockfile poisoning  │
│ - JWT 'none' signature bypass       │ - Typosquatting injection        │
│ - Path traversal & LFI probes       │ - Unpinned external artifacts    │
└─────────────────────────────────────┴──────────────────────────────────┘
```

### Defense Requirement
- **100% Detection Rate**: The audit engine must identify and reject all 250 adversarial mutation variants without false negatives.
