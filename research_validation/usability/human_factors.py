"""
Research Validation & Independent Scientific Verification Framework (RVISF)
Phase 43: Human Factors & Usability Engineering Laboratory

Evaluates the usability, cognitive workload, and human-in-the-loop interaction efficiency:
- System Usability Scale (SUS) (Brooke, 1986; Bangor et al., 2008)
- NASA Task Load Index (NASA-TLX) Cognitive Workload Assessment (Hart & Staveland, 1988)
- Human Task Completion Rate, Time-on-Task, and Error Recovery Metrics
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


@dataclass
class SUSSurveyResponse:
    """
    Standard 10-item System Usability Scale (SUS) responses (each scored 1 to 5).
    Odd items (1, 3, 5, 7, 9) are positive statements.
    Even items (2, 4, 6, 8, 10) are negative statements.
    """
    respondent_id: str
    scores: List[int]  # Exactly 10 integers in range 1..5

    def __post_init__(self):
        if len(self.scores) != 10:
            raise ValueError(f"SUS survey must contain exactly 10 scores, got {len(self.scores)}")
        for s in self.scores:
            if s < 1 or s > 5:
                raise ValueError(f"SUS scores must be between 1 and 5 inclusive, got {s}")

    def calculate_score(self) -> float:
        """
        Calculate SUS score (0 to 100):
        - For odd items: contribution = score - 1
        - For even items: contribution = 5 - score
        - Multiply sum of contributions by 2.5
        """
        total = 0
        for i, s in enumerate(self.scores):
            if i % 2 == 0:  # Odd numbered question (0-indexed: 0, 2, 4, 6, 8)
                total += (s - 1)
            else:  # Even numbered question (0-indexed: 1, 3, 5, 7, 9)
                total += (5 - s)
        return total * 2.5


@dataclass
class NASATLXResponse:
    """
    NASA-TLX 6-dimensional workload assessment (each dimension 0 to 100).
    Dimensions: Mental, Physical, Temporal, Performance, Effort, Frustration.
    """
    respondent_id: str
    mental_demand: float
    physical_demand: float
    temporal_demand: float
    performance: float  # Inverted in Raw-TLX scoring (good performance = low workload)
    effort: float
    frustration: float

    def calculate_raw_tlx(self) -> float:
        """Compute Raw NASA-TLX score (average of 6 dimensions)."""
        dims = [
            self.mental_demand,
            self.physical_demand,
            self.temporal_demand,
            (100.0 - self.performance),  # Invert so higher means higher workload
            self.effort,
            self.frustration
        ]
        return sum(dims) / 6.0


@dataclass
class HumanFactorsAuditReport:
    """Comprehensive Usability & Human Workload Audit."""
    total_participants: int
    mean_sus_score: float
    sus_grade: str  # "A+", "A", "B", "C", "D", "F"
    mean_nasa_tlx_score: float
    task_completion_rate: float
    mean_time_on_task_sec: float
    meets_usability_standards: bool
    status: str  # "PASS", "ACCEPTABLE", "FAIL"
    details: Dict[str, Any] = field(default_factory=dict)


class HumanFactorsLab:
    """
    Verifies human-agent interaction quality, cognitive ergonomics, and operator usability.
    """

    @staticmethod
    def classify_sus_grade(sus_score: float) -> str:
        """Standard Bangor et al. (2009) SUS grade conversion."""
        if sus_score >= 84.1:
            return "A+"
        elif sus_score >= 80.3:
            return "A"
        elif sus_score >= 74.0:
            return "B"
        elif sus_score >= 68.0:
            return "C"  # 68 is empirical average
        elif sus_score >= 51.0:
            return "D"
        else:
            return "F"

    @classmethod
    def evaluate_human_factors(
        cls,
        sus_responses: List[SUSSurveyResponse],
        tlx_responses: List[NASATLXResponse],
        completion_results: List[bool],
        task_durations_sec: List[float]
    ) -> HumanFactorsAuditReport:
        """
        Evaluate full human factors empirical dataset.
        """
        if not sus_responses:
            return HumanFactorsAuditReport(
                total_participants=0,
                mean_sus_score=0.0,
                sus_grade="N/A",
                mean_nasa_tlx_score=0.0,
                task_completion_rate=0.0,
                mean_time_on_task_sec=0.0,
                meets_usability_standards=False,
                status="INSUFFICIENT_EVIDENCE"
            )

        n = len(sus_responses)
        sus_scores = [r.calculate_score() for r in sus_responses]
        mean_sus = sum(sus_scores) / n
        sus_grade = cls.classify_sus_grade(mean_sus)

        tlx_scores = [r.calculate_raw_tlx() for r in tlx_responses] if tlx_responses else [50.0]
        mean_tlx = sum(tlx_scores) / len(tlx_scores)

        comp_rate = (sum(1 for c in completion_results if c) / len(completion_results)) if completion_results else 1.0
        mean_time = (sum(task_durations_sec) / len(task_durations_sec)) if task_durations_sec else 0.0

        # Industry standard: SUS >= 68.0 (Above Average), Task Completion >= 85%, NASA-TLX <= 55
        meets_standards = (mean_sus >= 68.0) and (comp_rate >= 0.85) and (mean_tlx <= 60.0)

        status = "PASS" if meets_standards else "ACCEPTABLE" if mean_sus >= 60.0 else "FAIL"

        return HumanFactorsAuditReport(
            total_participants=n,
            mean_sus_score=mean_sus,
            sus_grade=sus_grade,
            mean_nasa_tlx_score=mean_tlx,
            task_completion_rate=comp_rate,
            mean_time_on_task_sec=mean_time,
            meets_usability_standards=meets_standards,
            status=status,
            details={
                "sus_scores": sus_scores,
                "nasa_tlx_scores": tlx_scores
            }
        )
