"""
Comprehensive Unit & Integration Test Suite for Enterprise Verification Core Components (Part 1.1B).
Validates all 16 core components against their interface contracts and tests end-to-end orchestration.
"""

import pytest

from app.platform_verification.components import (
    VerificationOrchestratorInterface,
    VerificationRegistryInterface,
    VerificationDefinitionManagerInterface,
    VerificationExecutionEngineInterface,
    DatasetManagerInterface,
    EnvironmentManagerInterface,
    ConfigurationManagerInterface,
    EvidenceManagerInterface,
    MetricsEngineInterface,
    StatisticalAnalysisEngineInterface,
    QualityGateEngineInterface,
    CertificationEngineInterface,
    ReportingEngineInterface,
    AuditManagerInterface,
    TraceabilityManagerInterface,
    PluginManagerInterface,
    VerificationOrchestrator,
    VerificationRegistry,
    VerificationDefinitionManager,
    VerificationExecutionEngine,
    DatasetManager,
    EnvironmentManager,
    ConfigurationManager,
    EvidenceManager,
    MetricsEngine,
    StatisticalAnalysisEngine,
    QualityGateEngine,
    CertificationEngine,
    ReportingEngine,
    AuditManager,
    TraceabilityManager,
    PluginManager,
)
from app.platform_verification.components.runtime import EnterpriseVerificationRuntime


@pytest.mark.asyncio
async def test_component_interfaces_conformance():
    """Verify that all 16 components implement their corresponding abstract interfaces."""
    assert issubclass(VerificationOrchestrator, VerificationOrchestratorInterface)
    assert issubclass(VerificationRegistry, VerificationRegistryInterface)
    assert issubclass(VerificationDefinitionManager, VerificationDefinitionManagerInterface)
    assert issubclass(VerificationExecutionEngine, VerificationExecutionEngineInterface)
    assert issubclass(DatasetManager, DatasetManagerInterface)
    assert issubclass(EnvironmentManager, EnvironmentManagerInterface)
    assert issubclass(ConfigurationManager, ConfigurationManagerInterface)
    assert issubclass(EvidenceManager, EvidenceManagerInterface)
    assert issubclass(MetricsEngine, MetricsEngineInterface)
    assert issubclass(StatisticalAnalysisEngine, StatisticalAnalysisEngineInterface)
    assert issubclass(QualityGateEngine, QualityGateEngineInterface)
    assert issubclass(CertificationEngine, CertificationEngineInterface)
    assert issubclass(ReportingEngine, ReportingEngineInterface)
    assert issubclass(AuditManager, AuditManagerInterface)
    assert issubclass(TraceabilityManager, TraceabilityManagerInterface)
    assert issubclass(PluginManager, PluginManagerInterface)


@pytest.mark.asyncio
async def test_orchestrator_lifecycle():
    orchestrator = VerificationOrchestrator()
    lifecycle_id = await orchestrator.initialize_lifecycle("run-101", "spec-202")
    assert lifecycle_id == "run-101"
    
    state = await orchestrator.transition_state("run-101", "EXECUTING")
    assert state == "EXECUTING"
    
    status = await orchestrator.get_status("run-101")
    assert status["state"] == "EXECUTING"
    assert status["spec_id"] == "spec-202"
    assert len(status["history"]) == 2


@pytest.mark.asyncio
async def test_registry_registration_and_lookup():
    registry = VerificationRegistry()
    await registry.register_capability(
        module_id="mod-ocr",
        capability="ocr_accuracy_eval",
        version="1.0.0",
        metadata={"domain": "vision", "tier": "critical"}
    )
    
    item = await registry.lookup_capability("mod-ocr")
    assert item is not None
    assert item["capability"] == "ocr_accuracy_eval"
    assert item["version"] == "1.0.0"
    
    all_caps = await registry.list_capabilities()
    assert "mod-ocr" in all_caps


@pytest.mark.asyncio
async def test_definition_manager():
    dm = VerificationDefinitionManager()
    spec = await dm.create_definition(
        spec_id="spec-v1",
        name="OCR Verification Spec",
        invariants=["accuracy > 0.95", "latency < 200ms"],
        parameters={"dataset": "ds-prod-sample"}
    )
    assert spec["spec_id"] == "spec-v1"
    assert len(spec["invariants"]) == 2
    
    val = await dm.validate_definition("spec-v1")
    assert val["valid"] is True
    
    retrieved = await dm.get_definition("spec-v1")
    assert retrieved["name"] == "OCR Verification Spec"


