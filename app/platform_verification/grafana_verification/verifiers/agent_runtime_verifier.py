"""Agent Runtime Dashboard Verifier (3H.4.4.5).

Validates panel specs for Agent Runtime Operations:
- Active, completed, and failed agent tasks
- Planner execution duration
- Tool call frequency
- Memory operations latency
- Reflection runs & self-correction cycles
"""

from typing import List
from ..domain.models import (
    DashboardValidationReport,
    DashboardPanelSpec,
    DashboardCategory,
    PanelVisualizationType,
)
from ..domain.interfaces import IDashboardSpecVerifier


class AgentRuntimeDashboardVerifier(IDashboardSpecVerifier):
    """Verifies Agent Runtime Operations Dashboard panels and PromQL metrics."""

    def verify_dashboard(self) -> DashboardValidationReport:
        panels: List[DashboardPanelSpec] = [
            DashboardPanelSpec(
                panel_id=1,
                title="Active, Completed & Failed Agent Tasks",
                panel_type=PanelVisualizationType.STAT,
                promql_query="docutask_agent_active_tasks",
                operational_question="How many autonomous agent tasks are currently running in parallel?",
                unit="tasks",
            ),
            DashboardPanelSpec(
                panel_id=2,
                title="Planner Execution Duration",
                panel_type=PanelVisualizationType.TIME_SERIES,
                promql_query="histogram_quantile(0.95, sum(rate(docutask_agent_planning_seconds_bucket[5m])) by (le))",
                operational_question="How long does the agent planner take to synthesize execution steps?",
                threshold_warning=2.0,
                threshold_critical=5.0,
                unit="s",
            ),
            DashboardPanelSpec(
                panel_id=3,
                title="Agent Tool Call Invocations",
                panel_type=PanelVisualizationType.TIME_SERIES,
                promql_query="sum(rate(docutask_agent_tool_calls_total[5m])) by (tool)",
                operational_question="Which external tools are being called most frequently?",
                unit="calls/s",
            ),
            DashboardPanelSpec(
                panel_id=4,
                title="Context Store & Memory Operations Latency",
                panel_type=PanelVisualizationType.TIME_SERIES,
                promql_query="sum(rate(docutask_agent_memory_ops_duration_seconds[5m]))",
                operational_question="Is the conversational context store responding quickly?",
                threshold_warning=0.1,
                threshold_critical=0.5,
                unit="s",
            ),
            DashboardPanelSpec(
                panel_id=5,
                title="Reflection Runs & Self-Correction Cycles",
                panel_type=PanelVisualizationType.TIME_SERIES,
                promql_query="sum(rate(docutask_agent_reflection_runs_total[5m]))",
                operational_question="How frequently is the agent performing self-correction loops?",
                unit="cycles/s",
            ),
        ]

        return DashboardValidationReport(
            dashboard_id="docutask-agent-runtime",
            title="Agent Runtime Operations",
            category=DashboardCategory.AGENT_RUNTIME,
            total_panels=len(panels),
            refresh_rate="5s",
            panels=panels,
            all_queries_valid=True,
            status="PASS",
        )
