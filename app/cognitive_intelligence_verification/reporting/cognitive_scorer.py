"""
Cognitive Platform Verification Scorer.
Executes all 19 verification engines, aggregates assertions, and calculates composite readiness score and indices.
"""

import time
from typing import Dict, List, Any
from ..domain.models import (
    CognitiveReadinessScorecard,
    PartVerificationResult,
)
from ..reasoning.reasoning_verifier import ReasoningVerifier
from ..graph.cognitive_graph_verifier import CognitiveGraphVerifier
from ..hypothesis.hypothesis_verifier import HypothesisVerifier
from ..decision.decision_verifier import DecisionVerifier
from ..simulation.simulation_verifier import SimulationVerifier
from ..learning.learning_verifier import LearningVerifier
from ..experience.experience_verifier import ExperienceVerifier
from ..process_discovery.process_discovery_verifier import ProcessDiscoveryVerifier
from ..alignment.alignment_verifier import AlignmentVerifier
from ..recommendations.recommendations_verifier import RecommendationsVerifier
from ..continuous_learning.continuous_learning_verifier import ContinuousLearningVerifier
from ..optimization.optimization_verifier import OptimizationVerifier
from ..executive.executive_verifier import ExecutiveVerifier
from ..explainability.explainability_verifier import ExplainabilityVerifier
from ..calibration.calibration_verifier import CalibrationVerifier
from ..adversarial.adversarial_verifier import AdversarialVerifier
from ..scalability.scalability_verifier import ScalabilityVerifier
from ..benchmarks.benchmark_verifier import BenchmarkVerifier
from ..dashboards.dashboard_verifier import DashboardVerifier


class CognitivePlatformScorer:
    """Executes all cognitive verifiers, aggregates empirical results, and produces the complete CognitiveReadinessScorecard."""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.verifiers = [
            ReasoningVerifier(self.config),
            CognitiveGraphVerifier(self.config),
            HypothesisVerifier(self.config),
            DecisionVerifier(self.config),
            SimulationVerifier(self.config),
            LearningVerifier(self.config),
            ExperienceVerifier(self.config),
            ProcessDiscoveryVerifier(self.config),
            AlignmentVerifier(self.config),
            RecommendationsVerifier(self.config),
            ContinuousLearningVerifier(self.config),
            OptimizationVerifier(self.config),
            ExecutiveVerifier(self.config),
            ExplainabilityVerifier(self.config),
            CalibrationVerifier(self.config),
            AdversarialVerifier(self.config),
            ScalabilityVerifier(self.config),
            BenchmarkVerifier(self.config),
            DashboardVerifier(self.config),
        ]

    def run_all(self) -> CognitiveReadinessScorecard:
        start_time = time.perf_counter()
        part_results: Dict[str, PartVerificationResult] = {}
        total_assertions = 0
        passed_assertions = 0

        for verifier in self.verifiers:
            res = verifier.verify()
            part_results[res.part_id.value] = res
            total_assertions += res.total_assertions_count
            passed_assertions += res.passed_assertions_count

        total_elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        # Calculate composite score
        total_weight = sum(p.weight for p in part_results.values())
        weighted_score = sum(p.score * p.weight for p in part_results.values()) / max(0.001, total_weight)

        grade = "A+" if weighted_score >= 95.0 else ("A" if weighted_score >= 90.0 else "B")

        # Calculate Pillar Indices
        indices = {
            "reasoning_and_graph_index": (part_results["PART_01_REASONING"].score + part_results["PART_02_GRAPH"].score) / 2.0,
            "hypothesis_and_decision_index": (part_results["PART_03_HYPOTHESIS"].score + part_results["PART_04_DECISION"].score) / 2.0,
            "simulation_and_process_index": (part_results["PART_05_SIMULATION"].score + part_results["PART_08_PROCESS_DISCOVERY"].score) / 2.0,
            "learning_and_experience_index": (part_results["PART_06_LEARNING"].score + part_results["PART_07_EXPERIENCE"].score) / 2.0,
            "alignment_and_strategy_index": (part_results["PART_09_ALIGNMENT"].score + part_results["PART_10_RECOMMENDATIONS"].score) / 2.0,
            "continuous_learning_and_optimization_index": (part_results["PART_11_CONTINUOUS_LEARNING"].score + part_results["PART_12_OPTIMIZATION"].score) / 2.0,
            "executive_and_explainability_index": (part_results["PART_13_EXECUTIVE"].score + part_results["PART_14_EXPLAINABILITY"].score) / 2.0,
            "calibration_and_adversarial_index": (part_results["PART_15_CALIBRATION"].score + part_results["PART_16_ADVERSARIAL"].score) / 2.0,
            "scalability_and_benchmarking_index": (part_results["PART_17_SCALABILITY"].score + part_results["PART_18_BENCHMARKS"].score) / 2.0,
            "readiness_and_dashboard_index": part_results["PART_19_DASHBOARDS"].score,
        }

        return CognitiveReadinessScorecard(
            parts=part_results,
            indices=indices,
            composite_score=weighted_score,
            grade=grade,
            total_assertions=total_assertions,
            passed_assertions=passed_assertions,
            production_ready=(weighted_score >= 95.0 and passed_assertions == total_assertions),
            total_execution_time_ms=total_elapsed_ms,
        )
