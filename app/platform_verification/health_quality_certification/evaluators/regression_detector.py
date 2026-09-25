"""
Phase 3H.5.11.4: Automated Health Quality Regression Detector
"""
from typing import Dict, List, Optional
from ..domain.models import (
    RegressionReport,
    RegressionComparison,
)
from ..domain.interfaces import IRegressionDetector


class RegressionDetector(IRegressionDetector):
    """
    Detects quality and health score regressions by comparing current verification results
    against prior baseline / deployment checkpoints.
    """

    DEFAULT_BASELINE = {
        "liveness": 97.0,
        "readiness": 96.0,
        "dependencies": 98.0,
        "failure_detection": 95.0,
        "recovery": 94.0,
        "monitoring": 96.0,
        "security": 100.0,
        "evidence": 100.0,
        "overall": 96.75,
    }

    def __init__(self, baseline: Optional[Dict[str, float]] = None):
        self.baseline = baseline or self.DEFAULT_BASELINE

    def detect_regression(
        self,
        current_scores: Dict[str, float],
        previous_scores: Optional[Dict[str, float]] = None,
    ) -> RegressionReport:
        base = previous_scores or self.baseline
        comparisons: List[RegressionComparison] = []
        any_regression = False

        for category, curr_score in current_scores.items():
            if category == "overall":
                continue
            prev_score = base.get(category, 90.0)
            delta = round(curr_score - prev_score, 2)
            # A regression is flagged if score drops by more than 2.0%
            is_regressed = delta < -2.0
            if is_regressed:
                any_regression = True

            comparisons.append(
                RegressionComparison(
                    category_name=category,
                    previous_score=prev_score,
                    current_score=curr_score,
                    delta=delta,
                    regression_detected=is_regressed,
                )
            )

        curr_overall = current_scores.get("overall", sum(current_scores.values()) / len(current_scores))
        prev_overall = base.get("overall", 96.75)
        overall_delta = round(curr_overall - prev_overall, 2)

        return RegressionReport(
            report_title="Health Quality Regression Verification Report",
            previous_overall_score=prev_overall,
            current_overall_score=round(curr_overall, 2),
            overall_delta=overall_delta,
            regression_detected=any_regression or (overall_delta < -2.0),
            categories=comparisons,
            regression_policy_passed=not any_regression and (overall_delta >= -2.0),
        )
