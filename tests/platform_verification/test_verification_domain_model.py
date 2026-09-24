"""
Comprehensive Unit & Integration Test Suite for Part 1.2:
Enterprise Verification Domain Model & Data Architecture (EV-DMDA).
"""
from app.platform_verification.domain_model.domain.verification_management import (
    VerificationDefinition, VerificationRequirement, VerificationCategory, VerificationStatus, RequirementSeverity
)
from app.platform_verification.domain_model.domain.verification_plan import (
    VerificationPlan, ExecutionStrategy, TimeoutPolicy, RetryPolicy
)
from app.platform_verification.domain_model.domain.dataset_management import (
    Dataset, DatasetVersion, DatasetClassification, DatasetLineage
)
from app.platform_verification.domain_model.domain.environment_management import (
    EnvironmentSnapshot, EnvironmentType, HardwareProfile
)
from app.platform_verification.domain_model.domain.configuration_management import (
    ConfigurationSnapshot
)
from app.platform_verification.domain_model.domain.execution_management import (
    VerificationExecution, ExecutionState, ExecutionAttempt
)
from app.platform_verification.domain_model.domain.evidence_management import (
    EvidenceArtifact, EvidenceType, EvidenceMetadata, RetentionPolicy
)
from app.platform_verification.domain_model.domain.metrics_management import (
    MetricResult, MetricCategory
)
from app.platform_verification.domain_model.domain.statistical_evaluation import (
    StatisticalAnalysis
)
from app.platform_verification.domain_model.domain.quality_management import (
    QualityGate, QualityDecision, QualityDecisionOutcome, GateSeverity
)
from app.platform_verification.domain_model.domain.certification_management import (
    Certification, CertificationLevel
)
from app.platform_verification.domain_model.lineage.evidence_graph import evidence_graph_engine
from app.platform_verification.domain_model.persistence.repositories.in_memory_repos import VerificationDomainRepository


def test_verification_definition_and_requirements():
    req1 = VerificationRequirement(
        metric_name="exact_match_accuracy",
        operator=">=",
        target_threshold=0.98,
        severity=RequirementSeverity.CRITICAL
    )
    req2 = VerificationRequirement(
        metric_name="p95_latency_seconds",
        operator="<=",
        target_threshold=1.5,
        severity=RequirementSeverity.HIGH
    )

    vdef = VerificationDefinition(
        name="Contract Extraction Validation",
        description="Validates key-value extraction accuracy for commercial contracts.",
        category=VerificationCategory.AI_QUALITY,
        objective="Ensure 98% accuracy on legal entities.",
        requirements=[req1, req2]
    )

    assert vdef.status == VerificationStatus.DRAFT
    assert len(vdef.requirements) == 2
    assert vdef.requirements[0].target_threshold == 0.98

    vdef.approve(approver="VP of AI Quality")
    assert vdef.status == VerificationStatus.APPROVED

    vdef.deprecate()
    assert vdef.status == VerificationStatus.DEPRECATED


def test_verification_plan_strategy_and_policies():
    plan = VerificationPlan(
        definition_id="vdef_contract_01",
        execution_strategy=ExecutionStrategy.PARALLEL,
        parallelism=16,
        timeout_policy=TimeoutPolicy(max_total_timeout_seconds=900),
        retry_policy=RetryPolicy(max_attempts=5)
    )

    assert plan.execution_strategy == ExecutionStrategy.PARALLEL
    assert plan.parallelism == 16
    assert plan.timeout_policy.max_total_timeout_seconds == 900
    assert plan.retry_policy.max_attempts == 5
    assert "NETWORK_TIMEOUT" in plan.retry_policy.retryable_errors


