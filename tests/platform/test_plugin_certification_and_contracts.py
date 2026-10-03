"""Tests for Plugin Certification and Auto-Generated Contracts."""

from app.platform.certification.certification_pipeline import (
    CertificationPipeline,
)
from app.platform.contracts.contract_generator import ContractGenerator


def test_plugin_certification_and_contracts():
    badge = CertificationPipeline.certify_plugin("plugin.invoice.processing")
    assert badge.certified is True
    assert badge.overall_score >= 95.0
    assert len(badge.checks) == 6
    assert badge.signature.startswith("sig_cert_")

    dossier = ContractGenerator.generate_all()
    assert "openapi" in dossier.openapi_spec
    assert "paths" in dossier.openapi_spec
    assert "DocuTaskPlatformClient" in dossier.sdk_client_stubs_python
