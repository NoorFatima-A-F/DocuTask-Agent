"""
Tests for Knowledge Domain Models and Lifecycle State Machine.
"""

import pytest
from app.knowledge.core.exceptions import InvalidKnowledgeStateError
from app.knowledge.core.models import (
    ClassificationLevel,
    KnowledgeDocument,
    KnowledgeLifecycleState,
    KnowledgeObject,
    KnowledgeObjectType,
    SensitivityLevel,
)
from app.knowledge.lifecycle.manager import KnowledgeLifecycleManager


def test_knowledge_domain_model_creation():
    kobj = KnowledgeObject(
        id="kobj-test-001",
        name="Global Security Policy",
        description="Standard information security guidelines",
        owner="security-team",
        department="infosec",
        classification=ClassificationLevel.RESTRICTED,
        sensitivity=SensitivityLevel.HIGH,
        status=KnowledgeLifecycleState.CREATED,
    )

    assert kobj.id == "kobj-test-001"
    assert kobj.department == "infosec"
    assert kobj.classification == ClassificationLevel.RESTRICTED
    assert kobj.status == KnowledgeLifecycleState.CREATED


def test_knowledge_lifecycle_valid_transitions():
    events_log = []
    manager = KnowledgeLifecycleManager(event_listener=lambda e: events_log.append(e))

    kobj = KnowledgeObject(
        id="kobj-lifecycle-test",
        name="Lifecycle Document",
        status=KnowledgeLifecycleState.CREATED,
    )

    # CREATED -> INGESTED
    manager.transition(kobj, KnowledgeLifecycleState.INGESTED, reason="Ingested from S3")
    assert kobj.status == KnowledgeLifecycleState.INGESTED

    # INGESTED -> VALIDATED
    manager.transition(kobj, KnowledgeLifecycleState.VALIDATED, reason="Content validated")
    assert kobj.status == KnowledgeLifecycleState.VALIDATED

    # VALIDATED -> CLASSIFIED
    manager.transition(kobj, KnowledgeLifecycleState.CLASSIFIED, reason="Security classification tagged")
    assert kobj.status == KnowledgeLifecycleState.CLASSIFIED

    # CLASSIFIED -> INDEXED
    manager.transition(kobj, KnowledgeLifecycleState.INDEXED, reason="Vector embeddings generated")
    assert kobj.status == KnowledgeLifecycleState.INDEXED

    # INDEXED -> PUBLISHED
    manager.transition(kobj, KnowledgeLifecycleState.PUBLISHED, reason="Approved for publishing")
    assert kobj.status == KnowledgeLifecycleState.PUBLISHED

    # PUBLISHED -> ACTIVE
    manager.transition(kobj, KnowledgeLifecycleState.ACTIVE, reason="Active for retrieval")
    assert kobj.status == KnowledgeLifecycleState.ACTIVE

    # ACTIVE -> SUPERSEDED
    manager.transition(kobj, KnowledgeLifecycleState.SUPERSEDED, reason="New version released")
    assert kobj.status == KnowledgeLifecycleState.SUPERSEDED

    # SUPERSEDED -> ARCHIVED
    manager.transition(kobj, KnowledgeLifecycleState.ARCHIVED, reason="Archived to cold storage")
    assert kobj.status == KnowledgeLifecycleState.ARCHIVED

    # Verify history
    history = manager.get_history(kobj.id)
    assert len(history) == 8
    assert len(events_log) == 8

    # Verify metrics
    metrics = manager.get_metrics()
    assert metrics[KnowledgeLifecycleState.ACTIVE.value] == 1
    assert metrics[KnowledgeLifecycleState.ARCHIVED.value] == 1


def test_knowledge_lifecycle_illegal_transition():
    manager = KnowledgeLifecycleManager()
    kobj = KnowledgeObject(
        id="kobj-illegal-test",
        name="Illegal Document",
        status=KnowledgeLifecycleState.CREATED,
    )

    # Cannot jump directly from CREATED to ACTIVE
    with pytest.raises(InvalidKnowledgeStateError) as exc_info:
        manager.transition(kobj, KnowledgeLifecycleState.ACTIVE)

    assert "Illegal transition" in str(exc_info.value)
    assert kobj.status == KnowledgeLifecycleState.CREATED
