"""
Independent Black-Box Evaluation Runner for AAOS.
Interacts exclusively via serialized API contracts, JSON artifacts, and CLI invocations.
Zero compile-time dependencies on internal agent or runtime classes.
"""

from __future__ import annotations

import json
import logging
import subprocess
import tempfile
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from evaluation.metrics.evaluation_metrics import EvaluationMetrics, EvaluationMetricSummary

logger = logging.getLogger(__name__)


@dataclass
class BlackBoxEvaluationTask:
    """Individual evaluation task containing document input and ground truth."""

    task_id: str
    domain: str
    document_type: str
    input_payload: Dict[str, Any]
    ground_truth_extracted: Dict[str, Any]
    difficulty_level: str  # "EASY", "MEDIUM", "HARD", "ADVERSARIAL"


@dataclass
class BlackBoxEvaluationResult:
    """Consolidated outcome of black-box independent evaluation."""

    suite_name: str
    total_tasks: int
    duration_seconds: float
    metrics: EvaluationMetricSummary
    task_results: List[Dict[str, Any]] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "suite_name": self.suite_name,
            "total_tasks": self.total_tasks,
            "duration_seconds": round(self.duration_seconds, 4),
            "metrics": self.metrics.to_dict(),
            "task_results": self.task_results,
            "created_at": self.created_at,
        }


class IndependentEvaluationRunner:
    """
    Executes black-box evaluation against any contract-compliant agent endpoint.
    """

    @classmethod
    def evaluate_endpoint(
        cls,
        suite_name: str,
        tasks: List[BlackBoxEvaluationTask],
        predict_fn: Callable[[Dict[str, Any]], Dict[str, Any]],
    ) -> BlackBoxEvaluationResult:
        """Evaluates a black-box callable function that conforms to the JSON I/O schema."""
        t0 = time.perf_counter()
        predictions: List[Dict[str, Any]] = []
        ground_truths: List[Dict[str, Any]] = []
        task_details: List[Dict[str, Any]] = []

        for task in tasks:
            t_start = time.perf_counter()
            try:
                # Black-box execution
                pred = predict_fn(task.input_payload)
            except Exception as e:
                pred = {"error": str(e), "status": "FAILED"}

            lat_ms = (time.perf_counter() - t_start) * 1000.0

            predictions.append(pred)
            ground_truths.append(task.ground_truth_extracted)

            task_details.append(
                {
                    "task_id": task.task_id,
                    "domain": task.domain,
                    "document_type": task.document_type,
                    "difficulty": task.difficulty_level,
                    "latency_ms": round(lat_ms, 2),
                    "is_exact_match": (pred == task.ground_truth_extracted),
                }
            )

        elapsed = time.perf_counter() - t0
        summary_metrics = EvaluationMetrics.evaluate_structured_extractions(ground_truths, predictions)

        return BlackBoxEvaluationResult(
            suite_name=suite_name,
            total_tasks=len(tasks),
            duration_seconds=elapsed,
            metrics=summary_metrics,
            task_results=task_details,
        )
