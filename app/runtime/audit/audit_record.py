"""
Enterprise Audit Record Schema.
Complies with banking-grade compliance, regulatory auditability, and tamper-evident hash chaining.
"""

from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from datetime import datetime, timezone


class AuditRecord(BaseModel):
    audit_id: str = Field(..., description="Unique audit record ID")
    mission_id: str = Field(..., description="Mission identifier")
    trace_id: Optional[str] = Field(default=None, description="Distributed trace ID")
    actor: str = Field(default="SYSTEM", description="Actor who initiated action (SYSTEM, WORKER, HUMAN_OPERATOR)")
    component: str = Field(..., description="Runtime subsystem component (PLANNER, WORKER, SMT_GOVERNANCE, MEMORY)")
    action: str = Field(..., description="Audited action name")
    reason: str = Field(..., description="Explicit rationale for action")
    evidence_ids: List[str] = Field(default_factory=list, description="Associated evidence IDs")
    input_payload: Dict[str, Any] = Field(default_factory=dict, description="Input parameters")
    output_payload: Dict[str, Any] = Field(default_factory=dict, description="Execution results")
    parent_event_id: Optional[str] = Field(default=None, description="Parent event ID")
    planner_generation: int = Field(default=1, description="Planner generation when action occurred")
    worker_id: Optional[str] = Field(default=None, description="Worker responsible")
    system_version: str = Field(default="v2.1-ESMR", description="System build version")
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    previous_sha256: str = Field(default="0" * 64, description="Hash pointer to previous audit record")
    sha256: Optional[str] = Field(default=None, description="Cryptographic hash of this record")
    signature: Optional[str] = Field(default=None, description="Cryptographic signature")
