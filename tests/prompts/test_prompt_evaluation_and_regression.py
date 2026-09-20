"""Tests for Prompt Evaluation Runner, Datasets, and Regression Testing (Phase 8D)."""

import pytest
from app.prompts.registry.repository import PromptRegistryRepository
from app.prompts.registry.service import PromptRegistryService
from app.prompts.evaluation.datasets import PromptEvaluationDataset
from app.prompts.evaluation.runner import PromptEvaluationRunner
from app.prompts.testing.regression import PromptRegressionTester


def test_prompt_evaluation_dataset_and_scoring():
    repo = PromptRegistryRepository()
    service = PromptRegistryService(repo)
    eval_runner = PromptEvaluationRunner()

    prompt, version = service.create_prompt(
        prompt_id="receipt_parser",
        name="Receipt Parser",
        organization_id="org_test",
        owner="finance@test.com",
        initial_template="Extract merchant and total from: {{ receipt_text }}",
        variables=["receipt_text"],
    )

    dataset = PromptEvaluationDataset(
        dataset_id="ds_receipts_v1",
        name="Receipt Golden Evaluation Dataset",
        organization_id="org_test",
    )
    dataset.add_case(
        variables={"receipt_text": "Walmart total $42.50"},
        expected_output="Merchant: Walmart, Total: 42.50",
    )
    dataset.add_case(
        variables={"receipt_text": "Target total $15.00"},
        expected_output="Merchant: Target, Total: 15.00",
    )

    def mock_model(rendered_prompt: str) -> str:
        if "Walmart" in rendered_prompt:
            return "Merchant: Walmart, Total: 42.50"
        return "Merchant: Target, Total: 15.00"

    metrics = eval_runner.evaluate_prompt(version, dataset, mock_model)
    assert metrics.accuracy_score == 1.0
    assert metrics.passed_cases == 2
    assert metrics.composite_score >= 0.90


def test_prompt_regression_detection():
    repo = PromptRegistryRepository()
    service = PromptRegistryService(repo)
    regression_tester = PromptRegressionTester()

    prompt, v1 = service.create_prompt(
        prompt_id="classifier_prompt",
        name="Document Classifier",
        organization_id="org_test",
        owner="ai@test.com",
        initial_template="Classify document: {{ text }}",
    )
    v2 = service.create_version(
        prompt_id="classifier_prompt",
        organization_id="org_test",
        prompt_template="Classify document into 1 of 5 categories: {{ text }}",
        version_number="1.1.0",
        created_by="ai@test.com",
        change_reason="Narrowed categories",
    )

    dataset = PromptEvaluationDataset(
        dataset_id="ds_classifier",
        name="Classification Dataset",
        organization_id="org_test",
    )
    dataset.add_case(variables={"text": "Invoice doc"}, expected_output="INVOICE")
    dataset.add_case(variables={"text": "Contract doc"}, expected_output="CONTRACT")

    # Mock model: v1 succeeds on all, v2 fails
    def mock_inference(rendered: str) -> str:
        if "into 1 of 5 categories" in rendered:
            return "UNKNOWN"  # v2 fails
        if "Invoice" in rendered:
            return "INVOICE"
        return "CONTRACT"

    report = regression_tester.test_regression(v1, v2, dataset, mock_inference)
    assert report.is_regression is True
    assert report.score_delta < 0
