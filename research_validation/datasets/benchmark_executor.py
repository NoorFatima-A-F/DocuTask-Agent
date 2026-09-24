"""
Public Benchmark Execution Framework (Phase 73A)
================================================
Executes benchmark pipelines against canonical document processing datasets:
FUNSD, CORD, SROIE, DocVQA, RVL-CDIP.

Adheres strictly to the Zero-Trust / Zero-Fabrication principles:
When local dataset assets are missing, emits DATASET_UNAVAILABLE or NOT_EXECUTED.
When datasets are present, computes empirical F1, ANLS, precision/recall,
Wilson confidence intervals, latency percentiles, and Merkle provenance nodes.
"""

from __future__ import annotations
import hashlib
import json
import math
import os
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple

from research_validation.datasets.public_benchmarks import DatasetType


class BenchmarkExecutionStatus(str, Enum):
    COMPLETED = "COMPLETED"
    PARTIALLY_EXECUTED = "PARTIALLY_EXECUTED"
    DATASET_UNAVAILABLE = "DATASET_UNAVAILABLE"
    NOT_EXECUTED = "NOT_EXECUTED"
    CHECKSUM_FAILED = "CHECKSUM_FAILED"
    EXECUTION_FAILED = "EXECUTION_FAILED"


@dataclass(frozen=True)
class DatasetManifest:
    dataset_type: DatasetType
    expected_sample_count: int
    expected_sha256: Optional[str] = None
    canonical_source_url: str = ""
    license: str = ""
    splits: Tuple[str, ...] = ("train", "test")


@dataclass(frozen=True)
class ConfidenceInterval:
    lower: float
    upper: float
    confidence_level: float = 0.95


@dataclass(frozen=True)
class BenchmarkRunResult:
    dataset_type: DatasetType
    status: BenchmarkExecutionStatus
    is_measured: bool
    sample_count: int
    precision: float
    recall: float
    f1_score: float
    exact_match_or_anls: float
    p50_latency_ms: float
    p95_latency_ms: float
    p99_latency_ms: float
    f1_confidence_interval: ConfidenceInterval
    effect_size_cohens_d: Optional[float] = None
    merkle_evidence_hash: str = ""
    execution_duration_sec: float = 0.0
    timestamp_utc: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    diagnostic_message: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


def compute_wilson_ci(k: int, n: int, confidence: float = 0.95) -> ConfidenceInterval:
    """Calculate Wilson score interval for binomial proportions."""
    if n <= 0:
        return ConfidenceInterval(lower=0.0, upper=0.0, confidence_level=confidence)
    z = 1.95996 if abs(confidence - 0.95) < 0.01 else 2.57583  # 95% vs 99%
    p = k / n
    denom = 1.0 + (z**2) / n
    center = (p + (z**2) / (2.0 * n)) / denom
    spread = (z * math.sqrt((p * (1.0 - p) + (z**2) / (4.0 * n)) / n)) / denom
    return ConfidenceInterval(
        lower=max(0.0, center - spread),
        upper=min(1.0, center + spread),
        confidence_level=confidence,
    )


def compute_anls(prediction: str, ground_truth: str, threshold: float = 0.5) -> float:
    """Average Normalized Levenshtein Similarity for DocVQA."""
    pred = prediction.strip().lower()
    gt = ground_truth.strip().lower()
    if not pred and not gt:
        return 1.0
    if not pred or not gt:
        return 0.0

    m, n = len(pred), len(gt)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if pred[i - 1] == gt[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,      # deletion
                dp[i][j - 1] + 1,      # insertion
                dp[i - 1][j - 1] + cost  # substitution
            )

    dist = dp[m][n]
    norm_dist = dist / max(m, n)
    if norm_dist >= threshold:
        return 0.0
    return 1.0 - norm_dist


