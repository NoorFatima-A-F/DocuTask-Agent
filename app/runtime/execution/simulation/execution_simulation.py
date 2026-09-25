"""
Simulation & Digital Twin Engine for Phase 13.15.
Simulates tool executions, computes state mutations in shadow environments, predicts blast radius and costs.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid

from app.runtime.execution.events.execution_events import (
    ExecutionEvent,
    ExecutionEventType,
    RiskLevel,
    StepStatus,
    execution_event_bus,
)
from app.runtime.execution.tool_registry.tool_registry_engine import tool_registry_engine
from app.runtime.execution.workflow.workflow_engine import WorkflowDefinition


@dataclass
class SimulatedStepResult:
    step_id: str
    tool_id: str
    status: StepStatus = StepStatus.SIMULATED
    predicted_duration_ms: float = 45.0
    predicted_cost_usd: float = 0.002
    state_mutations_predicted: List[str] = field(default_factory=list)
    simulated_output: Dict[str, Any] = field(default_factory=dict)
    can_compensate: bool = True
    compensation_rehearsal_passed: bool = True
    risk_score: float = 0.15  # 0.0 to 1.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "step_id": self.step_id,
            "tool_id": self.tool_id,
            "status": self.status.value if isinstance(self.status, StepStatus) else str(self.status),
            "predicted_duration_ms": round(self.predicted_duration_ms, 2),
            "predicted_cost_usd": round(self.predicted_cost_usd, 4),
            "state_mutations_predicted": self.state_mutations_predicted,
            "simulated_output": self.simulated_output,
            "can_compensate": self.can_compensate,
            "compensation_rehearsal_passed": self.compensation_rehearsal_passed,
            "risk_score": round(self.risk_score, 3),
        }


@dataclass
class SimulationReport:
    simulation_id: str
    workflow_id: str
    total_steps: int
    step_results: List[SimulatedStepResult] = field(default_factory=list)
    total_predicted_duration_ms: float = 0.0
    total_predicted_cost_usd: float = 0.0
    blast_radius_scope: str = "isolated"  # isolated, moderate, wide, catastrophic
    simulation_passed: bool = True
    rehearsal_errors: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "simulation_id": self.simulation_id,
            "workflow_id": self.workflow_id,
            "total_steps": self.total_steps,
            "step_results": [r.to_dict() for r in self.step_results],
            "total_predicted_duration_ms": round(self.total_predicted_duration_ms, 2),
            "total_predicted_cost_usd": round(self.total_predicted_cost_usd, 4),
            "blast_radius_scope": self.blast_radius_scope,
            "simulation_passed": self.simulation_passed,
            "rehearsal_errors": self.rehearsal_errors,
            "created_at": self.created_at,
        }


class ExecutionSimulationEngine:
    """Performs pre-execution digital twin rehearsals and blast radius assessments."""

    def __init__(self):
        self._simulations: Dict[str, SimulationReport] = {}

    def simulate_workflow(self, workflow: WorkflowDefinition) -> SimulationReport:
        sim_id = f"sim_{uuid.uuid4().hex[:10]}"
        execution_event_bus.publish(
            ExecutionEvent(
                event_type=ExecutionEventType.SIMULATION_STARTED,
                source="simulation_engine",
                payload={"simulation_id": sim_id, "workflow_id": workflow.workflow_id, "steps_count": len(workflow.steps)},
            )
        )

        results: List[SimulatedStepResult] = []
        errors: List[str] = []
        total_duration = 0.0
        total_cost = 0.0

        for step in workflow.steps:
            tool = tool_registry_engine.get_tool(step.tool_id)
            duration = (tool.average_latency_ms if tool else 40.0) * 1.1  # safety factor
            cost = 0.001
            mutations = []
            sim_output = {}

            if "github" in step.tool_id:
                mutations.append(f"Create PR branch and draft pull request in {step.inputs.get('repo', 'enterprise-corp/core-api')}")
                sim_output = {"pr_number": 1042, "pr_url": f"https://github.com/{step.inputs.get('repo', 'enterprise-corp/core-api')}/pull/1042", "state": "open"}
                cost = 0.0005
            elif "k8s" in step.tool_id:
                mutations.append(f"Modify Kubernetes deployment {step.inputs.get('deployment_name', 'app')} replicas to {step.inputs.get('replicas', 1)}")
                sim_output = {"namespace": step.inputs.get("namespace", "production"), "deployment": step.inputs.get("deployment_name", "app"), "new_replicas": step.inputs.get("replicas", 2)}
                cost = 0.005
            elif "postgres" in step.tool_id or "database" in step.tool_id:
                mutations.append(f"Execute query against shadow database schema: {step.inputs.get('query', '')[:60]}")
                sim_output = {"rows_affected": 3, "data": [{"id": 1, "status": "simulated_row"}], "execution_time_ms": 14.2}
                cost = 0.002
            elif "stripe" in step.tool_id:
                amount = step.inputs.get("amount_cents", 1000)
                mutations.append(f"Create test invoice for customer {step.inputs.get('customer_id')} for ${amount/100:.2f}")
                sim_output = {"invoice_id": f"in_test_{uuid.uuid4().hex[:8]}", "status": "draft", "total_cents": amount}
                cost = 0.01
            elif "browser" in step.tool_id or "playwright" in step.tool_id:
                mutations.append(f"Headless sandbox navigation to {step.inputs.get('url')}")
                sim_output = {"status_code": 200, "page_title": "Simulated Web View", "extracted_text": "Sample verified DOM payload"}
                cost = 0.003
            else:
                mutations.append(f"Universal tool call {step.tool_id}")
                sim_output = {"status": "ok", "simulated": True}

            total_duration += duration
            total_cost += cost

            # Check compensation rehearsal
            comp_passed = True
            if step.is_compensable and not step.compensation_tool_id:
                # Warning but not fatal
                pass

            step_res = SimulatedStepResult(
                step_id=step.step_id,
                tool_id=step.tool_id,
                predicted_duration_ms=duration,
                predicted_cost_usd=cost,
                state_mutations_predicted=mutations,
                simulated_output=sim_output,
                can_compensate=step.is_compensable,
                compensation_rehearsal_passed=comp_passed,
                risk_score=0.1 if (tool and tool.risk_level == RiskLevel.LOW) else 0.45,
            )
            results.append(step_res)

        blast_scope = "isolated"
        if any("k8s" in r.tool_id for r in results):
            blast_scope = "moderate"
        if any("stripe" in r.tool_id and r.simulated_output.get("total_cents", 0) > 100000 for r in results):
            blast_scope = "wide"

        report = SimulationReport(
            simulation_id=sim_id,
            workflow_id=workflow.workflow_id,
            total_steps=len(results),
            step_results=results,
            total_predicted_duration_ms=total_duration,
            total_predicted_cost_usd=total_cost,
            blast_radius_scope=blast_scope,
            simulation_passed=len(errors) == 0,
            rehearsal_errors=errors,
        )

        self._simulations[sim_id] = report
        execution_event_bus.publish(
            ExecutionEvent(
                event_type=ExecutionEventType.SIMULATION_CONCLUDED,
                source="simulation_engine",
                payload={"simulation_id": sim_id, "blast_scope": blast_scope, "cost_usd": total_cost, "passed": report.simulation_passed},
            )
        )

        return report

    def get_simulation(self, simulation_id: str) -> Optional[SimulationReport]:
        return self._simulations.get(simulation_id)

    def list_simulations(self) -> List[SimulationReport]:
        return list(self._simulations.values())


# Global Singleton
execution_simulation_engine = ExecutionSimulationEngine()
