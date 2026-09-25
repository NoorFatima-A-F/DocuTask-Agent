"""
DocuTask Agent - Recovery Strategy Data Models
Phase 12: Autonomous Production Reliability & Operational Resilience (APRCORP+)
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Any
import time


class FallbackTriggerType(str, Enum):
    LLM_TIMEOUT = "LLM_TIMEOUT"
    OCR_SIGSEGV = "OCR_SIGSEGV"
    CACHE_UNAVAILABLE = "CACHE_UNAVAILABLE"
    MEMORY_CORRUPT = "MEMORY_CORRUPT"
    DAG_DEADLOCK = "DAG_DEADLOCK"
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"
    INVARIANT_BREACH = "INVARIANT_BREACH"


@dataclass
class RecoveryStrategy:
    strategy_id: str
    name: str
    trigger_type: FallbackTriggerType
    target_component: str
    action_type: str  # "MODEL_SWAP", "CIRCUIT_BREAKER", "WARM_RESTORE", "DAG_BRANCH_PRUNE", "RETRY_BACKOFF"
    success_rate_pct: float = 99.4
    mean_recovery_ms: float = 120.5
    cost_impact_usd: float = 0.0002
    description: str = ""
    fallback_chain: List[str] = field(default_factory=list)
    total_invocations: int = 0
    total_successes: int = 0
    is_active: bool = True
    parameters: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RecoveryExecutionResult:
    execution_id: str
    strategy_id: str
    trigger: FallbackTriggerType
    timestamp_utc: float = field(default_factory=time.time)
    duration_ms: float = 85.0
    status: str = "SUCCESS"  # "SUCCESS", "PARTIAL", "FAILED"
    details: Dict[str, Any] = field(default_factory=dict)
    state_parity_achieved_pct: float = 99.98
