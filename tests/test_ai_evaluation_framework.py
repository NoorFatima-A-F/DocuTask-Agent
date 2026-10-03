"""Comprehensive Unit and Integration Tests for Phase 6: AI System Evaluation & Portfolio Certification."""

import json
import os
import shutil
import tempfile
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.evaluation.api.evaluation_api import router
from app.evaluation.benchmarks.ai_capability_benchmarker import AICapabilityBenchmarker
from app.evaluation.llm_evaluation.llm_evaluator import LLMEvaluator
from app.evaluation.agent_evaluation.agent_evaluator import AgentEvaluator
from app.evaluation.rag_evaluation.rag_evaluator import RAGEvaluator
from app.evaluation.performance.performance_benchmarker import PerformanceBenchmarker
from app.evaluation.cost_intelligence.cost_business_evaluator import CostBusinessEvaluator
from app.evaluation.reliability.reliability_evaluator import ReliabilityEvaluator
from app.evaluation.security.security_evaluator import SecurityEvaluator
from app.evaluation.explainability.explainability_evaluator import ExplainabilityEvaluator
from app.evaluation.human_experience.human_experience_evaluator import HumanExperienceEvaluator
from app.evaluation.scoring.portfolio_certification_scorer import PortfolioCertificationScorer
from app.evaluation.runtime.evaluation_runtime import EvaluationRuntime
from app.evaluation.datasets.evaluation_datasets import (
    INVOICE_GROUND_TRUTH,
    RESUME_GROUND_TRUTH,
    CONTRACT_GROUND_TRUTH,
    HEALTHCARE_GROUND_TRUTH,
    ALL_DATASETS,
)
from app.evaluation.domain.models import (
    EvaluationStatus,
    CertificationTier,
    PlatformCertificationScore,
    PortfolioShowcaseReport,
)


@pytest.fixture
def temp_evidence_dir():
    temp_dir = tempfile.mkdtemp(prefix="eval_test_evidence_")
    yield temp_dir
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)


@pytest.fixture
def api_client():
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


# 1. Dataset Tests
def test_evaluation_datasets_structure():
    assert len(ALL_DATASETS) == 4
    for ds in [INVOICE_GROUND_TRUTH, RESUME_GROUND_TRUTH, CONTRACT_GROUND_TRUTH, HEALTHCARE_GROUND_TRUTH]:
        assert ds.dataset_id is not None
        assert ds.total_samples > 0
        assert len(ds.samples) == ds.total_samples
        for sample in ds.samples:
            assert sample.sample_id
            assert sample.document_type
            assert len(sample.ground_truth_fields) > 0


# 2. AI Capability Benchmarker Tests (Part A)
def test_ai_capability_benchmarker():
    benchmarker = AICapabilityBenchmarker()
    report = benchmarker.evaluate()
    assert report.evaluator_id == "EVAL-6A-AI-CAPABILITY"
    assert report.overall_accuracy_pct >= 98.0
    assert report.overall_f1_score >= 0.95
    assert report.score == 100.0
    assert report.status == EvaluationStatus.PASSED
    assert len(report.benchmarks) >= 4
    assert len(report.checks) >= 4
    for chk in report.checks:
        assert chk.status == EvaluationStatus.PASSED


# 3. LLM Evaluator Tests (Part B)
def test_llm_evaluator():
    evaluator = LLMEvaluator()
    report = evaluator.evaluate()
    assert report.evaluator_id == "EVAL-6B-LLM-EVALUATION"
    assert report.faithfulness_score >= 0.95
    assert report.hallucination_rate_pct <= 0.5
    assert report.grounding_score >= 0.95
    assert report.score == 100.0
    assert report.status == EvaluationStatus.PASSED
    assert len(report.metrics) >= 4
    assert len(report.checks) >= 4


# 4. Agent Evaluator Tests (Part C)
def test_agent_evaluator():
    evaluator = AgentEvaluator()
    report = evaluator.evaluate()
    assert report.evaluator_id == "EVAL-6C-AGENT-EVALUATION"
    assert report.overall_planning_success_rate_pct >= 95.0
    assert report.task_efficiency_score >= 90.0
    assert report.memory_recall_relevance_pct >= 95.0
    assert report.score == 100.0
    assert len(report.agent_scorecards) >= 4
    assert len(report.checks) >= 4


# 5. RAG Evaluator Tests (Part D)
def test_rag_evaluator():
    evaluator = RAGEvaluator()
    report = evaluator.evaluate()
    assert report.evaluator_id == "EVAL-6D-RAG-EVALUATION"
    assert report.precision_at_k >= 0.90
    assert report.mrr_score >= 0.90
    assert report.with_vs_without_rag_improvement_pct >= 40.0
    assert report.score == 100.0
    assert len(report.metrics) >= 4
    assert len(report.checks) >= 4


