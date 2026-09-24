"""
Test Suite: Executive Coordination & Strategic Mission Direction
Validates executive decision issuing, multi-department mission lifecycle, barrier sync, and delegation policies.
"""
from app.runtime.executive.executive_controller import ExecutiveController
from app.runtime.executive.mission_director import MissionDirector
from app.runtime.executive.coordination_engine import CoordinationEngine
from app.runtime.executive.delegation_manager import DelegationManager
from app.runtime.executive.executive_metrics import ExecutiveMetricsEngine


def test_executive_controller_decision_making():
    ctrl = ExecutiveController()
    
    decisions = ctrl.list_executive_decisions()
    assert len(decisions) >= 2

    new_dec = ctrl.issue_decision(
        mission_id="mission_test_999",
        decision_type="RESOURCE_REALLOCATION",
        decision_title="Authorize GPU Boost",
        rationale="Burst in OCR processing queue",
        affected_departments=["dept_ocr"],
    )
    assert new_dec.mission_id == "mission_test_999"
    assert new_dec.authorized_by == "Chief Executive Agent"
    assert new_dec.approval_hash.startswith("sha256_exec_")


def test_mission_director_lifecycle_and_stages():
    director = MissionDirector()
    
    missions = director.list_missions()
    assert len(missions) >= 1
    m1 = director.get_mission("mission_live_001")
    assert m1 is not None
    assert m1.priority == "CRITICAL"
    assert len(m1.stages) == 5

    # Advance stage
    director.advance_stage("mission_live_001", stage_index=3, duration_ms=410.0, summary="Extraction done")
    m1_updated = director.get_mission("mission_live_001")
    assert m1_updated.stages[2].status == "COMPLETED"
    assert m1_updated.stages[3].status == "IN_PROGRESS"


def test_coordination_engine_barriers():
    engine = CoordinationEngine()
    
    barrier = engine.create_barrier("bar_test_01", "m1", ["dept_ocr", "dept_validation"])
    assert barrier.is_released is False

    # Dept 1 arrives
    rel1 = engine.arrive_at_barrier("bar_test_01", "dept_ocr")
    assert rel1 is False

    # Dept 2 arrives -> barrier released
    rel2 = engine.arrive_at_barrier("bar_test_01", "dept_validation")
    assert rel2 is True


def test_delegation_manager_and_metrics():
    del_mgr = DelegationManager()
    
    assert del_mgr.can_autonomously_execute("dept_ocr", estimated_cost_usd=2.50) is True
    assert del_mgr.can_autonomously_execute("dept_ocr", estimated_cost_usd=15.00) is False

    summary = ExecutiveMetricsEngine.get_executive_summary()
    assert summary["strategic_alignment_score_pct"] >= 95.0
    assert summary["autonomous_delegation_ratio_pct"] >= 90.0
    assert summary["executive_status"] == "STRATEGIC_ALIGNMENT_NOMINAL"
