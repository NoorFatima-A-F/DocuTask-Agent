"""
DocuTask Agent - Incident Commander Models
Phase 12: Autonomous Production Reliability & Operational Resilience (APRCORP+)
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Any, Optional
import time


class IncidentSeverity(str, Enum):
    SEV1_CRITICAL = "SEV1_CRITICAL"
    SEV2_HIGH = "SEV2_HIGH"
    SEV3_MEDIUM = "SEV3_MEDIUM"
    SEV4_LOW = "SEV4_LOW"


class IncidentState(str, Enum):
    DETECTED = "DETECTED"
    TRIAGING = "TRIAGING"
    ISOLATING = "ISOLATING"
    RECOVERING = "RECOVERING"
    VERIFYING = "VERIFYING"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"


@dataclass
class IncidentTimelineEntry:
    entry_id: str
    timestamp_utc: float
    state: IncidentState
    message: str
    actor: str  # "AUTONOMOUS_INCIDENT_COMMANDER", "DIAGNOSTIC_SUBAGENT", "CHAOS_ORCHESTRATOR", "OPERATOR"
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class IncidentReport:
    incident_id: str
    title: str
    severity: IncidentSeverity
    current_state: IncidentState
    root_cause_node_id: str
    blast_radius_nodes: List[str]
    created_at_utc: float = field(default_factory=time.time)
    resolved_at_utc: Optional[float] = None
    timeline: List[IncidentTimelineEntry] = field(default_factory=list)
    mitigation_strategy_id: Optional[str] = None
    post_mortem_summary: Optional[str] = None
    invariants_compromised: List[str] = field(default_factory=list)
    forensic_snapshot_id: Optional[str] = None
