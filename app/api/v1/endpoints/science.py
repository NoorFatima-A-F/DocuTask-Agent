"""
FastAPI REST Endpoints for Phase 13.12: Autonomous Scientific Discovery, Hypothesis Generation & Continuous Knowledge Evolution Platform.
Mounted at /api/v1/science.
"""

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from app.runtime.science import ScientificRuntime

router = APIRouter()

# Global ScientificRuntime singleton
scientific_runtime = ScientificRuntime()


# --- Request/Response Models ---

class DiscoveryCycleRequest(BaseModel):
    domain: str = Field(default="performance", description="Domain of scientific exploration")


class HypothesisCreateRequest(BaseModel):
    title: str
    statement: str
    domain: str
    rationale: str
    prior_probability: float = 0.50
    expected_information_gain: float = 0.50
    tags: List[str] = []
    knowledge_gap_id: Optional[str] = None


class KnowledgeGapCreateRequest(BaseModel):
    domain: str
    description: str
    priority: int = 1
    impact_score: float = 0.75


class ExperimentCreateRequest(BaseModel):
    hypothesis_id: str
    title: str
    description: str
    domain: str
    control_group_config: Dict[str, Any] = {}
    treatment_group_config: Dict[str, Any] = {}
    metrics_to_track: List[str] = []
    sample_size: int = 50


class ExperimentExecuteRequest(BaseModel):
    control_samples: Optional[List[float]] = None
    treatment_samples: Optional[List[float]] = None


class EvidenceCreateRequest(BaseModel):
    hypothesis_id: str
    experiment_id: Optional[str] = None
    title: str
    data_payload: Dict[str, Any] = {}
    confidence_score: float = 0.90
    empirical_sample_size: int = 50
    provenance: Dict[str, Any] = {}


class ValidationRunRequest(BaseModel):
    hypothesis_id: str
    experiment_id: Optional[str] = None
    evidence_ids: List[str] = []
    control_data: List[float] = [0.80, 0.82, 0.79, 0.81, 0.80]
    treatment_data: List[float] = [0.93, 0.95, 0.92, 0.94, 0.96]


class FactCreateRequest(BaseModel):
    statement: str
    domain: str
    source_evidence_ids: List[str] = []
    hypothesis_id: Optional[str] = None
    confidence: float = 0.95


class LawCreateRequest(BaseModel):
    title: str
    governing_equation: str
    domain: str
    supporting_fact_ids: List[str] = []
    variables: Dict[str, str] = {}
    confidence: float = 0.90


class ResearchStreamCreateRequest(BaseModel):
    title: str
    description: str
    domain: str
    allocated_compute_units: float = 100.0


class PublicationCreateRequest(BaseModel):
    title: str
    abstract: str
    authors: List[str]
    domain: str
    hypothesis_ids: List[str] = []
    experiment_ids: List[str] = []
    evidence_ids: List[str] = []
    conclusion: str = ""


class ConsensusReviewRequest(BaseModel):
    hypothesis_id: str
    evidence_ids: List[str] = []
    validation_id: Optional[str] = None
    tribunal_members: Optional[List[str]] = None


class ConceptCreateRequest(BaseModel):
    name: str
    domain: str
    definition: str
    synonyms: List[str] = []
    attributes: Dict[str, Any] = {}
    confidence: float = 0.90


class RelationCreateRequest(BaseModel):
    source_concept_id: str
    target_concept_id: str
    relation_type: str
    weight: float = 1.0
    evidence_ids: List[str] = []
    confidence: float = 0.85


# --- Endpoints ---

@router.get("/overview")
def get_overview() -> Dict[str, Any]:
    """Provides platform overview and metrics across all 9 scientific engines."""
    return scientific_runtime.get_overview()


@router.get("/metrics")
def get_metrics() -> Dict[str, Any]:
    """Provides executive metrics for the AI Chief Scientist dashboard."""
    return scientific_runtime.get_executive_metrics()


