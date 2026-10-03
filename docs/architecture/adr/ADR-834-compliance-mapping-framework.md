# ADR-834: Compliance Mapping & Regulatory Assessment Framework

## Status
Accepted

## Context
DocuTask Agent operates in regulated enterprise domains requiring demonstrable adherence to global frameworks: SOC 2 Type II, ISO/IEC 27001, GDPR, HIPAA, NIST AI RMF 1.0, ISO/IEC 42001 (AIMS), and the EU Artificial Intelligence Act. Manual compliance verification is slow, error-prone, and unsustainable.

## Decision
We implemented a dynamic compliance mapping and evaluation engine under `app/audit/compliance/`:
1. **Standardized Control Model (`ComplianceControl`)**: Models regulatory requirements across SOC 2 (CC6.1, CC7.2), ISO 27001 (A.12.4.1), GDPR (Art. 30, 32), NIST AI RMF (GOVERN 1.2, MANAGE 2.4), and EU AI Act (Art. 12, 14, 15).
2. **Automated Evaluation Engine (`evaluate_compliance()`)**:
   - Inspects tenant audit event logs and evidence artifacts.
   - Evaluates evidence coverage against control requirements.
   - Computes compliance percentages, highlights missing evidence, and issues proactive remediation recommendations.

## Consequences
### Positive
- Continuous, automated compliance posture monitoring.
- Real-time gap analysis and evidence tracking for internal and external auditors.