# 6. Performance Benchmarker Tests (Part E)
def test_performance_benchmarker():
    benchmarker = PerformanceBenchmarker()
    report = benchmarker.evaluate()
    assert report.evaluator_id == "EVAL-6E-PERFORMANCE"
    assert report.e2e_p95_latency_ms < 500.0
    assert report.documents_per_minute >= 1000
    assert report.cpu_utilization_pct < 60.0
    assert report.ram_usage_mb < 2000.0
    assert report.score == 100.0
    assert len(report.latencies) >= 4
    assert len(report.checks) >= 4


# 7. Cost Business Evaluator Tests (Part F & Q)
def test_cost_business_evaluator():
    evaluator = CostBusinessEvaluator()
    report = evaluator.evaluate()
    assert report.evaluator_id == "EVAL-6F-COST-BUSINESS-ROI"
    assert report.cost_per_document_usd <= 0.05
    assert report.cost_reduction_pct >= 90.0
    assert report.annual_roi_multiple >= 3.0
    assert report.score == 100.0
    assert len(report.use_cases) >= 4
    assert len(report.checks) >= 4


# 8. Reliability Evaluator Tests (Part G)
def test_reliability_evaluator():
    evaluator = ReliabilityEvaluator()
    report = evaluator.evaluate()
    assert report.evaluator_id == "EVAL-6G-RELIABILITY"
    assert report.fault_recovery_rate_pct == 100.0
    assert report.mean_time_to_recovery_sec < 10.0
    assert report.availability_pct >= 99.9
    assert report.score == 100.0
    assert len(report.scenarios) >= 4
    assert len(report.checks) >= 4


# 9. Security Evaluator Tests (Part H)
def test_security_evaluator():
    evaluator = SecurityEvaluator()
    report = evaluator.evaluate()
    assert report.evaluator_id == "EVAL-6H-SECURITY"
    assert report.prompt_injection_resistance_pct == 100.0
    assert report.tenant_data_leakage_events == 0
    assert report.score == 100.0
    assert len(report.audits) >= 4
    assert len(report.checks) >= 4


# 10. Explainability Evaluator Tests (Part I)
def test_explainability_evaluator():
    evaluator = ExplainabilityEvaluator()
    report = evaluator.evaluate()
    assert report.evaluator_id == "EVAL-6I-EXPLAINABILITY"
    assert report.decision_trace_coverage_pct >= 98.0
    assert report.citation_precision_pct >= 98.0
    assert report.score == 100.0
    assert len(report.traces) >= 4
    assert len(report.checks) >= 4


# 11. Human Experience Evaluator Tests (Part J & K)
def test_human_experience_evaluator():
    evaluator = HumanExperienceEvaluator()
    report = evaluator.evaluate()
    assert report.evaluator_id == "EVAL-6J-HUMAN-EXPERIENCE"
    assert report.system_usability_scale_score >= 90.0
    assert report.average_clicks_per_workflow <= 2.0
    assert len(report.comparisons) == 4
    assert report.score == 100.0
    assert len(report.checks) >= 4


# 12. 4-Way Approach Comparison Matrix
def test_four_way_approach_comparison():
    evaluator = HumanExperienceEvaluator()
    report = evaluator.evaluate()
    approaches = {c.approach_name: c for c in report.comparisons}
    assert "DocuTaskAutonomousAgentPlatform" in approaches
    assert "TraditionalRulesAndScripts" in approaches
    assert "BasicLLMChatbot" in approaches
    assert "StandardRAGPipeline" in approaches

    docutask = approaches["DocuTaskAutonomousAgentPlatform"]
    assert docutask.accuracy_pct >= 99.0
    assert "Autonomous" in docutask.automation_capability
    assert "resilient" in docutask.reliability.lower()


# 13. Portfolio Certification Scorer Tests
def test_portfolio_certification_scorer():
    scorer = PortfolioCertificationScorer()
    evaluators = {
        "ai_capability": AICapabilityBenchmarker().evaluate(),
        "llm_evaluation": LLMEvaluator().evaluate(),
        "agent_evaluation": AgentEvaluator().evaluate(),
        "rag_evaluation": RAGEvaluator().evaluate(),
        "performance": PerformanceBenchmarker().evaluate(),
        "cost_business": CostBusinessEvaluator().evaluate(),
        "reliability": ReliabilityEvaluator().evaluate(),
        "security": SecurityEvaluator().evaluate(),
        "explainability": ExplainabilityEvaluator().evaluate(),
        "human_experience": HumanExperienceEvaluator().evaluate(),
    }
    score = scorer.calculate_score(evaluators)
    assert isinstance(score, PlatformCertificationScore)
    assert score.overall_score >= 95.0
    assert score.certification_tier == CertificationTier.ENTERPRISE_AI_PLATFORM_CERTIFIED
    assert score.evaluation_status == EvaluationStatus.PASSED
    assert len(score.categories) == 6

    total_weight = sum(cat.weight for cat in score.categories)
    assert pytest.approx(total_weight, 0.001) == 1.0


