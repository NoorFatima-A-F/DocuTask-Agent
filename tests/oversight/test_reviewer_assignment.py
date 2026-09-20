"""Tests for Reviewer Assignment Engine, Skills, and Authority Matrix."""

import pytest
from app.oversight.core.context import OversightContext
from app.oversight.reviews.requests import ReviewRequest
from app.oversight.reviews.assignments import (
    Reviewer,
    ReviewerAuthority,
    ReviewerAssignmentEngine,
)


def test_reviewer_registration_and_retrieval():
    engine = ReviewerAssignmentEngine()
    r1 = Reviewer(
        user_id="usr_bob",
        name="Bob Jones",
        email="bob@example.com",
        department="Finance",
        roles=["finance_manager"],
        skills=["tax_audit", "erp_validation"],
        authority=ReviewerAuthority(
            max_financial_limit=100000.0,
            authorized_risk_levels=["LOW", "MEDIUM", "HIGH"],
            authorized_roles=["finance_manager"],
        ),
    )
    engine.register_reviewer(r1)
    assert engine.get_reviewer("usr_bob") == r1
    assert len(engine.list_reviewers()) == 1


def test_reviewer_authority_limits():
    engine = ReviewerAssignmentEngine()
    r = Reviewer(
        user_id="usr_junior",
        name="Junior Analyst",
        email="junior@example.com",
        department="Operations",
        roles=["reviewer"],
        authority=ReviewerAuthority(
            max_financial_limit=5000.0,
            authorized_data_classifications=["PUBLIC", "INTERNAL"],
        ),
    )
    engine.register_reviewer(r)

    # Exceeding financial limit
    high_value_ctx = OversightContext(
        tenant_id="tenant_1",
        financial_impact=12000.0,
    )
    authorized, reason = engine.verify_authority(r, high_value_ctx)
    assert authorized is False
    assert "Financial impact" in reason

    # Restricted data classification
    restricted_ctx = OversightContext(
        tenant_id="tenant_1",
        financial_impact=100.0,
        data_classification="RESTRICTED",
    )
    authorized, reason = engine.verify_authority(r, restricted_ctx)
    assert authorized is False
    assert "Data classification" in reason


def test_least_busy_reviewer_assignment():
    engine = ReviewerAssignmentEngine()
    r1 = Reviewer(
        user_id="r1",
        name="Reviewer 1",
        email="r1@example.com",
        department="Legal",
        roles=["legal_counsel"],
        active_reviews_count=3,
    )
    r2 = Reviewer(
        user_id="r2",
        name="Reviewer 2",
        email="r2@example.com",
        department="Legal",
        roles=["legal_counsel"],
        active_reviews_count=1,
    )
    engine.register_reviewer(r1)
    engine.register_reviewer(r2)

    req = ReviewRequest(
        request_id="req_1",
        tenant_id="tenant_1",
        title="Contract Sign-off",
        resource_id="doc_contract",
        required_roles=["legal_counsel"],
    )

    assigned = engine.assign_reviewer(req)
    assert assigned is not None
    assert assigned.user_id == "r2"  # Least busy reviewer selected
    assert r2.active_reviews_count == 2
    assert "r2" in req.assigned_reviewers

    # Release reviewer
    engine.release_reviewer("r2")
    assert r2.active_reviews_count == 1
