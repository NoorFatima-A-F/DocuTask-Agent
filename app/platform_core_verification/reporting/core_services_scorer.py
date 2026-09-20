"""
Core Services Scorer for Part 4 - Platform Core Services Verification.
Aggregates section verification results and calculates composite score and maturity grades.
"""

from typing import Dict, List, Optional
from ..domain.models import (
    PlatformCoreVerificationScorecard,
    SectionId,
    SectionVerificationResult,
    VerificationStatus,
)


class CoreServicesScorer:
    def __init__(self):
        # Equal weights (1.0 each) for all 14 sections
        self.section_weights: Dict[SectionId, float] = {
            SectionId.SECTION_A_ORCHESTRATOR: 1.0,
            SectionId.SECTION_B_AGENT_KERNEL: 1.0,
            SectionId.SECTION_C_WORKFLOW_ENGINE: 1.0,
            SectionId.SECTION_D_SCHEDULER: 1.0,
            SectionId.SECTION_E_QUEUES: 1.0,
            SectionId.SECTION_F_STORAGE: 1.0,
            SectionId.SECTION_G_API_GATEWAY: 1.0,
            SectionId.SECTION_H_EVENT_BUS: 1.0,
            SectionId.SECTION_I_CONFIG_SECRETS: 1.0,
            SectionId.SECTION_J_CACHING: 1.0,
            SectionId.SECTION_K_IDENTITY_AUTH: 1.0,
            SectionId.SECTION_L_OBSERVABILITY: 1.0,
            SectionId.SECTION_M_RESILIENCE: 1.0,
            SectionId.SECTION_N_CROSS_SERVICE: 1.0,
        }

    def calculate_scorecard(
        self, section_results: Dict[str, SectionVerificationResult]
    ) -> PlatformCoreVerificationScorecard:
        total_weight = 0.0
        weighted_score_sum = 0.0
        total_assertions = 0
        passed_assertions = 0
        total_exec_time = 0.0

        for sec_id, res in section_results.items():
            weight = res.weight
            total_weight += weight
            weighted_score_sum += res.score * weight
            total_assertions += res.total_assertions_count
            passed_assertions += res.passed_assertions_count
            total_exec_time += res.execution_time_ms

        composite_score = weighted_score_sum / max(1.0, total_weight)
        grade = self._derive_grade(composite_score)

        return PlatformCoreVerificationScorecard(
            sections=section_results,
            composite_score=composite_score,
            grade=grade,
            total_assertions=total_assertions,
            passed_assertions=passed_assertions,
            total_execution_time_ms=total_exec_time,
        )

    def _derive_grade(self, score: float) -> str:
        if score >= 98.0:
            return "A+"
        elif score >= 90.0:
            return "A"
        elif score >= 80.0:
            return "B"
        elif score >= 70.0:
            return "C"
        elif score >= 60.0:
            return "D"
        return "F"