@pytest.mark.asyncio
async def test_execution_engine():
    engine = VerificationExecutionEngine()
    result = await engine.execute_task(
        task_id="task-01",
        executable=lambda: {"processed": 100, "success": 99},
        context={"env": "staging"}
    )
    assert result["status"] == "COMPLETED"
    assert result["task_id"] == "task-01"
    assert result["result"]["processed"] == 100


@pytest.mark.asyncio
async def test_dataset_manager():
    dm = DatasetManager()
    data_content = b"sample document payload for verification"
    ds = await dm.register_dataset(
        dataset_id="ds-01",
        category="golden",
        content_or_uri=data_content,
        metadata={"rows": 1}
    )
    assert ds["category"] == "golden"
    assert len(ds["hash"]) == 64  # SHA256
    
    integrity = await dm.verify_integrity("ds-01", data_content)
    assert integrity is True
    
    integrity_fail = await dm.verify_integrity("ds-01", b"tampered content")
    assert integrity_fail is False


@pytest.mark.asyncio
async def test_environment_manager():
    em = EnvironmentManager()
    env = await em.register_environment(
        env_id="env-preprod",
        tier="preprod",
        profile={"gpu": "A100", "cpu_cores": 32, "ram_gb": 128}
    )
    assert env["tier"] == "preprod"
    
    readiness = await em.validate_readiness("env-preprod")
    assert readiness["ready"] is True
    assert readiness["hardware_profile"]["gpu"] == "A100"


@pytest.mark.asyncio
async def test_configuration_manager():
    cm = ConfigurationManager()
    cfg = await cm.resolve_configuration(
        run_id="run-cfg-1",
        tier_overrides={"timeout_seconds": 60, "threshold": 0.98}
    )
    assert cfg["timeout_seconds"] == 60
    assert cfg["threshold"] == 0.98
    assert "snapshot_hash" in cfg
    
    snapshot = await cm.get_snapshot("run-cfg-1")
    assert snapshot["run_id"] == "run-cfg-1"


@pytest.mark.asyncio
async def test_evidence_manager():
    em = EvidenceManager()
    sample_evidence = b"Evidence report text content"
    evidence = await em.record_evidence(
        evidence_id="evi-101",
        run_id="run-101",
        tier="hot",
        content=sample_evidence,
        tags=["ocr", "raw_output"]
    )
    assert evidence["evidence_id"] == "evi-101"
    assert evidence["retention_tier"] == "hot"
    assert evidence["size_bytes"] == len(sample_evidence)
    assert len(evidence["cas_hash"]) == 64
    
    retrieved = await em.get_evidence("evi-101")
    assert retrieved["content"] == sample_evidence


@pytest.mark.asyncio
async def test_metrics_engine():
    me = MetricsEngine()
    await me.record_metric("run-m-1", "accuracy", 0.985, "ai_quality")
    await me.record_metric("run-m-1", "latency_ms", 45.2, "performance")
    
    metrics = await me.get_metrics("run-m-1")
    assert len(metrics) == 2
    assert metrics["accuracy"]["value"] == 0.985
    assert metrics["accuracy"]["category"] == "ai_quality"


@pytest.mark.asyncio
async def test_statistical_analysis_engine():
    sae = StatisticalAnalysisEngine()
    data_points = [0.94, 0.95, 0.96, 0.95, 0.97, 0.96, 0.95, 0.98]
    stats = await sae.analyze_distribution(data_points)
    assert stats["sample_size"] == 8
    assert stats["mean"] > 0.95
    assert stats["stddev"] > 0
    assert "ci_95_lower" in stats
    assert "ci_95_upper" in stats
    assert stats["ci_95_lower"] <= stats["mean"] <= stats["ci_95_upper"]
    
    # Test insufficient samples handling (< 5 samples)
    small_stats = await sae.analyze_distribution([0.95, 0.96])
    assert small_stats["confidence_reliable"] is False


