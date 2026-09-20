"""
Execution Strategy Model (Phase 87C)
===================================
Defines runtime constraints, checkpointing frequencies, retry budgets,
and statistical convergence thresholds for planned experiment DAGs.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class TargetHardware(str, Enum):
    CPU_STANDARD = "CPU_STANDARD"
    GPU_T4 = "GPU_T4"
    GPU_A100 = "GPU_A100"
    AUTO = "AUTO"


@dataclass(frozen=True)
class AdaptiveExecutionStrategy:
    """Execution parameters configured dynamically for an experiment plan."""
    target_hardware: TargetHardware
    max_concurrency: int
    max_retries_per_stage: int
    checkpoint_cadence_seconds: float
    confidence_target: float          # e.g., 0.95
    max_ci_width: float                # e.g., 0.05
    early_stopping_patience_steps: int
    timeout_seconds: float
    parameters: Dict[str, Any] = field(default_factory=dict)
