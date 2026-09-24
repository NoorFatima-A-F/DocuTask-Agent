"""
SQLAlchemy 2.0 Declarative Persistence Models for Verification Platform.
"""
from typing import Any, Dict, List, Optional
from sqlalchemy import (
    String, Integer, Float, Boolean, ForeignKey, Text, JSON
)
from sqlalchemy.orm import Mapped, mapped_column
from app.platform_verification.domain_model.persistence.database import VerificationBase


class DBVerificationDefinition(VerificationBase):
    __tablename__ = "vp_verification_definitions"

    definition_id: Mapped[str] = mapped_column(String(64), primary_key=True, index=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True, default="default-tenant")
    name: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[str] = mapped_column(Text)
    category: Mapped[str] = mapped_column(String(64), index=True)
    verification_type: Mapped[str] = mapped_column(String(64))
    owner: Mapped[str] = mapped_column(String(128))
    priority: Mapped[int] = mapped_column(Integer, default=1)
    risk_level: Mapped[str] = mapped_column(String(32))
    status: Mapped[str] = mapped_column(String(32), default="DRAFT", index=True)
    semantic_version: Mapped[str] = mapped_column(String(32), default="1.0.0")
    objective: Mapped[str] = mapped_column(Text)
    requirements_json: Mapped[Dict[str, Any]] = mapped_column(JSON, default=list)
    required_datasets_json: Mapped[List[str]] = mapped_column(JSON, default=list)
    required_plugins_json: Mapped[List[str]] = mapped_column(JSON, default=list)
    created_at: Mapped[str] = mapped_column(String(64))
    updated_at: Mapped[str] = mapped_column(String(64))


class DBVerificationPlan(VerificationBase):
    __tablename__ = "vp_verification_plans"

    plan_id: Mapped[str] = mapped_column(String(64), primary_key=True, index=True)
    definition_id: Mapped[str] = mapped_column(String(64), ForeignKey("vp_verification_definitions.definition_id"), index=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True, default="default-tenant")
    version: Mapped[str] = mapped_column(String(32), default="1.0.0")
    execution_strategy: Mapped[str] = mapped_column(String(64))
    parallelism: Mapped[int] = mapped_column(Integer, default=4)
    timeout_policy_json: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    retry_policy_json: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    resource_requirements_json: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    created_at: Mapped[str] = mapped_column(String(64))


class DBDataset(VerificationBase):
    __tablename__ = "vp_datasets"

    dataset_id: Mapped[str] = mapped_column(String(64), primary_key=True, index=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True, default="default-tenant")
    name: Mapped[str] = mapped_column(String(255), index=True)
    purpose: Mapped[str] = mapped_column(Text)
    classification: Mapped[str] = mapped_column(String(64), index=True)
    owner: Mapped[str] = mapped_column(String(128))
    source: Mapped[str] = mapped_column(String(255))
    current_version: Mapped[str] = mapped_column(String(32), default="1.0.0")
    created_at: Mapped[str] = mapped_column(String(64))


class DBDatasetVersion(VerificationBase):
    __tablename__ = "vp_dataset_versions"

    dataset_version_id: Mapped[str] = mapped_column(String(64), primary_key=True, index=True)
    dataset_id: Mapped[str] = mapped_column(String(64), ForeignKey("vp_datasets.dataset_id"), index=True)
    semantic_version: Mapped[str] = mapped_column(String(32), default="1.0.0")
    checksum_sha256: Mapped[str] = mapped_column(String(64), index=True)
    item_count: Mapped[int] = mapped_column(Integer, default=100)
    size_bytes: Mapped[int] = mapped_column(Integer, default=1024)
    storage_location: Mapped[str] = mapped_column(String(512))
    integrity_status: Mapped[str] = mapped_column(String(64), default="VERIFIED")
    lineage_json: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    creator: Mapped[str] = mapped_column(String(128))
    created_at: Mapped[str] = mapped_column(String(64))


class DBEnvironmentSnapshot(VerificationBase):
    __tablename__ = "vp_environment_snapshots"

    snapshot_id: Mapped[str] = mapped_column(String(64), primary_key=True, index=True)
    environment_id: Mapped[str] = mapped_column(String(64), index=True)
    tier: Mapped[str] = mapped_column(String(64), index=True)
    operating_system: Mapped[str] = mapped_column(String(128))
    runtime_version: Mapped[str] = mapped_column(String(64))
    container_image_digest: Mapped[str] = mapped_column(String(128))
    infrastructure_version: Mapped[str] = mapped_column(String(64))
    dependency_fingerprint_sha256: Mapped[str] = mapped_column(String(64), index=True)
    git_commit_sha: Mapped[str] = mapped_column(String(64), index=True)
    hardware_profile_json: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    created_at: Mapped[str] = mapped_column(String(64))


class DBConfigurationSnapshot(VerificationBase):
    __tablename__ = "vp_configuration_snapshots"

    snapshot_id: Mapped[str] = mapped_column(String(64), primary_key=True, index=True)
    configuration_id: Mapped[str] = mapped_column(String(64), index=True)
    canonical_hash_sha256: Mapped[str] = mapped_column(String(64), index=True)
    resolved_values: Mapped[Dict[str, Any]] = mapped_column(JSON)
    is_frozen: Mapped[bool] = mapped_column(Boolean, default=True)
    created_by: Mapped[str] = mapped_column(String(128))
    created_at: Mapped[str] = mapped_column(String(64))


