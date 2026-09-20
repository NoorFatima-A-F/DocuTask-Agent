"""
AOIS-HROP Phase 13.7 - Diagnosis Confidence Calculator
Computes statistical confidence scores for inferred root-cause hypotheses.
"""

from typing import List


class DiagnosisConfidenceCalculator:
    """
    Evaluates evidence corroboration across telemetry, event store logs, and replay traces to score diagnostic certainty.
    """

    def calculate_confidence(
        self,
        telemetry_corroborated: bool = True,
        event_store_confirmed: bool = True,
        replay_trace_matched: bool = True,
        truth_ledger_verified: bool = True,
        supporting_alert_count: int = 3,
    ) -> float:
        score = 0.50
        if telemetry_corroborated:
            score += 0.15
        if event_store_confirmed:
            score += 0.15
        if replay_trace_matched:
            score += 0.10
        if truth_ledger_verified:
            score += 0.05
        if supporting_alert_count > 2:
            score += 0.05

        return round(min(1.0, score), 4)