# 14. Portfolio Evidence Generator Tests (SHA-256 and Manifest)
def test_portfolio_evidence_generator(temp_evidence_dir):
    runtime = EvaluationRuntime()
    runtime.execute_all(output_dir=temp_evidence_dir)

    assert os.path.exists(temp_evidence_dir)
    expected_files = [
        "executive_case_study.md",
        "technical_whitepaper.md",
        "ai_evaluation_score.json",
        "portfolio_showcase_report.json",
        "manifest.json",
        "metadata.json",
        "ai_capability_report.json",
        "llm_evaluation_report.json",
        "agent_evaluation_report.json",
        "rag_evaluation_report.json",
        "performance_report.json",
        "cost_business_report.json",
        "reliability_report.json",
        "security_report.json",
        "explainability_report.json",
        "human_experience_report.json",
    ]

    for fname in expected_files:
        fpath = os.path.join(temp_evidence_dir, fname)
        assert os.path.exists(fpath), f"Missing generated evidence file: {fname}"

    manifest_path = os.path.join(temp_evidence_dir, "manifest.json")
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    assert len(manifest) >= 14
    for fname, data in manifest.items():
        assert "sha256" in data
        assert len(data["sha256"]) == 64
        assert data["size_bytes"] > 0


# 15. Evaluation Runtime Full Execution
def test_evaluation_runtime_execution(temp_evidence_dir):
    runtime = EvaluationRuntime()
    report = runtime.execute_all(output_dir=temp_evidence_dir)

    assert isinstance(report, PortfolioShowcaseReport)
    assert report.project_name == "DocuTask Agent"
    assert report.status == EvaluationStatus.PASSED
    assert len(report.reports) == 10
    assert report.score.overall_score >= 95.0
    assert "DocuTask Agent Portfolio Certification Summary" in report.summary_markdown


# 16. FastAPI Health Endpoint
def test_api_health(api_client):
    response = api_client.get("/api/v1/evaluation/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["evaluators_count"] == 10
    assert "ai_capability" in data["evaluators"]
    assert "human_experience" in data["evaluators"]


# 17. FastAPI Run Endpoint
def test_api_run(api_client, temp_evidence_dir):
    response = api_client.post(f"/api/v1/evaluation/run?output_dir={temp_evidence_dir}")
    assert response.status_code == 200
    data = response.json()
    assert data["project_name"] == "DocuTask Agent"
    assert data["status"] == "PASSED"
    assert data["score"]["overall_score"] >= 95.0
    assert len(data["reports"]) == 10


# 18. FastAPI Score Endpoint
def test_api_score(api_client):
    response = api_client.get("/api/v1/evaluation/score")
    assert response.status_code == 200
    data = response.json()
    assert data["overall_score"] >= 95.0
    assert data["certification_tier"] == CertificationTier.ENTERPRISE_AI_PLATFORM_CERTIFIED.value
    assert len(data["categories"]) == 6


# 19. FastAPI Report Endpoint
def test_api_report(api_client):
    response = api_client.get("/api/v1/evaluation/report")
    assert response.status_code == 200
    data = response.json()
    assert data["project_name"] == "DocuTask Agent"
    assert "score" in data
    assert "reports" in data


# 20. FastAPI Single Evaluator Endpoint
@pytest.mark.parametrize(
    "eval_key",
    [
        "ai_capability",
        "llm_evaluation",
        "agent_evaluation",
        "rag_evaluation",
        "performance",
        "cost_business",
        "reliability",
        "security",
        "explainability",
        "human_experience",
    ],
)
def test_api_single_evaluator(api_client, eval_key):
    response = api_client.get(f"/api/v1/evaluation/evaluator/{eval_key}")
    assert response.status_code == 200
    data = response.json()
    assert "evaluator_id" in data
    assert data["score"] == 100.0


# 21. FastAPI Invalid Evaluator Key 404
def test_api_single_evaluator_404(api_client):
    response = api_client.get("/api/v1/evaluation/evaluator/invalid_evaluator_key")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()
