"""
Unit and integration tests for Phase V7 — Enterprise Cognitive Intelligence Verification & Validation Program (ECIVVP).
"""

import os
import json
from app.cognitive_intelligence_verification import (
    PartId,
    ReasoningType,
    HypothesisType,
    VerificationStatus,
    ReasoningTrace,
    CognitiveNode,
    CognitiveEdge,
    Hypothesis,
    CognitivePlatformScorer,
    EvidenceGenerator,
)
from app.cognitive_intelligence_verification.reasoning.reasoning_verifier import ReasoningVerifier
from app.cognitive_intelligence_verification.graph.cognitive_graph_verifier import CognitiveGraphVerifier
from app.cognitive_intelligence_verification.hypothesis.hypothesis_verifier import HypothesisVerifier
from app.cognitive_intelligence_verification.decision.decision_verifier import DecisionVerifier
from app.cognitive_intelligence_verification.simulation.simulation_verifier import SimulationVerifier
from app.cognitive_intelligence_verification.learning.learning_verifier import LearningVerifier
from app.cognitive_intelligence_verification.experience.experience_verifier import ExperienceVerifier
from app.cognitive_intelligence_verification.process_discovery.process_discovery_verifier import ProcessDiscoveryVerifier
from app.cognitive_intelligence_verification.alignment.alignment_verifier import AlignmentVerifier
from app.cognitive_intelligence_verification.recommendations.recommendations_verifier import RecommendationsVerifier
from app.cognitive_intelligence_verification.continuous_learning.continuous_learning_verifier import ContinuousLearningVerifier
from app.cognitive_intelligence_verification.optimization.optimization_verifier import OptimizationVerifier
from app.cognitive_intelligence_verification.executive.executive_verifier import ExecutiveVerifier
from app.cognitive_intelligence_verification.explainability.explainability_verifier import ExplainabilityVerifier
from app.cognitive_intelligence_verification.calibration.calibration_verifier import CalibrationVerifier
from app.cognitive_intelligence_verification.adversarial.adversarial_verifier import AdversarialVerifier
from app.cognitive_intelligence_verification.scalability.scalability_verifier import ScalabilityVerifier
from app.cognitive_intelligence_verification.benchmarks.benchmark_verifier import BenchmarkVerifier
from app.cognitive_intelligence_verification.dashboards.dashboard_verifier import DashboardVerifier


def test_domain_models():
    trace = ReasoningTrace(
        trace_id="trc_1",
        reasoning_type=ReasoningType.DEDUCTIVE,
        premises=["P1", "P2"],
        inferences=["I1"],
        conclusion="C1",
        confidence=0.99,
    )
    d = trace.to_dict()
    assert d["trace_id"] == "trc_1"
    assert d["reasoning_type"] == "DEDUCTIVE"

    node = CognitiveNode(node_id="cn1", node_type="CONCEPT", label="TaxLaw")
    edge = CognitiveEdge(source_id="cn1", target_id="cn2", relation_type="CAUSES")
    assert node.label == "TaxLaw"
    assert edge.relation_type == "CAUSES"

    hyp = Hypothesis(
        hypothesis_id="h1",
        hypothesis_type=HypothesisType.ROOT_CAUSE,
        statement="OCR failure caused by low DPI",
        plausibility=0.92,
        evidence_support_count=3,
    )
    assert hyp.plausibility == 0.92


def test_part_01_reasoning():
    v = ReasoningVerifier()
    res = v.verify()
    assert res.part_id == PartId.PART_01_REASONING
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4
    assert all(a.passed for a in res.assertions)


def test_part_02_graph():
    v = CognitiveGraphVerifier()
    res = v.verify()
    assert res.part_id == PartId.PART_02_GRAPH
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_part_03_hypothesis():
    v = HypothesisVerifier()
    res = v.verify()
    assert res.part_id == PartId.PART_03_HYPOTHESIS
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_part_04_decision():
    v = DecisionVerifier()
    res = v.verify()
    assert res.part_id == PartId.PART_04_DECISION
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_part_05_simulation():
    v = SimulationVerifier()
    res = v.verify()
    assert res.part_id == PartId.PART_05_SIMULATION
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_part_06_learning():
    v = LearningVerifier()
    res = v.verify()
    assert res.part_id == PartId.PART_06_LEARNING
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_part_07_experience():
    v = ExperienceVerifier()
    res = v.verify()
    assert res.part_id == PartId.PART_07_EXPERIENCE
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_part_08_process_discovery():
    v = ProcessDiscoveryVerifier()
    res = v.verify()
    assert res.part_id == PartId.PART_08_PROCESS_DISCOVERY
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_part_09_alignment():
    v = AlignmentVerifier()
    res = v.verify()
    assert res.part_id == PartId.PART_09_ALIGNMENT
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_part_10_recommendations():
    v = RecommendationsVerifier()
    res = v.verify()
    assert res.part_id == PartId.PART_10_RECOMMENDATIONS
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_part_11_continuous_learning():
    v = ContinuousLearningVerifier()
    res = v.verify()
    assert res.part_id == PartId.PART_11_CONTINUOUS_LEARNING
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_part_12_optimization():
    v = OptimizationVerifier()
    res = v.verify()
    assert res.part_id == PartId.PART_12_OPTIMIZATION
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_part_13_executive():
    v = ExecutiveVerifier()
    res = v.verify()
    assert res.part_id == PartId.PART_13_EXECUTIVE
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_part_14_explainability():
    v = ExplainabilityVerifier()
    res = v.verify()
    assert res.part_id == PartId.PART_14_EXPLAINABILITY
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_part_15_calibration():
    v = CalibrationVerifier()
    res = v.verify()
    assert res.part_id == PartId.PART_15_CALIBRATION
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_part_16_adversarial():
    v = AdversarialVerifier()
    res = v.verify()
    assert res.part_id == PartId.PART_16_ADVERSARIAL
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_part_17_scalability():
    v = ScalabilityVerifier()
    res = v.verify()
    assert res.part_id == PartId.PART_17_SCALABILITY
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_part_18_benchmarks():
    v = BenchmarkVerifier()
    res = v.verify()
    assert res.part_id == PartId.PART_18_BENCHMARKS
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_part_19_dashboards():
    v = DashboardVerifier()
    res = v.verify()
    assert res.part_id == PartId.PART_19_DASHBOARDS
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_cognitive_scorer_and_scorecard():
    scorer = CognitivePlatformScorer()
    scorecard = scorer.run_all()

    assert scorecard.composite_score == 100.0
    assert scorecard.grade == "A+"
    assert scorecard.production_ready is True
    assert scorecard.total_assertions == 76
    assert scorecard.passed_assertions == 76
    assert len(scorecard.parts) == 19
    assert len(scorecard.indices) == 10
    assert scorecard.total_execution_time_ms < 1000.0


def test_evidence_export_and_manifest(tmp_path):
    out_dir = tmp_path / "evidence"
    report_file = tmp_path / "docs" / "report.md"

    scorer = CognitivePlatformScorer()
    scorecard = scorer.run_all()

    exporter = EvidenceGenerator(output_dir=str(out_dir), report_path=str(report_file))
    summary = exporter.export_all(scorecard)

    assert os.path.exists(summary["manifest_file"])
    assert os.path.exists(summary["report_path"])

    with open(summary["manifest_file"], "r", encoding="utf-8") as f:
        manifest = json.load(f)

    assert manifest["composite_score"] == 100.0
    assert manifest["production_ready"] is True
    assert len(manifest["checksums"]) == 20  # 1 summary + 19 parts