def test_dataset_classification_and_lineage():
    dset = Dataset(
        name="Adversarial Prompt Injection Corpus",
        purpose="Testing model resilience to multi-turn jailbreaks.",
        classification=DatasetClassification.ADVERSARIAL
    )
    assert dset.classification == DatasetClassification.ADVERSARIAL

    lineage = DatasetLineage(
        dataset_version_id="dver_adv_v1",
        original_sources=["HuggingFace RedTeam Bench", "Internal Synthetic Fuzzer"],
        transformation_pipeline=["Token Normalization", "PII Stripping"],
        anonymization_applied=True
    )

    dver = DatasetVersion(
        dataset_id=dset.dataset_id,
        semantic_version="1.0.0",
        checksum_sha256="b8c7d6e5f4a3b2c1" * 4,
        item_count=1200,
        lineage=lineage
    )

    assert dver.lineage is not None
    assert dver.lineage.anonymization_applied is True
    assert len(dver.lineage.original_sources) == 2


def test_environment_and_configuration_snapshots():
    # 1. Environment Snapshot
    env_snap = EnvironmentSnapshot(
        environment_id="env_staging_cluster",
        tier=EnvironmentType.STAGING,
        operating_system="Linux 6.8 x86_64",
        hardware_profile=HardwareProfile(cpu_cores=16, ram_gb=64.0, gpu_count=2)
    )
    assert env_snap.tier == EnvironmentType.STAGING
    assert env_snap.hardware_profile.gpu_count == 2
    assert env_snap.operating_system == "Linux 6.8 x86_64"

    # 2. Configuration Snapshot
    cfg_snap = ConfigurationSnapshot(
        configuration_id="cfg_ai_eval_prod",
        canonical_hash_sha256="1234567890abcdef" * 4,
        resolved_values={"temperature": 0.0, "top_p": 0.9, "max_tokens": 4096}
    )
    assert cfg_snap.is_frozen is True
    assert cfg_snap.resolved_values["temperature"] == 0.0


def test_execution_lifecycle_state_machine():
    execution = VerificationExecution(
        verification_definition_id="vdef_sample",
        plan_id="vplan_sample",
        dataset_version_id="dver_sample",
        environment_snapshot_id="env_snap_sample",
        configuration_snapshot_id="cfg_snap_sample"
    )
    assert execution.status == ExecutionState.CREATED

    execution.start()
    assert execution.status == ExecutionState.RUNNING
    assert execution.started_at is not None

    execution.complete()
    assert execution.status == ExecutionState.COMPLETED
    assert execution.completed_at is not None

    # Retry attempt recording
    attempt = ExecutionAttempt(
        execution_id=execution.execution_id,
        attempt_number=1,
        is_success=True,
        duration_ms=4520.0
    )
    execution.attempts.append(attempt)
    assert len(execution.attempts) == 1


def test_evidence_artifact_cas_and_retention():
    evidence = EvidenceArtifact(
        execution_id="exec_999",
        evidence_type=EvidenceType.API_RESPONSE,
        storage_location="cas://evidence/sha256/response_999.json",
        content_hash_sha256="abcdef1234567890" * 4,
        size_bytes=8192,
        metadata=EvidenceMetadata(
            classification_level="RESTRICTED",
            retention_policy=RetentionPolicy.COLD_COMPLIANCE_7_YEARS
        )
    )

    assert evidence.integrity_status == "VERIFIED_SEALED"
    assert evidence.metadata.retention_policy == RetentionPolicy.COLD_COMPLIANCE_7_YEARS
    assert evidence.evidence_type == EvidenceType.API_RESPONSE


