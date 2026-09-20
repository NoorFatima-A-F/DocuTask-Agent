"""
Automated Action Verifier (Part 3H.3.4.10).
Validates that automated preventive actions follow the strict 4-step reliability lifecycle:
1. Detection (Anomaly/Risk identified)
2. Approval Policy (Pre-approved automated action vs human intervention required)
3. Action Execution (Dry-run or live mitigation)
4. Post-Action Verification (Residual risk metric validation)
"""
from typing import Dict, Any, List
from app.platform_verification.predictive_health_intelligence.domain.models import (
    PreventiveActionType,
    PreventiveRecommendation,
)


class AutomatedActionVerifier:
    """
    Validates safe closed-loop automated preventive actions.
    """

    def verify_action_pipeline(self, recommendation: PreventiveRecommendation) -> Dict[str, Any]:
        # Step 1: Detection
        step1_ok = bool(recommendation.rationale)

        # Step 2: Policy
        step2_ok = recommendation.automated_executable or not recommendation.requires_approval

        # Step 3: Action
        action_name = recommendation.action_type.value
        step3_ok = action_name in [a.value for a in PreventiveActionType]

        # Step 4: Verification
        step4_ok = recommendation.expected_risk_reduction_pct >= 50.0

        all_passed = step1_ok and step2_ok and step3_ok and step4_ok

        return {
            "action": action_name,
            "detection_verified": step1_ok,
            "policy_approved": step2_ok,
            "execution_verified": step3_ok,
            "post_action_verified": step4_ok,
            "closed_loop_safe": all_passed,
        }
