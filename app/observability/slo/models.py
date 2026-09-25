"""Service Level Objective (SLO) and SLI Data Models."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum


class SLIType(str, Enum):
    AVAILABILITY = "AVAILABILITY"
    LATENCY = "LATENCY"
    ERROR_RATE = "ERROR_RATE"
    THROUGHPUT = "THROUGHPUT"
    RECOVERY_TIME = "RECOVERY_TIME"


@dataclass
class SLI:
    name: str
    sli_type: SLIType
    good_events_query: str
    total_events_query: str
    latency_threshold_ms: float = 500.0
    description: str = ""


@dataclass
class ServiceLevelObjective:
    slo_id: str
    name: str
    service_name: str
    target_percent: float = 99.9  # e.g. 99.9%
    sli: SLI = field(default_factory=lambda: SLI("default-sli", SLIType.AVAILABILITY, "success", "total"))
    window_days: int = 30
    tier: str = "TIER_1_CRITICAL"
    created_at: float = field(default_factory=time.time)
