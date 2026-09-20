"""
Configuration Lifecycle State Machine and Governance.
"""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional, Set
from app.shared_kernel.exceptions import InvariantViolationError


class ConfigurationLifecycleState(str, Enum):
    CREATED = "CREATED"
    VALIDATED = "VALIDATED"
    APPROVED = "APPROVED"
    VERSIONED = "VERSIONED"
    ACTIVATED = "ACTIVATED"
    DEPRECATED = "DEPRECATED"
    ARCHIVED = "ARCHIVED"


CONFIG_ALLOWED_TRANSITIONS: Dict[ConfigurationLifecycleState, Set[ConfigurationLifecycleState]] = {
    ConfigurationLifecycleState.CREATED: {ConfigurationLifecycleState.VALIDATED, ConfigurationLifecycleState.ARCHIVED},
    ConfigurationLifecycleState.VALIDATED: {ConfigurationLifecycleState.APPROVED, ConfigurationLifecycleState.CREATED, ConfigurationLifecycleState.ARCHIVED},
    ConfigurationLifecycleState.APPROVED: {ConfigurationLifecycleState.VERSIONED, ConfigurationLifecycleState.ARCHIVED},
    ConfigurationLifecycleState.VERSIONED: {ConfigurationLifecycleState.ACTIVATED, ConfigurationLifecycleState.DEPRECATED},
    ConfigurationLifecycleState.ACTIVATED: {ConfigurationLifecycleState.DEPRECATED, ConfigurationLifecycleState.ARCHIVED},
    ConfigurationLifecycleState.DEPRECATED: {ConfigurationLifecycleState.ARCHIVED, ConfigurationLifecycleState.ACTIVATED},
    ConfigurationLifecycleState.ARCHIVED: set()
}


@dataclass
class ConfigurationLifecycleRecord:
    config_id: str
    current_state: ConfigurationLifecycleState = ConfigurationLifecycleState.CREATED
    version: str = "1.0.0"
    approver: Optional[str] = None
    history: List[Dict[str, str]] = field(default_factory=list)

    def transition_to(self, target_state: ConfigurationLifecycleState, actor: str, reason: str = "") -> None:
        allowed = CONFIG_ALLOWED_TRANSITIONS.get(self.current_state, set())
        if target_state not in allowed:
            raise InvariantViolationError(
                f"Illegal configuration lifecycle transition: {self.current_state.value} -> {target_state.value}",
                details={"config_id": self.config_id, "current": self.current_state.value, "target": target_state.value}
            )
        self.history.append({
            "from_state": self.current_state.value,
            "to_state": target_state.value,
            "actor": actor,
            "reason": reason,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
        self.current_state = target_state