def test_metrics_and_statistical_evaluation():
    # 1. Metric results across multiple categories
    m1 = MetricResult(
        execution_id="exec_stat_test",
        metric_id="m_faithfulness",
        metric_name="rag_faithfulness",
        category=MetricCategory.AI_QUALITY,
        value=0.965,
        unit="ratio"
    )
    m2 = MetricResult(
        execution_id="exec_stat_test",
        metric_id="m_latency_p95",
        metric_name="p95_latency",
        category=MetricCategory.PERFORMANCE,
        value=1.12,
        unit="seconds"
    )
    m3 = MetricResult(
        execution_id="exec_stat_test",
        metric_id="m_tokens",
        metric_name="token_consumption",
        category=MetricCategory.COST,
        value=14250.0,
        unit="tokens"
    )

    assert m1.category == MetricCategory.AI_QUALITY
    assert m2.category == MetricCategory.PERFORMANCE
    assert m3.category == MetricCategory.COST

    # 2. Statistical Analysis
    samples = [0.95, 0.96, 0.97, 0.94, 0.98, 0.95, 0.96, 0.97]
    analysis = StatisticalAnalysis.from_samples(
        execution_id="exec_stat_test",
        metric_name="rag_faithfulness",
        samples=samples
    )

    assert analysis.sample_size == 8
    assert analysis.mean >= 0.95
    assert analysis.variance >= 0.0
    assert analysis.ci_lower < analysis.mean < analysis.ci_upper


def test_quality_gates_and_certification():
    # 1. Quality Gate
    gate = QualityGate(
        name="Enterprise Safety & Grounding Gate",
        criteria={"min_faithfulness": 0.95, "max_hallucination": 0.01},
        severity=GateSeverity.HARD_BLOCKER
    )
    assert gate.severity == GateSeverity.HARD_BLOCKER

    # 2. Quality Decision
    qdec = QualityDecision(
        execution_id="exec_cert_test",
        gate_id=gate.gate_id,
        gate_name=gate.name,
        outcome=QualityDecisionOutcome.PASSED,
        composite_score=0.995,
        passed_requirements_count=5,
        failed_requirements_count=0
    )
    assert qdec.outcome == QualityDecisionOutcome.PASSED

    # 3. Certification
    cert = Certification(
        execution_id="exec_cert_test",
        verification_definition_id="vdef_finance_agent",
        level=CertificationLevel.ENTERPRISE_CERTIFIED,
        composite_quality_score=0.995,
        evidence_bundle_hash="bundle_sha256_xyz"
    )
    assert cert.level == CertificationLevel.ENTERPRISE_CERTIFIED
    assert cert.is_active is True

    # Revocation test
    cert.revoke("Post-deployment regression detected in canary")
    assert cert.is_active is False
    assert "regression" in cert.revocation_reason


def test_audit_records_and_tamper_evident_chain():
    repo = VerificationDomainRepository()

    rec1 = repo.append_audit_record(
        entity_type="VerificationDefinition",
        entity_id="vdef_100",
        action="CREATE",
        new_state={"name": "Test Suite"}
    )
    assert len(rec1.record_hash) == 64
    assert rec1.previous_hash == "0" * 64

    rec2 = repo.append_audit_record(
        entity_type="VerificationDefinition",
        entity_id="vdef_100",
        action="UPDATE",
        new_state={"status": "APPROVED"},
        previous_state={"status": "DRAFT"}
    )
    assert len(rec2.record_hash) == 64
    assert rec2.previous_hash == rec1.record_hash

    rec3 = repo.append_audit_record(
        entity_type="Certification",
        entity_id="cert_100",
        action="CERTIFY",
        new_state={"level": "ENTERPRISE_CERTIFIED"}
    )
    assert rec3.previous_hash == rec2.record_hash
    assert len(repo.list_audit_trail()) == 3


def test_end_to_end_evidence_graph_lineage():
    # Use seeded data from verification_domain_runtime
    cert_id = "cert_docutask_ocr_gold_2026"
    chain = evidence_graph_engine.build_provenance_chain(cert_id)

    assert chain["is_provenance_complete"] is True
    assert chain["certification"]["certification_id"] == cert_id
    assert chain["certification"]["level"] == "ENTERPRISE_CERTIFIED"
    assert chain["verification_definition"]["name"] == "Invoice OCR Extraction Invariant Suite"
    assert chain["dataset_version"]["dataset_version_id"] == "dver_invoice_v2_1"
    assert chain["execution"]["status"] == "COMPLETED"
    assert chain["evidence_count"] >= 1
    assert len(chain["metrics_evaluated"]) >= 2
    assert len(chain["quality_decisions"]) >= 1
