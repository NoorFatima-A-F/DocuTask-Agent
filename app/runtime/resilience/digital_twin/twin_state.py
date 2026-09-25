"""
DocuTask Agent - Operational Digital Twin State Models
Phase 12: Autonomous Production Reliability & Operational Resilience (APRCORP+)
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Any, Optional
import time


class NodeHealthStatus(str, Enum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    FAILING = "FAILING"
    RECOVERING = "RECOVERING"
    ISOLATED = "ISOLATED"
    OFFLINE = "OFFLINE"


class ComponentCategory(str, Enum):
    PLANNER = "PLANNER"
    WORKER = "WORKER"
    MEMORY = "MEMORY"
    TRUTH_LEDGER = "TRUTH_LEDGER"
    EVIDENCE = "EVIDENCE"
    POLICY = "POLICY"
    STORAGE = "STORAGE"
    PROVIDER = "PROVIDER"
    INCIDENT_COMMANDER = "INCIDENT_COMMANDER"


@dataclass
class DigitalTwinNode:
    node_id: str
    name: str
    category: ComponentCategory
    health: NodeHealthStatus = NodeHealthStatus.HEALTHY
    latency_ms: float = 24.5
    error_rate: float = 0.00
    cpu_usage_pct: float = 12.4
    memory_usage_mb: float = 128.0
    active_connections: int = 4
    last_heartbeat_utc: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)
    replicas: int = 2
    invariants_passed: int = 14
    invariants_failed: int = 0


@dataclass
class DigitalTwinEdge:
    source_id: str
    target_id: str
    edge_type: str  # e.g., "CALLS", "READS_FROM", "WRITES_TO", "GOVERNS"
    latency_p95_ms: float = 18.0
    throughput_rps: float = 42.0
    error_rate: float = 0.00
    is_critical_path: bool = True
    circuit_breaker_open: bool = False


@dataclass
class OperationalTwinSnapshot:
    snapshot_id: str
    mission_id: Optional[str]
    timestamp_utc: float = field(default_factory=time.time)
    nodes: Dict[str, DigitalTwinNode] = field(default_factory=dict)
    edges: List[DigitalTwinEdge] = field(default_factory=list)
    overall_health_score: float = 99.4
    active_incidents_count: int = 0
    active_chaos_injections_count: int = 0
    sync_parity_pct: float = 99.98
