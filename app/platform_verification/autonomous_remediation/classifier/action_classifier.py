"""Recovery Action Classifier (3H.4.3.3).

Categorizes remediation operations into standardized Action Levels:
- Level 0: Informational (Telemetry, logs only)
- Level 1: Automatic Safe Actions (Pool refresh, cache purge, fallback activation)
- Level 2: Controlled Recovery Actions (Worker restarts, container scaling)
- Level 3: Human Approval Required Actions (Database restore, data migration, cluster rollback)
"""

from typing import Dict, Any
from ..domain.models import ActionLevel, RemediationRisk, ExecutionApproval
from ..domain.interfaces import IActionClassifier


class ActionClassifier(IActionClassifier):
    """Classifies remediation actions and assigns safety profiles."""

    def __init__(self):
        self._action_registry: Dict[str, Dict[str, Any]] = {
            "log_latency_telemetry_only": {
                "level": ActionLevel.LEVEL_0,
                "risk": RemediationRisk.LOW,
                "approval": ExecutionApproval.AUTOMATIC,
                "description": "Log performance metrics without modifying infrastructure",
            },
            "restart_connection_pool": {
                "level": ActionLevel.LEVEL_1,
                "risk": RemediationRisk.LOW,
                "approval": ExecutionApproval.AUTOMATIC,
                "description": "Safe reset of dormant or stale PostgreSQL pool connections",
            },
            "clear_expired_cache": {
                "level": ActionLevel.LEVEL_1,
                "risk": RemediationRisk.LOW,
                "approval": ExecutionApproval.AUTOMATIC,
                "description": "Purge expired Redis keys to reclaim working memory",
            },
            "activate_fallback_provider": {
                "level": ActionLevel.LEVEL_1,
                "risk": RemediationRisk.LOW,
                "approval": ExecutionApproval.AUTOMATIC,
                "description": "Reroute LLM queries to secondary fallback model (Claude/vLLM)",
            },
            "restart_worker_container": {
                "level": ActionLevel.LEVEL_2,
                "risk": RemediationRisk.MEDIUM,
                "approval": ExecutionApproval.AUTOMATIC,
                "description": "Restart unresponsive Celery worker pod with graceful drain",
            },
            "scale_queue_workers": {
                "level": ActionLevel.LEVEL_2,
                "risk": RemediationRisk.MEDIUM,
                "approval": ExecutionApproval.AUTOMATIC,
                "description": "Scale worker replicas to drain pending Redis job queue",
            },
            "restore_database_from_backup": {
                "level": ActionLevel.LEVEL_3,
                "risk": RemediationRisk.CRITICAL,
                "approval": ExecutionApproval.PENDING_HUMAN,
                "description": "Full database point-in-time restore requiring SRE approval",
            },
        }

    def classify_action(self, action_name: str) -> Dict[str, Any]:
        """Classifies a given action name into its level and safety parameters."""
        if action_name in self._action_registry:
            return self._action_registry[action_name]
        return {
            "level": ActionLevel.LEVEL_3,
            "risk": RemediationRisk.HIGH,
            "approval": ExecutionApproval.PENDING_HUMAN,
            "description": "Unregistered custom action requiring explicit approval",
        }
