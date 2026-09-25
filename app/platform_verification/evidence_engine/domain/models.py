"""
Domain Models for Enterprise Verification Evidence Collection, Traceability & Audit Architecture (PART 4).
"""
from __future__ import annotations
import hashlib
import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class EvidenceCategory(str, Enum):
    EXECUTION_EVIDENCE = "EXECUTION_EVIDENCE"
    INPUT_EVIDENCE = "INPUT_EVIDENCE"
    RUNTIME_EVIDENCE = "RUNTIME_EVIDENCE"
    OUTPUT_EVIDENCE = "OUTPUT_EVIDENCE"
    EVALUATION_EVIDENCE = "EVALUATION_EVIDENCE"
    HUMAN_REVIEW_EVIDENCE = "HUMAN_REVIEW_EVIDENCE"


class EvidenceLifecycleState(str, Enum):
    CREATED = "CREATED"
    VALIDATED = "VALIDATED"
    ACTIVE = "ACTIVE"
    CERTIFIED = "CERTIFIED"
    ARCHIVED = "ARCHIVED"
    DELETED = "DELETED"


class EvidenceClassification(str, Enum):
    PUBLIC = "PUBLIC"
    INTERNAL = "INTERNAL"
    CONFIDENTIAL = "CONFIDENTIAL"
    RESTRICTED = "RESTRICTED"


class EvidenceRole(str, Enum):
    DEVELOPER = "DEVELOPER"
    REVIEWER = "REVIEWER"
    AUDITOR = "AUDITOR"
    ADMINISTRATOR = "ADMINISTRATOR"


class LineageRelation(str, Enum):
    GENERATED_BY = "generated_by"
    DERIVED_FROM = "derived_from"
    EVALUATED_BY = "evaluated_by"
    APPROVED_BY = "approved_by"
    SUPERSEDED_BY = "superseded_by"


class EvidenceArtifact(BaseModel):
    artifact_id: str = Field(default_factory=lambda: f"art_{uuid.uuid4().hex[:10]}")
    execution_id: str
    category: EvidenceCategory
    producer: str = "Verification Execution Engine"
    version: str = "1.0.0"
    content_type: str = "application/json"
    checksum_sha256: str
    storage_uri: str
    classification: EvidenceClassification = EvidenceClassification.INTERNAL
    lifecycle_state: EvidenceLifecycleState = EvidenceLifecycleState.ACTIVE
    metadata: Dict[str, Any] = Field(default_factory=dict)
    retention_days: int = 2555  # 7 years for enterprise compliance
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class IntegrityRecord(BaseModel):
    artifact_id: str
    hash: str
    algorithm: str = "SHA-256"
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    verified: bool = True


class EvidenceContext(BaseModel):
    execution_id: str
    test_id: str
    environment: str
    dataset_version: str
    configuration_hash: str
    model_version: str
    artifact_registry: List[str] = Field(default_factory=list)


class AiDecisionEvidence(BaseModel):
    model_info: Dict[str, Any] = Field(default_factory=dict)       # provider, name, version, params
    prompt_info: Dict[str, Any] = Field(default_factory=dict)      # system, user, template_ver
    context_info: Dict[str, Any] = Field(default_factory=dict)     # retrieved_docs, embeddings, ranking
    tool_calls: List[Dict[str, Any]] = Field(default_factory=list) # tool name, params, outputs
    permitted_reasoning: Dict[str, Any] = Field(default_factory=dict) # decision summaries, confidence


class ValidationReport(BaseModel):
    is_valid: bool
    completeness: bool
    integrity_verified: bool
    consistency: bool
    authenticity: bool
    security_passed: bool
    issues: List[str] = Field(default_factory=list)
    validated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ExecutionTraceSpan(BaseModel):
    span_id: str = Field(default_factory=lambda: f"span_{uuid.uuid4().hex[:8]}")
    trace_id: str
    parent_span_id: Optional[str] = None
    name: str
    kind: str = "INTERNAL"  # INTERNAL, AGENT_TOOL, WORKFLOW_STEP, LLM_CALL
    start_time_iso: str
    end_time_iso: str
    duration_ms: float
    status_code: str = "OK"
    attributes: Dict[str, Any] = Field(default_factory=dict)
    events: List[Dict[str, Any]] = Field(default_factory=list)


class AuditEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: f"aud_{uuid.uuid4().hex[:10]}")
    actor: str
    action: str  # Past-tense: EvidenceCreated, EvidenceUpdated, EvidenceAccessed, EvidenceVerified, EvidenceExported, CertificationGenerated
    resource: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    previous_state: Optional[str] = None
    new_state: Optional[str] = None
    details: Dict[str, Any] = Field(default_factory=dict)
    event_signature: str = ""

    def compute_signature(self) -> str:
        payload = f"{self.event_id}:{self.actor}:{self.action}:{self.resource}:{self.timestamp}:{self.new_state}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def __init__(self, **data):
        super().__init__(**data)
        if not self.event_signature:
            self.event_signature = self.compute_signature()


class EvidenceLineageNode(BaseModel):
    node_id: str
    node_type: str  # DATASET, TEST_DEFINITION, EXECUTION, MODEL, PROMPT, OUTPUT, METRICS, CERTIFICATION
    attributes: Dict[str, Any] = Field(default_factory=dict)
    parents: List[str] = Field(default_factory=list)
    children: List[str] = Field(default_factory=list)
    relations: Dict[str, str] = Field(default_factory=dict)  # parent_id -> relation_type
    checksum: str = ""


class CertificationEvidencePackage(BaseModel):
    package_id: str = Field(default_factory=lambda: f"pkg_{uuid.uuid4().hex[:12]}")
    verification_id: str
    execution_id: str
    verification_definition_id: str
    environment_snapshot_id: str
    dataset_snapshot_id: str
    configuration_snapshot_id: str
    execution_trace_id: str
    metrics_report: Dict[str, Any]
    raw_artifacts_uris: List[str]
    evaluation_decision: Dict[str, Any]
    approval_records: List[Dict[str, Any]] = Field(default_factory=list)
    package_manifest_hash: str
    compiled_by: str = "Certification Authority Workflow"
    compiled_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
