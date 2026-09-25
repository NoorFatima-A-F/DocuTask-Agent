"""
Explainable AI Decision Models.
Defines DecisionExplanation, ReasoningStep, Evidence, and DecisionGraph.
Provides human-readable and machine-readable audit traces for governance.
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from app.agents.decision.reasoning import ReasoningStep


class Evidence(BaseModel):
    """Supporting empirical evidence for a decision outcome."""
    source_type: str = Field(default="POLICY_EVALUATION")
    description: str
    data: Dict[str, Any] = Field(default_factory=dict)
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    model_config = {"frozen": True}


class DecisionGraphNode(BaseModel):
    """Node in a decision reasoning graph."""
    node_id: str
    label: str
    node_type: str = Field(default="RULE")
    outcome: str = Field(default="PASSED")
    model_config = {"frozen": True}


class DecisionGraphEdge(BaseModel):
    """Edge connecting decision graph nodes."""
    source_id: str
    target_id: str
    relationship: str = Field(default="DEPENDS_ON")
    model_config = {"frozen": True}


class DecisionGraph(BaseModel):
    """Graph structure representing hierarchical policy and rule evaluation."""
    nodes: List[DecisionGraphNode] = Field(default_factory=list)
    edges: List[DecisionGraphEdge] = Field(default_factory=list)
    model_config = {"frozen": True}


class DecisionExplanation(BaseModel):
    """Human-readable and machine-readable explanation of a decision."""

    summary: str
    reasoning_steps: List[ReasoningStep] = Field(default_factory=list)
    evidence: List[Evidence] = Field(default_factory=list)
    decision_graph: Optional[DecisionGraph] = Field(default=None)
    confidence_breakdown: float = Field(default=1.0, ge=0.0, le=1.0)
    model_config = {"frozen": True}
