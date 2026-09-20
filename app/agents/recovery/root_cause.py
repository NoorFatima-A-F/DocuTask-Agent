"""
Root Cause Analysis Engine.
Reconstructs causal chains and produces structured RootCauseReports.
"""

from typing import List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from app.agents.recovery.failure import Failure


class CausalLink(BaseModel):
    """Link in a causal chain of events leading to failure."""
    step: int
    component: str
    action: str
    outcome: str
    model_config = {"frozen": True}


class RootCauseReport(BaseModel):
    """Comprehensive diagnostic report on the root cause of an execution failure."""
    report_id: UUID = Field(default_factory=uuid4)
    failure_id: UUID
    primary_cause: str
    secondary_causes: List[str] = Field(default_factory=list)
    affected_components: List[str] = Field(default_factory=list)
    causal_chain: List[CausalLink] = Field(default_factory=list)
    confidence: float = Field(default=0.9, ge=0.0, le=1.0)
    remediation_recommendation: str = Field(default="RETRY")
    model_config = {"frozen": True}


class RootCauseAnalyzer:
    """Reconstructs causal chains across tools, workers, and dependencies."""

    def analyze(self, failure: Failure) -> RootCauseReport:
        primary = failure.probable_cause
        secondary = [f"Category: {failure.category.value}", f"Severity: {failure.severity.value}"]
        components = []
        if failure.identity.node_id:
            components.append(f"Node: {failure.identity.node_id}")
        if failure.identity.worker_id:
            components.append(f"Worker: {failure.identity.worker_id}")
        if failure.identity.tool_name:
            components.append(f"Tool: {failure.identity.tool_name}")

        chain = [
            CausalLink(
                step=1,
                component=components[0] if components else "ExecutionEngine",
                action="Execute task node",
                outcome=failure.evidence.error_message
            )
        ]

        rec = "RETRY"
        if failure.recoverability_score < 0.5:
            rec = "ESCALATE_OR_ROLLBACK"

        return RootCauseReport(
            failure_id=failure.identity.failure_id,
            primary_cause=primary,
            secondary_causes=secondary,
            affected_components=components,
            causal_chain=chain,
            confidence=failure.confidence,
            remediation_recommendation=rec
        )