@pytest.mark.asyncio
async def test_quality_gate_engine():
    qge = QualityGateEngine()
    metrics = {"accuracy": 0.97, "latency_ms": 120.0}
    rules = [
        {"metric": "accuracy", "operator": ">=", "threshold": 0.95, "severity": "hard_blocker"},
        {"metric": "latency_ms", "operator": "<=", "threshold": 200.0, "severity": "soft_blocker"}
    ]
    eval_result = await qge.evaluate_gates(metrics, rules)
    assert eval_result["passed"] is True
    assert eval_result["composite_score"] == 1.0
    
    # Failing gate test
    failing_metrics = {"accuracy": 0.89, "latency_ms": 120.0}
    eval_fail = await qge.evaluate_gates(failing_metrics, rules)
    assert eval_fail["passed"] is False
    assert len(eval_fail["blockers"]) == 1


@pytest.mark.asyncio
async def test_certification_engine():
    ce = CertificationEngine()
    cert = await ce.issue_certificate(
        run_id="run-cert-1",
        level="production_ready",
        metadata={"approver": "lead_architect", "score": 0.99}
    )
    assert cert["level"] == "production_ready"
    assert cert["status"] == "active"
    assert "digital_signature_hash" in cert
    assert len(cert["digital_signature_hash"]) == 64
    
    # Revocation
    revocation = await ce.revoke_certificate(cert["certificate_id"], "Discovered regression in edge cases")
    assert revocation["status"] == "revoked"
    assert revocation["reason"] == "Discovered regression in edge cases"


@pytest.mark.asyncio
async def test_reporting_engine():
    re = ReportingEngine()
    summary = {
        "run_id": "run-rep-1",
        "passed": True,
        "metrics": {"accuracy": 0.98},
        "score": 0.98
    }
    report = await re.generate_report("run-rep-1", "executive", summary)
    assert report["format"] == "executive"
    assert report["run_id"] == "run-rep-1"
    assert "Executive Verification Summary" in report["content"]


@pytest.mark.asyncio
async def test_audit_manager_hash_chain():
    am = AuditManager()
    
    # Genesis event
    evt1 = await am.log_event(
        event_type="LIFECYCLE_INITIALIZED",
        actor="system",
        payload={"run_id": "run-audit-1", "spec": "spec-1"}
    )
    assert evt1["sequence"] == 1
    assert evt1["previous_hash"] == "0000000000000000000000000000000000000000000000000000000000000000"
    
    # Second event in chain
    evt2 = await am.log_event(
        event_type="TASK_EXECUTED",
        actor="execution_engine",
        payload={"task_id": "task-01", "status": "SUCCESS"}
    )
    assert evt2["sequence"] == 2
    assert evt2["previous_hash"] == evt1["record_hash"]
    
    # Verify chain integrity
    is_valid = am.verify_chain_integrity()
    assert is_valid is True


@pytest.mark.asyncio
async def test_traceability_manager_lineage():
    tm = TraceabilityManager()
    await tm.link_nodes("objective-1", "spec-1", "DEFINES_SPEC")
    await tm.link_nodes("spec-1", "run-1", "EXECUTES_SPEC")
    await tm.link_nodes("run-1", "cert-1", "PRODUCES_CERT")
    
    lineage = await tm.get_lineage("objective-1")
    assert len(lineage) == 3
    assert lineage[0]["to"] == "spec-1"
    assert lineage[1]["to"] == "run-1"
    assert lineage[2]["to"] == "cert-1"


@pytest.mark.asyncio
async def test_plugin_manager():
    pm = PluginManager()
    reg = await pm.register_plugin(
        plugin_id="plugin-llm-eval",
        name="LLM Semantic Evaluator",
        capabilities=["semantic_similarity", "hallucination_detection"]
    )
    assert reg["plugin_id"] == "plugin-llm-eval"
    
    active = await pm.list_active_plugins()
    assert len(active) == 1
    assert active[0]["name"] == "LLM Semantic Evaluator"