@router.post("/cycle")
def run_discovery_cycle(req: DiscoveryCycleRequest) -> Dict[str, Any]:
    """Executes a complete end-to-end Autonomous Scientific Discovery Cycle."""
    result = scientific_runtime.run_discovery_cycle(domain=req.domain)
    return result.to_dict()


# --- Hypotheses & Knowledge Gaps ---

@router.get("/hypotheses")
def list_hypotheses(
    domain: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
) -> List[Dict[str, Any]]:
    """Lists scientific hypotheses with optional domain/status filtering."""
    hypos = scientific_runtime.hypothesis_engine.list_hypotheses(domain=domain, status=status)
    return [h.to_dict() for h in hypos]


@router.get("/hypotheses/{hypothesis_id}")
def get_hypothesis(hypothesis_id: str) -> Dict[str, Any]:
    """Retrieves a specific scientific hypothesis."""
    hypo = scientific_runtime.hypothesis_engine.get_hypothesis(hypothesis_id)
    if not hypo:
        raise HTTPException(status_code=404, detail="Hypothesis not found")
    return hypo.to_dict()


@router.post("/hypotheses")
def create_hypothesis(req: HypothesisCreateRequest) -> Dict[str, Any]:
    """Formulates a new scientific hypothesis."""
    hypo = scientific_runtime.hypothesis_engine.formulate_hypothesis(
        title=req.title,
        statement=req.statement,
        domain=req.domain,
        rationale=req.rationale,
        prior_probability=req.prior_probability,
        expected_information_gain=req.expected_information_gain,
        tags=req.tags,
        knowledge_gap_id=req.knowledge_gap_id,
    )
    return hypo.to_dict()


@router.get("/knowledge-gaps")
def list_knowledge_gaps(domain: Optional[str] = Query(None)) -> List[Dict[str, Any]]:
    """Lists detected knowledge gaps."""
    gaps = scientific_runtime.hypothesis_engine.list_knowledge_gaps(domain=domain)
    return [g.to_dict() for g in gaps]


@router.post("/knowledge-gaps")
def create_knowledge_gap(req: KnowledgeGapCreateRequest) -> Dict[str, Any]:
    """Detects and records a new knowledge gap."""
    gap = scientific_runtime.hypothesis_engine.detect_knowledge_gap(
        domain=req.domain,
        description=req.description,
        priority=req.priority,
        impact_score=req.impact_score,
    )
    return gap.to_dict()


# --- Experiments ---

@router.get("/experiments")
def list_experiments(
    domain: Optional[str] = Query(None),
    hypothesis_id: Optional[str] = Query(None),
) -> List[Dict[str, Any]]:
    """Lists scientific experiments."""
    exps = scientific_runtime.experiment_engine.list_experiments(
        domain=domain,
        hypothesis_id=hypothesis_id,
    )
    return [e.to_dict() for e in exps]


@router.post("/experiments")
def create_experiment(req: ExperimentCreateRequest) -> Dict[str, Any]:
    """Designs a new scientific experiment."""
    exp = scientific_runtime.experiment_engine.design_experiment(
        hypothesis_id=req.hypothesis_id,
        title=req.title,
        description=req.description,
        domain=req.domain,
        control_group_config=req.control_group_config,
        treatment_group_config=req.treatment_group_config,
        metrics_to_track=req.metrics_to_track,
        sample_size=req.sample_size,
    )
    return exp.to_dict()


@router.post("/experiments/{experiment_id}/execute")
def execute_experiment(experiment_id: str, req: ExperimentExecuteRequest) -> Dict[str, Any]:
    """Executes a scientific experiment."""
    res = scientific_runtime.experiment_engine.execute_experiment(
        experiment_id=experiment_id,
        control_samples=req.control_samples,
        treatment_samples=req.treatment_samples,
    )
    return res


# --- Evidence ---

@router.get("/evidence")
def list_evidence(
    hypothesis_id: Optional[str] = Query(None),
    experiment_id: Optional[str] = Query(None),
) -> List[Dict[str, Any]]:
    """Lists empirical evidence records."""
    evs = scientific_runtime.evidence_engine.list_evidence(
        hypothesis_id=hypothesis_id,
        experiment_id=experiment_id,
    )
    return [e.to_dict() for e in evs]


