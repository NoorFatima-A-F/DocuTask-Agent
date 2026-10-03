# Evidence Reliability Index (ERI) & Composite Trust Score Model

## Overview

The **Enterprise Audit Trust Metrics Engine** (`enterprise_audit_engine/trust_metrics`) provides a deterministic, mathematically sound framework to score audit trustworthiness. It combines the **Evidence Reliability Index (ERI)** and multi-dimensional trust dimensions to produce an unambiguous **Evidence Trust Score (0–100)**.

---

## 1. Evidence Reliability Index (ERI)

The **Evidence Reliability Index (ERI)** measures the intrinsic quality and empirical verifiability of collected audit evidence.

### Formula & Dimensional Weights

$$\text{ERI} = 0.30 \cdot S_{\text{execution}} + 0.25 \cdot S_{\text{confirmation}} + 0.20 \cdot S_{\text{completeness}} + 0.15 \cdot S_{\text{stability}} + 0.10 \cdot S_{\text{reproducibility}}$$

| Dimension | Weight | Description |
| :--- | :---: | :--- |
| **Execution Reality ($S_{\text{execution}}$)** | **30%** | Proportion of assertions validated through live binary/runtime execution rather than static code inspection or self-declared documentation. |
| **Independent Confirmation ($S_{\text{confirmation}}$)** | **25%** | Proportion of claims verified by independent out-of-band probes (API, DB, security probes). |
| **Artifact Completeness ($S_{\text{completeness}}$)** | **20%** | Integrity of cryptographic hashes, Merkle root inclusion, and complete provenance tracking for all cited artifacts. |
| **Historical Stability ($S_{\text{stability}}$)** | **15%** | Consistency of evidence and zero regression across consecutive audit runs and release cycles. |
| **External Reproducibility ($S_{\text{reproducibility}}$)** | **10%** | Verification success when the standalone zero-dependency verification package is evaluated in an isolated external sandbox. |

---

## 2. Composite Evidence Trust Score

The Composite Trust Score synthesizes collector health, cryptographic integrity, contradiction penalties, and persona consensus into a single 0–100 scale:

$$\text{Trust Score} = \left( \sum_{i} w_i \cdot D_i \right) - P_{\text{contradictions}} - P_{\text{drift}} - P_{\text{blockers}}$$

### Score Categorization & Certification Eligibility

| Score Range | Trust Tier | Certification Eligibility |
| :--- | :--- | :--- |
| **90.0 – 100.0** | **Grade A: High Trust (Enterprise Certified)** | Eligible for full production certification and compliance sealing. |
| **80.0 – 89.9** | **Grade B: Qualified Trust** | Eligible with conditional remediations or non-critical waivers. |
| **65.0 – 79.9** | **Grade C: Insufficient Trust** | Ineligible. Requires remediation of evidence gaps. |
| **< 65.0** | **Grade F: Untrusted / Tampered** | Immediate `CERTIFICATION_REJECTED`. Potential security violations or unverified claims. |

---

## 3. Strict Penalty Matrix

1. **Unresolved Contradiction Penalty**: $-50.0$ points per confirmed contradiction (immediately forces Grade F).
2. **Missing Cryptographic Proof**: $-15.0$ points per missing SHA-256 or broken Merkle proof.
3. **Auditor Persona Blocker**: $-25.0$ points per persona blocker veto.
4. **Drift Divergence**: $-10.0$ points if code/dependency drift exceeds configured threshold ($> 15\%$).
