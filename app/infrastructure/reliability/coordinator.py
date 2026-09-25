"""
Reliability Coordinator.

Coordinates resilience actions, evaluates system-level SLA/SLO/RTO/RPO margins,
and issues degradation and failover recommendations based on live telemetry.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

from app.infrastructure.reliability.models import (
    FaultDomain,
    ReliabilityState,
    ReliabilityTarget,
)
from app.infrastructure.reliability.state_machine import ReliabilityLifecycleStateMachine

logger = logging.getLogger("infrastructure.reliability.coordinator")


class ReliabilityAssessment(BaseModel):
    """Assessment of component or platform resilience."""
    target_id: str
    component_name: str
    state: ReliabilityState
    fault_domain: FaultDomain
    sla_compliance_percent: float
    rto_margin_seconds: float
    rpo_margin_seconds: float
    at_risk: bool
    recommended_action: Optional[str] = None
    assessed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ReliabilityCoordinator:
    """
    Evaluates live reliability targets, calculates SLA/RTO/RPO margins,
    and initiates resilience mitigations.
    """

    def __init__(self) -> None:
        self._targets: Dict[str, ReliabilityTarget] = {}
        self._state_machines: Dict[str, ReliabilityLifecycleStateMachine] = {}
        self._assessments: Dict[str, ReliabilityAssessment] = {}

    def register_target(self, target: ReliabilityTarget) -> None:
        self._targets[target.target_id] = target
        if target.target_id not in self._state_machines:
            self._state_machines[target.target_id] = ReliabilityLifecycleStateMachine(target.target_id)

    def get_state_machine(self, target_id: str) -> Optional[ReliabilityLifecycleStateMachine]:
        return self._state_machines.get(target_id)

    def assess_component(
        self,
        target_id: str,
        current_downtime_seconds: float = 0.0,
        current_lag_seconds: float = 0.0,
        measured_availability_percent: float = 100.0,
    ) -> ReliabilityAssessment:
        """
        Assess component health against its RTO, RPO, and SLA targets.
        """
        target = self._targets.get(target_id)
        if not target:
            raise KeyError(f"Reliability target '{target_id}' not registered.")

        sm = self._state_machines[target_id]
        rto_margin = target.rto.target_seconds - current_downtime_seconds
        rpo_margin = target.rpo.target_seconds - current_lag_seconds

        at_risk = False
        recommended_action = None

        if current_downtime_seconds > target.rto.max_acceptable_seconds:
            at_risk = True
            recommended_action = "TRIGGER_EMERGENCY_FAILOVER"
            if sm.can_transition_to(ReliabilityState.OUTAGE):
                sm.transition_to(ReliabilityState.OUTAGE, reason="RTO max acceptable threshold breached", trigger_source="coordinator")
        elif current_downtime_seconds > target.rto.target_seconds:
            at_risk = True
            recommended_action = "INITIATE_FAILOVER_PLANNING"
            if sm.can_transition_to(ReliabilityState.FAILING):
                sm.transition_to(ReliabilityState.FAILING, reason="RTO target threshold breached", trigger_source="coordinator")
        elif current_lag_seconds > target.rpo.target_seconds:
            at_risk = True
            recommended_action = "THROTTLE_INGESTION_AND_SYNC"
            if sm.can_transition_to(ReliabilityState.DEGRADED):
                sm.transition_to(ReliabilityState.DEGRADED, reason="RPO replication lag threshold breached", trigger_source="coordinator")
        elif sm.current_state in (ReliabilityState.DEGRADED, ReliabilityState.FAILING, ReliabilityState.RECOVERED):
            if current_downtime_seconds == 0.0 and current_lag_seconds < target.rpo.target_seconds:
                if sm.can_transition_to(ReliabilityState.OPTIMAL):
                    sm.transition_to(ReliabilityState.OPTIMAL, reason="Metrics returned to normal", trigger_source="coordinator")

        assessment = ReliabilityAssessment(
            target_id=target_id,
            component_name=target.component_name,
            state=sm.current_state,
            fault_domain=target.fault_domain,
            sla_compliance_percent=min(100.0, measured_availability_percent),
            rto_margin_seconds=rto_margin,
            rpo_margin_seconds=rpo_margin,
            at_risk=at_risk,
            recommended_action=recommended_action,
        )
        self._assessments[target_id] = assessment
        return assessment

    def get_all_assessments(self) -> List[ReliabilityAssessment]:
        return list(self._assessments.values())
