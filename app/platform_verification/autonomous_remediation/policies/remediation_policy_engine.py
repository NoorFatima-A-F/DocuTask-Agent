"""Remediation Policy Engine (3H.4.3.2).

Maps operational failure conditions to approved remediation actions, action levels,
risk classifications, execution limits, and safety cooldowns.
"""

from typing import Dict, List, Optional
from ..domain.models import (
    RemediationPolicyItem,
    RemediationPolicyReport,
    ActionLevel,
    RemediationRisk,
)
from ..domain.interfaces import IRemediationPolicyEngine


class RemediationPolicyEngine(IRemediationPolicyEngine):
    """Manages and evaluates registered remediation policies."""

    def __init__(self):
        self._policies: List[RemediationPolicyItem] = [
            # Level 0 - Informational
            RemediationPolicyItem(
                condition="p95_latency_slight_increase",
                target_component="api_gateway",
                action="log_latency_telemetry_only",
                action_level=ActionLevel.LEVEL_0,
                risk=RemediationRisk.LOW,
                max_attempts=0,
                cooldown_seconds=0,
                blast_radius="single_instance",
                requires_preconditions=False,
                rollback_supported=False,
            ),
            # Level 1 - Auto Safe Actions
            RemediationPolicyItem(
                condition="database_connection_exhausted",
                target_component="postgresql_pool",
                action="restart_connection_pool",
                action_level=ActionLevel.LEVEL_1,
                risk=RemediationRisk.LOW,
                max_attempts=3,
                cooldown_seconds=300,
                blast_radius="single_instance",
                requires_preconditions=True,
                rollback_supported=True,
            ),
            RemediationPolicyItem(
                condition="cache_memory_saturation",
                target_component="redis_cache",
                action="clear_expired_cache",
                action_level=ActionLevel.LEVEL_1,
                risk=RemediationRisk.LOW,
                max_attempts=3,
                cooldown_seconds=180,
                blast_radius="single_instance",
                requires_preconditions=True,
                rollback_supported=True,
            ),
            RemediationPolicyItem(
                condition="gemini_api_503_outage",
                target_component="ai_provider_router",
                action="activate_fallback_provider",
                action_level=ActionLevel.LEVEL_1,
                risk=RemediationRisk.LOW,
                max_attempts=1,
                cooldown_seconds=60,
                blast_radius="local_service",
                requires_preconditions=True,
                rollback_supported=True,
            ),
            # Level 2 - Controlled Recovery Actions
            RemediationPolicyItem(
                condition="worker_heartbeat_missing",
                target_component="celery_worker",
                action="restart_worker_container",
                action_level=ActionLevel.LEVEL_2,
                risk=RemediationRisk.MEDIUM,
                max_attempts=3,
                cooldown_seconds=300,
                blast_radius="single_instance",
                requires_preconditions=True,
                rollback_supported=True,
            ),
            RemediationPolicyItem(
                condition="redis_queue_backlog",
                target_component="queue_fleet",
                action="scale_queue_workers",
                action_level=ActionLevel.LEVEL_2,
                risk=RemediationRisk.MEDIUM,
                max_attempts=2,
                cooldown_seconds=600,
                blast_radius="local_service",
                requires_preconditions=True,
                rollback_supported=True,
            ),
            # Level 3 - Human Approval Required Actions
            RemediationPolicyItem(
                condition="database_corruption_detected",
                target_component="database_cluster",
                action="restore_database_from_backup",
                action_level=ActionLevel.LEVEL_3,
                risk=RemediationRisk.CRITICAL,
                max_attempts=1,
                cooldown_seconds=3600,
                blast_radius="fleet",
                requires_preconditions=True,
                rollback_supported=True,
            ),
        ]

    def find_policy_for_condition(self, condition: str) -> Optional[RemediationPolicyItem]:
        """Finds matching remediation policy by failure condition name."""
        for p in self._policies:
            if p.condition == condition:
                return p
        return None

    def get_policy_report(self) -> RemediationPolicyReport:
        """Generates comprehensive policy inventory report."""
        l0 = sum(1 for p in self._policies if p.action_level == ActionLevel.LEVEL_0)
        l1 = sum(1 for p in self._policies if p.action_level == ActionLevel.LEVEL_1)
        l2 = sum(1 for p in self._policies if p.action_level == ActionLevel.LEVEL_2)
        l3 = sum(1 for p in self._policies if p.action_level == ActionLevel.LEVEL_3)

        return RemediationPolicyReport(
            total_policies=len(self._policies),
            level_0_count=l0,
            level_1_count=l1,
            level_2_count=l2,
            level_3_count=l3,
            policies=self._policies,
            status="PASS",
        )
