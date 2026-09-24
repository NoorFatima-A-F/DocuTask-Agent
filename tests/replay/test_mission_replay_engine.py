"""
Tests for Phase 13.4: Autonomous Event-Sourced Mission Replay, Runtime Forensics & Enterprise Audit Intelligence Platform (AESMR-EAIP).
"""

import pytest
from app.runtime.replay.engine.replay_controller import replay_controller
from app.runtime.replay.reconstruction.mission_reconstructor import MissionReconstructor
from app.runtime.replay.reconstruction.planner_reconstructor import PlannerReconstructor
from app.runtime.replay.reconstruction.scheduler_reconstructor import SchedulerReconstructor
from app.runtime.replay.reconstruction.worker_reconstructor import WorkerReconstructor
from app.runtime.replay.reconstruction.confidence_reconstructor import ConfidenceReconstructor
from app.runtime.replay.reconstruction.truth_reconstructor import TruthReconstructor
from app.runtime.replay.forensic.forensic_engine import ForensicEngine
from app.runtime.replay.forensic.root_cause_analyzer import RootCauseAnalyzer
from app.runtime.replay.forensic.timeline_diff import TimelineDiffEngine
from app.runtime.replay.verification.replay_verifier import ReplayVerifier
from app.runtime.replay.snapshots.snapshot_manager import SnapshotManager
from app.runtime.replay.audit.audit_report_generator import AuditReportGenerator
from app.runtime.replay.audit.audit_certificate import AuditCertificateIssuer


@pytest.fixture
def sample_events():
    return [
        {
            "event_id": "ev_001",
            "event_type": "mission.started",
            "timestamp": "2026-09-12T00:00:01Z",
            "payload": {"goal": "Process Invoice"},
        },
        {
            "event_id": "ev_002",
            "event_type": "planner.lifecycle.transition",
            "timestamp": "2026-09-12T00:00:02Z",
            "payload": {"state": "DECOMPOSING", "goal": "Extract Items"},
        },
        {
            "event_id": "ev_003",
            "event_type": "planner.task_decomposed",
            "timestamp": "2026-09-12T00:00:03Z",
            "payload": {
                "tasks": [
                    {"task_id": "t1", "type": "OCR"},
                    {"task_id": "t2", "type": "SCHEMA"},
                ]
            },
        },
        {
            "event_id": "ev_004",
            "event_type": "schedule.assigned",
            "timestamp": "2026-09-12T00:00:04Z",
            "payload": {"task_id": "t1", "worker_id": "w1", "wavefront_index": 0},
        },
        {
            "event_id": "ev_005",
            "event_type": "worker.started",
            "timestamp": "2026-09-12T00:00:05Z",
            "payload": {"worker_id": "w1", "task_id": "t1", "role": "ocr"},
        },
        {
            "event_id": "ev_006",
            "event_type": "worker.completed",
            "timestamp": "2026-09-12T00:00:08Z",
            "payload": {"worker_id": "w1", "task_id": "t1", "duration_ms": 300.0},
        },
        {
            "event_id": "ev_007",
            "event_type": "confidence.evaluated",
            "timestamp": "2026-09-12T00:00:09Z",
            "payload": {
                "overall_score": 0.985,
                "formula_version": "WeightedEnsemble (v1.3.0)",
                "dimension_scores": {"ocr": 0.99},
            },
        },
        {
            "event_id": "ev_008",
            "event_type": "truth.invariant.checked",
            "timestamp": "2026-09-12T00:00:10Z",
            "payload": {"rule_id": "INV_01", "passed": True},
        },
        {
            "event_id": "ev_009",
            "event_type": "mission.completed",
            "timestamp": "2026-09-12T00:00:12Z",
            "payload": {"status": "SUCCESS", "total_runtime_ms": 500.0},
        },
    ]


def test_deterministic_mission_reconstruction(sample_events):
    mission_id = "test_mission_001"
    state_a = MissionReconstructor.reconstruct_up_to_cursor(mission_id, sample_events, 5)
    state_b = MissionReconstructor.reconstruct_up_to_cursor(mission_id, sample_events, 5)

    assert state_a.current_cursor == 5
    assert state_a.total_events_processed == 6
    assert state_a.state_merkle_hash == state_b.state_merkle_hash
    assert state_a.status == "RUNNING"


