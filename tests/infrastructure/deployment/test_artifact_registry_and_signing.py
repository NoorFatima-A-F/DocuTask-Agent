"""Tests for Artifact Registry, SBOM, Cryptographic Signing, and Supply Chain Security."""

import pytest
from app.infrastructure.deployment.artifacts import (
    ArtifactType,
    VulnerabilitySeverity,
    VulnerabilityFinding,
    SBOMComponent,
    ArtifactMetadata,
    ArtifactSigner,
    ArtifactRegistry,
)


def test_artifact_registration_signing_and_tampering_detection() -> None:
    signer = ArtifactSigner(signing_secret="custom-secret-key")
    registry = ArtifactRegistry(signer=signer)

    sbom = [SBOMComponent(name="cryptography", version="42.0.0", purl="pkg:pypi/cryptography@42.0.0")]
    art = registry.register_artifact(
        name="docutask-ocr",
        version="1.0.0",
        artifact_type=ArtifactType.CONTAINER_IMAGE,
        commit_sha="c1d2e3f4",
        sbom=sbom,
        auto_sign=True,
    )

    assert art.artifact_id is not None
    assert art.signature is not None
    assert signer.verify_signature(art) is True

    # Tampering test (modified digest)
    art.digest_sha256 = "00000000000000000000000000000000"
    assert signer.verify_signature(art) is False


def test_artifact_promotion_gating_on_vulnerabilities() -> None:
    registry = ArtifactRegistry()

    # Artifact with critical CVE
    art_vuln = registry.register_artifact(
        name="vulnerable-pkg",
        version="0.9.0",
        artifact_type=ArtifactType.PYTHON_WHEEL,
        commit_sha="998877",
        vulnerabilities=[
            VulnerabilityFinding(
                cve_id="CVE-2026-1234",
                package_name="openssl",
                installed_version="1.1.1",
                severity=VulnerabilitySeverity.CRITICAL,
            )
        ],
    )
    assert art_vuln.has_critical_vulnerabilities is True

    # Promotion to staging allowed (for remediation testing)
    assert registry.promote_artifact(art_vuln.artifact_id, target_tier="staging") is True

    # Promotion to prod blocked by policy
    with pytest.raises(ValueError, match="CRITICAL/HIGH vulnerabilities"):
        registry.promote_artifact(art_vuln.artifact_id, target_tier="prod")
