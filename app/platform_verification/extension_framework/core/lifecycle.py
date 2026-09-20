"""
Plugin Lifecycle Manager governing 10 discrete states with observable audit trails.
States: DISCOVERED -> VALIDATED -> REGISTERED -> INITIALIZED -> READY -> EXECUTING -> PAUSED -> DISABLED -> FAILED -> REMOVED
"""
from typing import Dict, List, Tuple
from datetime import datetime, timezone
from app.platform_verification.extension_framework.domain.models import PluginLifecycleState
from app.platform_verification.extension_framework.domain.interfaces import PluginLifecycleManagerInterface


class PluginLifecycleManager(PluginLifecycleManagerInterface):
    # Valid transitions map
    VALID_TRANSITIONS: Dict[PluginLifecycleState, List[PluginLifecycleState]] = {
        PluginLifecycleState.DISCOVERED: [PluginLifecycleState.VALIDATED, PluginLifecycleState.FAILED],
        PluginLifecycleState.VALIDATED: [PluginLifecycleState.REGISTERED, PluginLifecycleState.FAILED],
        PluginLifecycleState.REGISTERED: [PluginLifecycleState.INITIALIZED, PluginLifecycleState.DISABLED, PluginLifecycleState.REMOVED],
        PluginLifecycleState.INITIALIZED: [PluginLifecycleState.READY, PluginLifecycleState.FAILED, PluginLifecycleState.DISABLED],
        PluginLifecycleState.READY: [PluginLifecycleState.EXECUTING, PluginLifecycleState.PAUSED, PluginLifecycleState.DISABLED, PluginLifecycleState.REMOVED],
        PluginLifecycleState.EXECUTING: [PluginLifecycleState.READY, PluginLifecycleState.FAILED, PluginLifecycleState.DISABLED],
        PluginLifecycleState.PAUSED: [PluginLifecycleState.READY, PluginLifecycleState.DISABLED, PluginLifecycleState.REMOVED],
        PluginLifecycleState.DISABLED: [PluginLifecycleState.INITIALIZED, PluginLifecycleState.READY, PluginLifecycleState.REMOVED],
        PluginLifecycleState.FAILED: [PluginLifecycleState.VALIDATED, PluginLifecycleState.INITIALIZED, PluginLifecycleState.REMOVED, PluginLifecycleState.DISABLED],
        PluginLifecycleState.REMOVED: []
    }

    def __init__(self):
        self._states: Dict[str, PluginLifecycleState] = {}
        self._audit_log: List[Dict[str, str]] = []

    def set_initial_state(self, plugin_id: str, state: PluginLifecycleState = PluginLifecycleState.DISCOVERED) -> None:
        self._states[plugin_id] = state
        self._record_transition(plugin_id, None, state, "Initial state assignment")

    def transition_state(
        self,
        plugin_id: str,
        target_state: PluginLifecycleState,
        reason: str = ""
    ) -> PluginLifecycleState:
        current_state = self._states.get(plugin_id, PluginLifecycleState.DISCOVERED)
        allowed = self.VALID_TRANSITIONS.get(current_state, [])

        if target_state not in allowed and target_state != current_state:
            raise ValueError(
                f"Illegal state transition for plugin '{plugin_id}': cannot transition from {current_state.value} to {target_state.value}."
            )

        self._states[plugin_id] = target_state
        self._record_transition(plugin_id, current_state, target_state, reason)
        return target_state

    def get_state(self, plugin_id: str) -> PluginLifecycleState:
        return self._states.get(plugin_id, PluginLifecycleState.DISCOVERED)

    def _record_transition(self, plugin_id: str, from_state: Optional[PluginLifecycleState], to_state: PluginLifecycleState, reason: str):
        self._audit_log.append({
            "plugin_id": plugin_id,
            "from_state": from_state.value if from_state else "NONE",
            "to_state": to_state.value,
            "reason": reason,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })

    def get_audit_trail(self, plugin_id: Optional[str] = None) -> List[Dict[str, str]]:
        if plugin_id:
            return [log for log in self._audit_log if log["plugin_id"] == plugin_id]
        return list(self._audit_log)


plugin_lifecycle_manager = PluginLifecycleManager()
