"""
Phase 13.12: Autonomous Scientific Discovery, Hypothesis Generation & Continuous Knowledge Evolution Platform (ASD-HGCKEP).
"""

from app.runtime.science.consensus.consensus_engine import ConsensusEngine, ConsensusReview
from app.runtime.science.events.science_events import (
    EvidenceStrength,
    HypothesisStatus,
    KnowledgeConfidence,
    PublicationState,
    ResearchPriority,
    ScienceEventBus,
    ScientificConsensus,
    ScientificDomainEvent,
    ScientificEventType,
    ValidationMethod,
)
from app.runtime.science.evidence.evidence_engine import EvidenceEngine, ScientificEvidence
from app.runtime.science.experiment.experiment_engine import (
    ExperimentEngine,
    ExperimentStatus,
    ExperimentVariable,
    ScientificExperiment,
)
from app.runtime.science.hypothesis.hypothesis_engine import (
    HypothesisEngine,
    KnowledgeGap,
    ScientificHypothesis,
)
from app.runtime.science.knowledge.knowledge_engine import (
    KnowledgeEngine,
    ScientificFact,
    ScientificLaw,
)
from app.runtime.science.ontology.ontology_engine import (
    OntologyConcept,
    OntologyEngine,
    OntologyRelation,
)
from app.runtime.science.publication.publication_engine import (
    PublicationEngine,
    ScientificPublication,
)
from app.runtime.science.research.research_engine import (
    ResearchEngine,
    ResearchRoadmap,
    ResearchStream,
)
from app.runtime.science.runtime.scientific_runtime import (
    DiscoveryCycleResult,
    ScientificRuntime,
)
from app.runtime.science.validation.validation_engine import (
    ValidationEngine,
    ValidationReport,
)

__all__ = [
    # Events & Enums
    "ScientificEventType",
    "EvidenceStrength",
    "HypothesisStatus",
    "ResearchPriority",
    "ExperimentStatus",
    "KnowledgeConfidence",
    "PublicationState",
    "ScientificConsensus",
    "ValidationMethod",
    "ScientificDomainEvent",
    "ScienceEventBus",
    # Engines & Data Models
    "ScientificHypothesis",
    "KnowledgeGap",
    "HypothesisEngine",
    "ScientificExperiment",
    "ExperimentVariable",
    "ExperimentEngine",
    "ScientificEvidence",
    "EvidenceEngine",
    "ValidationReport",
    "ValidationEngine",
    "ScientificFact",
    "ScientificLaw",
    "KnowledgeEngine",
    "ResearchStream",
    "ResearchRoadmap",
    "ResearchEngine",
    "ScientificPublication",
    "PublicationEngine",
    "ConsensusReview",
    "ConsensusEngine",
    "OntologyConcept",
    "OntologyRelation",
    "OntologyEngine",
    "ScientificRuntime",
    "DiscoveryCycleResult",
]
