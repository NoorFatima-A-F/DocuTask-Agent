"""CI/CD Deployment Gate Evaluator (3H.3.12.10).

Evaluates whether readiness verification and audit packages satisfy deployment gating thresholds:
- Zero critical readiness failures
- Evidence package complete (all 13 manifests present)
- Certification score >= 95.0%
"""

from typing import Dict, Any
from ..domain.models import AuditQualityScorecard


class CICDDeploymentGateEvaluator:
    """Evaluates readiness evidence against CI/CD release gating policies."""

    def evaluate_gate(self, scorecard: AuditQualityScorecard, manifests_count: int) -> Dict[str, Any]:
        has_critical_failure = not scorecard.passed
        evidence_complete = (manifests_count >= 13)
        score_meets_threshold = (scorecard.overall_score >= 95.0)

        gate_approved = (not has_critical_failure) and evidence_complete and score_meets_threshold

        return {
            "deployment_gate_decision": "APPROVED" if gate_approved else "REJECTED",
            "passed": gate_approved,
            "checks": {
                "no_critical_failures": not has_critical_failure,
                "evidence_manifests_complete": evidence_complete,
                "certification_score_threshold_met": score_meets_threshold,
            },
            "score": scorecard.overall_score,
            "minimum_required_score": 95.0,
        }
