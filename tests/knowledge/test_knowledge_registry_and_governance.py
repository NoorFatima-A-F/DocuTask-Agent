"""
Tests for KnowledgeRegistry and KnowledgeGovernanceEngine.
"""

import pytest
from app.knowledge.core.exceptions import (
    ClassificationViolationError,
    KnowledgeNotFoundError,
    PermissionDeniedError,
)
from app.knowledge.core.models import (
    ClassificationLevel,
    KnowledgeChunk,
    KnowledgeLifecycleState,
    KnowledgeObject,
    KnowledgePermission,
    RetrievalResult,
)
from app.knowledge.governance.engine import KnowledgeGovernanceEngine, UserSecurityContext
from app.knowledge.registry.registry import KnowledgeRegistry


def test_knowledge_registry_crud_and_versions():
    registry = KnowledgeRegistry()

    kobj = KnowledgeObject(
        id="kobj-handbook",
        name="Employee Handbook",
        department="HR",
        owner="alice",
        classification=ClassificationLevel.INTERNAL,
        status=KnowledgeLifecycleState.ACTIVE,
    )

    registry.register(kobj, initial_version="1.0.0")

    # Get
    fetched = registry.get("kobj-handbook")
    assert fetched.name == "Employee Handbook"

    # Create new version
    v2 = registry.create_version("kobj-handbook", "1.1.0", change_summary="Updated parental leave policy")
    assert v2.version_number == "1.1.0"
    assert registry.get("kobj-handbook").version == "1.1.0"

    versions = registry.list_versions("kobj-handbook")
    assert len(versions) == 2

    # Search with filtering
    results_hr = registry.search(department="HR")
    assert len(results_hr) == 1

    results_eng = registry.search(department="Engineering")
    assert len(results_eng) == 0

    # Archive and Restore
    registry.archive("kobj-handbook")
    assert registry.get("kobj-handbook").status == KnowledgeLifecycleState.ARCHIVED

    registry.restore("kobj-handbook")
    assert registry.get("kobj-handbook").status == KnowledgeLifecycleState.ACTIVE


def test_knowledge_governance_clearance_and_tenant_isolation():
    gov = KnowledgeGovernanceEngine()

    public_doc = KnowledgeObject(
        id="kobj-pub",
        name="Public FAQ",
        organization_id="org-acme",
        classification=ClassificationLevel.PUBLIC,
    )
    confidential_doc = KnowledgeObject(
        id="kobj-conf",
        name="M&A Deal Memo",
        organization_id="org-acme",
        classification=ClassificationLevel.CONFIDENTIAL,
    )
    restricted_doc = KnowledgeObject(
        id="kobj-rest",
        name="Executive Compensation",
        organization_id="org-acme",
        classification=ClassificationLevel.RESTRICTED,
    )

    # User with INTERNAL clearance
    standard_user = UserSecurityContext(
        user_id="user-bob",
        organization_id="org-acme",
        clearance=ClassificationLevel.INTERNAL,
    )

    # Executive user with RESTRICTED clearance
    exec_user = UserSecurityContext(
        user_id="user-ceo",
        organization_id="org-acme",
        clearance=ClassificationLevel.RESTRICTED,
    )

    # External tenant user
    other_tenant_user = UserSecurityContext(
        user_id="user-intruder",
        organization_id="org-other",
        clearance=ClassificationLevel.HIGHLY_RESTRICTED,
    )

    # 1. Standard user can access PUBLIC doc
    assert gov.check_access(public_doc, standard_user) is True

    # 2. Standard user CANNOT access CONFIDENTIAL doc
    with pytest.raises(ClassificationViolationError):
        gov.check_access(confidential_doc, standard_user)

    # 3. Exec user CAN access CONFIDENTIAL and RESTRICTED
    assert gov.check_access(confidential_doc, exec_user) is True
    assert gov.check_access(restricted_doc, exec_user) is True

    # 4. Other tenant user rejected by tenant isolation check
    with pytest.raises(PermissionDeniedError):
        gov.check_access(public_doc, other_tenant_user)


def test_governance_retrieval_filtering():
    gov = KnowledgeGovernanceEngine()

    doc1 = KnowledgeObject(id="kobj-1", name="Doc 1", organization_id="org-1", classification=ClassificationLevel.PUBLIC)
    doc2 = KnowledgeObject(id="kobj-2", name="Doc 2", organization_id="org-1", classification=ClassificationLevel.RESTRICTED)

    objects_map = {"kobj-1": doc1, "kobj-2": doc2}

    chunk1 = KnowledgeChunk(chunk_id="chk-1", document_id="doc-1", knowledge_id="kobj-1", content="Public info")
    chunk2 = KnowledgeChunk(chunk_id="chk-2", document_id="doc-2", knowledge_id="kobj-2", content="Restricted secret")

    candidates = [
        RetrievalResult(chunk=chunk1, score=0.9),
        RetrievalResult(chunk=chunk2, score=0.95),
    ]

    standard_user = UserSecurityContext(
        user_id="user-1",
        organization_id="org-1",
        clearance=ClassificationLevel.INTERNAL,
    )

    filtered = gov.filter_retrieval_results(candidates, standard_user, objects_map)
    # chunk2 must be filtered out
    assert len(filtered) == 1
    assert filtered[0].chunk.chunk_id == "chk-1"
