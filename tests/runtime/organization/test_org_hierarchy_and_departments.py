"""
Test Suite: Organizational Hierarchy & Specialized Department Engine
Validates organizational departments, graph topology, state manager metrics, and escalation paths.
"""
import pytest
from app.runtime.organization.department import CANONICAL_DEPARTMENTS, Department
from app.runtime.organization.organization_graph import OrganizationGraphBuilder
from app.runtime.organization.organizational_state import OrganizationalStateManager
from app.runtime.organization.hierarchy_manager import HierarchyManager
from app.runtime.organization.organization_registry import OrganizationRegistry


def test_canonical_departments_integrity():
    assert len(CANONICAL_DEPARTMENTS) == 8
    assert "dept_executive" in CANONICAL_DEPARTMENTS
    assert "dept_ocr" in CANONICAL_DEPARTMENTS
    assert "dept_extraction" in CANONICAL_DEPARTMENTS
    assert "dept_validation" in CANONICAL_DEPARTMENTS
    assert "dept_governance" in CANONICAL_DEPARTMENTS

    # Executive is root
    exec_dept = CANONICAL_DEPARTMENTS["dept_executive"]
    assert exec_dept.parent_department_id is None
    assert len(exec_dept.sub_departments) == 7
    assert exec_dept.health_score > 90.0


def test_organization_graph_structure():
    graph = OrganizationGraphBuilder.get_organization_graph()
    
    assert graph["total_departments"] == 8
    assert graph["total_active_agents"] >= 20
    assert len(graph["nodes"]) == 8
    assert len(graph["edges"]) >= 10
    assert graph["reporting_root"] == "dept_executive"


def test_organizational_state_manager():
    mgr = OrganizationalStateManager()
    
    kpis = mgr.get_organizational_kpis()
    assert kpis["organization_health_index"] >= 95.0
    assert kpis["total_active_agents"] >= 20
    assert kpis["macro_sla_compliance_pct"] >= 98.0
    assert kpis["status"] == "HEALTHY_OPTIMAL"

    # Update metric
    updated = mgr.update_department_metrics("dept_ocr", queue_delta=2, budget_spent_delta=0.50)
    assert updated is not None
    assert updated.queue_depth >= 2


def test_hierarchy_manager_escalation_and_reporting():
    crit_esc = HierarchyManager.get_escalation_path("dept_validation", issue_severity="CRITICAL")
    assert crit_esc.target_department_id == "dept_executive"
    assert crit_esc.approver_role == "Chief Executive Agent"

    ocr_esc = HierarchyManager.get_escalation_path("dept_ocr", issue_severity="NORMAL")
    assert ocr_esc.target_department_id == "dept_research"

    chain = HierarchyManager.get_reporting_chain("dept_extraction")
    assert len(chain) == 2
    assert chain[0]["department_id"] == "dept_extraction"
    assert chain[1]["department_id"] == "dept_executive"


def test_organization_registry_lookups():
    cap_dept = OrganizationRegistry.find_department_for_capability("bounding box")
    assert cap_dept == "dept_ocr"

    roster = OrganizationRegistry.get_agent_roster()
    assert len(roster) == 8
    assert any(r["agent_title"] == "Chief Executive Agent" for r in roster)
