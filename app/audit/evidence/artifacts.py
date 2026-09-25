"""Evidence Artifact Domain Models & Classification."""

from enum import Enum
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timezone
import uuid


class EvidenceType(str, Enum):
    AI_EVIDENCE = "AI_EVIDENCE"                # Model card, prompt template, evaluation metrics, citations
    DATA_EVIDENCE = "DATA_EVIDENCE"            # Source document hash, lineage snapshot, schema delta
    GOVERNANCE_EVIDENCE = "GOVERNANCE_EVIDENCE" # Policy rule snapshot, approval records, risk score
    EXECUTION_EVIDENCE = "EXECUTION_EVIDENCE"  # DAG trace, tool parameters, error log, latency
    SAFETY_EVIDENCE = "SAFETY_EVIDENCE"        # Injection scan result, toxicity report, PII redaction log
    COMPLIANCE_EVIDENCE = "COMPLIANCE_EVIDENCE" # Control assessment report, auditor certification


class EvidenceArtifact(BaseModel):
    """Immutable evidence artifact supporting regulatory scrutiny."""
    evidence_id: str = Field(default_factory=lambda: f"evi_{uuid.uuid4().hex[:12]}")
    tenant_id: str
    name: str
    evidence_type: EvidenceType
    source: str  # e.g., "model_registry", "workflow_engine", "safety_gateway"
    related_event_ids: List[str] = Field(default_factory=list)
    content_hash: str
    storage_location: Optional[str] = None
    classification: str = "CONFIDENTIAL"
    retention_policy_id: Optional[str] = None
    owner: str = "system"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)
