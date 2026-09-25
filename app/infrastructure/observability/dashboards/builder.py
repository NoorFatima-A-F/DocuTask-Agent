"""
Dashboard Templates & Factory Builder.

Provides pre-built operational dashboard templates for Executive, SRE, Operations,
AI Runtime, Workflow Platform, and Multi-Tenant views.
"""

from __future__ import annotations

from app.infrastructure.observability.dashboards.models import (
    Dashboard,
    DashboardPanel,
    DashboardWidget,
    WidgetType,
)


class DashboardBuilder:
    """
    Factory generating standardized operational dashboard layouts.
    """

    @staticmethod
    def build_sre_dashboard(dashboard_id: str = "dash-sre-overview") -> Dashboard:
        return Dashboard(
            dashboard_id=dashboard_id,
            title="SRE Platform Health & Latency Overview",
            category="SRE",
            panels=[
                DashboardPanel(
                    panel_id="panel-traffic",
                    title="Traffic & Latency Overview",
                    widgets=[
                        DashboardWidget(
                            widget_id="w-req-rate",
                            title="Total Request Rate (rps)",
                            widget_type=WidgetType.TIMESERIES,
                            metric_query="system_network_rx_mbps",
                        ),
                        DashboardWidget(
                            widget_id="w-p99-latency",
                            title="p99 Latency (ms)",
                            widget_type=WidgetType.GAUGE,
                            metric_query="workflow_task_duration_seconds",
                        ),
                    ],
                ),
                DashboardPanel(
                    panel_id="panel-resources",
                    title="Cluster Resource Utilization",
                    widgets=[
                        DashboardWidget(
                            widget_id="w-cpu-usage",
                            title="CPU Utilization %",
                            widget_type=WidgetType.GAUGE,
                            metric_query="system_cpu_usage_percent",
                        ),
                        DashboardWidget(
                            widget_id="w-mem-usage",
                            title="Memory Utilization %",
                            widget_type=WidgetType.GAUGE,
                            metric_query="system_memory_usage_percent",
                        ),
                    ],
                ),
            ],
            tags=["sre", "infrastructure", "latency"],
        )

    @staticmethod
    def build_ai_runtime_dashboard(dashboard_id: str = "dash-ai-runtime") -> Dashboard:
        return Dashboard(
            dashboard_id=dashboard_id,
            title="AI Runtime & Model Execution Insights",
            category="AI_RUNTIME",
            panels=[
                DashboardPanel(
                    panel_id="panel-ai-tokens",
                    title="Inference & Token Consumption",
                    widgets=[
                        DashboardWidget(
                            widget_id="w-tokens-total",
                            title="Total AI Tokens Processed",
                            widget_type=WidgetType.SINGLESTAT,
                            metric_query="ai_prompt_tokens_total",
                        ),
                        DashboardWidget(
                            widget_id="w-cost-total",
                            title="Total Inference Cost (USD)",
                            widget_type=WidgetType.SINGLESTAT,
                            metric_query="ai_cost_usd_total",
                        ),
                        DashboardWidget(
                            widget_id="w-ai-latency",
                            title="Model Prompt Latency (s)",
                            widget_type=WidgetType.TIMESERIES,
                            metric_query="ai_inference_latency_seconds",
                        ),
                    ],
                ),
            ],
            tags=["ai", "llm", "cost", "tokens"],
        )

    @staticmethod
    def build_workflow_dashboard(dashboard_id: str = "dash-workflows") -> Dashboard:
        return Dashboard(
            dashboard_id=dashboard_id,
            title="Workflows & Task Queue Telemetry",
            category="WORKFLOW",
            panels=[
                DashboardPanel(
                    panel_id="panel-queues",
                    title="Queue Depth & Throughput",
                    widgets=[
                        DashboardWidget(
                            widget_id="w-queue-depth",
                            title="Active Queue Backlog",
                            widget_type=WidgetType.GAUGE,
                            metric_query="queue_depth_messages",
                        ),
                        DashboardWidget(
                            widget_id="w-tasks-total",
                            title="Completed Tasks",
                            widget_type=WidgetType.SINGLESTAT,
                            metric_query="workflow_tasks_total",
                        ),
                    ],
                ),
            ],
            tags=["workflows", "queues", "tasks"],
        )
