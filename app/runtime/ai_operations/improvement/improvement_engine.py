"""
Phase 13.17: Improvement Engine (Controlled Self-Improvement & HITL Approval)
Generates optimization proposals, evaluates diffs, and manages the Human-In-The-Loop approval gate.
"""

from __future__ import annotations
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any
from app.runtime.ai_operations.models.schemas import (
    ImprovementProposal,
    ProposalStatus,
    EvaluationResult,
    FailureAnalysisResult,
)
from app.runtime.ai_operations.models.events import (
    AIOpsEvent,
    AIOpsEventType,
    AIOpsEventBus,
)
from app.runtime.ai_operations.improvement.experiment_engine import ExperimentEngine


class ImprovementEngine:
    """Manages the controlled self-improvement proposal lifecycle with mandatory HITL approval."""

    def __init__(self, experiment_engine: Optional[ExperimentEngine] = None, event_bus: Optional[AIOpsEventBus] = None):
        self.experiment_engine = experiment_engine or ExperimentEngine()
        self.event_bus = event_bus or AIOpsEventBus()
        self._proposals: Dict[str, ImprovementProposal] = {}
        self._seed_proposals()

    def _seed_proposals(self):
        p1 = ImprovementProposal(
            proposal_id="prop_001_architect_refine",
            target_agent_id="agent_chief_architect",
            title="Inject Strict Dependency Schema Constraints in Chief Architect Prompt",
            description="Automated failure analysis detected 12% schema drift in graph outputs. Adding explicit Pydantic JSON schema instructions.",
            proposal_type="PROMPT_REFINEMENT",
            status=ProposalStatus.PENDING_HITL_APPROVAL,
            proposed_changes={
                "prompt_version": "v1.1.0",
                "system_instruction_addition": "Enforce strict JSON schema validation for all dependency recommendations.",
            },
            diff_summary="+ Add 'Enforce strict JSON schema validation'\n+ Add few-shot schema error recovery examples",
            expected_quality_delta=0.08,
            expected_latency_delta_ms=-70.0,
            expected_cost_delta_pct=-16.0,
            experiment_id="exp_001_architect_schema",
        )
        self._proposals[p1.proposal_id] = p1

    def create_proposal_from_analysis(
        self,
        agent_id: str,
        title: str,
        description: str,
        proposal_type: str,
        changes: Dict[str, Any],
        diff_summary: str,
        expected_quality_delta: float = 0.05,
    ) -> ImprovementProposal:
        proposal = ImprovementProposal(
            target_agent_id=agent_id,
            title=title,
            description=description,
            proposal_type=proposal_type,
            status=ProposalStatus.PENDING_HITL_APPROVAL,
            proposed_changes=changes,
            diff_summary=diff_summary,
            expected_quality_delta=expected_quality_delta,
        )
        self._proposals[proposal.proposal_id] = proposal
        return proposal

    def approve_proposal(self, proposal_id: str, approved_by: str = "Enterprise Administrator") -> Optional[ImprovementProposal]:
        prop = self._proposals.get(proposal_id)
        if not prop:
            return None

        prop.status = ProposalStatus.APPROVED
        prop.approved_by = approved_by
        prop.approved_at = datetime.now(timezone.utc).isoformat()
        return prop

    def reject_proposal(self, proposal_id: str, reason: str = "Rejected by reviewer") -> Optional[ImprovementProposal]:
        prop = self._proposals.get(proposal_id)
        if not prop:
            return None

        prop.status = ProposalStatus.REJECTED
        prop.rejection_reason = reason
        return prop

    def deploy_proposal(self, proposal_id: str) -> Optional[ImprovementProposal]:
        prop = self._proposals.get(proposal_id)
        if not prop or prop.status != ProposalStatus.APPROVED:
            return None

        prop.status = ProposalStatus.DEPLOYED
        return prop

    def list_proposals(self, agent_id: Optional[str] = None) -> List[ImprovementProposal]:
        props = list(self._proposals.values())
        if agent_id:
            props = [p for p in props if p.target_agent_id == agent_id]
        return props
