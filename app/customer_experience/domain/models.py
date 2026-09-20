"""Domain Models for Phase 7: Enterprise AI Automation Experience & Customer Simulation Platform."""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


# ============================================================================
# Enums
# ============================================================================

class IndustrySector(str, Enum):
    FINANCE = "Finance & Banking"
    HEALTHCARE = "Healthcare & Life Sciences"
    HR_RECRUITING = "HR & Talent Acquisition"
    LEGAL = "Legal & Compliance"
    CUSTOMER_SUPPORT = "Customer Support & Operations"


class OnboardingStepStatus(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class ConnectorCategory(str, Enum):
    COMMUNICATION = "COMMUNICATION"
    STORAGE = "STORAGE"
    BUSINESS_SYSTEM = "BUSINESS_SYSTEM"
    API = "API"


class ConnectorStatus(str, Enum):
    CONNECTED = "CONNECTED"
    DISCONNECTED = "DISCONNECTED"
    AUTH_REQUIRED = "AUTH_REQUIRED"
    ERROR = "ERROR"


class WorkflowNodeType(str, Enum):
    TRIGGER = "TRIGGER"
    AGENT = "AGENT"
    TOOL = "TOOL"
    CONDITION = "CONDITION"
    APPROVAL = "APPROVAL"
    ACTION = "ACTION"


class ApprovalStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    ESCALATED = "ESCALATED"
    AUTO_APPROVED = "AUTO_APPROVED"


class ExceptionSeverity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class SimulationRunStatus(str, Enum):
    INITIALIZING = "INITIALIZING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


# ============================================================================
# Part A: Enterprise Tenant Simulation Models
# ============================================================================

class TenantDepartment(BaseModel):
    department_id: str
    name: str
    head_of_department: str
    active_workflows_count: int = 0
    monthly_budget_usd: float = 10000.0


class TenantUser(BaseModel):
    user_id: str
    full_name: str
    email: str
    role: str
    department_id: str
    is_admin: bool = False


class TenantCustomization(BaseModel):
    brand_name: str
    primary_color: str = "#0066FF"
    custom_domain: str = ""
    compliance_frameworks: List[str] = Field(default_factory=list)
    data_retention_days: int = 90


class EnterpriseTenant(BaseModel):
    tenant_id: str
    name: str
    industry: IndustrySector
    tier: str = "Enterprise Platinum"
    departments: List[TenantDepartment] = Field(default_factory=list)
    users: List[TenantUser] = Field(default_factory=list)
    customization: TenantCustomization = Field(default_factory=TenantCustomization)
    connected_integrations_count: int = 0
    total_documents_processed: int = 0
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# ============================================================================
# Part B: Customer Onboarding Models
# ============================================================================

class OnboardingStep(BaseModel):
    step_number: int
    title: str
    description: str
    status: OnboardingStepStatus = OnboardingStepStatus.PENDING
    completed_at: Optional[str] = None
    output_data: Dict[str, Any] = Field(default_factory=dict)


class OnboardingJourney(BaseModel):
    journey_id: str
    tenant_id: str
    company_name: str
    industry: IndustrySector
    current_step: int = 1
    total_steps: int = 7
    steps: List[OnboardingStep] = Field(default_factory=list)
    is_completed: bool = False
    started_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    completed_at: Optional[str] = None


# ============================================================================
# Part C: AI Automation Template Marketplace Models
# ============================================================================

class TemplateKPI(BaseModel):
    metric_name: str
    baseline_value: str
    projected_ai_value: str
    expected_improvement: str


class AutomationTemplate(BaseModel):
    template_id: str
    title: str
    industry: IndustrySector
    category: str
    description: str
    agent_roles_required: List[str] = Field(default_factory=list)
    tools_required: List[str] = Field(default_factory=list)
    connectors_required: List[str] = Field(default_factory=list)
    kpis: List[TemplateKPI] = Field(default_factory=list)
    estimated_deployment_minutes: int = 5
    is_featured: bool = False
    rating: float = 4.9


# ============================================================================
# Part D: Visual AI Workflow Builder Models
# ============================================================================

class WorkflowNode(BaseModel):
    node_id: str
    label: str
    node_type: WorkflowNodeType
    config: Dict[str, Any] = Field(default_factory=dict)
    position: Dict[str, int] = Field(default_factory=lambda: {"x": 0, "y": 0})


class WorkflowEdge(BaseModel):
    edge_id: str
    source_node_id: str
    target_node_id: str
    condition_label: Optional[str] = None


class WorkflowDefinition(BaseModel):
    workflow_id: str
    tenant_id: str
    name: str
    description: str = ""
    version: str = "v1.0.0"
    is_active: bool = True
    nodes: List[WorkflowNode] = Field(default_factory=list)
    edges: List[WorkflowEdge] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class WorkflowExecutionResult(BaseModel):
    execution_id: str
    workflow_id: str
    tenant_id: str
    status: str
    nodes_executed: int
    duration_ms: float
    output_summary: str
    errors: List[str] = Field(default_factory=list)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# ============================================================================
# Part E: Enterprise Connector Simulation Models
# ============================================================================

class ConnectorAuth(BaseModel):
    auth_type: str  # OAuth2, API_KEY, WEBHOOK, MTLS
    is_authenticated: bool = True
    token_preview: str = "tok_live_..."
    last_validated: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class EnterpriseConnector(BaseModel):
    connector_id: str
    name: str
    category: ConnectorCategory
    description: str
    status: ConnectorStatus = ConnectorStatus.CONNECTED
    auth: ConnectorAuth = Field(default_factory=ConnectorAuth)
    supported_events: List[str] = Field(default_factory=list)
    total_calls_24h: int = 0
    avg_latency_ms: float = 45.0
    error_rate_pct: float = 0.0


# ============================================================================
# Part F: Human-in-the-Loop Collaboration Models
# ============================================================================

class BoundingBoxCitation(BaseModel):
    page_number: int
    coordinates: List[float] = Field(default_factory=lambda: [0.1, 0.2, 0.4, 0.8])
    extracted_text: str
    field_name: str


class ApprovalItem(BaseModel):
    approval_id: str
    tenant_id: str
    workflow_id: str
    document_title: str
    document_type: str
    ai_confidence_score: float
    recommended_action: str
    status: ApprovalStatus = ApprovalStatus.PENDING
    citations: List[BoundingBoxCitation] = Field(default_factory=list)
    reviewer_notes: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    decided_at: Optional[str] = None


class ExceptionItem(BaseModel):
    exception_id: str
    tenant_id: str
    workflow_id: str
    severity: ExceptionSeverity
    error_type: str
    description: str
    suggested_remediation: str
    resolved: bool = False
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# ============================================================================
# Part G: Customer Analytics & ROI Models
# ============================================================================

class AutomationMetric(BaseModel):
    metric_key: str
    label: str
    value: float
    unit: str
    trend_pct: float


class FinancialROISummary(BaseModel):
    tenant_id: str
    currency: str = "USD"
    manual_annual_cost: float = 2450000.0
    ai_platform_annual_cost: float = 170000.0
    net_annual_savings: float = 2280000.0
    cost_reduction_pct: float = 92.8
    roi_multiple: float = 4.2
    human_hours_liberated: float = 57500.0
    payback_period_months: float = 1.4


class CustomerAnalyticsReport(BaseModel):
    tenant_id: str
    total_documents_processed_month: int
    automation_rate_pct: float
    straight_through_processing_pct: float
    human_review_rate_pct: float
    avg_processing_time_seconds: float
    accuracy_rate_pct: float
    financial_roi: FinancialROISummary
    metrics: List[AutomationMetric] = Field(default_factory=list)
    generated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


# ============================================================================
# Part H: AI Trust Center Models
# ============================================================================

class SecurityBoundarySpec(BaseModel):
    boundary_name: str
    status: str
    encryption_algorithm: str = "AES-256-GCM / TLS 1.3"
    tenant_isolation_mechanism: str = "Cryptographic Tenant Partitioning"
    audit_trail_immutable: bool = True


class ModelGovernanceRecord(BaseModel):
    model_alias: str
    provider: str
    model_version: str
    temperature: float
    guardrails_enforced: List[str] = Field(default_factory=list)
    prompt_hash: str


class TrustCenterReport(BaseModel):
    overall_trust_score: float = 100.0
    compliance_standards: List[str] = Field(
        default_factory=lambda: ["SOC2 Type II", "HIPAA Security Rule", "GDPR Article 28", "ISO 27001"]
    )
    security_boundaries: List[SecurityBoundarySpec] = Field(default_factory=list)
    model_governance: List[ModelGovernanceRecord] = Field(default_factory=list)
    total_audit_logs_recorded: int = 145000
    last_penetration_test_date: str = "2026-08-30"


# ============================================================================
# Part I: Interactive Demo Engine Models
# ============================================================================

class DemoStepEvent(BaseModel):
    step_id: str
    stage_name: str
    status: str
    duration_ms: float
    agent_in_charge: str
    action_description: str
    artifacts_emitted: Dict[str, Any] = Field(default_factory=dict)
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class DemoRunResult(BaseModel):
    demo_run_id: str
    scenario_name: str
    status: SimulationRunStatus = SimulationRunStatus.COMPLETED
    total_duration_ms: float
    steps: List[DemoStepEvent] = Field(default_factory=list)
    extracted_fields: Dict[str, Any] = Field(default_factory=dict)
    confidence_score: float
    roi_summary: Dict[str, Any] = Field(default_factory=dict)
    audit_trace_id: str


# ============================================================================
# Part J-M: Portfolio Presentation Models
# ============================================================================

class CaseStudyDocument(BaseModel):
    title: str
    client_industry: str
    challenge: str
    solution_architecture: str
    quantified_impact: Dict[str, str] = Field(default_factory=dict)
    full_markdown: str


class DemoScript(BaseModel):
    target_audience: str  # Recruiter (5-min), Client (10-min), Technical Interviewer (30-min)
    duration_minutes: int
    opening_hook: str
    key_talking_points: List[str] = Field(default_factory=list)
    live_demonstration_steps: List[str] = Field(default_factory=list)
    handling_tough_questions: Dict[str, str] = Field(default_factory=dict)
    closing_call_to_action: str


class PortfolioPresentationArtifacts(BaseModel):
    architecture_diagram_mermaid: str
    case_studies: List[CaseStudyDocument] = Field(default_factory=list)
    demo_scripts: List[DemoScript] = Field(default_factory=list)
    generated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
