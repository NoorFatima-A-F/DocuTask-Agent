"""Prompt Quality Benchmark Suite (Phase 8D)."""

from __future__ import annotations

from typing import Any, Callable, List, Optional
from app.prompts.registry.models import PromptVersion
from app.prompts.evaluation.datasets import PromptEvaluationDataset
from app.prompts.evaluation.metrics import PromptEvaluationMetrics
from app.prompts.evaluation.runner import PromptEvaluationRunner


class PromptBenchmarkRunner:
    """Runs standard automated benchmark suites across prompt templates."""

    def __init__(self, runner: Optional[PromptEvaluationRunner] = None):
        self.runner = runner or PromptEvaluationRunner()

    def run_suite(
        self,
        version: PromptVersion,
        datasets: List[PromptEvaluationDataset],
        inference_fn: Callable[[str], Any],
    ) -> List[PromptEvaluationMetrics]:
        """Execute multiple domain benchmark datasets."""
        results = []
        for ds in datasets:
            metrics = self.runner.evaluate_prompt(version, ds, inference_fn)
            results.append(metrics)
        return results
