from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional
import uuid
from .definitions import VerificationSpecification
from app.shared_kernel.exceptions import EnvironmentNotReadyError, InvariantViolationError

@dataclass(frozen=True)
class ExecutionStep:
    step_id: str
    step_name: str
    action_type: str
    dependencies: List[str] = field(default_factory=list)
    estimated_duration_seconds: float = 1.0
    payload: Dict[str, str] = field(default_factory=dict)

@dataclass(frozen=True)
class VerificationPlan:
    plan_id: str
    specification_id: str
    steps: List[ExecutionStep]
    estimated_total_duration_seconds: float
    risk_level: str = "LOW"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class VerificationPlanner:
    @staticmethod
    def plan_verification(spec: VerificationSpecification) -> VerificationPlan:
        step1 = ExecutionStep(
            step_id=f"step_{uuid.uuid4().hex[:8]}",
            step_name="prepare_dataset",
            action_type="DATASET_PROVISION",
            payload={"dataset_class": spec.dataset_class}
        )
        step2 = ExecutionStep(
            step_id=f"step_{uuid.uuid4().hex[:8]}",
            step_name="execute_workload",
            action_type="RUN_WORKLOAD",
            dependencies=[step1.step_id],
            payload={"subsystem": spec.target_subsystem, "version": spec.target_version}
        )
        step3 = ExecutionStep(
            step_id=f"step_{uuid.uuid4().hex[:8]}",
            step_name="extract_metrics",
            action_type="METRICS_EXTRACTION",
            dependencies=[step2.step_id],
            payload={"metrics": ",".join(spec.required_metrics)}
        )
        step4 = ExecutionStep(
            step_id=f"step_{uuid.uuid4().hex[:8]}",
            step_name="evaluate_quality_gates",
            action_type="GATE_EVALUATION",
            dependencies=[step3.step_id]
        )

        steps = [step1, step2, step3, step4]
        total_duration = sum(s.estimated_duration_seconds for s in steps)

        return VerificationPlan(
            plan_id=f"vplan_{uuid.uuid4().hex[:12]}",
            specification_id=spec.specification_id,
            steps=steps,
            estimated_total_duration_seconds=total_duration,
            risk_level="LOW" if spec.environment_tier == "staging" else "MEDIUM"
        )

    @staticmethod
    def validate_plan_readiness(plan: VerificationPlan, environment_ready: bool = True, dataset_ready: bool = True) -> bool:
        if not environment_ready:
            raise EnvironmentNotReadyError("Target execution environment probe failed.")
        if not dataset_ready:
            raise InvariantViolationError("Required dataset is not available in CAS storage.")
        return True
