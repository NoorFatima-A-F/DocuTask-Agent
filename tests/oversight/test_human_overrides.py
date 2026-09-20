"""Tests for Controlled Human Overrides, Safety Limits, and Validation."""

import pytest
from app.oversight.core.context import OversightContext
from app.oversight.core.exceptions import InvalidOverrideError
from app.oversight.overrides.policies import OverridePolicy
from app.oversight.overrides.validation import OverrideValidator
from app.oversight.overrides.service import OverrideService


def test_valid_human_override_execution():
    service = OverrideService()
    ctx = OversightContext(
        tenant_id="tenant_1",
        risk_score=0.40,
        action_type="DOCUMENT_EXTRACTION",
    )

    record = service.execute_override(
        review_id="rev_ovr_01",
        reviewer_id="usr_supervisor",
        reviewer_role="supervisor",
        original_ai_decision={"total_amount": 1000.0},
        overridden_human_decision={"total_amount": 1250.0},
        justification="Corrected invoice amount by adding unparsed freight fee.",
        context=ctx,
    )

    assert record.override_id.startswith("ovr_")
    assert record.reviewer_id == "usr_supervisor"
    assert record.overridden_human_decision["total_amount"] == 1250.0
    assert service.get_override(record.override_id) == record


def test_override_fails_on_short_justification():
    service = OverrideService()
    ctx = OversightContext(
        tenant_id="tenant_1",
        risk_score=0.40,
    )

    with pytest.raises(InvalidOverrideError) as exc:
        service.execute_override(
            review_id="rev_ovr_02",
            reviewer_id="usr_supervisor",
            reviewer_role="supervisor",
            original_ai_decision="A",
            overridden_human_decision="B",
            justification="Fixed",  # Too short (<15 chars)
            context=ctx,
        )
    assert "justification must be at least" in str(exc.value)


def test_override_fails_on_unauthorized_role():
    service = OverrideService()
    ctx = OversightContext(
        tenant_id="tenant_1",
        risk_score=0.40,
    )

    with pytest.raises(InvalidOverrideError) as exc:
        service.execute_override(
            review_id="rev_ovr_03",
            reviewer_id="usr_guest",
            reviewer_role="guest_user",  # Not in allowed roles
            original_ai_decision="A",
            overridden_human_decision="B",
            justification="Manual change requested by customer support.",
            context=ctx,
        )
    assert "not authorized to perform overrides" in str(exc.value)


def test_override_fails_on_excessive_risk_threshold():
    service = OverrideService()
    ctx = OversightContext(
        tenant_id="tenant_1",
        risk_score=0.99,  # Severe risk (>0.95 cannot be manually overridden)
    )

    with pytest.raises(InvalidOverrideError) as exc:
        service.execute_override(
            review_id="rev_ovr_04",
            reviewer_id="usr_supervisor",
            reviewer_role="supervisor",
            original_ai_decision="A",
            overridden_human_decision="B",
            justification="Attempting to force high risk override.",
            context=ctx,
        )
    assert "maximum overrideable safety threshold" in str(exc.value)
