"""
Test Suite for Phase 13.12: Autonomous Scientific Discovery, Hypothesis Generation & Continuous Knowledge Evolution Platform (ASD-HGCKEP).
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

from app.runtime.science import (
    ConsensusEngine,
    EvidenceEngine,
    EvidenceStrength,
    ExperimentEngine,
    ExperimentStatus,
    HypothesisEngine,
    HypothesisStatus,
    KnowledgeEngine,
    OntologyEngine,
    PublicationEngine,
    PublicationState,
    ResearchEngine,
    ResearchPriority,
    ScienceEventBus,
    ScientificConsensus,
    ScientificRuntime,
    ValidationEngine,
    ValidationMethod,
)


@pytest.fixture
def event_bus():
    return ScienceEventBus()


@pytest.fixture
def hypothesis_engine(event_bus):
    return HypothesisEngine(event_bus=event_bus)


@pytest.fixture
def experiment_engine(event_bus):
    return ExperimentEngine(event_bus=event_bus)


@pytest.fixture
def evidence_engine(event_bus):
    return EvidenceEngine(event_bus=event_bus)


@pytest.fixture
def validation_engine(event_bus):
    return ValidationEngine(event_bus=event_bus)


@pytest.fixture
def knowledge_engine(event_bus):
    return KnowledgeEngine(event_bus=event_bus)


@pytest.fixture
def research_engine(event_bus):
    return ResearchEngine(event_bus=event_bus)


@pytest.fixture
def publication_engine(event_bus):
    return PublicationEngine(event_bus=event_bus)


@pytest.fixture
def consensus_engine(event_bus):
    return ConsensusEngine(event_bus=event_bus)


@pytest.fixture
def ontology_engine(event_bus):
    return OntologyEngine(event_bus=event_bus)


@pytest.fixture
def scientific_runtime():
    return ScientificRuntime()


@pytest.fixture
def client():
    return TestClient(app)


# --- 1. Hypothesis Engine Tests ---

def test_hypothesis_formulation_and_gaps(hypothesis_engine):
    gap = hypothesis_engine.detect_knowledge_gap(
        domain="caching",
        description="Impact of L1 LRU vs LFU under bursty document load.",
        priority=3,
        impact_score=0.85,
    )
    assert gap.gap_id.startswith("gap_")
    assert gap.priority == ResearchPriority.HIGH

    hypo = hypothesis_engine.formulate_hypothesis(
        title="Adaptive LFU Caching Hypothesis",
        statement="Adaptive LFU reduces cache miss rate by 20% compared to LRU under bursty ingestion.",
        domain="caching",
        rationale="Burst patterns exhibit high frequency reuse.",
        prior_probability=0.5,
        expected_information_gain=0.75,
        tags=["cache", "performance"],
        knowledge_gap_id=gap.gap_id,
    )
    assert hypo.hypothesis_id.startswith("hypo_")
    assert hypo.status == HypothesisStatus.PROPOSED
    assert hypo.prior_probability == 0.5

    # Update prior
    updated = hypothesis_engine.update_prior(hypo.hypothesis_id, 0.85)
    assert updated.prior_probability == 0.85

    # Confirm hypothesis
    confirmed = hypothesis_engine.confirm_hypothesis(hypo.hypothesis_id)
    assert confirmed.status == HypothesisStatus.CONFIRMED


# --- 2. Experiment Engine Tests ---

def test_experiment_design_and_execution(experiment_engine):
    exp = experiment_engine.design_experiment(
        hypothesis_id="hypo_test_123",
        title="Cache Policy A/B Trial",
        description="Evaluate hit rates under synthetic burst load.",
        domain="caching",
        control_group_config={"policy": "LRU"},
        treatment_group_config={"policy": "AdaptiveLFU"},
        metrics_to_track=["hit_rate", "latency_ms"],
        sample_size=30,
    )
    assert exp.experiment_id.startswith("exp_")
    assert exp.status == ExperimentStatus.DESIGNED

    result = experiment_engine.execute_experiment(
        experiment_id=exp.experiment_id,
        control_samples=[0.70, 0.72, 0.71, 0.69, 0.73],
        treatment_samples=[0.88, 0.90, 0.87, 0.89, 0.91],
    )
    assert result["status"] == "completed"
    assert exp.status == ExperimentStatus.COMPLETED
    assert exp.metrics_observed["effect_size_cohens_d"] > 1.0


# --- 3. Evidence Engine Tests ---

def test_evidence_recording_and_integrity(evidence_engine):
    ev = evidence_engine.record_evidence(
        hypothesis_id="hypo_test_123",
        experiment_id="exp_test_456",
        title="Cache Hit Telemetry",
        data_payload={"control_mean": 0.71, "treatment_mean": 0.89},
        confidence_score=0.92,
        empirical_sample_size=50,
        provenance={"source": "telemetry_harvester"},
    )
    assert ev.evidence_id.startswith("ev_")
    assert len(ev.evidence_hash_sha256) == 64
    assert ev.strength in [EvidenceStrength.STATISTICALLY_SIGNIFICANT, EvidenceStrength.EMPIRICAL_DEFINITIVE, EvidenceStrength.VERY_STRONG]
    assert evidence_engine.verify_evidence_integrity(ev.evidence_id) is True


# --- 4. Validation Engine Tests ---

def test_statistical_validation(validation_engine):
    report = validation_engine.validate_hypothesis(
        hypothesis_id="hypo_test_123",
        experiment_id="exp_test_456",
        evidence_ids=["ev_test_789"],
        control_data=[0.70, 0.72, 0.71, 0.69, 0.73, 0.70, 0.72],
        treatment_data=[0.88, 0.90, 0.87, 0.89, 0.91, 0.88, 0.90],
        validation_method=ValidationMethod.T_TEST,
    )
    assert report.report_id.startswith("val_")
    assert report.p_value < 0.05
    assert report.is_statistically_significant is True
    assert report.effect_size_cohens_d > 0.8
    assert report.statistical_power >= 0.8


# --- 5. Knowledge Engine Tests ---

def test_knowledge_facts_and_laws(knowledge_engine):
    fact = knowledge_engine.record_fact(
        statement="Adaptive LFU yields 18.2% higher cache hit rates in bursty workloads.",
        domain="caching",
        source_evidence_ids=["ev_test_01"],
        confidence=0.97,
    )
    assert fact.fact_id.startswith("fact_")

    law = knowledge_engine.formulate_law(
        title="Cache Eviction Efficacy Relation",
        governing_equation="Hit_Rate = Base + alpha * log(Frequency_Weight)",
        domain="caching",
        supporting_fact_ids=[fact.fact_id],
        variables={"Base": "Baseline LRU hit rate", "alpha": "Adaptivity coefficient"},
        confidence=0.93,
    )
    assert law.law_id.startswith("law_")
    assert "Base" in law.variables


# --- 6. Research Engine Tests ---

def test_research_streams_and_roadmaps(research_engine):
    stream = research_engine.create_stream(
        title="Distributed Query Acceleration",
        description="Investigating lock-free query queues across swarm nodes.",
        domain="distributed_systems",
        allocated_compute_units=200.0,
    )
    assert stream.stream_id.startswith("stream_")

    roadmap = research_engine.create_roadmap(
        title="2026 Core Discovery Roadmap",
        theme="Sub-millisecond Swarm Coordination",
        stream_ids=[stream.stream_id],
        milestones=["Benchmark Baseline", "Deploy Adaptive Queues", "Formal Law Formulation"],
    )
    assert roadmap.roadmap_id.startswith("roadmap_")
    assert len(roadmap.stream_ids) == 1


# --- 7. Publication Engine Tests ---

def test_publication_and_doi_signing(publication_engine):
    pub = publication_engine.create_publication(
        title="Empirical Validation of Adaptive Caching in Swarm Memory",
        abstract="We present rigorous experimental findings demonstrating 20% lower cache miss rates.",
        authors=["AI Chief Scientist", "Swarm Telemetry Agent"],
        domain="systems",
        hypothesis_ids=["hypo_cache_01"],
        experiment_ids=["exp_cache_01"],
        evidence_ids=["ev_cache_01"],
        conclusion="Adaptive caching provides superior performance in distributed agent platforms.",
    )
    assert pub.publication_id.startswith("pub_")
    assert pub.publication_state == PublicationState.DRAFT

    signed_pub = publication_engine.sign_and_publish(pub.publication_id)
    assert signed_pub.publication_state == PublicationState.PUBLISHED
    assert signed_pub.doi.startswith("doi:10.5555/ai-scientist.")
    assert len(signed_pub.cryptographic_signature) == 64


# --- 8. Consensus Engine Tests ---

def test_consensus_review_tribunal(consensus_engine):
    review = consensus_engine.conduct_consensus_review(
        hypothesis_id="hypo_test_123",
        evidence_ids=["ev_test_456"],
        validation_id="val_test_789",
        tribunal_members=["Agent_Sentinel", "Agent_Statistician", "Agent_Architect"],
    )
    assert review.review_id.startswith("rev_")
    assert review.consensus_state in [ScientificConsensus.ACCEPTED, ScientificConsensus.PROVISIONAL]
    assert review.consensus_score >= 0.5
    assert len(review.tribunal_members) == 3


# --- 9. Ontology Engine Tests ---

def test_ontology_concepts_and_paths(ontology_engine):
    concept1 = ontology_engine.register_concept(
        name="Vector Cache Memory",
        domain="caching",
        definition="Quantized embedding cache layer in memory.",
    )
    concept2 = ontology_engine.register_concept(
        name="Semantic Retrieval Latency",
        domain="performance",
        definition="Time required to match queries against vector cache.",
    )

    rel = ontology_engine.link_concepts(
        source_concept_id=concept1.concept_id,
        target_concept_id=concept2.concept_id,
        relation_type="optimizes",
        weight=0.95,
    )
    assert rel.relation_id.startswith("rel_")

    paths = ontology_engine.find_paths(concept1.concept_id, concept2.concept_id)
    assert len(paths) >= 1
    assert paths[0][0]["relation"] == "optimizes"


# --- 10. Scientific Runtime End-to-End Cycle Tests ---

def test_scientific_runtime_discovery_cycle(scientific_runtime):
    result = scientific_runtime.run_discovery_cycle(domain="performance")
    assert result.cycle_id.startswith("cycle_")
    assert result.hypotheses_generated == 1
    assert result.experiments_executed == 1
    assert result.evidence_collected == 1
    assert result.validations_passed == 1
    assert result.facts_discovered == 1
    assert result.laws_formulated == 1
    assert result.publications_created == 1

    overview = scientific_runtime.get_overview()
    assert overview["summary"]["total_hypotheses"] >= 2
    assert overview["summary"]["total_facts"] >= 2
    assert overview["summary"]["total_publications"] >= 1
    assert len(overview["recent_cycles"]) >= 1

    metrics = scientific_runtime.get_executive_metrics()
    assert metrics["scientific_maturity_score"] > 0.8
    assert metrics["total_verified_facts"] >= 2


# --- 11. FastAPI REST API Endpoint Tests ---

def test_fastapi_science_endpoints(client):
    # GET overview
    res = client.get("/api/v1/science/overview")
    assert res.status_code == 200
    data = res.json()
    assert "summary" in data

    # GET metrics
    res = client.get("/api/v1/science/metrics")
    assert res.status_code == 200
    metrics = res.json()
    assert "scientific_maturity_score" in metrics

    # POST cycle
    res = client.post("/api/v1/science/cycle", json={"domain": "resilience"})
    assert res.status_code == 200
    cycle = res.json()
    assert "cycle_id" in cycle
    assert cycle["domain"] == "resilience"

    # GET hypotheses
    res = client.get("/api/v1/science/hypotheses")
    assert res.status_code == 200
    assert isinstance(res.json(), list)

    # POST hypothesis
    res = client.post(
        "/api/v1/science/hypotheses",
        json={
            "title": "API Test Hypothesis",
            "statement": "FastAPI router caching reduces handler latency by 30%.",
            "domain": "api_performance",
            "rationale": "Static endpoints do not require re-serialization.",
            "prior_probability": 0.6,
            "expected_information_gain": 0.8,
            "tags": ["api", "cache"],
        },
    )
    assert res.status_code == 200
    hypo_data = res.json()
    assert hypo_data["title"] == "API Test Hypothesis"

    # GET knowledge/facts & laws
    res = client.get("/api/v1/science/knowledge/facts")
    assert res.status_code == 200
    assert len(res.json()) >= 1

    res = client.get("/api/v1/science/knowledge/laws")
    assert res.status_code == 200
    assert len(res.json()) >= 1

    # GET publications
    res = client.get("/api/v1/science/publications")
    assert res.status_code == 200
    assert len(res.json()) >= 1

    # GET ontology concepts & relations
    res = client.get("/api/v1/science/ontology/concepts")
    assert res.status_code == 200
    assert len(res.json()) >= 1

    res = client.get("/api/v1/science/ontology/relations")
    assert res.status_code == 200
    assert len(res.json()) >= 1
