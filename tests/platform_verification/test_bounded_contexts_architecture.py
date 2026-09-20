"""
Unit and Integration Test Suite for Enterprise Bounded Contexts and Hexagonal Architecture.
Validates independent execution, CQRS application services, Domain Event Bus, and Anti-Corruption Layers.
"""
import pytest
import asyncio
from typing import List

from app.contexts.runtime import BoundedContextsRuntime, get_contexts_runtime
from app.shared_kernel.events import DomainEvent, get_event_bus
from app.infrastructure.acl import GeminiAiAntiCorruptionLayer, OcrEngineAntiCorruptionLayer
from app.contexts.verification.contracts import VerificationDefinitionCreated
from app.contexts.execution.contracts import ExecutionStarted, ExecutionCompleted
from app.contexts.datasets.contracts import DatasetRegistered
from app.contexts.audit.contracts import AuditRecordAppended


@pytest.fixture
def runtime():
    return BoundedContextsRuntime()


@pytest.mark.asyncio
async def test_all_12_bounded_contexts_integration(runtime):
    """Executes a full cross-bounded-context flow via published contracts and events."""
    event_bus = get_event_bus()
    event_bus.clear()

    captured_events: List[DomainEvent] = []

    async def on_event(evt: DomainEvent):
        captured_events.append(evt)

    event_bus.subscribe(VerificationDefinitionCreated, on_event)
    event_bus.subscribe(ExecutionStarted, on_event)
    event_bus.subscribe(DatasetRegistered, on_event)
    event_bus.subscribe(AuditRecordAppended, on_event)

    # 1. Verification Context
    v_res = await runtime.verification.create_definition(
        spec_id="spec_invoice_val_01",
        name="Invoice Verification Spec",
        invariants=["accuracy >= 0.95"],
        parameters={"format": "pdf"}
    )
    assert v_res.is_ok is True
    assert v_res.unwrap().name == "Invoice Verification Spec"

    # 2. Datasets Context
    ds_res = await runtime.datasets.register_dataset(
        dataset_id="ds_golden_inv",
        name="Golden Invoice Dataset",
        category="GOLDEN",
        content=b"Sample PDF invoice binary payload"
    )
    assert ds_res.is_ok is True
    assert len(ds_res.unwrap().sha256_checksum) == 64

    # 3. Environments Context
    env_res = await runtime.environments.register_and_validate(
        env_id="env_staging_worker",
        name="Staging OCR Worker Cluster",
        tier="STAGING",
        profile={"cpu": 16, "gpu": True}
    )
    assert env_res.is_ok is True
    assert env_res.unwrap().is_ready is True

    # 4. Configuration Context
    cfg_res = await runtime.configuration.resolve_snapshot(
        config_id="cfg_run_101",
        tier="STAGING",
        overrides={"timeout_seconds": 120}
    )
    assert cfg_res.is_ok is True
    assert cfg_res.unwrap().parameters["timeout_seconds"] == 120

    # 5. Execution Context
    exec_res = await runtime.execution.execute_task(
        task_id="task_run_101",
        spec_id=v_res.unwrap().id,
        workload=lambda: {"processed": 100, "accuracy_scores": [0.98, 0.99, 0.97, 0.98, 0.99]}
    )
    assert exec_res.is_ok is True
    assert exec_res.unwrap()["processed"] == 100

    # 6. Evidence Context
    ev_res = await runtime.evidence.record_evidence(
        evidence_id="ev_raw_output_01",
        run_id="task_run_101",
        payload=b'{"items": 100, "status": "OK"}',
        tier="WARM"
    )
    assert ev_res.is_ok is True
    assert len(ev_res.unwrap().cas_hash) == 64

    # 7. Metrics Context
    m_res = await runtime.metrics.record_metric(
        metric_id="m_acc_01",
        run_id="task_run_101",
        name="accuracy",
        value=0.982,
        category="AI_QUALITY"
    )
    assert m_res.is_ok is True
    assert m_res.unwrap().value == 0.982

    # 8. Statistics Context
    scores = exec_res.unwrap()["accuracy_scores"]
    stat_res = await runtime.statistics.analyze_samples(
        analysis_id="stat_01",
        metric_name="accuracy",
        samples=scores
    )
    assert stat_res.is_ok is True
    stat_agg = stat_res.unwrap()
    assert stat_agg.sample_size == 5
    assert stat_agg.mean > 0.97
    assert stat_agg.ci_lower_95 <= stat_agg.mean <= stat_agg.ci_upper_95

    # 9. Quality Context
    q_res = await runtime.quality.evaluate_metrics(
        gate_id="gate_01",
        run_id="task_run_101",
        metrics={"accuracy": stat_agg.mean},
        rules=[{"metric": "accuracy", "threshold": 0.95}]
    )
    assert q_res.is_ok is True
    assert q_res.unwrap().is_passed is True

    # 10. Certification Context
    cert_res = await runtime.certification.issue_certificate(
        cert_id="cert_prod_01",
        run_id="task_run_101",
        level="ENTERPRISE_CERTIFIED",
        metadata={"approver": "lead_architect", "score": stat_agg.mean}
    )
    assert cert_res.is_ok is True
    assert len(cert_res.unwrap().digital_signature_hash) == 64

    # 11. Audit Context (Hash Chain)
    audit1 = await runtime.audit.log_action("EXECUTION_START", "orchestrator", {"task": "task_run_101"})
    audit2 = await runtime.audit.log_action("CERTIFICATION_ISSUED", "cert_engine", {"cert": "cert_prod_01"})
    assert audit1.is_ok is True
    assert audit2.is_ok is True
    assert runtime.audit.verify_integrity() is True

    # 12. Plugins Context
    p_res = await runtime.plugins.register_plugin(
        plugin_id="plugin_layout_eval",
        name="LayoutLM Evaluator",
        capabilities=["bbox_overlap", "key_value_extraction"]
    )
    assert p_res.is_ok is True
    assert p_res.unwrap().status == "ACTIVE"

    # Verify event subscriptions fired decoupled events
    assert len(captured_events) >= 4
    event_types = {type(e) for e in captured_events}
    assert VerificationDefinitionCreated in event_types
    assert ExecutionStarted in event_types
    assert DatasetRegistered in event_types
    assert AuditRecordAppended in event_types


def test_anti_corruption_layers():
    """Verify ACLs protect domain models from third-party vendor representations."""
    # 1. Gemini AI ACL
    gemini_acl = GeminiAiAntiCorruptionLayer(model_name="gemini-2.5-flash")
    gemini_res = gemini_acl.evaluate_response_faithfulness(
        prompt="Extract total amount",
        generated_text="Total amount is $450.00",
        context="$450.00"
    )
    assert gemini_res.is_ok is True
    payload = gemini_res.unwrap()
    assert payload["provider"] == "google_gemini"
    assert payload["faithfulness_score"] >= 0.90
    assert payload["hallucination_detected"] is False

    # 2. OCR Engine ACL
    ocr_acl = OcrEngineAntiCorruptionLayer(engine_name="tesseract_v5")
    ocr_res = ocr_acl.normalize_ocr_output({"text": "INVOICE #98214\nTotal: $1,200.00"})
    assert ocr_res.is_ok is True
    ocr_payload = ocr_res.unwrap()
    assert ocr_payload["engine"] == "tesseract_v5"
    assert ocr_payload["character_error_rate"] <= 0.02
    assert ocr_payload["confidence"] == 0.99
