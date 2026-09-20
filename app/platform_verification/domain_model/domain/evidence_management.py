"""
Evidence Domain: Content-Addressable Storage (CAS), Artifacts, Retention Policies, and Lineage Proof.
"""
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field
import uuid


class EvidenceType(str, Enum):
    LOGS = "LOGS"
    SCREENSHOT = "SCREENSHOT"
    DOCUMENT = "DOCUMENT"
    TRACE = "TRACE"
    API_RESPONSE = "API_RESPONSE"
    PROMPT = "PROMPT"
    MODEL_OUTPUT = "MODEL_OUTPUT"
    EVALUATION_MATRIX = "EVALUATION_MATRIX"


class RetentionPolicy(str, Enum):
    HOT_30_DAYS = "HOT_30_DAYS"
    WARM_1_YEAR = "WARM_1_YEAR"
    COLD_COMPLIANCE_7_YEARS = "COLD_COMPLIANCE_7_YEARS"
    PERMANENT_GOLDEN = "PERMANENT_GOLDEN"


class EvidenceMetadata(BaseModel):
    source_service: str = "DocuTask Verification Runner"
    creator_identity: str = "WorkerNode-01"
    classification_level: str = "CONFIDENTIAL"
    retention_policy: RetentionPolicy = RetentionPolicy.WARM_1_YEAR
    custom_tags: Dict[str, str] = Field(default_factory=dict)


class EvidenceArtifact(BaseModel):
    evidence_id: str = Field(default_factory=lambda: f"evi_{uuid.uuid4().hex[:8]}")
    execution_id: str
    evidence_type: EvidenceType
    storage_location: str  # cas://evidence/sha256/...
    content_hash_sha256: str
    size_bytes: int
    integrity_status: str = "VERIFIED_SEALED"
    metadata: EvidenceMetadata = Field(default_factory=EvidenceMetadata)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
