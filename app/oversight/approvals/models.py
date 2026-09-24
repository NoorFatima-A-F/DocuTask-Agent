"""Approval Policy Types, Step Definitions, and Chains."""

from enum import Enum
from typing import List, Dict, Any
from pydantic import BaseModel, Field
import uuid


class ApprovalPolicyType(str, Enum):
    SECURITY_APPROVAL = "SECURITY_APPROVAL"
    FINANCIAL_APPROVAL = "FINANCIAL_APPROVAL"
    LEGAL_APPROVAL = "LEGAL_APPROVAL"
    COMPLIANCE_APPROVAL = "COMPLIANCE_APPROVAL"
    DATA_ACCESS_APPROVAL = "DATA_ACCESS_APPROVAL"
    MODEL_CHANGE_APPROVAL = "MODEL_CHANGE_APPROVAL"
    PROMPT_CHANGE_APPROVAL = "PROMPT_CHANGE_APPROVAL"
    WORKFLOW_APPROVAL = "WORKFLOW_APPROVAL"
    HIGH_RISK_AI_APPROVAL = "HIGH_RISK_AI_APPROVAL"
    CUSTOM = "CUSTOM"


class StepExecutionStatus(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    SKIPPED = "SKIPPED"


class ApprovalStep(BaseModel):
    step_id: str = Field(default_factory=lambda: f"step_{uuid.uuid4().hex[:8]}")
    order: int = 1
    name: str
    required_roles: List[str] = Field(default_factory=list)
    min_approvals_required: int = 1
    assigned_reviewers: List[str] = Field(default_factory=list)
    approved_by: List[str] = Field(default_factory=list)
    rejected_by: List[str] = Field(default_factory=list)
    status: StepExecutionStatus = StepExecutionStatus.PENDING


class ApprovalStrategy(str, Enum):
    SEQUENTIAL = "SEQUENTIAL"    # Step 1 -> Step 2 -> Step 3
    PARALLEL = "PARALLEL"        # All steps must be approved concurrently
    THRESHOLD = "THRESHOLD"      # M-of-N approvers across pool


class ApprovalChain(BaseModel):
    chain_id: str = Field(default_factory=lambda: f"chn_{uuid.uuid4().hex[:10]}")
    tenant_id: str
    name: str
    strategy: ApprovalStrategy = ApprovalStrategy.SEQUENTIAL
    steps: List[ApprovalStep] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
