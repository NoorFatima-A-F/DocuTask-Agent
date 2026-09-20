"""
AI Evaluation and Prompt Regression Verifier.
"""
from typing import Dict, Any, List
from app.platform_verification.test_architecture_verification.domain.models import AiEvaluationTestReport
from app.platform_verification.test_architecture_verification.domain.interfaces import IAiEvaluationVerifier


class AiEvaluationVerifier(IAiEvaluationVerifier):
    """Verifies prompt regression thresholds, ground truth F1, and hallucination rates."""

    def verify_ai_evaluation_suite(self, ai_test_data: Dict[str, Any]) -> AiEvaluationTestReport:
        prompt_reg_pass = ai_test_data.get("prompt_regression_passed", True)
        f1 = ai_test_data.get("ground_truth_f1_score", 0.945)
        hallucination_pct = ai_test_data.get("hallucination_rate_pct", 1.5)
        consistency_pct = ai_test_data.get("stochastic_consistency_pct", 98.0)
        scenarios = ai_test_data.get("evaluated_scenarios", 100)
        issues: List[str] = []

        if not prompt_reg_pass:
            issues.append("Prompt regression detected: extraction quality degraded against baseline")
        if f1 < 0.90:
            issues.append(f"Ground truth F1 score ({f1:.3f}) below threshold 0.90")
        if hallucination_pct > 3.0:
            issues.append(f"Hallucination rate ({hallucination_pct:.1f}%) exceeds safety limit of 3.0%")
        if consistency_pct < 95.0:
            issues.append(f"Stochastic consistency ({consistency_pct:.1f}%) below tolerance of 95.0%")

        status = "PASS" if len(issues) == 0 else "FAIL"

        return AiEvaluationTestReport(
            status=status,
            prompt_regression_passed=prompt_reg_pass,
            ground_truth_f1_score=f1,
            hallucination_rate_pct=hallucination_pct,
            stochastic_consistency_pct=consistency_pct,
            evaluated_scenarios=scenarios,
            issues=issues,
        )
