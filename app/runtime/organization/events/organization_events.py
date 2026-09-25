"""
Phase 13.14 - Organizational Domain Events & Invariant Models
Autonomous AI Organization, Multi-Agent Enterprise Governance & Mission Execution Platform (AAO-MAGEMEP)
"""

from __future__ import annotations
import time
import uuid
from enum import Enum
from typing import Dict, List, Any, Optional, Callable
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class OrganizationState(str, Enum):
    CREATED = "CREATED"
    PLANNING = "PLANNING"
    EXECUTING = "EXECUTING"
    OPTIMIZING = "OPTIMIZING"
    PAUSED = "PAUSED"
    FAILED = "FAILED"
    COMPLETED = "COMPLETED"
    ARCHIVED = "ARCHIVED"


class MissionPriority(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    EXPERIMENTAL = "EXPERIMENTAL"


class AgentRole(str, Enum):
    CEO_AGENT = "CEO_AGENT"
    CTO_AGENT = "CTO_AGENT"
    RESEARCH_AGENT = "RESEARCH_AGENT"
    ENGINEERING_AGENT = "ENGINEERING_AGENT"
    ANALYST_AGENT = "ANALYST_AGENT"
    SECURITY_AGENT = "SECURITY_AGENT"
    FINANCE_AGENT = "FINANCE_AGENT"
    OPERATIONS_AGENT = "OPERATIONS_AGENT"
    CUSTOMER_AGENT = "CUSTOMER_AGENT"


class DecisionConfidence(str, Enum):
    VERY_LOW = "VERY_LOW"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    VERY_HIGH = "VERY_HIGH"


class PerformanceState(str, Enum):
    EXCEEDING = "EXCEEDING"
    OPTIMAL = "OPTIMAL"
    WARNING = "WARNING"
    DEGRADED = "DEGRADED"
    FAILED = "FAILED"


class ConflictStatus(str, Enum):
    DETECTED = "DETECTED"
    IN_NEGOTIATION = "IN_NEGOTIATION"
    RESOLVED = "RESOLVED"
    ESCALATED = "ESCALATED"
    DEADLOCKED = "DEADLOCKED"


class GovernanceVerdict(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    CONDITIONAL = "CONDITIONAL"
    ESCALATED_TO_HUMAN = "ESCALATED_TO_HUMAN"


class SimulationType(str, Enum):
    DIGITAL_TWIN = "DIGITAL_TWIN"
    MONTE_CARLO = "MONTE_CARLO"
    HISTORICAL_REPLAY = "HISTORICAL_REPLAY"
    CHAOS_STRESS = "CHAOS_STRESS"


# ---------------------------------------------------------------------------
# Base Domain Event
# ---------------------------------------------------------------------------

class OrganizationDomainEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: f"org_evt_{uuid.uuid4().hex[:10]}")
    event_type: str
    organization_id: str = "org_enterprise_root"
    timestamp_utc: float = Field(default_factory=time.time)
    actor_agent_role: AgentRole = AgentRole.CEO_AGENT
    confidence: DecisionConfidence = DecisionConfidence.HIGH
    payload: Dict[str, Any] = Field(default_factory=dict)
    causality_link_id: Optional[str] = None


# ---------------------------------------------------------------------------
# 40+ Specific Domain Events
# ---------------------------------------------------------------------------

class MissionCreated(OrganizationDomainEvent):
    event_type: str = "MissionCreated"

class MissionValidated(OrganizationDomainEvent):
    event_type: str = "MissionValidated"

class StrategyGenerated(OrganizationDomainEvent):
    event_type: str = "StrategyGenerated"

class OrganizationDesigned(OrganizationDomainEvent):
    event_type: str = "OrganizationDesigned"

class DepartmentCreated(OrganizationDomainEvent):
    event_type: str = "DepartmentCreated"

class AgentAssigned(OrganizationDomainEvent):
    event_type: str = "AgentAssigned"

class AgentCapabilityExpanded(OrganizationDomainEvent):
    event_type: str = "AgentCapabilityExpanded"

class ProjectCreated(OrganizationDomainEvent):
    event_type: str = "ProjectCreated"

class ProjectCompleted(OrganizationDomainEvent):
    event_type: str = "ProjectCompleted"

class ResourceAllocated(OrganizationDomainEvent):
    event_type: str = "ResourceAllocated"

class BudgetOptimized(OrganizationDomainEvent):
    event_type: str = "BudgetOptimized"

class DecisionGenerated(OrganizationDomainEvent):
    event_type: str = "DecisionGenerated"

class DecisionApproved(OrganizationDomainEvent):
    event_type: str = "DecisionApproved"

class DecisionRejected(OrganizationDomainEvent):
    event_type: str = "DecisionRejected"

class ConflictDetected(OrganizationDomainEvent):
    event_type: str = "ConflictDetected"

class ConflictResolved(OrganizationDomainEvent):
    event_type: str = "ConflictResolved"

class PerformanceMeasured(OrganizationDomainEvent):
    event_type: str = "PerformanceMeasured"

class PerformanceRegressionDetected(OrganizationDomainEvent):
    event_type: str = "PerformanceRegressionDetected"

class ObjectiveCompleted(OrganizationDomainEvent):
    event_type: str = "ObjectiveCompleted"

class ObjectiveFailed(OrganizationDomainEvent):
    event_type: str = "ObjectiveFailed"

class OrganizationOptimized(OrganizationDomainEvent):
    event_type: str = "OrganizationOptimized"

class AgentRetired(OrganizationDomainEvent):
    event_type: str = "AgentRetired"

class AgentPromoted(OrganizationDomainEvent):
    event_type: str = "AgentPromoted"

class TeamMerged(OrganizationDomainEvent):
    event_type: str = "TeamMerged"

class TeamSplit(OrganizationDomainEvent):
    event_type: str = "TeamSplit"

class KnowledgeTransferred(OrganizationDomainEvent):
    event_type: str = "KnowledgeTransferred"

class StrategyUpdated(OrganizationDomainEvent):
    event_type: str = "StrategyUpdated"

class ROIImproved(OrganizationDomainEvent):
    event_type: str = "ROIImproved"

class CostReduced(OrganizationDomainEvent):
    event_type: str = "CostReduced"

class RiskDetected(OrganizationDomainEvent):
    event_type: str = "RiskDetected"

class SimulationStarted(OrganizationDomainEvent):
    event_type: str = "SimulationStarted"

class SimulationCompleted(OrganizationDomainEvent):
    event_type: str = "SimulationCompleted"

class GovernanceApproved(OrganizationDomainEvent):
    event_type: str = "GovernanceApproved"

class GovernanceRejected(OrganizationDomainEvent):
    event_type: str = "GovernanceRejected"

class OrganizationPaused(OrganizationDomainEvent):
    event_type: str = "OrganizationPaused"

class OrganizationResumed(OrganizationDomainEvent):
    event_type: str = "OrganizationResumed"

class LearningCycleCompleted(OrganizationDomainEvent):
    event_type: str = "LearningCycleCompleted"

class OrganizationEvolutionTriggered(OrganizationDomainEvent):
    event_type: str = "OrganizationEvolutionTriggered"


# ---------------------------------------------------------------------------
# Organization Event Bus
# ---------------------------------------------------------------------------

class OrganizationEventBus:
    """In-memory typed event bus for organizational runtime events."""

    def __init__(self) -> None:
        self._handlers: Dict[str, List[Callable[[OrganizationDomainEvent], Any]]] = {}
        self._history: List[OrganizationDomainEvent] = []

    def subscribe(self, event_type: str, handler: Callable[[OrganizationDomainEvent], Any]) -> None:
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    def publish(self, event: OrganizationDomainEvent) -> None:
        self._history.append(event)
        if len(self._history) > 2000:
            self._history = self._history[-2000:]
        for handler in self._handlers.get(event.event_type, []):
            try:
                handler(event)
            except Exception:
                pass
        for handler in self._handlers.get("*", []):
            try:
                handler(event)
            except Exception:
                pass

    def get_history(self, limit: int = 100, event_type: Optional[str] = None) -> List[Dict[str, Any]]:
        events = self._history
        if event_type:
            events = [e for e in events if e.event_type == event_type]
        return [e.model_dump() for e in events[-limit:]]

    def clear(self) -> None:
        self._history.clear()


# Global Singleton Event Bus
org_event_bus = OrganizationEventBus()
