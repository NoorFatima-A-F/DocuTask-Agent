"""
Comprehensive test suite for Enterprise Evidence Collection, Traceability & Audit Architecture (PART 4).
"""
from app.platform_verification.evidence_engine import (
    EvidenceCategory,
    EvidenceClassification,
    EvidenceRole,
    LineageRelation,
    AiDecisionEvidence,
    EvidencePlatformRuntime,
)


def test_cas_storage_and_integrity_verification():
    runtime = EvidencePlatformRuntime()
    exec_id = "exec_test_001"

    payload = {"invoice_id": "INV-999", "total": 1250.00, "status": "APPROVED"}
    artifact = runtime.collect_evidence(
        execution_id=exec_id,
        category=EvidenceCategory.OUTPUT_EVIDENCE,
        data=payload,
        metadata={"document_type": "invoice"},
    )

    assert artifact.storage_uri.startswith("cas://sha256/")
    assert len(artifact.checksum_sha256) == 64

    # Verify integrity
    integrity = runtime.store.verify_integrity(artifact.artifact_id)
    assert integrity.verified is True
    assert integrity.hash == artifact.checksum_sha256


def test_ai_decision_evidence_sanitization():
    runtime = EvidencePlatformRuntime()
    ai_evidence = AiDecisionEvidence(
        model_info={"provider": "google", "model": "gemini-1.5-pro", "version": "1.5"},
        prompt_info={"template": "extract_invoice", "version": "2.0"},
        context_info={"retrieved_chunks": ["Invoice #123 Acme Corp $500"]},
        tool_calls=[{"tool": "ocr_extractor", "args": {"page": 1}}],
        permitted_reasoning={"confidence": 0.98, "private_cot": "Secret chain of thought"},
    )

    art = runtime.capture_ai_decision("exec_ai_001", ai_evidence)
    content = runtime.store.retrieve_artifact(art.storage_uri)
    assert b"Secret chain of thought" not in content
    assert b"gemini-1.5-pro" in content


def test_evidence_validation_engine():
    runtime = EvidencePlatformRuntime()
    art = runtime.collect_evidence(
        execution_id="exec_val_001",
        category=EvidenceCategory.INPUT_EVIDENCE,
        data={"prompt": "Translate this doc"},
        metadata={"safe_key": "safe_val"},
    )

    report = runtime.validate_artifact(art.artifact_id)
    assert report.is_valid is True
    assert report.integrity_verified is True
    assert report.security_passed is True


def test_lineage_dag_provenance():
    runtime = EvidencePlatformRuntime()

    # Register nodes
    runtime.lineage_engine.register_node("ds_inv_v1", "DATASET")
    runtime.lineage_engine.register_node("test_ocr_01", "TEST_DEFINITION")
    runtime.lineage_engine.register_node("exec_run_01", "EXECUTION")
    runtime.lineage_engine.register_node("out_json_01", "OUTPUT")
    runtime.lineage_engine.register_node("metric_acc_01", "METRICS")
    runtime.lineage_engine.register_node("cert_pkg_01", "CERTIFICATION")

    # Link nodes
    runtime.lineage_engine.link_nodes("ds_inv_v1", "exec_run_01", relation=LineageRelation.GENERATED_BY.value)
    runtime.lineage_engine.link_nodes("test_ocr_01", "exec_run_01", relation=LineageRelation.GENERATED_BY.value)
    runtime.lineage_engine.link_nodes("exec_run_01", "out_json_01", relation=LineageRelation.DERIVED_FROM.value)
    runtime.lineage_engine.link_nodes("out_json_01", "metric_acc_01", relation=LineageRelation.EVALUATED_BY.value)
    runtime.lineage_engine.link_nodes("metric_acc_01", "cert_pkg_01", relation=LineageRelation.APPROVED_BY.value)

    lineage = runtime.lineage_engine.trace_lineage("cert_pkg_01")
    assert lineage["total_ancestors"] >= 4
    assert lineage["target_type"] == "CERTIFICATION"


def test_rbac_access_control():
    runtime = EvidencePlatformRuntime()
    ac = runtime.access_control

    # Developer cannot view RESTRICTED
    assert ac.check_permission(EvidenceRole.DEVELOPER, "VIEW", EvidenceClassification.RESTRICTED) is False
    # Auditor can view RESTRICTED
    assert ac.check_permission(EvidenceRole.AUDITOR, "VIEW", EvidenceClassification.RESTRICTED) is True
    # Admin can export RESTRICTED
    assert ac.check_permission(EvidenceRole.ADMINISTRATOR, "EXPORT", EvidenceClassification.RESTRICTED) is True


def test_certification_package_compiler_and_api():
    runtime = EvidencePlatformRuntime()
    exec_id = "exec_cert_999"

    runtime.collect_evidence(exec_id, EvidenceCategory.INPUT_EVIDENCE, {"doc": "invoice.pdf"})
    runtime.collect_evidence(exec_id, EvidenceCategory.OUTPUT_EVIDENCE, {"total": 500})

    metrics = {"accuracy": 98.5, "latency_ms": 320.0}
    decision = {"status": "PASSED", "band": "Enterprise Certified"}

    # Compile package
    pkg = runtime.compile_certification_package(exec_id, "VERIF-OCR-001", metrics, decision)
    assert pkg.execution_id == exec_id
    assert len(pkg.package_manifest_hash) == 64
    assert len(pkg.raw_artifacts_uris) >= 2

    # Check Audit Log (Past-Tense naming convention)
    audit_events = runtime.audit_trail.get_events_for_resource(pkg.package_id)
    assert len(audit_events) == 1
    assert audit_events[0].action == "CertificationGenerated"

    # API verification
    pkg_api = runtime.api.generate_package(exec_id, "VERIF-OCR-001", metrics, decision)
    assert pkg_api["package_id"] is not None
