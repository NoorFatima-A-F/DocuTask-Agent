"""Unit tests for Artifact Management Platform."""
import pytest
from app.deployment.artifacts.registry import ArtifactRegistry
from app.deployment.artifacts.versions import ArtifactVersion
from app.deployment.core.exceptions import ArtifactValidationException


def test_artifact_version_semver_sorting():
    v1 = ArtifactVersion("1.0.0")
    v2 = ArtifactVersion("1.1.0")
    v3 = ArtifactVersion("2.0.0-alpha.1")
    v4 = ArtifactVersion("2.0.0")

    assert v1 < v2 < v3 < v4
    assert v1.bump_patch() == ArtifactVersion("1.0.1")
    assert v1.bump_minor() == ArtifactVersion("1.1.0")
    assert v1.bump_major() == ArtifactVersion("2.0.0")


def test_artifact_registry_registration_and_signing():
    registry = ArtifactRegistry(default_signing_key="test-key-123")
    payload = b"binary-container-image-content-v1.0.0"

    meta = registry.register_artifact(
        name="docutask-ocr-worker",
        version="1.0.0",
        data=payload,
        sbom_components=[{"name": "tesseract", "version": "5.3.0"}],
        auto_sign=True,
    )

    assert meta.verified is True
    assert registry.verify_artifact(meta.artifact_id, secret_key="test-key-123") is True
    assert registry.verify_artifact(meta.artifact_id, secret_key="wrong-key") is False


def test_artifact_provenance_enforcement():
    registry = ArtifactRegistry(default_signing_key="secret-key")
    payload = b"ai-agent-model-v2"

    meta = registry.register_artifact(
        name="docutask-agent",
        version="2.0.0",
        data=payload,
    )

    # Clean scan
    registry.record_vulnerability_scan(meta.artifact_id, critical=0, high=0)
    assert registry.enforce_provenance(meta.artifact_id) is True

    # Failing scan
    registry.record_vulnerability_scan(meta.artifact_id, critical=2, high=1)
    with pytest.raises(ArtifactValidationException, match="failing vulnerability scan"):
        registry.enforce_provenance(meta.artifact_id)
