"""Prompt Metadata Schemas (Phase 8D).

Defines multi-dimensional metadata for prompt assets:
- Technical (Context limits, model compatibility, variables, schema)
- Business (Owner, department, purpose, SLA, business unit)
- AI & Knowledge (Required RAG collections, agent role, tools)
- Governance & Security (Classification, risk tier, audit requirements)
"""

from __future__ import annotations

from typing import Any, Dict, List
from pydantic import BaseModel, Field
from app.prompts.registry.models import RiskLevel


class PromptTechnicalMetadata(BaseModel):
    """Technical requirements and runtime specifications."""
    estimated_tokens: int = 150
    recommended_temperature: float = 0.2
    max_tokens: int = 2048
    compatible_models: List[str] = Field(default_factory=lambda: ["*"])
    supports_streaming: bool = True
    requires_json_mode: bool = False


class PromptBusinessMetadata(BaseModel):
    """Business ownership, alignment, and operational context."""
    business_owner_email: str = "ai-core@enterprise.com"
    department: str = "AI Engineering"
    cost_center: str = "CC-102"
    sla_response_time_ms: int = 2000
    business_criticality: str = "HIGH"


class PromptGovernanceMetadata(BaseModel):
    """Governance, compliance, and auditing restrictions."""
    risk_level: RiskLevel = RiskLevel.MEDIUM
    requires_human_review_for_changes: bool = True
    allowed_environments: List[str] = Field(default_factory=lambda: ["Development", "Staging", "Production"])
    data_classification: str = "CONFIDENTIAL"
    gdpr_compliant: bool = True


class ComprehensivePromptMetadata(BaseModel):
    """Unified 3D enterprise prompt metadata descriptor."""
    prompt_id: str
    technical: PromptTechnicalMetadata = Field(default_factory=PromptTechnicalMetadata)
    business: PromptBusinessMetadata = Field(default_factory=PromptBusinessMetadata)
    governance: PromptGovernanceMetadata = Field(default_factory=PromptGovernanceMetadata)
    custom_attributes: Dict[str, Any] = Field(default_factory=dict)
