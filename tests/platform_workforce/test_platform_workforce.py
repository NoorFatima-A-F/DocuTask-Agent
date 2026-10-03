"""
Unit and Integration Tests for Phase 13.23: Enterprise Autonomous Agent Workforce & Digital Organization Platform (EAAWDOP)
"""
from app.platform_workforce.models.schemas import (
    DigitalEmployee, EmployeeRole, DepartmentType
)
from app.platform_workforce.registry.workforce_registry import workforce_registry
from app.platform_workforce.hierarchy.organization_hierarchy_engine import organization_hierarchy_engine
from app.platform_workforce.teams.dynamic_team_formation_engine import dynamic_team_formation_engine
from app.platform_workforce.marketplace.task_marketplace import task_marketplace
from app.platform_workforce.negotiation.negotiation_engine import negotiation_engine
from app.platform_workforce.collaboration.collaboration_protocol_engine import collaboration_protocol_engine
from app.platform_workforce.management.manager_ai_engine import manager_ai_engine
from app.platform_workforce.council.executive_council_engine import executive_council_engine
from app.platform_workforce.performance.workforce_performance_intelligence import workforce_performance_intelligence
from app.platform_workforce.economics.resource_allocation_engine import economic_resource_allocation_engine
from app.platform_workforce.hiring.autonomous_hiring_engine import autonomous_hiring_engine
from app.platform_workforce.career.promotion_career_engine import promotion_career_engine
from app.platform_workforce.scheduler.workforce_scheduler import workforce_scheduler
from app.platform_workforce.memory.collective_memory_engine import collective_memory_engine
from app.platform_workforce.conflict.conflict_resolution_engine import conflict_resolution_engine
from app.platform_workforce.runtime.workforce_master_orchestrator import workforce_master_orchestrator

def test_workforce_registry_and_employees():
    tenant = "test-tenant-wf"
    emp = DigitalEmployee(
        tenant_id=tenant,
        name="Autonomous Tester 01",
        role=EmployeeRole.SENIOR_SPECIALIST,
        department=DepartmentType.ENGINEERING,
        skills=["Python", "FastAPI", "Distributed Systems"],
        trust_score=0.96
    )
    saved = workforce_registry.register_employee(emp)
    assert saved.id == emp.id
    
    fetched = workforce_registry.get_employee(emp.id, tenant)
    assert fetched is not None
    assert fetched.name == "Autonomous Tester 01"
    
    # Task completion
    workforce_registry.record_task_completion(emp.id, success=True, latency_ms=45.0, tenant_id=tenant)
    assert fetched.lifetime_tasks_completed == 1
    assert fetched.task_success_rate == 1.0

def test_organization_hierarchy():
    chart = organization_hierarchy_engine.get_organization_chart("default-tenant")
    assert chart["total_headcount"] >= 5
    assert len(chart["root_nodes"]) >= 1
    depts = organization_hierarchy_engine.get_departments("default-tenant")
    assert len(depts) >= 5

def test_dynamic_team_formation():
    tenant = "default-tenant"
    team = dynamic_team_formation_engine.form_dynamic_team(
        team_name="Security Red Team",
        mission="Audit all endpoints against SQLi and token leakages",
        required_skills=["Zero-Trust Verification", "Forensic Auditing"],
        max_budget_usd=300.0,
        tenant_id=tenant
    )
    assert team.team_name == "Security Red Team"
    assert len(team.member_ids) > 0
    assert team.team_health_score >= 0.90

def test_task_marketplace_and_bidding():
    tenant = "test-tenant-wf"
    task = task_marketplace.post_task(
        title="Parse 10,000 Invoices",
        description="High throughput parallel OCR parsing",
        required_skills=["Document Extraction"],
        budget_max_usd=50.0,
        tenant_id=tenant
    )
    assert task.status == "OPEN"
    
    updated = task_marketplace.submit_bid(
        task_id=task.id,
        employee_id="emp-doc-spec-01",
        bid_cost_usd=20.0,
        estimated_duration_minutes=30.0,
        solution_outline="Async batch sharding",
        tenant_id=tenant
    )
    assert updated is not None
    assert len(updated.bids) == 1
    assert updated.status == "BIDDING"
    
    assigned = task_marketplace.assign_optimal_bid(task.id, tenant)
    assert assigned.status == "ASSIGNED"
    assert assigned.assigned_employee_id == "emp-doc-spec-01"

