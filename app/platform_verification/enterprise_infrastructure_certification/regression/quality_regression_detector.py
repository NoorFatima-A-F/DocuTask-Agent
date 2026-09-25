"""
Phase 3O: Quality Regression Detection System.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from ..domain.interfaces import IQualityRegressionDetector
from ..domain.models import (
    QualityRegressionReport,
    QualityScorecard,
    RegressionFinding,
    RiskLevel,
)


class QualityRegressionDetector(IQualityRegressionDetector):
    """
    Detects quality regressions by comparing current scorecard metrics against
    historical baseline scorecards.
    """

    def detect_regressions(
        self,
        current_scorecard: QualityScorecard,
        previous_data: Optional[Dict[str, Any]] = None,
    ) -> QualityRegressionReport:
        if previous_data is None:
            # Baseline baseline if no previous run data provided
            previous_overall = 95.0
            previous_categories = {
                "Reliability": 95.0,
                "Security": 95.0,
                "Scalability": 95.0,
                "Observability": 95.0,
                "Deployment Quality": 95.0,
                "Recovery Capability": 95.0,
            }
            prev_ver = "3.16.0"
        else:
            previous_overall = float(previous_data.get("overall_score", 95.0))
            previous_categories = previous_data.get("categories", {})
            prev_ver = previous_data.get("version", "3.16.0")

        findings: List[RegressionFinding] = []
        regression_flag = False

        for cat_name, cat_obj in current_scorecard.categories.items():
            prev_score = float(previous_categories.get(cat_name, 95.0))
            curr_score = cat_obj.score
            delta = round(curr_score - prev_score, 2)

            is_reg = delta < -3.0  # More than 3% drop is flagged as regression
            if is_reg:
                regression_flag = True
                if delta < -10.0:
                    sev = RiskLevel.HIGH
                else:
                    sev = RiskLevel.MEDIUM
            else:
                sev = RiskLevel.NONE

            findings.append(
                RegressionFinding(
                    category=cat_name,
                    metric_name=f"{cat_name} Score",
                    previous_score=prev_score,
                    current_score=curr_score,
                    delta=delta,
                    is_regression=is_reg,
                    severity=sev,
                )
            )

        overall_delta = round(current_scorecard.overall_score - previous_overall, 2)
        if overall_delta < -3.0:
            regression_flag = True

        return QualityRegressionReport(
            previous_version=prev_ver,
            current_version="3.17.0",
            previous_overall_score=previous_overall,
            current_overall_score=current_scorecard.overall_score,
            score_delta=overall_delta,
            regression_detected=regression_flag,
            findings=findings,
            analyzed_at=datetime.now(timezone.utc).isoformat(),
        )