@pytest.mark.asyncio
async def test_full_enterprise_runtime_pipeline():
    """End-to-end orchestration test exercising the entire enterprise runtime across all 16 components."""
    runtime = EnterpriseVerificationRuntime()
    
    # 1. Register Capability & Plugin
    await runtime.plugin_manager.register_plugin("p-ocr", "OCR Analyzer", ["ocr_extraction"])
    await runtime.registry.register_capability("mod-ocr", "ocr_extraction", "1.0.0")
    
    # 2. Register Environment & Dataset
    await runtime.environment_manager.register_environment("env-prod", "production", {"cpu": 16})
    sample_dataset = b"doc1,doc2,doc3"
    await runtime.dataset_manager.register_dataset("ds-golden-1", "golden", sample_dataset)
    
    # 3. Create Verification Definition
    spec = await runtime.definition_manager.create_definition(
        spec_id="spec-doc-eval",
        name="Production Document Pipeline Verification",
        invariants=["accuracy >= 0.95"],
        parameters={"dataset": "ds-golden-1"}
    )
    
    # 4. Resolve Configuration
    run_id = "run-e2e-2026"
    cfg = await runtime.configuration_manager.resolve_configuration(run_id, {"tier": "production"})
    
    # 5. Initialize Lifecycle & Audit
    await runtime.orchestrator.initialize_lifecycle(run_id, spec["spec_id"])
    await runtime.audit_manager.log_event("RUN_INITIALIZED", "orchestrator", {"run_id": run_id, "config": cfg})
    await runtime.traceability_manager.link_nodes("req-accuracy", spec["spec_id"], "SPECIFIES")
    await runtime.traceability_manager.link_nodes(spec["spec_id"], run_id, "EXECUTES")
    
    # 6. Execute Task & Record Evidence
    await runtime.orchestrator.transition_state(run_id, "EXECUTING")
    exec_result = await runtime.execution_engine.execute_task(
        "task-ocr-batch",
        lambda: {"items_evaluated": 100, "correct": 98, "accuracies": [0.97, 0.98, 0.99, 0.98, 0.98, 0.97]}
    )
    await runtime.evidence_manager.record_evidence(
        "evi-ocr-raw",
        run_id,
        "warm",
        b'{"items": 100, "correct": 98}'
    )
    
    # 7. Compute Metrics & Statistical Distribution
    accuracies = exec_result["result"]["accuracies"]
    stats = await runtime.statistical_analysis_engine.analyze_distribution(accuracies)
    await runtime.metrics_engine.record_metric(run_id, "accuracy", stats["mean"], "ai_quality")
    await runtime.metrics_engine.record_metric(run_id, "ci_95_lower", stats["ci_95_lower"], "ai_quality")
    
    # 8. Evaluate Quality Gate
    metrics_dict = {
        "accuracy": stats["mean"],
        "ci_95_lower": stats["ci_95_lower"]
    }
    gate_rules = [
        {"metric": "accuracy", "operator": ">=", "threshold": 0.95, "severity": "hard_blocker"},
        {"metric": "ci_95_lower", "operator": ">=", "threshold": 0.90, "severity": "hard_blocker"}
    ]
    gate_eval = await runtime.quality_gate_engine.evaluate_gates(metrics_dict, gate_rules)
    assert gate_eval["passed"] is True
    
    # 9. Issue Certification
    cert = await runtime.certification_engine.issue_certificate(run_id, "production_ready", {"score": stats["mean"]})
    await runtime.traceability_manager.link_nodes(run_id, cert["certificate_id"], "CERTIFIES")
    
    # 10. Generate Reports & Seal Audit Hash Chain
    await runtime.reporting_engine.generate_report(run_id, "executive", {"summary": "Passed all gates"})
    await runtime.audit_manager.log_event("RUN_CERTIFIED", "certification_engine", {"certificate_id": cert["certificate_id"]})
    await runtime.orchestrator.transition_state(run_id, "COMPLETED")
    
    # 11. Final Verifications
    chain_valid = runtime.audit_manager.verify_chain_integrity()
    assert chain_valid is True
    
    lineage = await runtime.traceability_manager.get_lineage("req-accuracy")
    assert len(lineage) == 3
    assert lineage[2]["to"] == cert["certificate_id"]
    
    run_status = await runtime.orchestrator.get_status(run_id)
    assert run_status["state"] == "COMPLETED"
