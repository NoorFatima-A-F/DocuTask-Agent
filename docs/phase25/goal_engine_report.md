# Phase 25.0 — Goal Understanding Engine Report

## 1. Objective & Scope

The Goal Understanding Engine transforms ambiguous user inputs into formal, verifiable `GoalSpecification` data structures. It bridges natural human intents with autonomous distributed agents by inferring document categories, parsing operational constraints, estimating risk, and synthesizing quantitative evaluation criteria.

---

## 2. Intent Classification Architecture

The `IntentClassifier` provides pattern recognition, keyword clustering, and contextual hints:

| Intent Category | Regex Patterns / Keywords | Target Domain | Default Risk Level |
| :--- | :--- | :--- | :--- |
| `INVOICE_PROCESSING` | `invoice`, `bill`, `accounts payable`, `line item`, `subtotal`, `po number` | Financial | Medium / Critical (if SOX) |
| `RECEIPT_ANALYSIS` | `receipt`, `expense`, `reimbursement`, `till slip` | Expenses | Low |
| `CONTRACT_REVIEW` | `contract`, `agreement`, `nda`, `clause`, `indemnification` | Legal | High |
| `COMPLIANCE_AUDIT` | `compliance`, `audit`, `regulatory`, `gdpr`, `hipaa`, `sox`, `kyc` | Compliance | Critical |
| `FRAUD_DETECTION` | `fraud`, `tamper`, `forgery`, `altered`, `irregularity` | Security | High |
| `BATCH_INGESTION` | `batch`, `bulk`, `dataset`, `directory`, `ingest all` | Operations | Medium |
| `RECONCILIATION` | `reconcile`, `3-way match`, `po match`, `discrepancy` | Accounting | Medium |
| `DATA_TRANSFORMATION` | `convert`, `transform`, `export`, `csv`, `parquet`, `json` | ETL | Low |

Confidence is calculated dynamically:
$$\text{Confidence} = \min\left(1.0, 0.70 + 0.15 \cdot (N_{\text{matches}} - 1)\right)$$
Domain specificity boosts are applied when distinct document indicators (e.g. invoices vs cross-cutting audit terms) are identified.

---

## 3. Constraint Extraction Engine

The `ConstraintExtractor` extracts both quantitative and qualitative invariants:
1. **Accuracy Threshold ($A_{\min}$):** Extracted from `%`, `percent`, or ratio formats (e.g. `accuracy >= 95%` $\to 0.95$).
2. **SLA & Latency Constraints:** Extracted from units:
   - Seconds (`s`, `sec`, `seconds`) $\to \Delta t$
   - Minutes (`m`, `min`, `minutes`) $\to \Delta t \cdot 60.0$
   - Milliseconds (`ms`, `milliseconds`) $\to \Delta t / 1000.0$
3. **Budget Caps:** Extracted from currency notations (e.g. `budget of $10` $\to \$10.00$).
4. **Compliance Mandates:** Enforces regulatory checks for `SOX`, `GDPR`, `HIPAA`, `PCI-DSS`, `SOC2`, and `ISO27001`.
5. **Human-in-the-loop Invariants:** Detects approval checkpoints and injects mandatory escalation gates.

---

## 4. Empirical Validation Evidence

- **Unit Tests:** 44 comprehensive tests in `tests/agents/intelligence/test_goal_understanding.py` (100% pass rate in 0.13s).
- **Ambiguity Detection:** Correctly identifies underspecified objectives ($\text{length} < 5$ chars or confidence $< 0.60$) and marks `requires_clarification = True`.
- **Criteria Evaluation:** Evaluates multi-metric completion payloads and sets `GoalStatus.COMPLETED` or `GoalStatus.FAILED`.
