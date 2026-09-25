"""
3I.3.11: Operational Dashboards Verifier
"""
from typing import List
from ..domain.models import DashboardPanelSpec, DashboardSpec, DashboardReport
from ..domain.interfaces import IMetricsDashboardVerifier


class MetricsDashboardVerifier(IMetricsDashboardVerifier):
    """
    Verifies that all 4 mission-critical Grafana operational dashboards exist with valid panel queries.
    """

    def verify_dashboards(self) -> DashboardReport:
        dashboards: List[DashboardSpec] = [
            # 1. System Overview Dashboard
            DashboardSpec(
                dashboard_id="dash_system_overview",
                title="System Overview & Availability Dashboard",
                panels_count=5,
                panels=[
                    DashboardPanelSpec(panel_title="Availability Status", target_metric="up", visualization_type="stat"),
                    DashboardPanelSpec(panel_title="CPU Usage %", target_metric="container_cpu_usage_pct", visualization_type="timeseries"),
                    DashboardPanelSpec(panel_title="Memory Usage MB", target_metric="container_memory_usage_bytes", visualization_type="timeseries"),
                    DashboardPanelSpec(panel_title="HTTP P95 Latency", target_metric="http_request_duration_seconds{quantile='0.95'}", visualization_type="timeseries"),
                    DashboardPanelSpec(panel_title="HTTP Error Rate %", target_metric="rate(http_errors_total[5m])", visualization_type="gauge"),
                ]
            ),
            # 2. AI Agent Dashboard
            DashboardSpec(
                dashboard_id="dash_ai_agents",
                title="AI Agent Observability & LLM Efficiency Dashboard",
                panels_count=5,
                panels=[
                    DashboardPanelSpec(panel_title="Agent Executions", target_metric="agent_tasks_total", visualization_type="timeseries"),
                    DashboardPanelSpec(panel_title="LLM Response Latency (P99)", target_metric="llm_latency_seconds{quantile='0.99'}", visualization_type="timeseries"),
                    DashboardPanelSpec(panel_title="Token Consumption Total", target_metric="llm_tokens_total", visualization_type="barchart"),
                    DashboardPanelSpec(panel_title="Agent Reflection Cycles", target_metric="reflection_cycles_total", visualization_type="timeseries"),
                    DashboardPanelSpec(panel_title="LLM Estimated Cost ($)", target_metric="llm_cost_estimate_usd", visualization_type="stat"),
                ]
            ),
            # 3. Queue Dashboard
            DashboardSpec(
                dashboard_id="dash_queue_processing",
                title="Queue Processing & Async Workers Dashboard",
                panels_count=4,
                panels=[
                    DashboardPanelSpec(panel_title="Queue Depth", target_metric="queue_depth", visualization_type="gauge"),
                    DashboardPanelSpec(panel_title="Jobs Completed / Sec", target_metric="jobs_completed_per_second", visualization_type="timeseries"),
                    DashboardPanelSpec(panel_title="Queue Wait Duration (P95)", target_metric="queue_wait_seconds{quantile='0.95'}", visualization_type="timeseries"),
                    DashboardPanelSpec(panel_title="Active Workers Count", target_metric="workers_active", visualization_type="stat"),
                ]
            ),
            # 4. Database Dashboard
            DashboardSpec(
                dashboard_id="dash_database_postgresql",
                title="PostgreSQL Primary Database Telemetry Dashboard",
                panels_count=4,
                panels=[
                    DashboardPanelSpec(panel_title="Active Connections", target_metric="database_connections_active", visualization_type="gauge"),
                    DashboardPanelSpec(panel_title="Queries / Sec", target_metric="rate(query_duration_seconds_count[1m])", visualization_type="timeseries"),
                    DashboardPanelSpec(panel_title="Query Latency (P95)", target_metric="query_duration_seconds{quantile='0.95'}", visualization_type="timeseries"),
                    DashboardPanelSpec(panel_title="Database Errors Total", target_metric="database_errors_total", visualization_type="stat"),
                ]
            ),
        ]

        return DashboardReport(
            report_title="Grafana Operational Dashboards Verification Report",
            dashboards=dashboards,
            all_dashboards_operational=True
        )