def test_subsystem_reconstructors(sample_events):
    planner = PlannerReconstructor.reconstruct_from_events(sample_events)
    assert planner.lifecycle_state == "DECOMPOSING"
    assert len(planner.tasks) == 2

    scheduler = SchedulerReconstructor.reconstruct_from_events(sample_events)
    assert scheduler.worker_allocations.get("t1") == "w1"

    workers = WorkerReconstructor.reconstruct_from_events(sample_events)
    assert "w1" in workers
    assert workers["w1"].completed_task_count == 1

    conf = ConfidenceReconstructor.reconstruct_from_events(sample_events)
    assert conf.current_score == 0.985
    assert conf.active_formula_version == "WeightedEnsemble (v1.3.0)"

    truth = TruthReconstructor.reconstruct_from_events(sample_events)
    assert len(truth.verified_invariants) == 1
    assert truth.all_invariants_satisfied is True


def test_replay_verification(sample_events):
    res = ReplayVerifier.verify_replay("test_mission_001", sample_events)
    assert res.is_valid is True
    assert res.total_events_checked == len(sample_events)
    assert res.root_merkle_hash.startswith("sha256:")


def test_forensic_investigation_and_root_cause(sample_events):
    # Add a fault event
    fault_events = list(sample_events) + [
        {
            "event_id": "ev_010_fault",
            "event_type": "worker.failed",
            "timestamp": "2026-09-12T00:00:15Z",
            "causation_id": "ev_005",
            "payload": {"error_message": "OCR quality below threshold", "status": "FAILED"},
        }
    ]

    report = ForensicEngine.investigate_mission("test_mission_001", fault_events)
    assert report.findings_count >= 1
    assert len(report.anomalies_detected) >= 1

    rc = RootCauseAnalyzer.analyze_fault(fault_events, "ev_010_fault")
    assert rc.fault_event_id == "ev_010_fault"
    assert rc.root_cause_category == "OCR_QUALITY_DEGRADATION"


def test_timeline_diff_engine(sample_events):
    diff = TimelineDiffEngine.compute_diff("m1", "m2", sample_events, sample_events)
    assert diff.similarity_score == 1.0
    assert len(diff.added_events) == 0
    assert len(diff.removed_events) == 0


def test_snapshot_and_checkpoint_manager():
    sm = SnapshotManager(checkpoint_interval=10)
    cp = sm.capture_checkpoint("m1", 20, {"key": "val"})
    assert cp.event_cursor == 20
    assert cp.state_hash.startswith("sha256:")

    nearest = sm.get_nearest_checkpoint("m1", 25)
    assert nearest is not None
    assert nearest.event_cursor == 20


def test_audit_package_and_certificate(sample_events):
    pkg = AuditReportGenerator.generate_audit_package("m1", sample_events)
    assert pkg.mission_id == "m1"
    assert pkg.is_audit_certified is True
    assert pkg.digital_signature.startswith("sig_")

    cert = AuditCertificateIssuer.issue_certificate("m1", pkg.replay_root_hash, "sha256:truth_test")
    assert cert.status == "VALID"
    assert cert.signature.startswith("sig_")


def test_replay_controller_lifecycle(sample_events):
    session = replay_controller.create_session("m1", len(sample_events))
    assert session.status == "PAUSED"
    assert session.current_cursor == 0

    replay_controller.play(session.session_id, speed=2.0)
    assert session.status == "PLAYING"
    assert session.playback_speed == 2.0

    replay_controller.step_forward(session.session_id)
    assert session.current_cursor == 1

    replay_controller.seek_to(session.session_id, 7)
    assert session.current_cursor == 7

    bm = replay_controller.add_bookmark(session.session_id, "Critical Step", "Observed OCR finish")
    assert bm.cursor == 7
    assert len(session.bookmarks) == 1
