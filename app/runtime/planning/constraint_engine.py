"""Constraint Extraction & Verification Engine for DocuTask Autonomous Planning Platform.

Extracts, normalizes, and verifies hard and soft operational constraints across cost, latency, SLA,
token budgets, privacy/compliance levels, worker availability, and accuracy gates.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ConstraintType(str, Enum):
    BUDGET_USD = "BUDGET_USD"
    LATENCY_MS = "LATENCY_MS"
    SLA_DEADLINE_MS = "SLA_DEADLINE_MS"
    TOKEN_LIMIT = "TOKEN_LIMIT"
    ACCURACY_GATE = "ACCURACY_GATE"
    SECURITY_CLEARANCE = "SECURITY_CLEARANCE"
    CONCURRENCY_LIMIT = "CONCURRENCY_LIMIT"
    WORKER_AFFINITY = "WORKER_AFFINITY"
    PRIVACY_TIER = "PRIVACY_TIER"
    MEMORY_RETENTION_DAYS = "MEMORY_RETENTION_DAYS"


class ConstraintEnforcement(str, Enum):
    HARD = "HARD"  # Violating invalidates the candidate strategy
    SOFT = "SOFT"  # Violating incurs a parameterized utility penalty


class MissionConstraint(BaseModel):
    """Single operational constraint."""
    constraint_id: str = Field(default_factory=lambda: f"cnstr_{uuid.uuid4().hex[:8]}")
    name: str
    constraint_type: ConstraintType
    enforcement: ConstraintEnforcement = ConstraintEnforcement.HARD
    limit_value: float
    unit: str = ""
    comparator: str = Field(default="<=", description="'<=', '>=', '==', '<', '>'")
    penalty_weight: float = Field(default=1.0, ge=0.0, description="Utility penalty weight if soft constraint is breached")
    description: str = ""

    def is_satisfied(self, candidate_value: float) -> bool:
        if self.comparator == "<=":
            return candidate_value <= self.limit_value
        elif self.comparator == ">=":
            return candidate_value >= self.limit_value
        elif self.comparator == "==":
            return abs(candidate_value - self.limit_value) < 1e-6
        elif self.comparator == "<":
            return candidate_value < self.limit_value
        elif self.comparator == ">":
            return candidate_value > self.limit_value
        return False

    def compute_violation_margin(self, candidate_value: float) -> float:
        """Returns 0.0 if satisfied, else positive magnitude of breach."""
        if self.is_satisfied(candidate_value):
            return 0.0
        if self.comparator in ["<=", "<"]:
            return max(0.0, candidate_value - self.limit_value)
        elif self.comparator in [">=", ">"]:
            return max(0.0, self.limit_value - candidate_value)
        return abs(candidate_value - self.limit_value)


class MissionConstraintSet(BaseModel):
    """Aggregated constraint set for a mission."""
    constraint_set_id: str = Field(default_factory=lambda: f"cset_{uuid.uuid4().hex[:10]}")
    mission_id: str
    constraints: List[MissionConstraint] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def get_hard_constraints(self) -> List[MissionConstraint]:
        return [c for c in self.constraints if c.enforcement == ConstraintEnforcement.HARD]

    def get_soft_constraints(self) -> List[MissionConstraint]:
        return [c for c in self.constraints if c.enforcement == ConstraintEnforcement.SOFT]

    def validate_candidate(self, metrics: Dict[str, float]) -> tuple[bool, List[str], float]:
        """Validates metrics dictionary against all constraints.
        
        Returns:
            (is_valid, violation_reasons, total_soft_penalty)
        """
        violations: List[str] = []
        soft_penalty: float = 0.0

        for c in self.constraints:
            key = c.constraint_type.value.lower()
            if key not in metrics:
                continue
            val = metrics[key]
            if not c.is_satisfied(val):
                margin = c.compute_violation_margin(val)
                msg = f"Constraint '{c.name}' [{c.constraint_type.value}] breached: {val} {c.comparator} {c.limit_value} (margin={margin:.3f})"
                if c.enforcement == ConstraintEnforcement.HARD:
                    violations.append(msg)
                else:
                    penalty = margin * c.penalty_weight
                    soft_penalty += penalty
                    violations.append(f"[SOFT] {msg} (penalty={penalty:.3f})")

        is_valid = len([v for v in violations if not v.startswith("[SOFT]")]) == 0
        return is_valid, violations, soft_penalty


class ConstraintExtractionEngine:
    """Extracts, normalizes, and builds MissionConstraintSet from mission configuration and defaults."""

    DEFAULT_BUDGET_USD = 0.50
    DEFAULT_LATENCY_MS = 5000.0
    DEFAULT_SLA_MS = 10000.0
    DEFAULT_TOKEN_LIMIT = 50000.0
    DEFAULT_ACCURACY_GATE = 0.90
    DEFAULT_CONCURRENCY = 8.0

    def extract_constraints(
        self,
        mission_id: str,
        user_constraints: Optional[Dict[str, Any]] = None,
        sla_tier: str = "ENTERPRISE_P99",
    ) -> MissionConstraintSet:
        """Constructs complete constraint profile combining user overrides and enterprise defaults."""
        user_constraints = user_constraints or {}
        constraints: List[MissionConstraint] = []

        # 1. Budget Constraint (USD)
        budget = float(user_constraints.get("budget_usd", self.DEFAULT_BUDGET_USD))
        constraints.append(
            MissionConstraint(
                name="Maximum Cost Budget",
                constraint_type=ConstraintType.BUDGET_USD,
                enforcement=ConstraintEnforcement.HARD,
                limit_value=budget,
                unit="USD",
                comparator="<=",
                description="Hard ceiling for combined LLM tokens, OCR API, and compute fees",
            )
        )

        # 2. Latency Constraint (ms)
        latency = float(user_constraints.get("max_latency_ms", self.DEFAULT_LATENCY_MS))
        constraints.append(
            MissionConstraint(
                name="Max Execution Latency",
                constraint_type=ConstraintType.LATENCY_MS,
                enforcement=ConstraintEnforcement.SOFT if "strict_latency" not in user_constraints else ConstraintEnforcement.HARD,
                limit_value=latency,
                unit="ms",
                comparator="<=",
                penalty_weight=0.001,
                description="Target response latency before degradation alert",
            )
        )

        # 3. Hard SLA Deadline
        sla = float(user_constraints.get("sla_deadline_ms", self.DEFAULT_SLA_MS))
        constraints.append(
            MissionConstraint(
                name="SLA Hard Deadline",
                constraint_type=ConstraintType.SLA_DEADLINE_MS,
                enforcement=ConstraintEnforcement.HARD,
                limit_value=sla,
                unit="ms",
                comparator="<=",
                description="Contractual mission deadline before mission timeout",
            )
        )

        # 4. Token Consumption Ceiling
        tokens = float(user_constraints.get("max_tokens", self.DEFAULT_TOKEN_LIMIT))
        constraints.append(
            MissionConstraint(
                name="Token Budget Limit",
                constraint_type=ConstraintType.TOKEN_LIMIT,
                enforcement=ConstraintEnforcement.HARD,
                limit_value=tokens,
                unit="tokens",
                comparator="<=",
                description="Maximum total prompt + completion tokens allocated across all steps",
            )
        )

        # 5. Accuracy Gate Threshold
        acc = float(user_constraints.get("min_accuracy", self.DEFAULT_ACCURACY_GATE))
        constraints.append(
            MissionConstraint(
                name="Accuracy Verification Gate",
                constraint_type=ConstraintType.ACCURACY_GATE,
                enforcement=ConstraintEnforcement.HARD,
                limit_value=acc,
                unit="ratio",
                comparator=">=",
                description="Minimum acceptable deterministic validation accuracy score",
            )
        )

        # 6. Concurrency Limit
        concurrency = float(user_constraints.get("concurrency_limit", self.DEFAULT_CONCURRENCY))
        constraints.append(
            MissionConstraint(
                name="Worker Concurrency Ceiling",
                constraint_type=ConstraintType.CONCURRENCY_LIMIT,
                enforcement=ConstraintEnforcement.HARD,
                limit_value=concurrency,
                unit="workers",
                comparator="<=",
                description="Maximum parallel worker processes allowed for this mission",
            )
        )

        return MissionConstraintSet(mission_id=mission_id, constraints=constraints)
