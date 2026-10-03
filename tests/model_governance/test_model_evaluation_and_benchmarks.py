"""Tests for Model Evaluation, Benchmarking, and Scoring Leaderboard (Phase 8C)."""

from app.model_governance.evaluation.metrics import ModelEvaluationMetrics
from app.model_governance.evaluation.benchmarks import ModelBenchmarkDataset, ModelBenchmarkRunner
from app.model_governance.evaluation.scoring import ModelEvaluationScorer
from app.model_governance.registry.models import Model, ModelCategory, ModelProvider


def test_model_evaluation_metrics_composite_score():
    metrics = ModelEvaluationMetrics(
        accuracy=0.92,
        faithfulness=0.88,
        completeness=0.90,
        consistency=0.95,
        hallucination_rate=0.04,
        avg_latency_ms=150.0,
    )

    composite = metrics.compute_composite_score()
    assert 0.85 <= composite <= 1.0


def test_benchmark_runner_and_scoring_leaderboard():
    runner = ModelBenchmarkRunner()
    scorer = ModelEvaluationScorer()

    dataset = ModelBenchmarkDataset(
        dataset_id="invoice_extraction_v1",
        name="Invoice Extraction Golden Dataset",
        domain="finance",
        samples=[
            {"input": "Invoice #1024 from Vendor Acme for $500", "expected": {"vendor": "Acme", "amount": 500}},
            {"input": "Bill #892 from Beta LLC for $1200", "expected": {"vendor": "Beta LLC", "amount": 1200}},
        ],
    )

    # Mock evaluators
    evaluator_a = lambda sample: {"vendor": sample["expected"]["vendor"], "amount": sample["expected"]["amount"]}
    evaluator_b = lambda sample: {"vendor": "Wrong Vendor", "amount": 0}

    model_a = Model(
        model_id="gemini-1-5-flash",
        model_name="Gemini Flash",
        organization_id="org_default",
        family_id="gemini-1-5",
        version="001",
        category=ModelCategory.FOUNDATION_LLM,
        provider=ModelProvider.GOOGLE,
    )

    model_b = Model(
        model_id="legacy-model",
        model_name="Legacy LLM",
        organization_id="org_default",
        family_id="legacy",
        version="v0",
        category=ModelCategory.FOUNDATION_LLM,
        provider=ModelProvider.SELF_HOSTED,
    )

    metrics_a = runner.run_benchmark(model_a, dataset, evaluator_a)
    metrics_b = runner.run_benchmark(model_b, dataset, evaluator_b)

    assert metrics_a.accuracy == 1.0
    assert metrics_b.accuracy == 0.0

    scorer.record_score("gemini-1-5-flash", metrics_a)
    scorer.record_score("legacy-model", metrics_b)

    leaderboard = scorer.get_leaderboard()
    assert len(leaderboard) == 2
    assert leaderboard[0]["model_id"] == "gemini-1-5-flash"
    assert leaderboard[0]["composite_score"] > leaderboard[1]["composite_score"]