@router.post("/evidence")
def record_evidence(req: EvidenceCreateRequest) -> Dict[str, Any]:
    """Records empirical evidence with SHA-256 integrity hash."""
    ev = scientific_runtime.evidence_engine.record_evidence(
        hypothesis_id=req.hypothesis_id,
        experiment_id=req.experiment_id,
        title=req.title,
        data_payload=req.data_payload,
        confidence_score=req.confidence_score,
        empirical_sample_size=req.empirical_sample_size,
        provenance=req.provenance,
    )
    return ev.to_dict()


# --- Validation ---

@router.get("/validations")
def list_validations(hypothesis_id: Optional[str] = Query(None)) -> List[Dict[str, Any]]:
    """Lists statistical validation reports."""
    reports = scientific_runtime.validation_engine.list_reports(hypothesis_id=hypothesis_id)
    return [r.to_dict() for r in reports]


@router.post("/validations")
def run_validation(req: ValidationRunRequest) -> Dict[str, Any]:
    """Performs rigorous statistical hypothesis validation."""
    report = scientific_runtime.validation_engine.validate_hypothesis(
        hypothesis_id=req.hypothesis_id,
        experiment_id=req.experiment_id,
        evidence_ids=req.evidence_ids,
        control_data=req.control_data,
        treatment_data=req.treatment_data,
    )
    return report.to_dict()


# --- Knowledge Base (Facts & Laws) ---

@router.get("/knowledge/facts")
def list_facts(domain: Optional[str] = Query(None)) -> List[Dict[str, Any]]:
    """Lists established scientific facts."""
    facts = scientific_runtime.knowledge_engine.list_facts(domain=domain)
    return [f.to_dict() for f in facts]


@router.post("/knowledge/facts")
def record_fact(req: FactCreateRequest) -> Dict[str, Any]:
    """Records a new verified scientific fact."""
    fact = scientific_runtime.knowledge_engine.record_fact(
        statement=req.statement,
        domain=req.domain,
        source_evidence_ids=req.source_evidence_ids,
        hypothesis_id=req.hypothesis_id,
        confidence=req.confidence,
    )
    return fact.to_dict()


@router.get("/knowledge/laws")
def list_laws(domain: Optional[str] = Query(None)) -> List[Dict[str, Any]]:
    """Lists formulated scientific laws and equations."""
    laws = scientific_runtime.knowledge_engine.list_laws(domain=domain)
    return [l.to_dict() for l in laws]


@router.post("/knowledge/laws")
def formulate_law(req: LawCreateRequest) -> Dict[str, Any]:
    """Formulates a new scientific law."""
    law = scientific_runtime.knowledge_engine.formulate_law(
        title=req.title,
        governing_equation=req.governing_equation,
        domain=req.domain,
        supporting_fact_ids=req.supporting_fact_ids,
        variables=req.variables,
        confidence=req.confidence,
    )
    return law.to_dict()


# --- Research Streams & Roadmaps ---

@router.get("/research/streams")
def list_research_streams(domain: Optional[str] = Query(None)) -> List[Dict[str, Any]]:
    """Lists research streams."""
    streams = scientific_runtime.research_engine.list_streams(domain=domain)
    return [s.to_dict() for s in streams]


@router.post("/research/streams")
def create_research_stream(req: ResearchStreamCreateRequest) -> Dict[str, Any]:
    """Creates a new research stream."""
    stream = scientific_runtime.research_engine.create_stream(
        title=req.title,
        description=req.description,
        domain=req.domain,
        allocated_compute_units=req.allocated_compute_units,
    )
    return stream.to_dict()


@router.get("/research/roadmaps")
def list_research_roadmaps() -> List[Dict[str, Any]]:
    """Lists strategic scientific research roadmaps."""
    roadmaps = scientific_runtime.research_engine.list_roadmaps()
    return [r.to_dict() for r in roadmaps]


# --- Publications ---

