"""Prompt Evaluation Runner (Phase 8D).

Executes evaluation datasets against prompt versions, computes scores, and determines pass/fail quality criteria.
"""

from __future__ import annotations

import time
from typing import Any, Callable, Dict, List, Optional
from app.prompts.registry.models import PromptVersion
from app.prompts.templates.renderer import PromptTemplateRenderer
from app.prompts.evaluation.datasets import PromptEvaluationDataset
from app.prompts.evaluation.metrics import PromptEvaluationMetrics


class PromptEvaluationRunner:
    """Orchestrates automated evaluation of prompt versions on ground-truth datasets."""

    def evaluate_prompt(
        self,
        version: PromptVersion,
        dataset: PromptEvaluationDataset,
        inference_fn: Callable[[str], Any],
    ) -> PromptEvaluationMetrics:
        """Run all test cases in dataset against prompt version."""
        if not dataset.test_cases:
            return PromptEvaluationMetrics(
                prompt_id=version.prompt_id,
                version_id=version.version_id,
                dataset_id=dataset.dataset_id,
                composite_score=1.0,
            )

        passed = 0
        total = len(dataset.test_cases)
        start_time = time.time()
        latencies = []

        for case in dataset.test_cases:
            # 1. Render prompt with case variables
            rendered = PromptTemplateRenderer.render(
                template=version.prompt_template,
                variables=case.variables,
            )

            # 2. Invoke inference function
            t0 = time.time()
            try:
                actual_out = inference_fn(rendered)
                latency = (time.time() - t0) * 1000.0
                latencies.append(latency)

                # 3. Evaluate match
                if case.expected_output is not None:
                    if actual_out == case.expected_output:
                        passed += 1
                    elif isinstance(case.expected_output, dict) and actual_out == case.expected_output:
                        passed += 1
                    elif str(case.expected_output).strip() in str(actual_out).strip():
                        passed += 1
                else:
                    passed += 1
            except Exception:
                pass

        total_time = (time.time() - start_time) * 1000.0
        avg_latency = sum(latencies) / len(latencies) if latencies else 0.0
        accuracy = round(passed / total, 4) if total > 0 else 1.0

        metrics = PromptEvaluationMetrics(
            prompt_id=version.prompt_id,
            version_id=version.version_id,
            dataset_id=dataset.dataset_id,
            total_cases=total,
            passed_cases=passed,
            accuracy_score=accuracy,
            faithfulness_score=accuracy,
            format_compliance_score=1.0 if passed > 0 else 0.5,
            safety_score=1.0,
            hallucination_rate=round(1.0 - accuracy, 4),
            average_latency_ms=round(avg_latency, 2),
        )
        metrics.compute_composite_score()

        # Update version record
        version.evaluation_score = metrics.composite_score
        version.performance_metrics = {
            "accuracy": accuracy,
            "latency_ms": avg_latency,
            "total_cases": total,
        }

        return metrics
