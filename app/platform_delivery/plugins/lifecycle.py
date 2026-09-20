"""Plugin Lifecycle States & State Machine (Req 61)."""
from enum import Enum


class PluginLifecycleState(str, Enum):
    DISCOVERED = "DISCOVERED"
    REGISTERED = "REGISTERED"
    VALIDATED = "VALIDATED"
    APPROVED = "APPROVED"
    INSTALLED = "INSTALLED"
    ACTIVE = "ACTIVE"
    DISABLED = "DISABLED"
    REMOVED = "REMOVED"
