"""
Test Suite: Enterprise Incident Command & Blameless Postmortems
Validates incident declaration, automated triage, resolution, blast radius assessment, and postmortems.
"""
import pytest
from app.runtime.incident.incident_commander import IncidentCommander
from app.runtime.incident.incident_manager import IncidentManager
from app.runtime.incident.postmortem_generator import PostmortemGenerator


def test_incident_lifecycle():
    commander = IncidentCommander()
    
    inc = commander.declare_incident(
        title="Test Invariant Failure Anomaly",
        severity="SEV2_HIGH",
        affected_departments=["dept_validation", "dept_governance"],
        root_cause_initial="Transient decimal precision mismatch on receipt footer",
    )

    assert inc.status == "TRIAGING"
    assert len(inc.timeline) >= 1
    assert inc.incident_commander == "Chief Executive Agent"

    # Resolve incident
    resolved = commander.resolve_incident(
        inc.incident_id,
        final_root_cause="Currency symbol Unicode normalization issue",
        mitigation_applied="Applied strip regex on decimal string",
    )
    assert resolved is not None
    assert resolved.status == "RESOLVED"
    assert resolved.resolved_at is not None


def test_incident_manager_blast_radius():
    blast = IncidentManager.analyze_incident_blast_radius("inc_2026_001")
    assert blast["incident_id"] == "inc_2026_001"
    assert blast["blast_radius_departments_count"] >= 2
    assert blast["data_loss_probability_pct"] == 0.0


def test_postmortem_generator():
    pm = PostmortemGenerator.generate_postmortem("inc_2026_001")
    assert pm["incident_id"] == "inc_2026_001"
    assert len(pm["root_cause_5_whys"]) == 5
    assert len(pm["corrective_action_items"]) >= 3
