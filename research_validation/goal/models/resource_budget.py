"""
Resource Budget Model
=====================
Specifies estimated and consumed computational resources across hardware and services.
"""

from dataclasses import dataclass, field
from typing import Dict


@dataclass(frozen=True)
class ResourceBudget:
    """Estimated resource allocation required for mission execution."""
    gpu_hours: float = 0.0
    cpu_hours: float = 1.0
    ram_gb: float = 4.0
    storage_gb: float = 10.0
    network_gb: float = 1.0
    energy_kwh: float = 0.5
    cost_usd: float = 5.0
    api_calls_count: int = 100
    custom_resources: Dict[str, float] = field(default_factory=dict)
