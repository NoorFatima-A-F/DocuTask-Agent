"""Multi-Dimensional Quality Scorer for Phase 4 Cross-System Integration."""

from datetime import datetime, timezone
from typing import Any, Dict, List
from ..domain.interfaces import ICrossSystemIntegrationQualityScorer
from ..domain.models import (
    CategoryScore,
    CertificationTier,
    CrossSystemIntegrationQualityScore,
    VerificationStatus,
)


class CrossSystemIntegrationQualityScorer(ICrossSystemIntegrationQualityScorer):
    """Calculates weighted certification score across 7 engineering pillars."""

    PILLAR_WEIGHTS = {
        "Architectural Decoupling & Dependencies": 0.15,
        "End-to-End Request & Workflow Chains": 0.20,
        "State, Data & Knowledge Flow Integrity": 0.20,
        "Security, Isolation & Tenant Boundaries": 0.15,
        "Multi-Agent, Eventing & Scheduling": 0.10,
        "Lifecycle, Deployment & Operational Reliability": 0.10,
        "Cross-System Performance & Evidence Assurance": 0.10,
    }

    PILLAR_REPORT_MAPPINGS = {
        "Architectural Decoupling & Dependencies": ["dependency_mapping", "interface_contract", "marketplace_validation"],
        "End-to-End Request & Workflow Chains": ["api_chain", "planning_pipeline", "enterprise_workflows"],
        "State, Data & Knowledge Flow Integrity": ["state_propagation", "knowledge_flow", "memory_interaction", "cognitive_integration", "data_integrity"],
        "Security, Isolation & Tenant Boundaries": ["security_boundary"],
        "Multi-Agent, Eventing & Scheduling": ["agent_collaboration", "event_bus", "scheduler"],
        "Lifecycle, Deployment & Operational Reliability": ["lifecycle_integration", "deployment_integration", "observability_integration", "failure_propagation"],
        "Cross-System Performance & Evidence Assurance": ["cross_system_performance", "integration_regression", "evidence_generation"],
    }

    def calculate_score(self, reports: Dict[str, Any]) -> CrossSystemIntegrationQualityScore:
        categories: List[CategoryScore] = []
        total_weighted_score = 0.0

        for pillar_name, weight in self.PILLAR_WEIGHTS.items():
            report_keys = self.PILLAR_REPORT_MAPPINGS.get(pillar_name, [])
            pillar_scores = []
            total_checks = 0
            passed_checks = 0

            for key in report_keys:
                rep = reports.get(key)
                if rep:
                    # rep can be model or dict
                    score_val = getattr(rep, "score", None) if hasattr(rep, "score") else rep.get("score", 0.0)
                    pillar_scores.append(float(score_val))
                    
                    checks = getattr(rep, "checks", None) if hasattr(rep, "checks") else rep.get("checks", [])
                    for chk in checks:
                        total_checks += 1
                        st = getattr(chk, "status", None) if hasattr(chk, "status") else chk.get("status")
                        if str(st) in ("VerificationStatus.PASSED", "PASSED"):
                            passed_checks += 1

            cat_avg_score = (sum(pillar_scores) / len(pillar_scores)) if pillar_scores else 100.0
            weighted_contribution = cat_avg_score * weight
            total_weighted_score += weighted_contribution

            cat_status = VerificationStatus.PASSED if cat_avg_score >= 80.0 else VerificationStatus.FAILED

            categories.append(
                CategoryScore(
                    name=pillar_name,
                    weight=weight,
                    score=round(cat_avg_score, 2),
                    weighted_score=round(weighted_contribution, 2),
                    checks_total=total_checks,
                    checks_passed=passed_checks,
                    status=cat_status,
                )
            )

        overall = round(total_weighted_score, 2)

        if overall >= 95.0:
            tier = CertificationTier.ENTERPRISE_INTEGRATION_CERTIFIED
            status = VerificationStatus.PASSED
        elif overall >= 90.0:
            tier = CertificationTier.HIGH_INTEGRATION_MATURITY
            status = VerificationStatus.PASSED
        elif overall >= 80.0:
            tier = CertificationTier.CONDITIONALLY_CERTIFIED
            status = VerificationStatus.WARNING
        else:
            tier = CertificationTier.CERTIFICATION_FAILED
            status = VerificationStatus.FAILED

        return CrossSystemIntegrationQualityScore(
            overall_score=overall,
            certification_tier=tier,
            verification_status=status,
            categories=categories,
            calculated_at=datetime.now(timezone.utc).isoformat(),
        )
