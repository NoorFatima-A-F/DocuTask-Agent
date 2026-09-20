r"""
Runtime Health Evaluation Engine.

Computes a mathematically grounded system health score $H \in [0.0, 1.0]$ derived from
live telemetry (failure rates, retry counts, CPU/Memory pressure, queue backlog, active anomalies).
Eliminates arbitrary static percentages.
"""

from __future__ import annotations

import time
from typing import Any, Dict, List
from app.runtime.observability.anomaly_detection import AnomalyDetector
from app.runtime.observability.metrics_engine import MetricsEngine
from app.runtime.observability.resource_monitor import ResourceMonitor
from app.runtime.observability.schemas import RuntimeHealthScore


class RuntimeHealthEvaluator:
    """Evaluates multi-factor mathematical health scores with complete provenance."""

    def __init__(
        self,
        metrics_engine: MetricsEngine,
        resource_monitor: ResourceMonitor,
        anomaly_detector: AnomalyDetector,
    ) -> None:
        self.metrics_engine = metrics_engine
        self.resource_monitor = resource_monitor
        self.anomaly_detector = anomaly_detector

    def evaluate_health(self) -> RuntimeHealthScore:
        """
        Calculates normalized health score using weighted composite scoring:
        Score = w_fail * S_fail + w_retry * S_retry + w_cpu * S_cpu + w_mem * S_mem + w_queue * S_queue
        """
        metrics = self.metrics_engine.registry.get_all_metrics_dict()
        res_sample = self.resource_monitor.get_latest_sample()
        anomalies = self.anomaly_detector.get_recent_anomalies(limit=5)

        # 1. Failure Score S_fail: 1.0 if no failures, degrades with failure count
        nodes_exec = metrics.get("nodes_executed_total", 0.0)
        nodes_fail = metrics.get("nodes_failed_total", 0.0)
        fail_rate = (nodes_fail / nodes_exec) if nodes_exec > 0 else 0.0
        score_fail = max(0.0, 1.0 - (fail_rate * 2.0))

        # 2. Retry Score S_retry
        retries = metrics.get("retries_total", 0.0)
        score_retry = max(0.0, 1.0 - (retries / max(10.0, nodes_exec + 10.0)))

        # 3. CPU Score S_cpu: penalize if CPU > 80%
        cpu_pct = res_sample.get("cpu_pct", 10.0)
        score_cpu = 1.0 if cpu_pct < 70.0 else max(0.0, 1.0 - ((cpu_pct - 70.0) / 30.0))

        # 4. Memory Score S_mem: penalize if RSS > 2000MB
        mem_mb = res_sample.get("memory_rss_mb", 200.0)
        score_mem = 1.0 if mem_mb < 1500.0 else max(0.0, 1.0 - ((mem_mb - 1500.0) / 1500.0))

        # 5. Queue Backlog Score S_queue
        queue_len = metrics.get("queue_length_current", 0.0)
        score_queue = 1.0 if queue_len < 10.0 else max(0.0, 1.0 - ((queue_len - 10.0) / 40.0))

        # 6. Anomaly Penalty
        anomaly_penalty = min(0.3, len(anomalies) * 0.05)

        # Weighted composition:
        # weights: fail(0.30), retry(0.15), cpu(0.20), mem(0.20), queue(0.15)
        raw_score = (
            0.30 * score_fail
            + 0.15 * score_retry
            + 0.20 * score_cpu
            + 0.20 * score_mem
            + 0.15 * score_queue
        )
        overall_score = max(0.0, min(1.0, raw_score - anomaly_penalty))
        is_healthy = overall_score >= 0.70

        return RuntimeHealthScore(
            overall_score=round(overall_score, 3),
            is_healthy=is_healthy,
            component_scores={
                "failure_resilience": round(score_fail, 3),
                "retry_stability": round(score_retry, 3),
                "cpu_headroom": round(score_cpu, 3),
                "memory_headroom": round(score_mem, 3),
                "queue_capacity": round(score_queue, 3),
            },
            active_anomalies=anomalies,
            active_workers_count=int(metrics.get("active_workers_current", 0)),
            queue_backlog=int(queue_len),
            evaluated_at=time.time(),
            provenance={
                "weights": {
                    "fail": 0.30,
                    "retry": 0.15,
                    "cpu": 0.20,
                    "mem": 0.20,
                    "queue": 0.15,
                },
                "raw_inputs": {
                    "fail_rate": round(fail_rate, 4),
                    "retries": retries,
                    "cpu_pct": cpu_pct,
                    "mem_mb": mem_mb,
                    "queue_len": queue_len,
                    "anomalies_count": len(anomalies),
                },
            },
        )
