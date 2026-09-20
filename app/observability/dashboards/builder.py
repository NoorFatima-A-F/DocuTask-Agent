"""Dashboard Engine and Pre-Configured Enterprise Dashboards."""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

from .widgets import DashboardWidget, WidgetType
from ..metrics.registry import MetricRegistry


class DashboardType(str, Enum):
    GLOBAL_PLATFORM = "GLOBAL_PLATFORM"
    SRE_GOLDEN_SIGNALS = "SRE_GOLDEN_SIGNALS"
    AI_OPERATIONS = "AI_OPERATIONS"
    TENANT_OPERATIONS = "TENANT_OPERATIONS"
    EXECUTIVE = "EXECUTIVE"


@dataclass
class Dashboard:
    dashboard_id: str
    name: str
    dashboard_type: DashboardType
    tenant_id: str = "system"
    widgets: List[DashboardWidget] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)


class DashboardEngine:
    """Creates, registers, and serves live platform operational dashboards."""

    def __init__(self, metric_registry: Optional[MetricRegistry] = None):
        self.metric_registry = metric_registry or MetricRegistry()
        self._dashboards: Dict[str, Dashboard] = {}
        self._initialize_default_dashboards()

    def _initialize_default_dashboards(self) -> None:
        # 1. Global Platform Dashboard
        global_db = Dashboard(
            dashboard_id="db-global-platform",
            name="Global Platform Operations & Infrastructure",
            dashboard_type=DashboardType.GLOBAL_PLATFORM,
            widgets=[
                DashboardWidget("w-node-health", "Cluster Node Health Status", WidgetType.GAUGE, ["node_health_status"]),
                DashboardWidget("w-node-cpu", "Cluster CPU Usage %", WidgetType.TIMESERIES, ["node_cpu_usage_percent"]),
                DashboardWidget("w-node-mem", "Cluster Memory Usage %", WidgetType.TIMESERIES, ["node_memory_usage_percent"]),
                DashboardWidget("w-active-workers", "Runtime Worker Count", WidgetType.GAUGE, ["runtime_worker_count"]),
            ],
            tags=["global", "sre", "infrastructure"],
        )
        self._dashboards[global_db.dashboard_id] = global_db

        # 2. SRE Golden Signals Dashboard
        sre_db = Dashboard(
            dashboard_id="db-sre-golden-signals",
            name="SRE Golden Signals & Reliability",
            dashboard_type=DashboardType.SRE_GOLDEN_SIGNALS,
            widgets=[
                DashboardWidget("w-traffic-rate", "Throughput (Docs/Min)", WidgetType.TIMESERIES, ["runtime_execution_rate_dpm"]),
                DashboardWidget("w-queue-depth", "Queue Backlog Depth", WidgetType.TIMESERIES, ["runtime_queue_depth"]),
                DashboardWidget("w-task-failures", "Task Failure Count", WidgetType.TIMESERIES, ["runtime_tasks_failed_total"]),
                DashboardWidget("w-slo-status", "API SLO Compliance Heatmap", WidgetType.SLO_HEATMAP, ["slo_compliance_percent"]),
            ],
            tags=["sre", "golden-signals", "reliability"],
        )
        self._dashboards[sre_db.dashboard_id] = sre_db

        # 3. AI Operations Dashboard
        ai_db = Dashboard(
            dashboard_id="db-ai-operations",
            name="AI System Performance & Model Operations",
            dashboard_type=DashboardType.AI_OPERATIONS,
            widgets=[
                DashboardWidget("w-ai-requests", "AI Model Invocations", WidgetType.TIMESERIES, ["ai_model_requests_total"]),
                DashboardWidget("w-ai-tokens", "Token Usage (Prompt & Completion)", WidgetType.TIMESERIES, ["ai_prompt_tokens_total", "ai_completion_tokens_total"]),
                DashboardWidget("w-ai-latency", "Model Inference Latency (p95)", WidgetType.TIMESERIES, ["ai_model_latency_seconds"]),
                DashboardWidget("w-ai-hallucinations", "Hallucination Events", WidgetType.TIMESERIES, ["ai_hallucinations_total"]),
            ],
            tags=["ai", "agents", "llm-ops"],
        )
        self._dashboards[ai_db.dashboard_id] = ai_db

        # 4. Tenant Operations Dashboard
        tenant_db = Dashboard(
            dashboard_id="db-tenant-operations",
            name="Tenant Workflow & Usage Dashboard",
            dashboard_type=DashboardType.TENANT_OPERATIONS,
            widgets=[
                DashboardWidget("w-tenant-wf-started", "Workflows Started", WidgetType.TIMESERIES, ["workflow_started_total"]),
                DashboardWidget("w-tenant-wf-failed", "Workflows Failed", WidgetType.TIMESERIES, ["workflow_failed_total"]),
                DashboardWidget("w-tenant-cost", "Cumulative AI Cost ($)", WidgetType.GAUGE, ["agent_cost_usd_total"]),
            ],
            tags=["tenant", "usage", "billing"],
        )
        self._dashboards[tenant_db.dashboard_id] = tenant_db

    def register_dashboard(self, dashboard: Dashboard) -> Dashboard:
        self._dashboards[dashboard.dashboard_id] = dashboard
        return dashboard

    def get_dashboard(self, dashboard_id: str) -> Optional[Dashboard]:
        return self._dashboards.get(dashboard_id)

    def list_dashboards(self, dashboard_type: Optional[DashboardType] = None) -> List[Dashboard]:
        if dashboard_type:
            return [d for d in self._dashboards.values() if d.dashboard_type == dashboard_type]
        return list(self._dashboards.values())

    def render_dashboard_data(self, dashboard_id: str) -> Dict[str, Any]:
        """Fetch live telemetry snapshot for widgets on the dashboard."""
        db = self.get_dashboard(dashboard_id)
        if not db:
            return {}

        snapshot = self.metric_registry.dump_snapshot()
        widgets_data: List[Dict[str, Any]] = []

        for w in db.widgets:
            w_values = {}
            for q in w.metric_queries:
                # Find matching counters, gauges, or histograms
                for c_key, c_val in snapshot["counters"].items():
                    if q in c_key:
                        w_values[c_key] = c_val
                for g_key, g_val in snapshot["gauges"].items():
                    if q in g_key:
                        w_values[g_key] = g_val
                for h_key, h_val in snapshot["histograms"].items():
                    if q in h_key:
                        w_values[h_key] = h_val

            widgets_data.append({
                "widget_id": w.widget_id,
                "title": w.title,
                "widget_type": w.widget_type.value,
                "data": w_values,
            })

        return {
            "dashboard_id": db.dashboard_id,
            "name": db.name,
            "dashboard_type": db.dashboard_type.value,
            "widgets": widgets_data,
        }
