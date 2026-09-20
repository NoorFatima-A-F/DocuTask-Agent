"""Test White-Label Branding, Custom Domains, and Compliance Framework."""

import pytest
from app.tenancy.core.models import ComplianceProfileType, Region
from app.tenancy.core.exceptions import ComplianceViolationError
from app.tenancy.branding.white_label import WhiteLabelEngine
from app.tenancy.domains.manager import CustomDomainManager
from app.tenancy.compliance.framework import ComplianceFramework


def test_white_label_branding_profile():
    """Verify white-label branding customization."""
    branding_engine = WhiteLabelEngine()
    org_id = "org_brand_test"

    profile = branding_engine.set_branding(
        organization_id=org_id,
        logo_url="https://assets.acme.com/logo.svg",
        primary_color="#FF5500",
        custom_login_title="Acme Autonomous Ops",
    )

    retrieved = branding_engine.get_branding(org_id)
    assert retrieved.primary_color == "#FF5500"
    assert retrieved.custom_login_title == "Acme Autonomous Ops"


def test_custom_domain_registration_and_routing():
    """Verify custom domain registration, DNS verification, and host resolution."""
    domain_mgr = CustomDomainManager()
    org_id = "org_domain_test"

    domain = domain_mgr.register_domain(org_id, "ai.acmecorp.com")
    assert domain.is_verified is False

    verified_domain = domain_mgr.verify_domain(domain.domain_id, mock_dns_verified=True)
    assert verified_domain.is_verified is True
    assert verified_domain.ssl_active is True

    # Host routing
    resolved_org = domain_mgr.resolve_organization_by_host("ai.acmecorp.com:443")
    assert resolved_org == org_id


def test_compliance_framework_rules():
    """Verify GDPR cross-border transfer constraints."""
    compliance = ComplianceFramework()

    # GDPR allowed in EU
    assert compliance.validate_operation(ComplianceProfileType.GDPR, Region.EU_WEST) is True

    # GDPR blocked in US Region without explicit transfer exception
    with pytest.raises(ComplianceViolationError):
        compliance.validate_operation(ComplianceProfileType.GDPR, Region.US_EAST)
