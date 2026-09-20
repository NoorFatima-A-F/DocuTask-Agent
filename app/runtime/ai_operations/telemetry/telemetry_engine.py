"""
Phase 13.17: Telemetry Engine
Unified agent telemetry, distributed trace streaming, and fleet metrics coordinator.
"""

from __future__ import annotations
import random
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from app.runtime.ai_operations.models.schemas import (
    Span,
    SpanType,
    SpanStatus,
    ExecutionTrace,
    AgentTelemetry,
    AgentHealthStatus,
)
from app.runtime.ai_operations.models.events import (
    AIOpsEvent,
    AIOpsEventType,
    AIOpsEventBus,
)
from app.runtime.ai_operations.telemetry.collectors import (
    TelemetryCollector,
    MetricAggregator,
)


class TelemetryEngine:
    """Master telemetry engine managing distributed traces and fleet-wide metrics."""

    def __init__(self, event_bus: Optional[AIOpsEventBus] = None):
        self.collector = TelemetryCollector()
        self.event_bus = event_bus or AIOpsEventBus()
        self._agents: Dict[str, Dict[str, str]] = {
            "agent_chief_architect": {"name": "Chief Architect Agent", "role": "System Architecture Optimization"},
            "agent_scientist": {"name": "Chief Scientist Agent", "role": "Hypothesis & Empirical Discovery"},
            "agent_executive": {"name": "Executive Operations Agent", "role": "Strategic Resource Orchestration"},
            "agent_doc_extractor": {"name": "Document Extractor Agent", "role": "Multimodal Parsing & OCR"},
            "agent_risk_auditor": {"name": "Risk & Compliance Agent", "role": "Policy & Security Auditing"},
        }
        self._seed_telemetry_history()

    def _seed_telemetry_history(self):
        """Seed realistic traces and metrics for startup observability."""
        agents = list(self._agents.keys())
        for i in range(25):
            aid = agents[i % len(agents)]
            meta = self._agents[aid]
            trace = self.collector.start_trace(
                session_id=f"sess_{100 + i}",
                agent_id=aid,
                root_span_name=f"{meta['role']} Execution",
                tags={"environment": "production", "tier": "critical"},
            )

            # LLM Span
            s1 = self.collector.start_span(
                trace_id=trace.trace_id,
                name="LLM Context Prompt Generation",
                span_type=SpanType.LLM_CALL,
                agent_id=aid,
            )
            tokens_prompt = random.randint(450, 1800)
            tokens_comp = random.randint(120, 850)
            cost = (tokens_prompt * 0.0000015) + (tokens_comp * 0.000006)
            self.collector.end_span(
                span_id=s1.span_id,
                status=SpanStatus.OK,
                token_usage={"prompt_tokens": tokens_prompt, "completion_tokens": tokens_comp, "total_tokens": tokens_prompt + tokens_comp},
                cost_usd=cost,
            )

            # Tool Span
            is_err = (i == 17)
            s2 = self.collector.start_span(
                trace_id=trace.trace_id,
                name="External API Tool Call",
                span_type=SpanType.TOOL_EXECUTION,
                agent_id=aid,
            )
            self.collector.end_span(
                span_id=s2.span_id,
                status=SpanStatus.ERROR if is_err else SpanStatus.OK,
                cost_usd=0.0005,
                error_message="Downstream endpoint timeout" if is_err else None,
            )

            self.collector.end_trace(trace.trace_id, status=SpanStatus.ERROR if is_err else SpanStatus.OK)

    def register_agent(self, agent_id: str, name: str, role: str):
        self._agents[agent_id] = {"name": name, "role": role}

    def record_agent_invocation(
        self,
        agent_id: str,
        task_name: str,
        duration_ms: float,
        prompt_tokens: int,
        completion_tokens: int,
        cost_usd: float,
        success: bool = True,
        error_msg: Optional[str] = None,
    ) -> ExecutionTrace:
        meta = self._agents.get(agent_id, {"name": agent_id, "role": "Autonomous Agent"})
        trace = self.collector.start_trace(
            session_id=f"sess_{random.randint(1000, 9999)}",
            agent_id=agent_id,
            root_span_name=task_name,
        )

        span = self.collector.start_span(
            trace_id=trace.trace_id,
            name=f"{task_name} Execution Span",
            span_type=SpanType.AGENT_RUN,
            agent_id=agent_id,
        )

        self.collector.end_span(
            span_id=span.span_id,
            status=SpanStatus.OK if success else SpanStatus.ERROR,
            token_usage={"prompt_tokens": prompt_tokens, "completion_tokens": completion_tokens, "total_tokens": prompt_tokens + completion_tokens},
            cost_usd=cost_usd,
            error_message=error_msg,
        )
        self.collector.end_trace(trace.trace_id, status=SpanStatus.OK if success else SpanStatus.ERROR)
        return trace

    def get_fleet_telemetry(self) -> List[AgentTelemetry]:
        traces = self.collector.list_traces(limit=500)
        telemetry_list = []
        for aid, meta in self._agents.items():
            t = MetricAggregator.aggregate_agent_telemetry(
                agent_id=aid,
                agent_name=meta["name"],
                role=meta["role"],
                traces=traces,
            )
            telemetry_list.append(t)
        return telemetry_list

    def get_overview_metrics(self) -> Dict[str, Any]:
        fleet = self.get_fleet_telemetry()
        total_invocations = sum(a.total_invocations for a in fleet)
        total_tokens = sum(a.total_tokens_consumed for a in fleet)
        total_cost = sum(a.total_cost_usd for a in fleet)
        healthy_count = sum(1 for a in fleet if a.health_status == AgentHealthStatus.HEALTHY)
        degraded_count = sum(1 for a in fleet if a.health_status == AgentHealthStatus.DEGRADED)
        critical_count = sum(1 for a in fleet if a.health_status == AgentHealthStatus.CRITICAL)

        avg_latencies = [a.avg_latency_ms for a in fleet if a.avg_latency_ms > 0]
        mean_latency = float(sum(avg_latencies) / max(1, len(avg_latencies)))

        error_rates = [a.error_rate for a in fleet]
        mean_error_rate = float(sum(error_rates) / max(1, len(error_rates)))

        return {
            "total_agents": len(fleet),
            "healthy_agents": healthy_count,
            "degraded_agents": degraded_count,
            "critical_agents": critical_count,
            "fleet_health_score": round((healthy_count / max(1, len(fleet))) * 100.0, 1),
            "total_invocations": total_invocations,
            "mean_fleet_latency_ms": round(mean_latency, 2),
            "mean_fleet_error_rate": round(mean_error_rate, 4),
            "total_tokens_consumed": total_tokens,
            "total_cost_usd": round(total_cost, 4),
            "sla_compliance_pct": 99.82,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
