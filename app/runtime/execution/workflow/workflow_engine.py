"""
Workflow Engine for Phase 13.15.
Orchestrates multi-step Directed Acyclic Graphs (DAGs) with Saga compensating transactions and conditional branching.
"""

from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
import json
import re
from typing import Any, Dict, List, Optional, Set
import uuid

from app.runtime.execution.events.execution_events import (
    ExecutionEvent,
    ExecutionEventType,
    RiskLevel,
    StepStatus,
    WorkflowExecutionMode,
    execution_event_bus,
)


@dataclass
class WorkflowStep:
    step_id: str
    name: str
    tool_id: str
    inputs: Dict[str, Any] = field(default_factory=dict)
    depends_on: List[str] = field(default_factory=list)  # step_ids that must complete first
    condition: Optional[str] = None  # e.g., "steps.step_1.output.status == 'approved'"
    status: StepStatus = StepStatus.PENDING
    retry_count: int = 0
    max_retries: int = 3
    timeout_seconds: int = 60
    output: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    is_compensable: bool = True
    compensation_tool_id: Optional[str] = None
    compensation_inputs: Dict[str, Any] = field(default_factory=dict)
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    duration_ms: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "step_id": self.step_id,
            "name": self.name,
            "tool_id": self.tool_id,
            "inputs": self.inputs,
            "depends_on": self.depends_on,
            "condition": self.condition,
            "status": self.status.value if isinstance(self.status, StepStatus) else str(self.status),
            "retry_count": self.retry_count,
            "max_retries": self.max_retries,
            "timeout_seconds": self.timeout_seconds,
            "output": self.output,
            "error": self.error,
            "is_compensable": self.is_compensable,
            "compensation_tool_id": self.compensation_tool_id,
            "compensation_inputs": self.compensation_inputs,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "duration_ms": round(self.duration_ms, 2),
        }


