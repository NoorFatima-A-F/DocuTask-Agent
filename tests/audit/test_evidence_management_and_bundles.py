"""Tests for Evidence Artifacts, Attachments, and Signed Evidence Bundles."""

import pytest
from app.audit.evidence.artifacts import EvidenceType, EvidenceArtifact
from app.audit.evidence.manager import EvidenceManager
from app.audit.storage.repository import AuditRepository
from app.audit.core.events import AuditEvent


def test_evidence_artifact_creation():
    manager = EvidenceManager()
    artifact = manager.create_artifact(
        tenant_id="tenant_evi",
        name="Model Card - Invoice Extractor v2",
        evidence_type=EvidenceType.AI_EVIDENCE,
        source="model_registry",
        content='{"model_id": "inv_extractor", "accuracy": 0.985}',
        classification="CONFIDENTIAL",
        owner="ml_lead",
    )

    assert artifact.evidence_id.startswith("evi_")
    assert artifact.content_hash is not None
    assert len(artifact.content_hash) == 64

    # Fetch
    fetched = manager.get_artifact(artifact.evidence_id, tenant_id="tenant_evi")
    assert fetched is not None
    assert fetched.name == "Model Card - Invoice Extractor v2"


def test_evidence_bundle_generation_and_manifest_signing():
    repo = AuditRepository()
    manager = EvidenceManager(repository=repo)

    # 1. Record events
    ev1 = repo.record(
        AuditEvent(
            event_id="ev_bnd_1",
            event_type="model.invoke",
            tenant_id="tenant_bundle",
            actor_id="user_1",
            action="invoke",
            resource_type="model",
            resource_id="gemini",
            correlation_id="corr_bnd_100",
        )
    )

    # 2. Record artifact
    art1 = manager.create_artifact(
        tenant_id="tenant_bundle",
        name="Evaluation Report",
        evidence_type=EvidenceType.AI_EVIDENCE,
        source="evaluator",
        content='{"score": 0.99}',
    )

    # 3. Create bundle
    bundle = manager.create_evidence_bundle(
        tenant_id="tenant_bundle",
        title="Q3 Model Compliance Package",
        purpose="SOC 2 Type II Audit Evidence",
        correlation_id="corr_bnd_100",
        artifact_ids=[art1.evidence_id],
    )

    assert bundle.bundle_id.startswith("bnd_")
    assert len(bundle.audit_events) == 1
    assert len(bundle.artifacts) == 1
    assert bundle.manifest_hash is not None
    assert bundle.signature is not None