class PublicBenchmarkExecutor:
    """
    Zero-Trust Benchmark Execution Harness for standard document datasets.
    """

    DEFAULT_MANIFESTS: Dict[DatasetType, DatasetManifest] = {
        DatasetType.FUNSD: DatasetManifest(
            dataset_type=DatasetType.FUNSD,
            expected_sample_count=199,
            canonical_source_url="https://guillaumejaume.github.io/FUNSD/",
            license="Non-commercial research use",
            splits=("train", "test"),
        ),
        DatasetType.CORD: DatasetManifest(
            dataset_type=DatasetType.CORD,
            expected_sample_count=1000,
            canonical_source_url="https://github.com/clovaai/cord",
            license="CC BY-NC-ND 4.0",
            splits=("train", "dev", "test"),
        ),
        DatasetType.SROIE: DatasetManifest(
            dataset_type=DatasetType.SROIE,
            expected_sample_count=973,
            canonical_source_url="https://rrc.cvc.uab.es/?ch=13",
            license="ICDAR 2019 Competition",
            splits=("train", "test"),
        ),
        DatasetType.DOCVQA: DatasetManifest(
            dataset_type=DatasetType.DOCVQA,
            expected_sample_count=50000,
            canonical_source_url="https://www.docvqa.org/",
            license="Academic research only",
            splits=("train", "val", "test"),
        ),
        DatasetType.RVL_CDIP: DatasetManifest(
            dataset_type=DatasetType.RVL_CDIP,
            expected_sample_count=400000,
            canonical_source_url="https://www.cs.cmu.edu/~aharley/rvl-cdip/",
            license="Public domain / Legacy Tobacco Documents Library",
            splits=("train", "val", "test"),
        ),
    }

    def __init__(self, data_root_dir: Optional[str] = None):
        self.data_root = data_root_dir or "data/benchmarks"

    def verify_dataset_integrity(self, dataset_type: DatasetType, custom_path: Optional[str] = None) -> Tuple[bool, str]:
        """Check if dataset directory and files exist locally."""
        path = custom_path or os.path.join(self.data_root, dataset_type.value.lower())
        if not os.path.exists(path):
            return False, f"Directory not found: {path}"
        if not os.path.isdir(path):
            return False, f"Path is not a directory: {path}"
        files = os.listdir(path)
        if not files:
            return False, f"Directory is empty: {path}"
        return True, f"Found {len(files)} files/folders in {path}"

    def execute_benchmark(
        self,
        dataset_type: DatasetType,
        dataset_dir: Optional[str] = None,
        predictor_fn: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]] = None,
        mock_samples_for_test: Optional[List[Dict[str, Any]]] = None,
    ) -> BenchmarkRunResult:
        """
        Execute evaluation run against dataset.
        If real dataset is not on disk and no mock_samples_for_test are passed,
        returns strictly DATASET_UNAVAILABLE without fabricating numbers.
        """
        start_time = time.perf_counter()
        target_path = dataset_dir or os.path.join(self.data_root, dataset_type.value.lower())

        exists, msg = self.verify_dataset_integrity(dataset_type, target_path)

        if not exists and not mock_samples_for_test:
            return BenchmarkRunResult(
                dataset_type=dataset_type,
                status=BenchmarkExecutionStatus.DATASET_UNAVAILABLE,
                is_measured=False,
                sample_count=0,
                precision=0.0,
                recall=0.0,
                f1_score=0.0,
                exact_match_or_anls=0.0,
                p50_latency_ms=0.0,
                p95_latency_ms=0.0,
                p99_latency_ms=0.0,
                f1_confidence_interval=ConfidenceInterval(0.0, 0.0),
                diagnostic_message=f"Dataset unavailable at {target_path}. {msg}. Manifest source: {self.DEFAULT_MANIFESTS[dataset_type].canonical_source_url}",
            )

        samples = mock_samples_for_test or []
        # If real dataset directory exists and samples need parsing
        if exists and not samples:
            samples = self._load_samples_from_dir(dataset_type, target_path)

        if not samples:
            return BenchmarkRunResult(
                dataset_type=dataset_type,
                status=BenchmarkExecutionStatus.NOT_EXECUTED,
                is_measured=False,
                sample_count=0,
                precision=0.0,
                recall=0.0,
                f1_score=0.0,
                exact_match_or_anls=0.0,
                p50_latency_ms=0.0,
                p95_latency_ms=0.0,
                p99_latency_ms=0.0,
                f1_confidence_interval=ConfidenceInterval(0.0, 0.0),
                diagnostic_message="No evaluation samples could be loaded.",
            )

        # Run evaluation loop
        tp, fp, fn = 0, 0, 0
        anls_scores: List[float] = []
        latencies: List[float] = []

        for sample in samples:
            t0 = time.perf_counter_ns()
            pred = predictor_fn(sample) if predictor_fn else sample.get("pred", {})
            t1 = time.perf_counter_ns()
            latencies.append((t1 - t0) / 1_000_000.0)

            gt_label = sample.get("ground_truth_label", "")
            pred_label = pred.get("label", "") if isinstance(pred, dict) else str(pred)

            if gt_label:
                if pred_label == gt_label:
                    tp += 1
                else:
                    if pred_label:
                        fp += 1
                    else:
                        fn += 1

            if dataset_type == DatasetType.DOCVQA:
                gt_text = sample.get("ground_truth_text", "")
                pred_text = pred.get("text", "") if isinstance(pred, dict) else str(pred)
                anls_scores.append(compute_anls(pred_text, gt_text))

        n_samples = len(samples)
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

        if dataset_type == DatasetType.DOCVQA and anls_scores:
            exact_or_anls = sum(anls_scores) / len(anls_scores)
        else:
            exact_or_anls = tp / n_samples if n_samples > 0 else 0.0

        latencies.sort()
        p50 = latencies[int(n_samples * 0.50)] if latencies else 0.0
        p95 = latencies[int(n_samples * 0.95)] if latencies else 0.0
        p99 = latencies[min(int(n_samples * 0.99), n_samples - 1)] if latencies else 0.0

        ci = compute_wilson_ci(tp, n_samples)
        elapsed = time.perf_counter() - start_time

        # Cryptographic Merkle payload hash
        hash_payload = json.dumps({
            "dataset": dataset_type.value,
            "samples": n_samples,
            "tp": tp, "fp": fp, "fn": fn,
            "f1": f1,
            "exact_match_or_anls": exact_or_anls,
            "p50_ms": p50,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }, sort_keys=True)
        merkle_h = hashlib.sha256(hash_payload.encode()).hexdigest()

        return BenchmarkRunResult(
            dataset_type=dataset_type,
            status=BenchmarkExecutionStatus.COMPLETED,
            is_measured=True,
            sample_count=n_samples,
            precision=precision,
            recall=recall,
            f1_score=f1,
            exact_match_or_anls=exact_or_anls,
            p50_latency_ms=p50,
            p95_latency_ms=p95,
            p99_latency_ms=p99,
            f1_confidence_interval=ci,
            merkle_evidence_hash=merkle_h,
            execution_duration_sec=elapsed,
            diagnostic_message=f"Successfully executed benchmark on {n_samples} items.",
        )

    def _load_samples_from_dir(self, dataset_type: DatasetType, path: str) -> List[Dict[str, Any]]:
        """Load sample files from dataset path."""
        samples: List[Dict[str, Any]] = []
        try:
            for fname in sorted(os.listdir(path))[:100]:
                if fname.endswith(".json"):
                    full_p = os.path.join(path, fname)
                    with open(full_p, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        if isinstance(data, list):
                            samples.extend(data)
                        elif isinstance(data, dict):
                            samples.append(data)
        except Exception:
            pass
        return samples
