"""
DocuTask Agent - Runtime Invariant Models & Matrix
Phase 12: Autonomous Production Reliability & Operational Resilience (APRCORP+)
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
import time


class InvariantSeverity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"


class InvariantStatus(str, Enum):
    PASSING = "PASSING"
    VIOLATED = "VIOLATED"
    WARNED = "WARNED"


@dataclass
class RuntimeInvariant:
    invariant_id: str
    name: str
    formal_definition: str
    severity: InvariantSeverity
    category: str  # "FINANCIAL", "CRYPTOGRAPHIC", "TOPOLOGICAL", "INTEGRITY", "TEMPORAL"
    status: InvariantStatus = InvariantStatus.PASSING
    total_checks: int = 0
    violations_count: int = 0
    last_checked_utc: float = field(default_factory=time.time)
    last_violation_details: Optional[str] = None
    assertion_lambda_name: str = "check_truth_monotonicity"
