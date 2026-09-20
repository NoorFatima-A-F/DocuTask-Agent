"""Governance Data Warehouse Fact and Dimension Models."""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field
import uuid


# ==========================================
# Dimension Tables
# ==========================================

class DimTenant(BaseModel):
    tenant_id: str
    organization_id: str = "org_default"
    workspace_id: str = "workspace_default"
    tier: str = "ENTERPRISE"
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class DimUser(BaseModel):
    user_id: str
    tenant_id: str
    name: str = "User"
    role: str = "operator"
    department: str = "Operations"


class DimAgent(BaseModel):
    agent_id: str
    tenant_id: str
    agent_name: str
    agent_type: str = "AUTONOMOUS_WORKER"
    autonomy_level: int = 1


class DimModel(BaseModel):
    model_id: str
    provider: str = "GOOGLE"
    family: str = "gemini"
    category: str = "FOUNDATION_LLM"
    risk_level: str = "MEDIUM"


class DimPolicy(BaseModel):
    policy_id: str
    tenant_id: str
    policy_name: str
    policy_type: str = "SECURITY_APPROVAL"
    severity: str = "HIGH"


class DimWorkflow(BaseModel):
    workflow_id: str
    tenant_id: str
    workflow_name: str
    criticality: str = "MEDIUM"


class DimTime(BaseModel):
    date_key: str  # YYYY-MM-DD-HH
    year: int
    month: int
    day: int
    hour: int
    day_of_week: int


# ==========================================
# Fact Tables
# ==========================================

class FactGovernanceDecision(BaseModel):
    decision_id: str = Field(default_factory=lambda: f"fdec_{uuid.uuid4().hex[:10]}")
    tenant_id: str
    user_id: Optional[str] = None
    agent_id: Optional[str] = None
    policy_id: Optional[str] = None
    outcome: str = "ALLOWED"          # ALLOWED, DENIED, BLOCKED, APPROVAL_REQUIRED
    risk_score: float = 0.0
    latency_ms: float = 0.0
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)


class FactPolicyEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: f"fpol_{uuid.uuid4().hex[:10]}")
    tenant_id: str
    policy_id: str
    policy_type: str = "SECURITY_APPROVAL"
    violation_type: str = "RULE_TRIGGERED"
    severity: str = "HIGH"
    actor_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)


class FactAIExecution(BaseModel):
    execution_id: str = Field(default_factory=lambda: f"faiex_{uuid.uuid4().hex[:10]}")
    tenant_id: str
    agent_id: Optional[str] = None
    workflow_id: Optional[str] = None
    model_id: Optional[str] = None
    prompt_id: Optional[str] = None
    cost_usd: float = 0.0
    latency_ms: float = 0.0
    risk_score: float = 0.0
    is_success: bool = True
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)


class FactRiskEvent(BaseModel):
    risk_event_id: str = Field(default_factory=lambda: f"frisk_{uuid.uuid4().hex[:10]}")
    tenant_id: str
    category: str = "Security Risk"   # Security, Privacy, Compliance, Model, Prompt, Data, Operational, Financial
    severity: str = "HIGH"
    risk_score: float = 0.8
    source_system: str = "safety_gateway"
    entity_id: str = "default_entity"
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)


class FactComplianceEvent(BaseModel):
    compliance_event_id: str = Field(default_factory=lambda: f"fcomp_{uuid.uuid4().hex[:10]}")
    tenant_id: str
    framework: str = "SOC2"           # SOC2, ISO27001, GDPR, HIPAA, EU_AI_ACT
    control_id: str = "CC6.1"
    status: str = "COMPLIANT"         # COMPLIANT, NON_COMPLIANT, AT_RISK, UNKNOWN
    evidence_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)


class FactApproval(BaseModel):
    approval_fact_id: str = Field(default_factory=lambda: f"fapp_{uuid.uuid4().hex[:10]}")
    tenant_id: str
    review_id: str
    reviewer_id: str
    strategy: str = "SEQUENTIAL"
    outcome: str = "APPROVED"         # APPROVED, REJECTED, MODIFIED, ESCALATED
    turnaround_time_seconds: float = 0.0
    escalation_level: int = 0
    is_override: bool = False
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)
