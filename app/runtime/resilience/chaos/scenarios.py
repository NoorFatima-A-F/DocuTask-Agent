"""
DocuTask Agent - Chaos Scenarios & Injection Definitions
Phase 12: Autonomous Production Reliability & Operational Resilience (APRCORP+)
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Any, Optional


class ChaosFaultType(str, Enum):
    GEMINI_TIMEOUT = "GEMINI_TIMEOUT"
    PROVIDER_LATENCY_SPIKE = "PROVIDER_LATENCY_SPIKE"
    OCR_ENGINE_CRASH = "OCR_ENGINE_CRASH"
    REDIS_CONNECTION_DROP = "REDIS_CONNECTION_DROP"
    MEMORY_CORRUPTION = "MEMORY_CORRUPTION"
    WORKER_NODE_PANIC = "WORKER_NODE_PANIC"
    POLICY_DRIFT_ANOMALY = "POLICY_DRIFT_ANOMALY"
    NETWORK_PARTITION = "NETWORK_PARTITION"
    TRUTH_LEDGER_MUTATION_ATTACK = "TRUTH_LEDGER_MUTATION_ATTACK"
    TOKEN_EXHAUSTION = "TOKEN_EXHAUSTION"


class InjectionStatus(str, Enum):
    SCHEDULED = "SCHEDULED"
    ACTIVE = "ACTIVE"
    CONTAINED = "CONTAINED"
    HEALED = "HEALED"
    ROLLED_BACK = "ROLLED_BACK"
    FAILED = "FAILED"


@dataclass
class ChaosScenario:
    scenario_id: str
    name: str
    fault_type: ChaosFaultType
    target_node_id: str
    target_component_name: str
    description: str
    severity: str  # "LOW", "MEDIUM", "HIGH", "CRITICAL"
    parameters: Dict[str, Any] = field(default_factory=dict)
    expected_recovery_strategy: str = "AUTONOMOUS_FALLBACK"
    blast_radius_nodes: List[str] = field(default_factory=list)
    injected_at_utc: Optional[float] = None
    resolved_at_utc: Optional[float] = None
    status: InjectionStatus = InjectionStatus.SCHEDULED
    recovery_latency_ms: Optional[float] = None
    mitigation_notes: Optional[str] = None