class DBVerificationExecution(VerificationBase):
    __tablename__ = "vp_verification_executions"

    execution_id: Mapped[str] = mapped_column(String(64), primary_key=True, index=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True, default="default-tenant")
    verification_definition_id: Mapped[str] = mapped_column(String(64), ForeignKey("vp_verification_definitions.definition_id"), index=True)
    plan_id: Mapped[str] = mapped_column(String(64), ForeignKey("vp_verification_plans.plan_id"), index=True)
    dataset_version_id: Mapped[str] = mapped_column(String(64), ForeignKey("vp_dataset_versions.dataset_version_id"), index=True)
    environment_snapshot_id: Mapped[str] = mapped_column(String(64), ForeignKey("vp_environment_snapshots.snapshot_id"), index=True)
    configuration_snapshot_id: Mapped[str] = mapped_column(String(64), ForeignKey("vp_configuration_snapshots.snapshot_id"), index=True)
    status: Mapped[str] = mapped_column(String(32), default="CREATED", index=True)
    started_at: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    completed_at: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    duration_ms: Mapped[float] = mapped_column(Float, default=0.0)
    triggered_by: Mapped[str] = mapped_column(String(128))
    created_at: Mapped[str] = mapped_column(String(64))


class DBEvidenceArtifact(VerificationBase):
    __tablename__ = "vp_evidence_artifacts"

    evidence_id: Mapped[str] = mapped_column(String(64), primary_key=True, index=True)
    execution_id: Mapped[str] = mapped_column(String(64), ForeignKey("vp_verification_executions.execution_id"), index=True)
    evidence_type: Mapped[str] = mapped_column(String(64), index=True)
    storage_location: Mapped[str] = mapped_column(String(512))
    content_hash_sha256: Mapped[str] = mapped_column(String(64), index=True)
    size_bytes: Mapped[int] = mapped_column(Integer)
    integrity_status: Mapped[str] = mapped_column(String(64), default="VERIFIED_SEALED")
    metadata_json: Mapped[Dict[str, Any]] = mapped_column(JSON, default=dict)
    created_at: Mapped[str] = mapped_column(String(64))


class DBMetricResult(VerificationBase):
    __tablename__ = "vp_metric_results"

    result_id: Mapped[str] = mapped_column(String(64), primary_key=True, index=True)
    execution_id: Mapped[str] = mapped_column(String(64), ForeignKey("vp_verification_executions.execution_id"), index=True)
    metric_id: Mapped[str] = mapped_column(String(64), index=True)
    metric_name: Mapped[str] = mapped_column(String(128), index=True)
    category: Mapped[str] = mapped_column(String(64), index=True)
    value: Mapped[float] = mapped_column(Float)
    unit: Mapped[str] = mapped_column(String(32))
    confidence_score: Mapped[float] = mapped_column(Float, default=1.0)
    passed: Mapped[bool] = mapped_column(Boolean, default=True)
    calculated_at: Mapped[str] = mapped_column(String(64))


class DBQualityDecision(VerificationBase):
    __tablename__ = "vp_quality_decisions"

    decision_id: Mapped[str] = mapped_column(String(64), primary_key=True, index=True)
    execution_id: Mapped[str] = mapped_column(String(64), ForeignKey("vp_verification_executions.execution_id"), index=True)
    gate_id: Mapped[str] = mapped_column(String(64), index=True)
    gate_name: Mapped[str] = mapped_column(String(128))
    outcome: Mapped[str] = mapped_column(String(32), index=True)
    composite_score: Mapped[float] = mapped_column(Float)
    passed_requirements_count: Mapped[int] = mapped_column(Integer)
    failed_requirements_count: Mapped[int] = mapped_column(Integer)
    reason: Mapped[str] = mapped_column(Text)
    evaluated_at: Mapped[str] = mapped_column(String(64))


class DBCertification(VerificationBase):
    __tablename__ = "vp_certifications"

    certification_id: Mapped[str] = mapped_column(String(64), primary_key=True, index=True)
    execution_id: Mapped[str] = mapped_column(String(64), ForeignKey("vp_verification_executions.execution_id"), index=True)
    verification_definition_id: Mapped[str] = mapped_column(String(64), ForeignKey("vp_verification_definitions.definition_id"), index=True)
    level: Mapped[str] = mapped_column(String(64), index=True)
    composite_quality_score: Mapped[float] = mapped_column(Float)
    evidence_bundle_hash: Mapped[str] = mapped_column(String(64), index=True)
    approved_by: Mapped[str] = mapped_column(String(128))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    issued_at: Mapped[str] = mapped_column(String(64))
    expiration_date: Mapped[str] = mapped_column(String(64))
    revocation_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)


class DBAuditRecord(VerificationBase):
    __tablename__ = "vp_audit_records"

    audit_id: Mapped[str] = mapped_column(String(64), primary_key=True, index=True)
    entity_type: Mapped[str] = mapped_column(String(64), index=True)
    entity_id: Mapped[str] = mapped_column(String(64), index=True)
    action: Mapped[str] = mapped_column(String(32), index=True)
    actor: Mapped[str] = mapped_column(String(128))
    previous_state: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    new_state: Mapped[Dict[str, Any]] = mapped_column(JSON)
    previous_hash: Mapped[str] = mapped_column(String(64))
    record_hash: Mapped[str] = mapped_column(String(64), index=True)
    timestamp: Mapped[str] = mapped_column(String(64))
