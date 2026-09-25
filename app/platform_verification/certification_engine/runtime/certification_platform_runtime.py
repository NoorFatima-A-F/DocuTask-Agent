"""
Enterprise Certification Platform Runtime facade.
"""
from __future__ import annotations
from typing import Dict, Optional
from app.platform_verification.certification_engine.core.approval_workflow import EnterpriseApprovalWorkflow
from app.platform_verification.certification_engine.core.certification_engine import EnterpriseCertificationEngine
from app.platform_verification.certification_engine.core.change_impact_analyzer import EnterpriseChangeImpactAnalyzer
from app.platform_verification.certification_engine.core.dashboard_engine import EnterpriseCertificationDashboardEngine
from app.platform_verification.certification_engine.core.decision_engine import EnterpriseDecisionEngine
from app.platform_verification.certification_engine.core.exception_manager import EnterpriseExceptionManager
from app.platform_verification.certification_engine.core.policy_engine import ConfigurablePolicyEngine
from app.platform_verification.certification_engine.core.quality_gate_engine import EnterpriseQualityGateEngine
from app.platform_verification.certification_engine.core.risk_engine import EnterpriseRiskEngine
from app.platform_verification.certification_engine.domain.models import QualityGateDecision


class EnterpriseCertificationPlatformRuntime:
    """Unified runtime connecting all verification governance and certification engines."""

    def __init__(self, secret_key: str = "enterprise_verification_sec_key"):
        self.policy_engine = ConfigurablePolicyEngine()
        self.risk_engine = EnterpriseRiskEngine()
        self.gate_engine = EnterpriseQualityGateEngine()
        self.decision_engine = EnterpriseDecisionEngine(
            gate_engine=self.gate_engine,
            policy_engine=self.policy_engine,
            risk_engine=self.risk_engine,
        )
        self.cert_engine = EnterpriseCertificationEngine(secret_key=secret_key)
        self.approval_workflow = EnterpriseApprovalWorkflow()
        self.exception_manager = EnterpriseExceptionManager()
        self.change_impact_analyzer = EnterpriseChangeImpactAnalyzer(cert_engine=self.cert_engine)
        self.dashboard_engine = EnterpriseCertificationDashboardEngine(cert_engine=self.cert_engine)
        self._decisions: Dict[str, QualityGateDecision] = {}

    def record_decision(self, decision: QualityGateDecision) -> None:
        self._decisions[decision.decision_id] = decision
        self.dashboard_engine.recent_decisions.append(decision)

    def get_decision(self, decision_id: str) -> Optional[QualityGateDecision]:
        return self._decisions.get(decision_id)
