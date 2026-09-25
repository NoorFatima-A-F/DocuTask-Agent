"""
Runtime Feature Flags.
Enables dynamic feature gating across Reflection, Recovery, Multi-Agent, and v2 engines without redeployment.
"""

from typing import Dict
from pydantic import BaseModel, Field


class RuntimeFeatureFlags(BaseModel):
    """Dynamic operational toggles for platform runtime capabilities."""
    enable_reflection: bool = True
    enable_recovery: bool = True
    enable_multi_agent: bool = True
    enable_experimental_planner: bool = False
    enable_planner_v2: bool = False
    enable_execution_v2: bool = False
    custom_flags: Dict[str, bool] = Field(default_factory=dict)

    def is_enabled(self, flag_name: str) -> bool:
        """Evaluates whether a feature flag is currently active."""
        if hasattr(self, flag_name):
            return bool(getattr(self, flag_name))
        return bool(self.custom_flags.get(flag_name, False))

    def set_flag(self, flag_name: str, value: bool) -> "RuntimeFeatureFlags":
        """Returns updated feature flags instance with modified toggle."""
        if hasattr(self, flag_name) and flag_name != "custom_flags":
            return self.model_copy(update={flag_name: value})
        new_custom = dict(self.custom_flags)
        new_custom[flag_name] = value
        return self.model_copy(update={"custom_flags": new_custom})

    model_config = {"frozen": True}
