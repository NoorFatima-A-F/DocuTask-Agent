"""
Goal Constraints Model
======================
Specifies resource budgets, execution limits, privacy rules, and governance restrictions.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from research_validation.goal.constants import (
    DEFAULT_MAX_RUNTIME_HOURS, DEFAULT_MAX_GPU_HOURS, DEFAULT_MAX_CPU_HOURS,
    DEFAULT_MAX_RAM_GB, DEFAULT_MAX_STORAGE_GB, DEFAULT_MAX_COST_USD,
    DEFAULT_MAX_CONCURRENCY, DEFAULT_MAX_RETRIES
)


@dataclass(frozen=True)
class GoalConstraints:
    """Immutable resource and policy constraints bounding an autonomous goal."""
    max_runtime_hours: float = DEFAULT_MAX_RUNTIME_HOURS
    max_gpu_hours: float = DEFAULT_MAX_GPU_HOURS
    max_cpu_hours: float = DEFAULT_MAX_CPU_HOURS
    max_ram_gb: float = DEFAULT_MAX_RAM_GB
    max_storage_gb: float = DEFAULT_MAX_STORAGE_GB
    max_cost_usd: float = DEFAULT_MAX_COST_USD
    max_concurrency: int = DEFAULT_MAX_CONCURRENCY
    max_retries: int = DEFAULT_MAX_RETRIES
    privacy_constraints: List[str] = field(default_factory=list)
    dataset_restrictions: List[str] = field(default_factory=list)
    security_restrictions: List[str] = field(default_factory=list)
    governance_constraints: List[str] = field(default_factory=list)
    custom_limits: Dict[str, Any] = field(default_factory=dict)
