"""
Autonomous Research - Master Research Engine Facade
Coordinates telemetry hypothesis generation, multi-armed bandit exploration, and discovery validation.
"""

from typing import Dict, List, Any
from app.runtime.research.hypothesis_generator import HypothesisGenerator
from app.runtime.research.exploration_strategy import ThompsonSamplingBandit
from app.runtime.research.discovery_validator import DiscoveryValidator


class AutonomousResearchEngine:
    """Master controller for autonomous scientific research and strategy discovery."""

    def __init__(self):
        self.hypothesis_gen = HypothesisGenerator()
        self.validator = DiscoveryValidator()
        self.bandit = ThompsonSamplingBandit(
            arm_names=[
                "ARM-FLASH-CACHED",
                "ARM-SPECULATIVE-PARALLEL",
                "ARM-ADAPTIVE-PRO-ROUTING",
                "ARM-ZERO-RETRY-FAST-FAIL",
            ]
        )

    def generate_hypotheses(
        self,
        p95_latency_ms: float = 950.0,
        avg_cost_usd: float = 0.008,
        ocr_confidence: float = 0.82,
    ) -> List[Dict[str, Any]]:
        hypotheses = self.hypothesis_gen.generate_hypotheses_from_telemetry(
            p95_latency_ms=p95_latency_ms,
            avg_cost_usd=avg_cost_usd,
            ocr_confidence=ocr_confidence,
        )
        return [h.to_dict() for h in hypotheses]

    def select_exploration_candidate(self) -> Dict[str, Any]:
        chosen_arm = self.bandit.select_arm()
        return {
            "selected_arm": chosen_arm,
            "bandit_algorithm": "Thompson Sampling (Beta Prior)",
            "arm_statistics": self.bandit.get_arm_statistics(),
        }

    def record_exploration_feedback(self, arm: str, reward: float):
        self.bandit.update(arm, reward)

    def validate_candidate(
        self,
        candidate_id: str,
        predicted_accuracy: float,
        predicted_latency_ms: float,
        predicted_cost_usd: float,
    ) -> Dict[str, Any]:
        report = self.validator.validate_candidate(
            candidate_id=candidate_id,
            predicted_accuracy=predicted_accuracy,
            predicted_latency_ms=predicted_latency_ms,
            predicted_cost_usd=predicted_cost_usd,
        )
        return report.to_dict()
