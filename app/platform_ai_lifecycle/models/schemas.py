"""
Phase 13.20: Autonomous AI Application Lifecycle Platform (AAILP) Schemas & Models.
Data models for enterprise agent inventory, semantic versioning, security scanning, testing, and deployment.
"""

from enum import Enum
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime, timezone


class AgentLifecycleState(str, Enum):
    DRAFT = "DRAFT"
    DEVELOPMENT = "DEVELOPMENT"
    TESTING = "TESTING"
    SECURITY_REVIEW = "SECURITY_REVIEW"
    APPROVED = "APPROVED"
    DEPLOYED = "DEPLOYED"
    DEPRECATED = "DEPRECATED"
    RETIRED = "RETIRED"


class AgentCategory(str, Enum):
    EXTRACTION = "EXTRACTION"
    RESEARCH = "RESEARCH"
    CUSTOMER_SUPPORT = "CUSTOMER_SUPPORT"
    AUTOMATION = "AUTOMATION"
    COMPLIANCE = "COMPLIANCE"
    FINANCIAL_AUDIT = "FINANCIAL_AUDIT"
    LEGAL_ANALYSIS = "LEGAL_ANALYSIS"


class DeploymentEnvironment(str, Enum):
    STAGING = "STAGING"
    CANARY = "CANARY"
    PRODUCTION = "PRODUCTION"


class DeploymentStrategy(str, Enum):
    DIRECT = "DIRECT"
    BLUE_GREEN = "BLUE_GREEN"
    CANARY = "CANARY"


class DeploymentStatus(str, Enum):
    BUILDING = "BUILDING"
    TESTING = "TESTING"
    STAGING = "STAGING"
    CANARY = "CANARY"
    PRODUCTION = "PRODUCTION"
    ROLLBACK = "ROLLBACK"
    FAILED = "FAILED"


class ApprovalStage(str, Enum):
    DEVELOPER_SUBMIT = "DEVELOPER_SUBMIT"
    SECURITY_REVIEW = "SECURITY_REVIEW"
    BUSINESS_APPROVAL = "BUSINESS_APPROVAL"
    COMPLIANCE_SIGNOFF = "COMPLIANCE_SIGNOFF"
    FINAL_RELEASE = "FINAL_RELEASE"


class ApprovalDecision(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class AgentApplication(BaseModel):
    agent_id: str
    tenant_id: str
    organization_id: str
    workspace_id: str
    name: str
    slug: str
    category: AgentCategory = AgentCategory.AUTOMATION
    owner_id: str
    owner_email: str
    description: str
    lifecycle_state: AgentLifecycleState = AgentLifecycleState.DRAFT
    current_version: str = "1.0.0"
    tags: List[str] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class AgentVersion(BaseModel):
    version_id: str
    agent_id: str
    version_tag: str  # e.g., "1.0.0", "1.1.0"
    model_family: str = "gemini-pro"
    system_prompt: str
    tools: List[str] = Field(default_factory=list)
    connectors: List[str] = Field(default_factory=list)
    parameters: Dict[str, Any] = Field(default_factory=dict)
    changelog: str = "Initial release"
    accuracy_score: float = 0.95
    cost_per_execution_usd: float = 0.004
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class AgentTestResult(BaseModel):
    test_id: str
    agent_id: str
    version_tag: str
    functional_pass: bool = True
    grounding_score: float = 0.98  # Phase 13.17 LLM Judge eval
    accuracy_score: float = 0.96
    hallucination_rate_pct: float = 0.8
    security_checks_passed: bool = True
    latency_p95_ms: float = 380.0
    cost_estimated_usd: float = 0.0035
    status: str = "PASSED"
    tested_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class SecurityVulnerability(BaseModel):
    vuln_id: str
    severity: str  # "CRITICAL", "HIGH", "MEDIUM", "LOW"
    category: str  # "PROMPT_INJECTION", "EXCESSIVE_PRIVILEGE", "PII_LEAKAGE", "VULNERABLE_DEPENDENCY"
    description: str
    recommendation: str


class AgentSecurityScan(BaseModel):
    scan_id: str
    agent_id: str
    version_tag: str
    security_score: int = 94  # 0 to 100
    risk_level: str = "LOW"  # "CRITICAL", "HIGH", "MEDIUM", "LOW"
    prompt_injection_resistance_pct: float = 99.2
    pii_leakage_detected: bool = False
    excessive_permissions: bool = False
    vulnerabilities: List[SecurityVulnerability] = Field(default_factory=list)
    scanned_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class AgentApproval(BaseModel):
    approval_id: str
    agent_id: str
    version_tag: str
    stage: ApprovalStage
    decision: ApprovalDecision = ApprovalDecision.PENDING
    approver_id: Optional[str] = None
    approver_email: Optional[str] = None
    comments: str = ""
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class AgentDeployment(BaseModel):
    deployment_id: str
    agent_id: str
    version_tag: str
    environment: DeploymentEnvironment = DeploymentEnvironment.PRODUCTION
    strategy: DeploymentStrategy = DeploymentStrategy.CANARY
    traffic_weight_pct: int = 100
    status: DeploymentStatus = DeploymentStatus.PRODUCTION
    distributed_cluster_id: str = "cluster_us_east_primary"
    active_instances_count: int = 4
    deployed_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class AgentDependency(BaseModel):
    dep_id: str
    agent_id: str
    dependency_type: str  # "TOOL", "MODEL", "CONNECTOR", "DATASET", "POLICY"
    target_resource_id: str
    target_resource_name: str
    is_breaking_change: bool = False


class AgentTemplate(BaseModel):
    template_id: str
    name: str
    category: AgentCategory
    description: str
    recommended_model: str = "gemini-pro"
    default_tools: List[str] = Field(default_factory=list)
    default_prompt: str


class AgentMarketplaceListing(BaseModel):
    listing_id: str
    agent_id: str
    title: str
    publisher_name: str
    category: AgentCategory
    description: str
    version: str
    rating: float = 4.9
    install_count: int = 1250
    certified_secure: bool = True
    price_monthly_usd: float = 0.0
    tags: List[str] = Field(default_factory=list)


class AgentAnalytics(BaseModel):
    agent_id: str
    name: str
    total_executions: int = 14500
    success_rate_pct: float = 99.4
    automation_roi_usd: float = 42500.0
    developer_hours_saved: float = 850.0
    adoption_score: float = 94.2
    avg_latency_ms: float = 340.0


class AgentRetirementPlan(BaseModel):
    retirement_id: str
    agent_id: str
    target_migration_agent_id: Optional[str] = None
    deprecation_notice: str
    sunset_date: str
    traffic_redirect_pct: int = 0
    archived: bool = False


class LifecycleOverview(BaseModel):
    total_managed_agents: int
    deployed_in_production: int
    in_review_or_testing: int
    deprecated_or_retired: int
    mean_security_score: float
    total_automation_roi_usd: float
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
