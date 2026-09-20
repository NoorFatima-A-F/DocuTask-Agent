"""
Phase 13.12: Autonomous Scientific Discovery, Hypothesis Generation & Continuous Knowledge Evolution Platform (ASD-HGCKEP)
Domain Events, Enums, and Event Bus.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Dict, List, Optional
import uuid


class EvidenceStrength(str, Enum):
    EMPIRICAL_DEFINITIVE = "EMPIRICAL_DEFINITIVE"
    STATISTICALLY_SIGNIFICANT = "STATISTICALLY_SIGNIFICANT"
    CORROBORATING = "CORROBORATING"
    PRELIMINARY = "PRELIMINARY"
    ANECDOTAL = "ANECDOTAL"
    CONTRADICTORY = "CONTRADICTORY"
    VERY_STRONG = "VERY_STRONG"
    STRONG = "STRONG"
    MODERATE = "MODERATE"
    WEAK = "WEAK"


class HypothesisStatus(str, Enum):
    PROPOSED = "PROPOSED"
    EXPERIMENTING = "EXPERIMENTING"
    CORROBORATED = "CORROBORATED"
    VALIDATED_LAW = "VALIDATED_LAW"
    FALSIFIED = "FALSIFIED"
    RETIRED = "RETIRED"
    REVIVED = "REVIVED"
    TESTING = "TESTING"
    CONFIRMED = "CONFIRMED"
    REJECTED = "REJECTED"


class ResearchPriority(str, Enum):
    BREAKTHROUGH = "BREAKTHROUGH"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    EXPLORATORY = "EXPLORATORY"
    MAINTENANCE = "MAINTENANCE"
    CRITICAL = "CRITICAL"
    LOW = "LOW"


class ExperimentStatus(str, Enum):
    DESIGNED = "DESIGNED"
    RUNNING = "RUNNING"
    ANALYZING = "ANALYZING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    REPLAYING = "REPLAYING"


class KnowledgeConfidence(str, Enum):
    ESTABLISHED_LAW = "ESTABLISHED_LAW"
    SOLID_THEORY = "SOLID_THEORY"
    WORKING_MODEL = "WORKING_MODEL"
    PLAUSIBLE_HYPOTHESIS = "PLAUSIBLE_HYPOTHESIS"
    SPECULATIVE = "SPECULATIVE"
    HIGH = "HIGH"
    CONFIRMED = "CONFIRMED"


class PublicationState(str, Enum):
    DRAFT = "DRAFT"
    PEER_REVIEW = "PEER_REVIEW"
    APPROVED = "APPROVED"
    PUBLISHED = "PUBLISHED"
    RETRACTED = "RETRACTED"


class ScientificConsensus(str, Enum):
    UNANIMOUS = "UNANIMOUS"
    SUPERMAJORITY = "SUPERMAJORITY"
    QUALIFIED_MAJORITY = "QUALIFIED_MAJORITY"
    DISPUTED = "DISPUTED"
    DEADLOCKED = "DEADLOCKED"
    ACCEPTED = "ACCEPTED"
    PROVISIONAL = "PROVISIONAL"
    REJECTED = "REJECTED"


class ValidationMethod(str, Enum):
    STATISTICAL_P_VALUE = "STATISTICAL_P_VALUE"
    DETERMINISTIC_REPLAY = "DETERMINISTIC_REPLAY"
    CROSS_VALIDATION_K_FOLD = "CROSS_VALIDATION_K_FOLD"
    BAYESIAN_FACTOR = "BAYESIAN_FACTOR"
    CHAOS_INJECTION = "CHAOS_INJECTION"
    T_TEST = "T_TEST"
    ANOVA = "ANOVA"


class ScientificEventType(str, Enum):
    HYPOTHESIS_FORMULATED = "HYPOTHESIS_FORMULATED"
    HYPOTHESIS_UPDATED = "HYPOTHESIS_UPDATED"
    HYPOTHESIS_CONFIRMED = "HYPOTHESIS_CONFIRMED"
    HYPOTHESIS_FALSIFIED = "HYPOTHESIS_FALSIFIED"
    KNOWLEDGE_GAP_DETECTED = "KNOWLEDGE_GAP_DETECTED"
    EXPERIMENT_DESIGNED = "EXPERIMENT_DESIGNED"
    EXPERIMENT_STARTED = "EXPERIMENT_STARTED"
    EXPERIMENT_COMPLETED = "EXPERIMENT_COMPLETED"
    EVIDENCE_RECORDED = "EVIDENCE_RECORDED"
    VALIDATION_COMPLETED = "VALIDATION_COMPLETED"
    FACT_RECORDED = "FACT_RECORDED"
    LAW_FORMULATED = "LAW_FORMULATED"
    RESEARCH_STREAM_CREATED = "RESEARCH_STREAM_CREATED"
    ROADMAP_CREATED = "ROADMAP_CREATED"
    PUBLICATION_CREATED = "PUBLICATION_CREATED"
    PUBLICATION_PUBLISHED = "PUBLICATION_PUBLISHED"
    CONSENSUS_REACHED = "CONSENSUS_REACHED"
    ONTOLOGY_EXPANDED = "ONTOLOGY_EXPANDED"
    DISCOVERY_CYCLE_STARTED = "DISCOVERY_CYCLE_STARTED"
    DISCOVERY_CYCLE_COMPLETED = "DISCOVERY_CYCLE_COMPLETED"


@dataclass
class ScientificDomainEvent:
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_type: Any = "SCIENTIFIC_EVENT"
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    source_component: str = "scientific_runtime"
    payload: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_type": str(self.event_type.value if isinstance(self.event_type, Enum) else self.event_type),
            "timestamp": self.timestamp,
            "source_component": self.source_component,
            "payload": self.payload,
            "metadata": self.metadata,
        }


@dataclass
class ScientificHypothesisCreated(ScientificDomainEvent):
    event_type: Any = ScientificEventType.HYPOTHESIS_FORMULATED
    hypothesis_id: str = ""
    statement: str = ""
    expected_information_gain: float = 0.0
    priority: ResearchPriority = ResearchPriority.HIGH


@dataclass
class ScientificHypothesisRejected(ScientificDomainEvent):
    event_type: Any = ScientificEventType.HYPOTHESIS_FALSIFIED
    hypothesis_id: str = ""
    falsification_reason: str = ""


@dataclass
class ExperimentDesigned(ScientificDomainEvent):
    event_type: Any = ScientificEventType.EXPERIMENT_DESIGNED
    experiment_id: str = ""
    hypothesis_id: str = ""
    control_group: str = ""
    treatment_group: str = ""


@dataclass
class ExperimentStarted(ScientificDomainEvent):
    event_type: Any = ScientificEventType.EXPERIMENT_STARTED
    experiment_id: str = ""
    sample_size: int = 100


@dataclass
class ExperimentCompleted(ScientificDomainEvent):
    event_type: Any = ScientificEventType.EXPERIMENT_COMPLETED
    experiment_id: str = ""
    outcome: str = ""
    effect_size: float = 0.0
    p_value: float = 0.0


@dataclass
class EvidenceCollected(ScientificDomainEvent):
    event_type: Any = ScientificEventType.EVIDENCE_RECORDED
    evidence_id: str = ""
    hypothesis_id: str = ""
    strength: Any = EvidenceStrength.STATISTICALLY_SIGNIFICANT
    provenance_hash: str = ""
    experiment_id: str = ""
    observation_count: int = 0
    confidence: float = 0.0


EmpiricalEvidenceRecorded = EvidenceCollected



@dataclass
class EvidenceValidated(ScientificDomainEvent):
    event_type: Any = ScientificEventType.VALIDATION_COMPLETED
    evidence_id: str = ""
    hypothesis_id: str = ""
    validation_method: Any = ValidationMethod.STATISTICAL_P_VALUE
    confidence_level: float = 0.95
    p_value: float = 0.0
    is_valid: bool = True


HypothesisValidated = EvidenceValidated



@dataclass
class EvidenceRejected(ScientificDomainEvent):
    event_type: Any = "EvidenceRejected"
    evidence_id: str = ""
    rejection_reason: str = ""


@dataclass
class CorrelationDiscovered(ScientificDomainEvent):
    event_type: Any = "CorrelationDiscovered"
    variable_a: str = ""
    variable_b: str = ""
    coefficient: float = 0.0


@dataclass
class CorrelationRejected(ScientificDomainEvent):
    event_type: Any = "CorrelationRejected"
    variable_a: str = ""
    variable_b: str = ""


@dataclass
class CausalTheoryUpdated(ScientificDomainEvent):
    event_type: Any = "CausalTheoryUpdated"
    theory_id: str = ""
    causal_direction: str = ""


@dataclass
class ScientificLawFormulated(ScientificDomainEvent):
    event_type: Any = ScientificEventType.LAW_FORMULATED
    law_id: str = ""
    equation_formula: str = ""
    domain: str = ""


@dataclass
class KnowledgePublished(ScientificDomainEvent):
    event_type: Any = ScientificEventType.PUBLICATION_PUBLISHED
    publication_id: str = ""
    title: str = ""
    doi_signature: str = ""


@dataclass
class ResearchConflictDetected(ScientificDomainEvent):
    event_type: Any = "ResearchConflictDetected"
    conflict_id: str = ""
    hypothesis_a_id: str = ""
    hypothesis_b_id: str = ""


@dataclass
class ResearchConsensusReached(ScientificDomainEvent):
    event_type: Any = ScientificEventType.CONSENSUS_REACHED
    consensus_id: str = ""
    topic: str = ""
    consensus_type: ScientificConsensus = ScientificConsensus.SUPERMAJORITY


@dataclass
class ScientificModelUpdated(ScientificDomainEvent):
    event_type: Any = "ScientificModelUpdated"
    model_id: str = ""
    parameter_delta: Dict[str, Any] = field(default_factory=dict)


@dataclass
class OntologyExpanded(ScientificDomainEvent):
    event_type: Any = ScientificEventType.ONTOLOGY_EXPANDED
    concept_id: str = ""
    concept_name: str = ""
    parent_concept_id: Optional[str] = None


@dataclass
class ResearchPriorityChanged(ScientificDomainEvent):
    event_type: Any = "ResearchPriorityChanged"
    research_id: str = ""
    new_priority: ResearchPriority = ResearchPriority.HIGH


@dataclass
class ExperimentReplayCompleted(ScientificDomainEvent):
    event_type: Any = "ExperimentReplayCompleted"
    experiment_id: str = ""
    reproducibility_verified: bool = True


@dataclass
class HypothesisRetired(ScientificDomainEvent):
    event_type: Any = "HypothesisRetired"
    hypothesis_id: str = ""
    retirement_reason: str = ""


@dataclass
class ScientificGovernanceApproved(ScientificDomainEvent):
    event_type: Any = "ScientificGovernanceApproved"
    publication_id: str = ""
    approver_signature: str = ""


@dataclass
class ScientificRollbackExecuted(ScientificDomainEvent):
    event_type: Any = "ScientificRollbackExecuted"
    checkpoint_id: str = ""
    restored_model_hash: str = ""


class ScienceEventBus:
    """In-memory reactive domain event bus for Phase 13.12."""

    def __init__(self):
        self._handlers: Dict[str, List[Callable[[ScientificDomainEvent], None]]] = {}
        self._history: List[ScientificDomainEvent] = []

    def subscribe(self, event_type: Any, handler: Callable[[ScientificDomainEvent], None]) -> None:
        key = event_type.value if isinstance(event_type, Enum) else str(event_type)
        self._handlers.setdefault(key, []).append(handler)

    def publish(self, event: ScientificDomainEvent) -> None:
        self._history.append(event)
        key = event.event_type.value if isinstance(event.event_type, Enum) else str(event.event_type)
        for handler in self._handlers.get(key, []):
            try:
                handler(event)
            except Exception:
                pass

    def get_history(self, limit: int = 100) -> List[ScientificDomainEvent]:
        return self._history[-limit:]
