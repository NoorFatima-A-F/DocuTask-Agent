"""
Automated Pytest Suite for Validation Framework & Evaluation Infrastructure.
Includes edge-case metrics testing and cryptographic SHA-256 evidence chain verification.
"""

import os
import pytest
from app.validation.datasets import DatasetManager
from app.validation.evidence import EvidenceLogger
from app.validation.metrics import EvaluationMetricsEngine
from app.validation.regression import RegressionEngine
from app.validation.reports import ReportGenerator
from app.validation.runner import ValidationRunner


def test_gold_dataset_loading():
    """Verifies Gold Dataset entry loading and filtering."""
    datasets = DatasetManager.get_gold_datasets()
    assert len(datasets) >= 5

    invoice_ds = DatasetManager.get_by_document_type("invoice")
    assert len(invoice_ds) >= 1
    assert invoice_ds[0].metadata.document_type == "invoice"
    assert "invoice_number" in invoice_ds[0].ground_truth_json


def test_metric_calculation_perfect_match():
    """Verifies 100% accuracy metrics for identical ground truth."""
    gt = {"vendor": "Acme", "total": 100.0, "date": "2026-08-15"}
    actual = {"vendor": "Acme", "total": 100.0, "date": "2026-08-15"}

    res = EvaluationMetricsEngine.evaluate(actual, gt, schema_valid=True, confidence=1.0)
    assert res.field_accuracy == 1.0
    assert res.exact_match_accuracy == 1.0
    assert res.f1_score == 1.0
    assert res.missing_fields == 0
    assert res.hallucinated_fields == 0


def test_metric_calculation_edge_cases():
    """Verifies metric engine edge cases: empty datasets, 100% missing, 100% hallucinated."""
    # 1. 100% Missing fields
    gt = {"vendor": "Acme", "total": 100.0}
    actual_missing = {"vendor": None, "total": None}
    res_missing = EvaluationMetricsEngine.evaluate(actual_missing, gt)
    assert res_missing.field_accuracy == 0.0
    assert res_missing.missing_field_rate == 1.0
    assert res_missing.recall == 0.0

    # 2. 100% Hallucinated fields
    actual_hallucinated = {"fake1": "val1", "fake2": "val2"}
    res_hallucinated = EvaluationMetricsEngine.evaluate(actual_hallucinated, gt)
    assert res_hallucinated.hallucination_rate > 0.0
    assert res_hallucinated.precision == 0.0


def test_evidence_sha256_hash_chain():
    """Verifies SHA-256 cryptographic evidence hash chaining."""
    gt = {"invoice_number": "INV-1"}
    act = {"invoice_number": "INV-1"}

    metrics = EvaluationMetricsEngine.evaluate(act, gt)

    rec1 = EvidenceLogger.log_evidence("test_doc_001", gt, act, metrics, test_id_prefix="chain1")
    rec2 = EvidenceLogger.log_evidence("test_doc_002", gt, act, metrics, test_id_prefix="chain2")

    assert rec1.result_hash != ""
    assert rec2.previous_hash == rec1.result_hash
    assert rec2.result_hash != rec1.result_hash


def test_regression_detection():
    """Verifies regression detection logic and severity categories."""
    gt = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}
    act = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}

    metrics = EvaluationMetricsEngine.evaluate(act, gt)

    # 1. No regression
    comp_none = RegressionEngine.compare(metrics, baseline_accuracy=0.95)
    assert comp_none.is_regression is False
    assert comp_none.regression_severity == "NONE"

    # 2. Minor regression (<2%)
    comp_minor = RegressionEngine.compare(metrics, baseline_accuracy=1.01)
    assert comp_minor.is_regression is True

    # 3. Critical regression (>5%)
    metrics_drop = EvaluationMetricsEngine.evaluate({"a": 1}, gt)
    comp_crit = RegressionEngine.compare(metrics_drop, baseline_accuracy=0.95)
    assert comp_crit.is_regression is True
    assert comp_crit.regression_severity in ("WARNING", "CRITICAL")


@pytest.mark.asyncio
async def test_validation_runner_execution():
    """Verifies end-to-end execution of full validation runner."""
    records = await ValidationRunner.run_full_validation()
    assert len(records) >= 5
    assert all(r.pass_fail == "PASS" for r in records)
