"""
Adaptation Engine.
Produces formal AdaptationProposal entities based on recommendations.
All adaptation proposals require explicit operational or human approval before activation.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from app.agents.reflection.exceptions import AdaptationApprovalRequiredError
from app.agents.reflection.interfaces import IAdaptationEngine
from app.agents.reflection.recommendation_engine import Recommendation, SubsystemTarget


class AdaptationType(str, Enum):
    """Supported adaptation domains."""
    PLANNER_ADAPTATION = "PLANNER_ADAPTATION"
    EXECUTION_ADAPTATION = "EXECUTION_ADAPTATION"
    SCHEDULING_ADAPTATION = "SCHEDULING_ADAPTATION"
    TOOL_ADAPTATION = "TOOL_ADAPTATION"
    RECOVERY_ADAPTATION = "RECOVERY_ADAPTATION"


class AdaptationStatus(str, Enum):
    """Approval lifecycle for adaptation proposals."""
    PROPOSED = "PROPOSED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    ACTIVATED = "ACTIVATED"


class AdaptationProposal(BaseModel):
    """Formal proposal to alter planner heuristics, runtime parameters, or tool mappings."""
    proposal_id: UUID = Field(default_factory=uuid4)
    adaptation_type: AdaptationType
    target_subsystem: SubsystemTarget
    title: str
    rationale: str
    suggested_configuration: Dict[str, Any] = Field(default_factory=dict)
    risk_assessment: str = Field(default="LOW")
    status: AdaptationStatus = Field(default=AdaptationStatus.PROPOSED)
    approved_by: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def approve(self, approver_id: str) -> "AdaptationProposal":
        """Approves proposal for activation."""
        return self.model_copy(update={
            "status": AdaptationStatus.APPROVED,
            "approved_by": approver_id
        })

    def activate(self) -> "AdaptationProposal":
        """Activates an approved adaptation."""
        if self.status != AdaptationStatus.APPROVED:
            raise AdaptationApprovalRequiredError(
                f"Proposal {self.proposal_id} cannot be activated without approval. Status: {self.status}"
            )
        return self.model_copy(update={"status": AdaptationStatus.ACTIVATED})


class AdaptationEngine(IAdaptationEngine):
    """Produces formal adaptation proposals from recommendations."""

    def generate_proposals(self, recommendations: List[Recommendation]) -> List[AdaptationProposal]:
        """Maps high-confidence recommendations to concrete adaptation proposals."""
        proposals: List[AdaptationProposal] = []

        for rec in recommendations:
            if rec.confidence < 0.7:
                continue

            if rec.target_subsystem == SubsystemTarget.PLANNER:
                proposals.append(AdaptationProposal(
                    proposal_id=uuid4(),
                    adaptation_type=AdaptationType.PLANNER_ADAPTATION,
                    target_subsystem=rec.target_subsystem,
                    title=f"Plan Heuristic Update: {rec.title}",
                    rationale=rec.rationale,
                    suggested_configuration={"constraint_check": True, "action": rec.action_type},
                    risk_assessment="LOW"
                ))
            elif rec.target_subsystem == SubsystemTarget.EXECUTION:
                proposals.append(AdaptationProposal(
                    proposal_id=uuid4(),
                    adaptation_type=AdaptationType.EXECUTION_ADAPTATION,
                    target_subsystem=rec.target_subsystem,
                    title=f"Runtime Optimization: {rec.title}",
                    rationale=rec.rationale,
                    suggested_configuration={"concurrency_target": 6},
                    risk_assessment="LOW"
                ))
            elif rec.target_subsystem == SubsystemTarget.TOOL_REGISTRY:
                proposals.append(AdaptationProposal(
                    proposal_id=uuid4(),
                    adaptation_type=AdaptationType.TOOL_ADAPTATION,
                    target_subsystem=rec.target_subsystem,
                    title=f"Tool Registry Adjustment: {rec.title}",
                    rationale=rec.rationale,
                    suggested_configuration={"prefer_validated_tools": True},
                    risk_assessment="LOW"
                ))
            elif rec.target_subsystem == SubsystemTarget.RECOVERY:
                proposals.append(AdaptationProposal(
                    proposal_id=uuid4(),
                    adaptation_type=AdaptationType.RECOVERY_ADAPTATION,
                    target_subsystem=rec.target_subsystem,
                    title=f"Recovery Tuning: {rec.title}",
                    rationale=rec.rationale,
                    suggested_configuration={"backoff_mode": "EXPONENTIAL_JITTER"},
                    risk_assessment="LOW"
                ))

        return proposals