@router.get("/publications")
def list_publications(domain: Optional[str] = Query(None)) -> List[Dict[str, Any]]:
    """Lists peer-reviewed scientific publications."""
    pubs = scientific_runtime.publication_engine.list_publications(domain=domain)
    return [p.to_dict() for p in pubs]


@router.post("/publications")
def create_publication(req: PublicationCreateRequest) -> Dict[str, Any]:
    """Drafts a machine-readable scientific publication."""
    pub = scientific_runtime.publication_engine.create_publication(
        title=req.title,
        abstract=req.abstract,
        authors=req.authors,
        domain=req.domain,
        hypothesis_ids=req.hypothesis_ids,
        experiment_ids=req.experiment_ids,
        evidence_ids=req.evidence_ids,
        conclusion=req.conclusion,
    )
    return pub.to_dict()


@router.post("/publications/{publication_id}/publish")
def publish_paper(publication_id: str) -> Dict[str, Any]:
    """Signs with cryptographic DOI and officially publishes scientific paper."""
    pub = scientific_runtime.publication_engine.sign_and_publish(publication_id)
    return pub.to_dict()


# --- Consensus Review ---

@router.get("/consensus/reviews")
def list_consensus_reviews(hypothesis_id: Optional[str] = Query(None)) -> List[Dict[str, Any]]:
    """Lists multi-agent consensus review tribunal decisions."""
    reviews = scientific_runtime.consensus_engine.list_reviews(hypothesis_id=hypothesis_id)
    return [r.to_dict() for r in reviews]


@router.post("/consensus/reviews")
def run_consensus_review(req: ConsensusReviewRequest) -> Dict[str, Any]:
    """Conducts multi-agent consensus arbitration tribunal."""
    review = scientific_runtime.consensus_engine.conduct_consensus_review(
        hypothesis_id=req.hypothesis_id,
        evidence_ids=req.evidence_ids,
        validation_id=req.validation_id,
        tribunal_members=req.tribunal_members,
    )
    return review.to_dict()


# --- Ontology Graph ---

@router.get("/ontology/concepts")
def list_ontology_concepts(domain: Optional[str] = Query(None)) -> List[Dict[str, Any]]:
    """Lists semantic ontology concepts."""
    concepts = scientific_runtime.ontology_engine.list_concepts(domain=domain)
    return [c.to_dict() for c in concepts]


@router.post("/ontology/concepts")
def create_ontology_concept(req: ConceptCreateRequest) -> Dict[str, Any]:
    """Registers a new ontology concept."""
    concept = scientific_runtime.ontology_engine.register_concept(
        name=req.name,
        domain=req.domain,
        definition=req.definition,
        synonyms=req.synonyms,
        attributes=req.attributes,
        confidence=req.confidence,
    )
    return concept.to_dict()


@router.get("/ontology/relations")
def list_ontology_relations() -> List[Dict[str, Any]]:
    """Lists semantic ontology relations."""
    rels = scientific_runtime.ontology_engine.list_relations()
    return [r.to_dict() for r in rels]


@router.post("/ontology/relations")
def create_ontology_relation(req: RelationCreateRequest) -> Dict[str, Any]:
    """Creates a directed semantic relation between concepts."""
    rel = scientific_runtime.ontology_engine.link_concepts(
        source_concept_id=req.source_concept_id,
        target_concept_id=req.target_concept_id,
        relation_type=req.relation_type,
        weight=req.weight,
        evidence_ids=req.evidence_ids,
        confidence=req.confidence,
    )
    return rel.to_dict()


@router.get("/ontology/paths")
def find_ontology_paths(
    source_concept_id: str = Query(...),
    target_concept_id: str = Query(...),
    max_depth: int = Query(4, ge=1, le=10),
) -> List[List[Dict[str, Any]]]:
    """Finds semantic paths between two concepts in the ontology graph."""
    paths = scientific_runtime.ontology_engine.find_paths(
        source_concept_id=source_concept_id,
        target_concept_id=target_concept_id,
        max_depth=max_depth,
    )
    return paths