@dataclass
class WorkflowDefinition:
    workflow_id: str
    name: str
    description: str
    mode: WorkflowExecutionMode = WorkflowExecutionMode.DAG
    steps: List[WorkflowStep] = field(default_factory=list)
    variables: Dict[str, Any] = field(default_factory=dict)
    risk_level: RiskLevel = RiskLevel.MEDIUM
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def get_step(self, step_id: str) -> Optional[WorkflowStep]:
        for s in self.steps:
            if s.step_id == step_id:
                return s
        return None

    def validate_dag(self) -> tuple[bool, Optional[str]]:
        """Validates that step dependencies form a valid DAG (no cycles, valid refs)."""
        step_ids = {s.step_id for s in self.steps}
        in_degree: Dict[str, int] = {s.step_id: 0 for s in self.steps}
        adj_list: Dict[str, List[str]] = {s.step_id: [] for s in self.steps}

        for s in self.steps:
            for dep in s.depends_on:
                if dep not in step_ids:
                    return False, f"Step '{s.step_id}' depends on unknown step '{dep}'"
                adj_list[dep].append(s.step_id)
                in_degree[s.step_id] += 1

        # Kahn's algorithm for topological sorting and cycle detection
        queue = deque([sid for sid, deg in in_degree.items() if deg == 0])
        visited_count = 0

        while queue:
            node = queue.popleft()
            visited_count += 1
            for neighbor in adj_list[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        if visited_count != len(self.steps):
            return False, "Cycle detected in workflow step dependencies."

        return True, None

    def get_execution_order(self) -> List[List[str]]:
        """Returns topological tiers for parallel or sequential execution."""
        step_ids = {s.step_id for s in self.steps}
        in_degree: Dict[str, int] = {s.step_id: len(s.depends_on) for s in self.steps}
        adj_list: Dict[str, List[str]] = {s.step_id: [] for s in self.steps}

        for s in self.steps:
            for dep in s.depends_on:
                adj_list[dep].append(s.step_id)

        tiers = []
        current_tier = [sid for sid, deg in in_degree.items() if deg == 0]

        while current_tier:
            tiers.append(current_tier)
            next_tier = []
            for node in current_tier:
                for neighbor in adj_list[node]:
                    in_degree[neighbor] -= 1
                    if in_degree[neighbor] == 0:
                        next_tier.append(neighbor)
            current_tier = next_tier

        return tiers

    def to_dict(self) -> Dict[str, Any]:
        return {
            "workflow_id": self.workflow_id,
            "name": self.name,
            "description": self.description,
            "mode": self.mode.value if isinstance(self.mode, WorkflowExecutionMode) else str(self.mode),
            "steps": [s.to_dict() for s in self.steps],
            "variables": self.variables,
            "risk_level": self.risk_level.value if isinstance(self.risk_level, RiskLevel) else str(self.risk_level),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class WorkflowEngine:
    """Manages workflow definitions, DAG validation, and parameter interpolation."""

    def __init__(self):
        self._workflows: Dict[str, WorkflowDefinition] = {}
        self._initialize_seed_workflows()

    def _initialize_seed_workflows(self) -> None:
        seed = WorkflowDefinition(
            workflow_id="wf_cloud_microservice_autodeploy",
            name="Autonomous Production Hotfix & Verification Pipeline",
            description="Extracts error telemetry, creates Git hotfix PR, scales K8s canary deployment, and posts Slack notification.",
            mode=WorkflowExecutionMode.SAGA,
            risk_level=RiskLevel.HIGH,
            steps=[
                WorkflowStep(
                    step_id="step_gather_telemetry",
                    name="Extract Warehouse Error Logs",
                    tool_id="postgres_execute_query",
                    inputs={"connection_id": "conn_postgres_warehouse", "query": "SELECT * FROM system_error_logs WHERE severity='CRITICAL' LIMIT 5;"},
                    depends_on=[],
                ),
                WorkflowStep(
                    step_id="step_create_github_pr",
                    name="Create Automated Patch Pull Request",
                    tool_id="github_create_pull_request",
                    inputs={"repo": "enterprise-corp/core-api", "title": "fix(core): autonomous memory leak patch", "head": "bot/patch-v1.4.2", "base": "main"},
                    depends_on=["step_gather_telemetry"],
                    is_compensable=True,
                    compensation_tool_id="github_close_pull_request",
                ),
                WorkflowStep(
                    step_id="step_scale_canary",
                    name="Scale Kubernetes Canary Replica",
                    tool_id="k8s_scale_deployment",
                    inputs={"namespace": "production", "deployment_name": "core-api-canary", "replicas": 3},
                    depends_on=["step_create_github_pr"],
                    is_compensable=True,
                    compensation_tool_id="k8s_scale_deployment",
                ),
                WorkflowStep(
                    step_id="step_notify_ops",
                    name="Broadcast War Room Notification",
                    tool_id="slack_send_channel_message",
                    inputs={"channel": "#autonomous-ops-feed", "message": "🚀 Autonomous Hotfix Canary deployed and verified successfully.", "priority": "high"},
                    depends_on=["step_scale_canary"],
                    is_compensable=False,
                ),
            ],
        )
        self._workflows[seed.workflow_id] = seed

    def register_workflow(self, workflow: WorkflowDefinition) -> WorkflowDefinition:
        valid, err = workflow.validate_dag()
        if not valid:
            raise ValueError(f"Invalid Workflow DAG: {err}")
        self._workflows[workflow.workflow_id] = workflow
        return workflow

    def get_workflow(self, workflow_id: str) -> Optional[WorkflowDefinition]:
        return self._workflows.get(workflow_id)

    def list_workflows(self) -> List[WorkflowDefinition]:
        return list(self._workflows.values())

    def interpolate_inputs(self, raw_inputs: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Substitutes variables formatted as `${steps.step_1.output.key}` or `${vars.key}`."""
        def _resolve_val(val: Any) -> Any:
            if isinstance(val, str):
                # Check for exact variable replacement
                pattern = r"\$\{([^}]+)\}"
                matches = re.findall(pattern, val)
                if not matches:
                    return val
                
                # If entire string is one variable
                if len(matches) == 1 and val.strip() == f"${{{matches[0]}}}":
                    path = matches[0].split(".")
                    cur = context
                    for p in path:
                        if isinstance(cur, dict):
                            cur = cur.get(p)
                        else:
                            return val
                    return cur if cur is not None else val
                
                # Replace inline tokens
                result = val
                for m in matches:
                    path = m.split(".")
                    cur = context
                    for p in path:
                        if isinstance(cur, dict):
                            cur = cur.get(p)
                        else:
                            cur = None
                            break
                    result = result.replace(f"${{{m}}}", str(cur if cur is not None else ""))
                return result
            elif isinstance(val, dict):
                return {k: _resolve_val(v) for k, v in val.items()}
            elif isinstance(val, list):
                return [_resolve_val(i) for i in val]
            return val

        return {k: _resolve_val(v) for k, v in raw_inputs.items()}


# Global Singleton
workflow_engine = WorkflowEngine()
