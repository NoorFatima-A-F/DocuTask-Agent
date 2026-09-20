"""
Reliability Manager.

Central manager providing lifecycle control, policy assignment, target tracking,
and platform resilience status reporting.
"""

from __future__ import annotations

import logging
from typing import Dict, List, Optional

from app.infrastructure.reliability.coordinator import ReliabilityAssessment, ReliabilityCoordinator
from app.infrastructure.reliability.models import (
    FaultDomain,
    ReliabilityPolicy,
    ReliabilityState,
    ReliabilityTarget,
    RTOObjective,
    RPOObjective,
)
from app.infrastructure.reliability.policies import ReliabilityPolicyEngine
from app.infrastructure.reliability.state_machine import ReliabilityLifecycleStateMachine

logger = logging.getLogger("infrastructure.reliability.manager")


class ReliabilityManager:
    """
    Unified manager for platform reliability policies, targets, and coordinator state.
    """

    def __init__(self) -> None:
        self.coordinator = ReliabilityCoordinator()
        self.policy_engine = ReliabilityPolicyEngine()
        self._component_policies: Dict[str, str] = {}  # target_id -> policy_id

    def register_target(
        self,
        target_id: str,
        component_name: str,
        fault_domain: FaultDomain = FaultDomain.SERVICE,
        availability_sla_percent: float = 99.99,
        rto_seconds: float = 300.0,
        rpo_seconds: float = 60.0,
        policy: Optional[ReliabilityPolicy] = None,
    ) -> ReliabilityTarget:
        target = ReliabilityTarget(
            target_id=target_id,
            component_name=component_name,
            fault_domain=fault_domain,
            availability_sla_percent=availability_sla_percent,
            rto=RTOObjective(target_seconds=rto_seconds),
            rpo=RPOObjective(target_seconds=rpo_seconds),
        )
        self.coordinator.register_target(target)
        if policy:
            self.policy_engine.register_policy(policy)
            self._component_policies[target_id] = policy.policy_id
        return target

    def bind_policy(self, target_id: str, policy: ReliabilityPolicy) -> None:
        self.policy_engine.register_policy(policy)
        self._component_policies[target_id] = policy.policy_id

    def get_policy_for_component(self, target_id: str) -> Optional[ReliabilityPolicy]:
        policy_id = self._component_policies.get(target_id)
        if policy_id:
            return self.policy_engine.get_policy(policy_id)
        return None

    def record_transition(
        self,
        target_id: str,
        to_state: ReliabilityState,
        reason: str,
        trigger_source: str = "manager",
    ) -> None:
        sm = self.coordinator.get_state_machine(target_id)
        if sm:
            sm.transition_to(to_state, reason=reason, trigger_source=trigger_source)

    def get_component_state(self, target_id: str) -> Optional[ReliabilityState]:
        sm = self.coordinator.get_state_machine(target_id)
        return sm.current_state if sm else None

    def get_resilience_summary(self) -> Dict[str, int]:
        """Return counts of targets across reliability states."""
        counts = {s.value: 0 for s in ReliabilityState}
        for target_id in self.coordinator._targets:
            sm = self.coordinator.get_state_machine(target_id)
            if sm:
                counts[sm.current_state.value] += 1
        return counts
