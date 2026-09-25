"""
Specialized Domain Metric Collectors.

Implements telemetry collectors for Infrastructure, Workflows, Queues, Workers,
and AI Runtime LLM execution.
"""

from __future__ import annotations

import logging
from typing import Dict, Optional

from app.infrastructure.observability.metrics.registry import MetricRegistry
from app.infrastructure.observability.metrics.types import MetricType

logger = logging.getLogger("infrastructure.observability.metrics.collectors")


class SystemMetricCollector:
    """Collects host, container, and cluster infrastructure metrics."""

    def __init__(self, registry: MetricRegistry) -> None:
        self.registry = registry

    def collect(
        self,
        cpu_usage_pct: float,
        memory_usage_pct: float,
        disk_usage_pct: float,
        network_rx_mbps: float = 0.0,
        network_tx_mbps: float = 0.0,
        labels: Optional[Dict[str, str]] = None,
    ) -> None:
        lbls = labels or {}
        self.registry.record("system_cpu_usage_percent", cpu_usage_pct, MetricType.GAUGE, lbls)
        self.registry.record("system_memory_usage_percent", memory_usage_pct, MetricType.GAUGE, lbls)
        self.registry.record("system_disk_usage_percent", disk_usage_pct, MetricType.GAUGE, lbls)
        self.registry.record("system_network_rx_mbps", network_rx_mbps, MetricType.GAUGE, lbls)
        self.registry.record("system_network_tx_mbps", network_tx_mbps, MetricType.GAUGE, lbls)


class WorkflowMetricCollector:
    """Collects workflow, task, and queue metrics."""

    def __init__(self, registry: MetricRegistry) -> None:
        self.registry = registry

    def record_task_execution(
        self,
        workflow_type: str,
        duration_seconds: float,
        success: bool,
        labels: Optional[Dict[str, str]] = None,
    ) -> None:
        lbls = {**(labels or {}), "workflow_type": workflow_type, "status": "SUCCESS" if success else "FAILED"}
        self.registry.increment("workflow_tasks_total", 1.0, lbls)
        self.registry.record("workflow_task_duration_seconds", duration_seconds, MetricType.HISTOGRAM, lbls)

    def record_queue_depth(self, queue_name: str, depth: int, labels: Optional[Dict[str, str]] = None) -> None:
        lbls = {**(labels or {}), "queue_name": queue_name}
        self.registry.record("queue_depth_messages", float(depth), MetricType.GAUGE, lbls)


class AIMetricCollector:
    """Collects AI model, prompt token, cost, safety, and hallucination metrics."""

    def __init__(self, registry: MetricRegistry) -> None:
        self.registry = registry

    def record_inference(
        self,
        model_id: str,
        provider: str,
        prompt_tokens: int,
        completion_tokens: int,
        latency_seconds: float,
        cost_usd: float = 0.0,
        safety_violation: bool = False,
        hallucination_score: float = 0.0,
        labels: Optional[Dict[str, str]] = None,
    ) -> None:
        lbls = {**(labels or {}), "model_id": model_id, "provider": provider}
        self.registry.increment("ai_inference_requests_total", 1.0, lbls)
        self.registry.increment("ai_prompt_tokens_total", float(prompt_tokens), lbls)
        self.registry.increment("ai_completion_tokens_total", float(completion_tokens), lbls)
        self.registry.record("ai_inference_latency_seconds", latency_seconds, MetricType.HISTOGRAM, lbls)
        self.registry.increment("ai_cost_usd_total", cost_usd, lbls)
        if safety_violation:
            self.registry.increment("ai_safety_violations_total", 1.0, lbls)
        if hallucination_score > 0.0:
            self.registry.record("ai_hallucination_score", hallucination_score, MetricType.GAUGE, lbls)
