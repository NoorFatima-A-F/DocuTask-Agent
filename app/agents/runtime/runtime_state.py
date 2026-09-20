"""
Runtime State Model.
Represents the live operational state of the Platform Runtime Kernel.
"""

from datetime import datetime, timezone
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field
from app.agents.runtime.runtime_lifecycle import RuntimeLifecycleState, RuntimeLifecycleStateMachine


class RuntimeState(BaseModel):
    """Observable operational state of the running platform kernel."""
    lifecycle_state: RuntimeLifecycleState = Field(default=RuntimeLifecycleState.OFFLINE)
    boot_timestamp: Optional[datetime] = None
    registered_services_count: int = 0
    active_modules_count: int = 0
    active_plugins_count: int = 0
    active_sessions_count: int = 0
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def transition_to(self, new_state: RuntimeLifecycleState) -> "RuntimeState":
        """Transitions to target state enforcing state machine rules."""
        RuntimeLifecycleStateMachine.validate_transition(self.lifecycle_state, new_state)
        update_dict: Dict[str, Any] = {"lifecycle_state": new_state}
        if new_state == RuntimeLifecycleState.BOOTING and not self.boot_timestamp:
            update_dict["boot_timestamp"] = datetime.now(timezone.utc)
        return self.model_copy(update=update_dict)

    model_config = {"frozen": True}
