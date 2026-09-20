"""Immutable Oversight Execution Context."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timezone
import uuid


class OversightContext(BaseModel):
    """Comprehensive, immutable context describing the AI decision or action under human oversight."""
    request_id: str = Field(default_factory=lambda: f"req_{uuid.uuid4().hex[:10]}")
    decision_id: str = Field(default_factory=lambda: f"dec_{uuid.uuid4().hex[:10]}")
    tenant_id: str
    organization_id: Optional[str] = None
    workspace_id: Optional[str] = None
    
    # Actor & Action Context
    user_id: Optional[str] = None
    agent_id: Optional[str] = None
    workflow_id: Optional[str] = None
    action_type: str = "EXECUTE"
    resource_type: str = "WORKFLOW"
    resource_id: str = "default_resource"
    
    # AI Governance Attributes
    model_id: Optional[str] = None
    prompt_id: Optional[str] = None
    prompt_version: Optional[str] = None
    data_classification: str = "INTERNAL"
    
    # Risk & Quality Metrics
    risk_score: float = 0.0          # 0.0 to 1.0 (or 0 to 100)
    trust_score: float = 1.0         # 0.0 to 1.0
    confidence_score: float = 1.0    # 0.0 to 1.0
    grounding_score: Optional[float] = 1.0
    
    # Business & Compliance Impact
    business_impact: str = "LOW"     # LOW, MEDIUM, HIGH, CRITICAL
    financial_impact: float = 0.0    # Estimated USD value
    compliance_category: Optional[str] = None
    
    # Oversight Constraints
    required_approval_level: int = 1
    deadline: Optional[datetime] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)
