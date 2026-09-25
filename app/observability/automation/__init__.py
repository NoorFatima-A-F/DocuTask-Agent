"""SRE Automation & Self-Healing Package."""

from .actions import (
    AutoActionType,
    AutomationExecutionResult,
    SREActionExecutor,
)
from .framework import (
    SelfHealingRule,
    SREAutomationFramework,
)

__all__ = [
    "AutoActionType",
    "AutomationExecutionResult",
    "SREActionExecutor",
    "SelfHealingRule",
    "SREAutomationFramework",
]
