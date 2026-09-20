"""
Tool Ecosystem Policies.
Defines SelectionPolicy, FallbackPolicy, RetryPolicy, HealthPolicy, RegistrationPolicy, ReplacementPolicy, and VersionPolicy.
"""

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class SelectionStrategyEnum(str, Enum):
    """Tool selection strategy enum."""
    HIGHEST_CONFIDENCE = "HIGHEST_CONFIDENCE"
    LOWEST_COST = "LOWEST_COST"
    LOWEST_LATENCY = "LOWEST_LATENCY"
    HYBRID_WEIGHTED = "HYBRID_WEIGHTED"
    RULE_BASED = "RULE_BASED"
    FALLBACK = "FALLBACK"


class SelectionPolicy(BaseModel):
    """Policy governing tool candidate selection."""
    strategy: SelectionStrategyEnum = Field(default=SelectionStrategyEnum.HYBRID_WEIGHTED)
    confidence_weight: float = Field(default=0.4, ge=0.0, le=1.0)
    cost_weight: float = Field(default=0.3, ge=0.0, le=1.0)
    latency_weight: float = Field(default=0.3, ge=0.0, le=1.0)
    model_config = {"frozen": True}


class FallbackPolicy(BaseModel):
    """Fallback tool selection policy."""
    enable_fallback: bool = Field(default=True)
    fallback_tool_ids: List[str] = Field(default_factory=list)
    model_config = {"frozen": True}


class HealthPolicy(BaseModel):
    """Tool health check policy."""
    check_interval_seconds: float = Field(default=30.0, gt=0.0)
    unhealthy_threshold_failures: int = Field(default=3, ge=1)
    auto_deregister_on_failure: bool = Field(default=False)
    model_config = {"frozen": True}


class RegistrationPolicy(BaseModel):
    """Tool registration validation policy."""
    allow_overwrite: bool = Field(default=False)
    require_health_check: bool = Field(default=True)
    model_config = {"frozen": True}
