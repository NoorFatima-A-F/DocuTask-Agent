"""Specialized Platform Metric Collectors (Infra, Runtime, Workflow, Agent, AI, Connectors)."""

from __future__ import annotations

from typing import Optional

from .registry import MetricRegistry


class PlatformMetricsCollector:
    """Collects domain-specific operational metrics across all platform layers."""

    def __init__(self, registry: Optional[MetricRegistry] = None):
        self.registry = registry or MetricRegistry()

    # 1. Infrastructure Metrics
    def record_infrastructure(
        self,
        node_id: str,
        cpu_usage_pct: float,
        memory_usage_pct: float,
        disk_usage_pct: float,
        network_rx_bytes: float = 0.0,
        network_tx_bytes: float = 0.0,
        healthy: bool = True,
    ) -> None:
        labels = {"node_id": node_id}
        self.registry.gauge("node_cpu_usage_percent", "Node CPU usage percentage", labels).set(cpu_usage_pct)
        self.registry.gauge("node_memory_usage_percent", "Node memory usage percentage", labels).set(memory_usage_pct)
        self.registry.gauge("node_disk_usage_percent", "Node disk usage percentage", labels).set(disk_usage_pct)
        self.registry.gauge("node_health_status", "Node health (1=healthy, 0=unhealthy)", labels).set(1.0 if healthy else 0.0)
        self.registry.counter("node_network_rx_bytes_total", "Total network received bytes", labels).inc(network_rx_bytes)
        self.registry.counter("node_network_tx_bytes_total", "Total network transmitted bytes", labels).inc(network_tx_bytes)

    # 2. Runtime Metrics
    def record_runtime(
        self,
        cluster_id: str,
        worker_count: int,
        queue_depth: int,
        execution_rate_dpm: float,
        failure_count: int = 0,
        retry_count: int = 0,
    ) -> None:
        labels = {"cluster_id": cluster_id}
        self.registry.gauge("runtime_worker_count", "Active runtime workers", labels).set(float(worker_count))
        self.registry.gauge("runtime_queue_depth", "Current queue depth", labels).set(float(queue_depth))
        self.registry.gauge("runtime_execution_rate_dpm", "Document processing rate per minute", labels).set(execution_rate_dpm)
        if failure_count > 0:
            self.registry.counter("runtime_tasks_failed_total", "Total runtime tasks failed", labels).inc(float(failure_count))
        if retry_count > 0:
            self.registry.counter("runtime_tasks_retried_total", "Total runtime tasks retried", labels).inc(float(retry_count))

    # 3. Workflow Metrics
    def record_workflow_execution(
        self,
        workflow_type: str,
        tenant_id: str,
        duration_seconds: float,
        success: bool,
    ) -> None:
        labels = {"workflow_type": workflow_type, "tenant_id": tenant_id}
        self.registry.counter("workflow_started_total", "Total workflows initiated", labels).inc(1.0)
        if success:
            self.registry.counter("workflow_completed_total", "Total workflows successfully completed", labels).inc(1.0)
        else:
            self.registry.counter("workflow_failed_total", "Total workflows failed", labels).inc(1.0)
        self.registry.histogram("workflow_duration_seconds", "Workflow total execution duration", labels=labels).observe(duration_seconds)

    # 4. Agent Execution Metrics
    def record_agent_execution(
        self,
        agent_role: str,
        tenant_id: str,
        latency_seconds: float,
        tool_calls: int,
        reasoning_steps: int,
        token_usage: int,
        cost_usd: float,
        success: bool,
    ) -> None:
        labels = {"agent_role": agent_role, "tenant_id": tenant_id}
        self.registry.counter("agent_executions_total", "Total agent executions", labels).inc(1.0)
        if not success:
            self.registry.counter("agent_failures_total", "Total agent execution failures", labels).inc(1.0)
        self.registry.counter("agent_tool_calls_total", "Total agent tool invocations", labels).inc(float(tool_calls))
        self.registry.counter("agent_reasoning_steps_total", "Total reasoning steps executed", labels).inc(float(reasoning_steps))
        self.registry.counter("agent_token_usage_total", "Total tokens used by agent", labels).inc(float(token_usage))
        self.registry.counter("agent_cost_usd_total", "Total dollar cost of agent runs", labels).inc(cost_usd)
        self.registry.histogram("agent_latency_seconds", "Agent end-to-end latency", labels=labels).observe(latency_seconds)

    # 5. AI Model Metrics
    def record_ai_inference(
        self,
        model_name: str,
        provider: str,
        latency_seconds: float,
        prompt_tokens: int,
        completion_tokens: int,
        hallucination_detected: bool = False,
        eval_score: float = 1.0,
        fallback_used: bool = False,
    ) -> None:
        labels = {"model": model_name, "provider": provider}
        self.registry.counter("ai_model_requests_total", "Total AI model invocations", labels).inc(1.0)
        self.registry.counter("ai_prompt_tokens_total", "Total prompt tokens", labels).inc(float(prompt_tokens))
        self.registry.counter("ai_completion_tokens_total", "Total completion tokens", labels).inc(float(completion_tokens))
        self.registry.histogram("ai_model_latency_seconds", "Model inference latency", labels=labels).observe(latency_seconds)
        self.registry.histogram("ai_eval_scores", "Model evaluation score", labels=labels).observe(eval_score)
        if hallucination_detected:
            self.registry.counter("ai_hallucinations_total", "Total hallucinations detected", labels).inc(1.0)
        if fallback_used:
            self.registry.counter("ai_fallbacks_total", "Total model fallbacks triggered", labels).inc(1.0)

    # 6. Connector Metrics
    def record_connector_call(
        self,
        connector_type: str,
        endpoint: str,
        latency_seconds: float,
        success: bool,
        rate_limited: bool = False,
    ) -> None:
        labels = {"connector": connector_type, "endpoint": endpoint}
        self.registry.counter("connector_calls_total", "Total connector API calls", labels).inc(1.0)
        if not success:
            self.registry.counter("connector_failures_total", "Total connector call failures", labels).inc(1.0)
        if rate_limited:
            self.registry.counter("connector_rate_limits_total", "Total connector rate limit events", labels).inc(1.0)
        self.registry.histogram("connector_latency_seconds", "Connector call latency", labels=labels).observe(latency_seconds)
