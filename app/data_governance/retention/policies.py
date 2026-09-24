"""Data Retention Policies (Phase 8B)."""

from __future__ import annotations

import enum
from typing import Dict
from pydantic import BaseModel


class RetentionAction(str, enum.Enum):
    """Action to execute when retention period expires."""
    ARCHIVE = "ARCHIVE"
    DELETE = "DELETE"
    REQUIRE_APPROVAL = "REQUIRE_APPROVAL"


class RetentionPolicy(BaseModel):
    """Governed retention schedule for a class of data assets."""
    policy_id: str
    name: str
    retention_days: int
    action_on_expiry: RetentionAction = RetentionAction.ARCHIVE
    requires_steward_approval: bool = True
    description: str = ""


DEFAULT_RETENTION_POLICIES: Dict[str, RetentionPolicy] = {
    "financial_records": RetentionPolicy(
        policy_id="ret_financial_7yr",
        name="Financial & Tax Records",
        retention_days=2555,  # 7 years
        action_on_expiry=RetentionAction.REQUIRE_APPROVAL,
        description="Legal mandate for financial audit records",
    ),
    "contracts": RetentionPolicy(
        policy_id="ret_contracts_10yr",
        name="Executed Contracts",
        retention_days=3650,  # 10 years
        action_on_expiry=RetentionAction.ARCHIVE,
        description="Corporate contracts and agreements",
    ),
    "ai_interactions": RetentionPolicy(
        policy_id="ret_ai_logs_1yr",
        name="AI Prompt & Execution Logs",
        retention_days=365,
        action_on_expiry=RetentionAction.DELETE,
        description="Operational LLM and agent execution logs",
    ),
    "temp_cache": RetentionPolicy(
        policy_id="ret_temp_30d",
        name="Temporary Processing Cache",
        retention_days=30,
        action_on_expiry=RetentionAction.DELETE,
        requires_steward_approval=False,
        description="Temporary processing artifacts",
    ),
}
