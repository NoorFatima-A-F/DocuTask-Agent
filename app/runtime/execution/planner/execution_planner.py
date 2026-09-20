"""
Execution Planner for Phase 13.15.
Translates high-level mission directives into optimized execution DAGs with Critical Path Method (CPM) and contingency branches.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid

from app.runtime.execution.events.execution_events import (
    ExecutionEvent,
    ExecutionEventType,
    RiskLevel,
    WorkflowExecutionMode,
    execution_event_bus,
)
from app.runtime.execution.tool_registry.tool_registry_engine import tool_registry_engine
from app.runtime.execution.workflow.workflow_engine import WorkflowDefinition, WorkflowStep


@dataclass
class PlannedStepNode:
    step_id: str
    tool_id: str
    name: str
    estimated_duration_ms: float
    risk_level: RiskLevel
    early_start: float = 0.0
    early_finish: float = 0.0
    late_start: float = 0.0
    late_finish: float = 0.0
    slack: float = 0.0
    is_critical_path: bool = False
    contingency_step_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "step_id": self.step_id,
            "tool_id": self.tool_id,
            "name": self.name,
            "estimated_duration_ms": round(self.estimated_duration_ms, 2),
            "risk_level": self.risk_level.value if isinstance(self.risk_level, RiskLevel) else str(self.risk_level),
            "early_start": round(self.early_start, 2),
            "early_finish": round(self.early_finish, 2),
            "late_start": round(self.late_start, 2),
            "late_finish": round(self.late_finish, 2),
            "slack": round(self.slack, 2),
            "is_critical_path": self.is_critical_path,
            "contingency_step_id": self.contingency_step_id,
        }


@dataclass
class ExecutionPlan:
    plan_id: str
    mission_goal: str
    workflow_id: str
    nodes: List[PlannedStepNode] = field(default_factory=list)
    total_estimated_duration_ms: float = 0.0
    critical_path_steps: List[str] = field(default_factory=list)
    overall_risk: RiskLevel = RiskLevel.MEDIUM
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "plan_id": self.plan_id,
            "mission_goal": self.mission_goal,
            "workflow_id": self.workflow_id,
            "nodes": [n.to_dict() for n in self.nodes],
            "total_estimated_duration_ms": round(self.total_estimated_duration_ms, 2),
            "critical_path_steps": self.critical_path_steps,
            "overall_risk": self.overall_risk.value if isinstance(self.overall_risk, RiskLevel) else str(self.overall_risk),
            "created_at": self.created_at,
        }


class ExecutionPlanner:
    """Decomposes goals into DAGs and computes CPM critical path analysis."""

    def __init__(self):
        self._plans: Dict[str, ExecutionPlan] = {}

    def plan_mission(self, mission_goal: str, target_tools: Optional[List[str]] = None) -> tuple[WorkflowDefinition, ExecutionPlan]:
        plan_id = f"plan_{uuid.uuid4().hex[:10]}"
        workflow_id = f"wf_{uuid.uuid4().hex[:10]}"

        # Intelligent tool matching based on mission keyword cues
        goal_lower = mission_goal.lower()
        steps: List[WorkflowStep] = []

        if "deploy" in goal_lower or "hotfix" in goal_lower or "scale" in goal_lower:
            steps = [
                WorkflowStep(
                    step_id="step_log_inspection",
                    name="Query Warehouse Diagnostics",
                    tool_id="postgres_execute_query",
                    inputs={"connection_id": "conn_postgres_warehouse", "query": "SELECT error_type, count(*) FROM logs GROUP BY error_type;"},
                    depends_on=[],
                ),
                WorkflowStep(
                    step_id="step_github_pr",
                    name="Open Patch Pull Request",
                    tool_id="github_create_pull_request",
                    inputs={"repo": "enterprise-corp/core-api", "title": f"fix: auto-resolved {mission_goal[:40]}", "head": "bot/auto-fix", "base": "main"},
                    depends_on=["step_log_inspection"],
                    is_compensable=True,
                    compensation_tool_id="github_close_pull_request",
                ),
                WorkflowStep(
                    step_id="step_k8s_deploy",
                    name="Deploy Kubernetes Canary",
                    tool_id="k8s_scale_deployment",
                    inputs={"namespace": "production", "deployment_name": "core-api-canary", "replicas": 2},
                    depends_on=["step_github_pr"],
                    is_compensable=True,
                    compensation_tool_id="k8s_scale_deployment",
                ),
                WorkflowStep(
                    step_id="step_slack_alert",
                    name="Send Deployment Notification",
                    tool_id="slack_send_channel_message",
                    inputs={"channel": "#autonomous-ops-feed", "message": f"Deployment executed for: {mission_goal}"},
                    depends_on=["step_k8s_deploy"],
                    is_compensable=False,
                ),
            ]
        elif "invoice" in goal_lower or "billing" in goal_lower or "stripe" in goal_lower:
            steps = [
                WorkflowStep(
                    step_id="step_fetch_customer",
                    name="Fetch Customer Record",
                    tool_id="postgres_execute_query",
                    inputs={"connection_id": "conn_postgres_warehouse", "query": "SELECT * FROM customers WHERE status='active' LIMIT 1;"},
                    depends_on=[],
                ),
                WorkflowStep(
                    step_id="step_generate_invoice",
                    name="Issue Stripe Customer Invoice",
                    tool_id="stripe_create_customer_invoice",
                    inputs={"customer_id": "cus_N8xL9p2q1", "amount_cents": 45000, "currency": "usd", "description": "Autonomous AI SLA tier"},
                    depends_on=["step_fetch_customer"],
                    is_compensable=True,
                ),
                WorkflowStep(
                    step_id="step_archive_receipt",
                    name="Archive S3 Receipt",
                    tool_id="aws_s3_upload_artifact",
                    inputs={"bucket": "enterprise-invoices-vault", "key": "invoices/inv_2026_09.json", "payload": "Invoice payload receipt"},
                    depends_on=["step_generate_invoice"],
                    is_compensable=True,
                    compensation_tool_id="aws_s3_delete_artifact",
                ),
                WorkflowStep(
                    step_id="step_notify_finance",
                    name="Notify Finance Channel",
                    tool_id="slack_send_channel_message",
                    inputs={"channel": "#finance-ops", "message": "Enterprise Invoice created and archived to AWS S3."},
                    depends_on=["step_archive_receipt"],
                ),
            ]
        elif "scrape" in goal_lower or "browse" in goal_lower or "portal" in goal_lower:
            steps = [
                WorkflowStep(
                    step_id="step_browse_portal",
                    name="Extract Portal Web Content",
                    tool_id="playwright_web_scraper",
                    inputs={"url": "https://portal.enterprise-vendor.com/invoices", "extract_selector": "div.invoice-table"},
                    depends_on=[],
                ),
                WorkflowStep(
                    step_id="step_store_parsed_data",
                    name="Persist Web Data in Warehouse",
                    tool_id="postgres_execute_query",
                    inputs={"connection_id": "conn_postgres_warehouse", "query": "INSERT INTO scraped_records (data) VALUES ('portal_data');"},
                    depends_on=["step_browse_portal"],
                ),
                WorkflowStep(
                    step_id="step_notify_completion",
                    name="Slack Scrape Report",
                    tool_id="slack_send_channel_message",
                    inputs={"channel": "#ops-feed", "message": "Playwright scraping mission completed."},
                    depends_on=["step_store_parsed_data"],
                ),
            ]
        else:
            # Universal fallback plan
            steps = [
                WorkflowStep(
                    step_id="step_query_db",
                    name="Inspect Relevant Data",
                    tool_id="postgres_execute_query",
                    inputs={"connection_id": "conn_postgres_warehouse", "query": "SELECT current_timestamp;"},
                    depends_on=[],
                ),
                WorkflowStep(
                    step_id="step_api_call",
                    name="Invoke External Universal API",
                    tool_id="rest_api_universal_caller",
                    inputs={"url": "https://api.enterprise.corp/v1/mission-sync", "method": "POST"},
                    depends_on=["step_query_db"],
                ),
                WorkflowStep(
                    step_id="step_notify",
                    name="Broadcast Status",
                    tool_id="slack_send_channel_message",
                    inputs={"channel": "#ops-feed", "message": f"Completed: {mission_goal}"},
                    depends_on=["step_api_call"],
                ),
            ]

        workflow = WorkflowDefinition(
            workflow_id=workflow_id,
            name=f"Autonomous Execution: {mission_goal[:50]}",
            description=f"Generated workflow for mission: {mission_goal}",
            mode=WorkflowExecutionMode.DAG,
            steps=steps,
        )

        # Critical Path Method (CPM) calculation
        nodes: List[PlannedStepNode] = []
        for s in steps:
            tool = tool_registry_engine.get_tool(s.tool_id)
            duration = tool.average_latency_ms if tool else 50.0
            risk = tool.risk_level if tool else RiskLevel.MEDIUM
            nodes.append(
                PlannedStepNode(
                    step_id=s.step_id,
                    tool_id=s.tool_id,
                    name=s.name,
                    estimated_duration_ms=duration,
                    risk_level=risk,
                    contingency_step_id=s.compensation_tool_id,
                )
            )

        # Forward Pass: Early Start (ES) & Early Finish (EF)
        node_map = {n.step_id: n for n in nodes}
        for s in steps:
            cur_node = node_map[s.step_id]
            if not s.depends_on:
                cur_node.early_start = 0.0
                cur_node.early_finish = cur_node.estimated_duration_ms
            else:
                max_ef = max(node_map[dep].early_finish for dep in s.depends_on if dep in node_map)
                cur_node.early_start = max_ef
                cur_node.early_finish = cur_node.early_start + cur_node.estimated_duration_ms

        total_duration = max((n.early_finish for n in nodes), default=0.0)

        # Backward Pass: Late Start (LS) & Late Finish (LF)
        for n in nodes:
            n.late_finish = total_duration
            n.late_start = n.late_finish - n.estimated_duration_ms

        for s in reversed(steps):
            cur_node = node_map[s.step_id]
            dependents = [step for step in steps if s.step_id in step.depends_on]
            if dependents:
                min_ls = min(node_map[dep.step_id].late_start for dep in dependents)
                cur_node.late_finish = min_ls
                cur_node.late_start = cur_node.late_finish - cur_node.estimated_duration_ms

            cur_node.slack = cur_node.late_start - cur_node.early_start
            cur_node.is_critical_path = abs(cur_node.slack) < 0.01

        critical_steps = [n.step_id for n in nodes if n.is_critical_path]
        overall_risk = max((n.risk_level for n in nodes), key=lambda r: ["minimal", "low", "medium", "high", "critical"].index(r.value), default=RiskLevel.LOW)

        plan = ExecutionPlan(
            plan_id=plan_id,
            mission_goal=mission_goal,
            workflow_id=workflow_id,
            nodes=nodes,
            total_estimated_duration_ms=total_duration,
            critical_path_steps=critical_steps,
            overall_risk=overall_risk,
        )

        self._plans[plan_id] = plan
        execution_event_bus.publish(
            ExecutionEvent(
                event_type=ExecutionEventType.PLAN_GENERATED,
                source="execution_planner",
                payload={"plan_id": plan_id, "workflow_id": workflow_id, "critical_path": critical_steps, "duration_ms": total_duration},
                risk_level=overall_risk,
            )
        )

        return workflow, plan

    def get_plan(self, plan_id: str) -> Optional[ExecutionPlan]:
        return self._plans.get(plan_id)

    def list_plans(self) -> List[ExecutionPlan]:
        return list(self._plans.values())


# Global Singleton
execution_planner = ExecutionPlanner()
