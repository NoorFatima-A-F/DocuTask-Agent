"""
Enterprise AI Risk Register Engine.
"""

from typing import List, Dict, Any
from app.certification.domain.models import RiskCategory, RiskSeverity, RiskEntry


class RiskRegisterEngine:
    """Compiles Technical, AI Cognitive, Security, and Business Operational risks with mitigations."""

    @staticmethod
    def get_full_risk_register() -> List[RiskEntry]:
        return [
            RiskEntry(
                risk_id="RISK-TECH-01",
                category=RiskCategory.TECHNICAL,
                description="Upstream LLM API latency spike or 503 outage causing document queue buildup",
                probability="MEDIUM",
                impact="HIGH",
                severity=RiskSeverity.HIGH,
                mitigation_control="Dynamic secondary model failover + asynchronous Celery exponential backoff queue",
                residual_risk="LOW",
                status="MITIGATED",
            ),
            RiskEntry(
                risk_id="RISK-AI-02",
                category=RiskCategory.AI_COGNITIVE,
                description="Hallucinated invoice total or line-item amount resulting in overpayment",
                probability="LOW",
                impact="HIGH",
                severity=RiskSeverity.HIGH,
                mitigation_control="Deterministic mathematical PO cross-validation + strict JSON schema grounding + HITL gate for value >$50k",
                residual_risk="VERY LOW",
                status="MITIGATED",
            ),
            RiskEntry(
                risk_id="RISK-SEC-03",
                category=RiskCategory.SECURITY,
                description="Indirect prompt injection embedded in scanned vendor PDF payload",
                probability="MEDIUM",
                impact="CRITICAL",
                severity=RiskSeverity.CRITICAL,
                mitigation_control="Pre-LLM document payload sanitizer, markdown escape delimiters, sandboxed tool permission gating",
                residual_risk="LOW",
                status="MITIGATED",
            ),
            RiskEntry(
                risk_id="RISK-SEC-04",
                category=RiskCategory.SECURITY,
                description="Cross-tenant document data leakage via vector similarity search",
                probability="LOW",
                impact="CRITICAL",
                severity=RiskSeverity.CRITICAL,
                mitigation_control="Hard cryptographic tenant_id partition filter enforced at the database/Qdrant collection level",
                residual_risk="NEGLIGIBLE",
                status="CONTROLLED",
            ),
            RiskEntry(
                risk_id="RISK-BIZ-05",
                category=RiskCategory.BUSINESS_OPERATIONAL,
                description="User resistance due to lack of explainability or trust in autonomous decisions",
                probability="MEDIUM",
                impact="MEDIUM",
                severity=RiskSeverity.MEDIUM,
                mitigation_control="Visual bounding-box provenance citations in Approval Center + clear decision audit trail",
                residual_risk="LOW",
                status="MITIGATED",
            ),
        ]
