"""
Scientific Experiment Engine - Experiment Registry
Tracks active, paused, converged, and promoted scientific experiments.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict, field
import uuid
import time


@dataclass
class ExperimentDefinition:
    experiment_id: str
    name: str
    description: str
    hypothesis: str
    control_policy: str
    treatment_policy: str
    sample_size_target: int
    traffic_allocation_pct: float
    status: str  # DRAFT | RUNNING | CONVERGED | PROMOTED | ROLLED_BACK
    control_samples: List[float] = field(default_factory=list)
    treatment_samples: List[float] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)
    concluded_at: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "experiment_id": self.experiment_id,
            "name": self.name,
            "description": self.description,
            "hypothesis": self.hypothesis,
            "control_policy": self.control_policy,
            "treatment_policy": self.treatment_policy,
            "sample_size_target": self.sample_size_target,
            "traffic_allocation_pct": self.traffic_allocation_pct,
            "status": self.status,
            "control_count": len(self.control_samples),
            "treatment_count": len(self.treatment_samples),
            "created_at": self.created_at,
            "concluded_at": self.concluded_at,
        }


class ExperimentRegistry:
    """In-memory persistent registry for scientific experiments."""

    def __init__(self):
        self.experiments: Dict[str, ExperimentDefinition] = {}
        self._seed_canonical_experiments()

    def _seed_canonical_experiments(self):
        exp1 = ExperimentDefinition(
            experiment_id="EXP-2026-001",
            name="Bayesian Cost Weight Prior Optimization",
            description="Evaluates whether shifting Pareto cost preference weight from 0.30 to 0.40 maintains >95% accuracy while cutting P95 cost by 18%.",
            hypothesis="Higher cost penalty reduces reliance on Gemini Pro without degrading SLA compliance.",
            control_policy="v4.2-pareto-default",
            treatment_policy="v5.0-bayesian-cost-optimized",
            sample_size_target=500,
            traffic_allocation_pct=20.0,
            status="RUNNING",
            control_samples=[0.88 + (i % 10) * 0.01 for i in range(120)],
            treatment_samples=[0.92 + (i % 8) * 0.008 for i in range(115)],
        )
        self.experiments[exp1.experiment_id] = exp1

    def create_experiment(
        self,
        name: str,
        hypothesis: str,
        control_policy: str,
        treatment_policy: str,
        sample_size_target: int = 500,
        traffic_allocation_pct: float = 15.0,
        description: str = "",
    ) -> ExperimentDefinition:
        exp_id = f"EXP-2026-{uuid.uuid4().hex[:4].upper()}"
        exp = ExperimentDefinition(
            experiment_id=exp_id,
            name=name,
            description=description,
            hypothesis=hypothesis,
            control_policy=control_policy,
            treatment_policy=treatment_policy,
            sample_size_target=sample_size_target,
            traffic_allocation_pct=traffic_allocation_pct,
            status="RUNNING",
        )
        self.experiments[exp_id] = exp
        return exp

    def list_experiments(self) -> List[ExperimentDefinition]:
        return list(self.experiments.values())

    def get_experiment(self, exp_id: str) -> Optional[ExperimentDefinition]:
        return self.experiments.get(exp_id)
