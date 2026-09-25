"""Human Override Service and Audit Records."""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field
import uuid

from .policies import OverridePolicy
from .validation import OverrideValidator
from ..core.context import OversightContext
from ..core.exceptions import InvalidOverrideError


class HumanOverrideRecord(BaseModel):
    """Immutable audit record of a manual human intervention/override."""
    override_id: str = Field(default_factory=lambda: f"ovr_{uuid.uuid4().hex[:10]}")
    review_id: str
    tenant_id: str
    reviewer_id: str
    reviewer_role: str
    
    # Intervention Details
    original_ai_decision: Any
    overridden_human_decision: Any
    justification: str
    policy_id: Optional[str] = None
    
    # Metadata & Signatures
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    dual_signoff_by: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class OverrideService:
    """Manages execution and recording of controlled human overrides."""

    def __init__(self, validator: Optional[OverrideValidator] = None):
        self.validator = validator or OverrideValidator()
        self._records: Dict[str, HumanOverrideRecord] = {}

    def execute_override(
        self,
        review_id: str,
        reviewer_id: str,
        reviewer_role: str,
        original_ai_decision: Any,
        overridden_human_decision: Any,
        justification: str,
        context: OversightContext,
        policy: Optional[OverridePolicy] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> HumanOverrideRecord:
        """Validates and executes a human override, creating an immutable record."""
        is_valid, reason = self.validator.validate_override(
            reviewer_id=reviewer_id,
            reviewer_role=reviewer_role,
            justification=justification,
            context=context,
            policy=policy,
        )

        if not is_valid:
            raise InvalidOverrideError(f"Human override rejected: {reason}")

        record = HumanOverrideRecord(
            review_id=review_id,
            tenant_id=context.tenant_id,
            reviewer_id=reviewer_id,
            reviewer_role=reviewer_role,
            original_ai_decision=original_ai_decision,
            overridden_human_decision=overridden_human_decision,
            justification=justification,
            policy_id=policy.policy_id if policy else None,
            metadata=metadata or {},
        )
        self._records[record.override_id] = record
        return record

    def get_override(self, override_id: str) -> Optional[HumanOverrideRecord]:
        return self._records.get(override_id)

    def list_overrides(self, tenant_id: Optional[str] = None) -> List[HumanOverrideRecord]:
        records = list(self._records.values())
        if tenant_id:
            return [r for r in records if r.tenant_id == tenant_id]
        return records
