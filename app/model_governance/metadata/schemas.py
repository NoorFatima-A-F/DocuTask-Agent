"""Model Metadata Schemas (Phase 8C).

Defines Technical, Business, and Governance metadata dimensions for AI models.
"""

from __future__ import annotations

from typing import List, Optional, Set
from pydantic import BaseModel, Field
from app.model_governance.registry.models import RiskLevel


class ModelTechnicalMetadata(BaseModel):
    """Technical performance and limits."""
    architecture: str = "Transformer"
    parameter_count_billion: float = 70.0
    context_window: int = 128000
    context_window_tokens: Optional[int] = None
    max_input_tokens: int = 128000
    max_output_tokens: int = 8192
    supported_modalities: List[str] = Field(default_factory=lambda: ["text"])
    input_token_price_usd_per_1k: float = 0.00015
    output_token_price_usd_per_1k: float = 0.00060
    typical_latency_ms: float = 450.0
    api_endpoint: str = "https://api.provider.ai/v1"
    available_regions: List[str] = Field(default_factory=lambda: ["us-east-1", "eu-west-1"])


class ModelBusinessMetadata(BaseModel):
    """Business alignment, ownership, approved/restricted use cases."""
    owner_user_id: str = "system"
    owner_email: Optional[str] = None
    business_unit: str = "Enterprise AI"
    department: str = "AI Core"
    cost_center: Optional[str] = None
    approved_use_cases: List[str] = Field(default_factory=list)
    restricted_use_cases: List[str] = Field(default_factory=list)
    compliance_level: str = "ENTERPRISE"
    risk_classification: RiskLevel = RiskLevel.MEDIUM


class ModelGovernanceMetadata(BaseModel):
    """Governance restrictions, allowed tenants/workflows, human-in-the-loop requirements."""
    allowed_tenants: Set[str] = Field(default_factory=lambda: {"*"})
    allowed_workflows: Set[str] = Field(default_factory=lambda: {"*"})
    allowed_agents: Set[str] = Field(default_factory=lambda: {"*"})
    data_residency_regions: List[str] = Field(default_factory=lambda: ["us-east-1"])
    gdpr_compliant: bool = True
    eu_ai_act_tier: Optional[str] = None
    requires_human_approval_for_actions: bool = False
    data_retention_days: int = 90
    audit_logging_enabled: bool = True


class ComprehensiveModelMetadata(BaseModel):
    """Unified 3D model metadata container."""
    model_id: str = "default_model"
    technical: ModelTechnicalMetadata = Field(default_factory=ModelTechnicalMetadata)
    business: ModelBusinessMetadata = Field(default_factory=ModelBusinessMetadata)
    governance: ModelGovernanceMetadata = Field(default_factory=ModelGovernanceMetadata)