def test_negotiation_and_collaboration():
    tenant = "test-tenant-wf"
    neg = negotiation_engine.start_negotiation(
        topic="Cross-department cache allocation",
        participant_ids=["emp-eng-mgr", "emp-sec-dir"],
        initial_proposal="Allocate 10GB Redis pool",
        tenant_id=tenant
    )
    assert neg.status == "IN_PROGRESS"
    
    resolved = negotiation_engine.add_counter_proposal(
        session_id=neg.id,
        employee_id="emp-sec-dir",
        proposal="Approved with TLS 1.3 requirement",
        consensus_reached=True,
        agreed_terms={"memory_gb": 10, "tls": "1.3"},
        tenant_id=tenant
    )
    assert resolved.consensus_reached is True
    assert resolved.status == "AGREED"
    
    # Collaboration Voting
    vote = collaboration_protocol_engine.create_proposal(
        title="Promote Agent to Fleet Lead",
        initiator_id="emp-eng-mgr",
        voter_ids=["emp-eng-mgr", "emp-sec-dir"],
        required_quorum=0.5,
        tenant_id=tenant
    )
    voted = collaboration_protocol_engine.cast_vote(vote.id, "emp-eng-mgr", "YES", tenant)
    assert voted.status == "APPROVED"

def test_management_and_executive_council():
    tenant = "default-tenant"
    # Manager review
    rev = manager_ai_engine.conduct_performance_review("emp-doc-spec-01", "emp-eng-mgr", tenant)
    assert rev is not None
    assert rev.performance_rating > 4.0
    
    # Executive Council
    prop = executive_council_engine.submit_proposition(
        title="Upgrade to Llama-3.3-70B-Quantized for all workers",
        summary="Reduces latency by 35% with 0 quality loss",
        category="ARCHITECTURAL",
        tenant_id=tenant
    )
    assert prop.quorum_met is False
    
    executive_council_engine.vote_on_proposition(prop.id, "CEO", "APPROVE", tenant)
    executive_council_engine.vote_on_proposition(prop.id, "VP_ENG", "APPROVE", tenant)
    final_prop = executive_council_engine.vote_on_proposition(prop.id, "FINANCE_DIR", "APPROVE", tenant)
    assert final_prop.quorum_met is True
    assert final_prop.enacted is True

def test_performance_economics_and_hiring():
    tenant = "default-tenant"
    perf = workforce_performance_intelligence.get_workforce_metrics(tenant)
    assert perf.total_workforce_headcount >= 5
    assert perf.average_trust_score >= 0.90
    
    budget = economic_resource_allocation_engine.get_budget(tenant)
    assert budget.total_budget_usd > 0
    assert budget.efficiency_roi_ratio > 1.0
    
    # Hiring
    req = autonomous_hiring_engine.create_requisition(
        department=DepartmentType.ENGINEERING,
        target_role=EmployeeRole.JUNIOR_WORKER,
        skills=["Python"],
        tenant_id=tenant
    )
    assert req.status == "APPROVED"
    new_hire = autonomous_hiring_engine.hire_candidate(req.id, "AutoWorker-101", tenant)
    assert new_hire is not None
    assert new_hire.name == "AutoWorker-101"

def test_career_scheduler_memory_conflict_and_orchestrator():
    tenant = "default-tenant"
    # Promotion
    path = promotion_career_engine.evaluate_promotion("emp-doc-spec-01", tenant)
    assert path is not None
    promoted = promotion_career_engine.execute_promotion(path.id, tenant)
    assert promoted.status == "PROMOTED"
    
    # Scheduler
    scheds = workforce_scheduler.get_schedules(tenant)
    assert len(scheds) >= 4
    
    # Collective Memory
    mem = collective_memory_engine.store_memory(
        title="Safe Schema Migrations",
        content="Use alembic offline mode before runtime lock",
        author_id="emp-eng-vp",
        tenant_id=tenant
    )
    assert mem.id.startswith("cmem-")
    
    # Conflict Resolution
    conf = conflict_resolution_engine.arbitrate_dispute(
        party_a_id="emp-eng-mgr",
        party_b_id="emp-sec-dir",
        dispute_subject="Token cache timeout",
        mediator_id="emp-ceo-01",
        resolution_summary="Set TTL to 1800s",
        binding_agreements=["TTL=1800s"],
        tenant_id=tenant
    )
    assert conf.status == "RESOLVED"
    
    # Master Orchestrator Overview
    overview = workforce_master_orchestrator.get_organization_overview(tenant)
    assert overview.total_employees >= 5
    assert overview.workforce_readiness_index >= 0.90
