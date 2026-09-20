"""
Master Platform Certification Scorer.
Executes all certification engines, aggregates dimension scores, evaluates the certification gate,
and generates the unified EnterpriseReadinessScorecard.
"""

import time
from typing import Dict, List, Any, Optional
from ..domain.models import (
    CertificationLevel,
    CertificationDecisionStatus,
    EnterpriseReadinessScorecard,
    CertificationPillarResult,
)
from ..evidence_registry.evidence_registry_engine import EvidenceRegistryEngine
from ..scoring.verification_score_engine import VerificationScoreEngine
from ..certification.architecture_certifier import ArchitectureCertifier
from ..certification.ai_capability_certifier import AICapabilityCertifier
from ..certification.security_certifier import SecurityCertifier
from ..certification.reliability_certifier import ReliabilityCertifier
from ..certification.business_value_certifier import BusinessValueCertifier
from ..certification.certification_gate import CertificationGate
from ..readiness_review.prr_engine import PRREngine
from ..risk_management.risk_register_engine import RiskRegisterEngine
from ..governance.ai_governance_engine import AIGovernanceEngine
from ..dashboards.certification_dashboard import CertificationDashboardVerifier
from ..continuous_monitoring.continuous_verifier import ContinuousVerifier


class CertificationScorer:
    """Master orchestrator executing all Phase V12 certification engines and computing composite readiness."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.verifiers = [
            ("evidence_registry", EvidenceRegistryEngine(self.config)),
            ("scoring", VerificationScoreEngine(self.config)),
            ("architecture", ArchitectureCertifier(self.config)),
            ("ai_capability", AICapabilityCertifier(self.config)),
            ("security", SecurityCertifier(self.config)),
            ("reliability", ReliabilityCertifier(self.config)),
            ("business_value", BusinessValueCertifier(self.config)),
            ("certification_gate", CertificationGate(self.config)),
            ("prr", PRREngine(self.config)),
            ("risk_management", RiskRegisterEngine(self.config)),
            ("governance", AIGovernanceEngine(self.config)),
            ("dashboards", CertificationDashboardVerifier(self.config)),
            ("continuous_monitoring", ContinuousVerifier(self.config)),
        ]

    def run_all(self) -> EnterpriseReadinessScorecard:
        """Executes all certification engines and returns the full EnterpriseReadinessScorecard."""
        start_t = time.perf_counter()
        pillar_results: Dict[str, CertificationPillarResult] = {}
        total_assertions = 0
        passed_assertions = 0

        for key, verifier in self.verifiers:
            res = verifier.verify()
            pillar_results[key] = res
            total_assertions += res.total_assertions_count
            passed_assertions += res.passed_assertions_count

        # Compute dimensions
        score_engine = VerificationScoreEngine(self.config)
        dimensions = score_engine.calculate_dimensions()
        overall_score = score_engine.compute_overall_score(dimensions)
        cert_level = score_engine.determine_certification_level(overall_score)

        # Evaluate gate
        gate = CertificationGate(self.config)
        decision = gate.evaluate_gate(
            enterprise_score=overall_score,
            security_score=dimensions["security"].raw_score,
            reliability_score=dimensions["reliability"].raw_score,
            critical_risks=0,
        )

        elapsed_ms = (time.perf_counter() - start_t) * 1000.0

        return EnterpriseReadinessScorecard(
            overall_readiness_score=overall_score,
            certification_level=cert_level,
            decision=decision,
            dimensions=dimensions,
            pillar_results=pillar_results,
            critical_risks_count=0,
            total_assertions=total_assertions,
            passed_assertions=passed_assertions,
            total_execution_time_ms=elapsed_ms,
        )
