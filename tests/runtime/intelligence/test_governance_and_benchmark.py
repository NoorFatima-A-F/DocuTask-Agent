from app.runtime.governance.formal_verification import FormalVerificationEngine
from app.runtime.governance.decision_provenance import DecisionProvenanceEngine
from app.runtime.governance.governance import EnterpriseGovernanceEngine
from app.runtime.governance.compliance_engine import RegulatoryComplianceEngine
from app.runtime.benchmark.planner_benchmark import ScientificPlannerBenchmark


def test_formal_verification_smt_bounds():
    verifier = FormalVerificationEngine()
    
    proof = verifier.verify_strategy(
        mission_id="m_formal_01",
        strategy_id="strat_delta",
        total_cost_usd=0.0022,
        budget_limit_usd=0.05,
        critical_path_ms=850.0,
        sla_limit_ms=5000.0,
        peak_memory_mb=2048.0,
        worker_memory_limit_mb=16384.0,
        estimated_accuracy=0.985,
        min_accuracy_gate=0.90,
    )
    
    assert proof.mission_id == "m_formal_01"
    assert proof.is_fully_satisfiable is True
    assert len(proof.invariants_evaluated) == 4


def test_decision_provenance_merkle_tree():
    provenance = DecisionProvenanceEngine()
    
    node1 = provenance.record_step(
        mission_id="m_merkle_001",
        phase="GOAL",
        summary="Goal Deconstruction and Prior Formulation",
        details={"goal": "Process financial ledger"},
    )
    
    node2 = provenance.record_step(
        mission_id="m_merkle_001",
        phase="BELIEF",
        summary="Posterior distribution updated",
        details={"variable": "ocr_success", "posterior": 0.94},
    )
    
    assert node1.node_hash != ""
    assert node2.parent_node_id == node1.node_id
    assert provenance.verify_integrity("m_merkle_001") is True


def test_governance_and_compliance():
    gov = EnterpriseGovernanceEngine()
    comp = RegulatoryComplianceEngine()
    
    decision = gov.evaluate_governance(
        mission_id="m_gov_001",
        strategy_id="strat_delta",
        estimated_risk=0.04,
        is_smt_verified=True,
        cost_usd=0.0022,
    )
    assert decision.is_approved is True
    assert decision.approval_tier == "AUTO_APPROVED"
    
    comp_report = comp.audit_mission_plan(
        mission_id="m_gov_001",
        has_pii_redaction=True,
        has_decision_provenance=True,
        is_smt_verified=True,
        data_retention_days=90,
    )
    assert comp_report.is_fully_compliant is True
    assert comp_report.overall_compliance_score == 1.0


def test_scientific_planner_benchmark():
    benchmark = ScientificPlannerBenchmark()
    result = benchmark.run_full_benchmark(mission_count=50)
    
    assert len(result.evaluated_algorithms) >= 5
    assert result.winner_algorithm == "ADIP_AAOS_PROBABILISTIC_PLANNER"
    assert result.utility_advantage_pct > 0
