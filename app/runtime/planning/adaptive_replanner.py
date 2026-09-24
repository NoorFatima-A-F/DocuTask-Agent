"""Adaptive Replanning Engine for DocuTask Autonomous Planning Platform.

Provides dynamic, localized sub-graph replanning triggered by runtime failures, confidence degradation,
latency drift, or human operator interventions, preserving already completed nodes.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from app.runtime.planning.mutable_dag import MutableExecutionDAG, DAGNode, DAGNodeStatus
from app.runtime.planning.capability_discovery import CapabilityDiscoveryEngine


class ReplanningTriggerType(str, Enum):
    NODE_FAILURE = "NODE_FAILURE"
    LOW_CONFIDENCE = "LOW_CONFIDENCE"
    LATENCY_DRIFT = "LATENCY_DRIFT"
    SCHEMA_VIOLATION = "SCHEMA_VIOLATION"
    HUMAN_INTERVENTION = "HUMAN_INTERVENTION"
    BUDGET_WARNING = "BUDGET_WARNING"


class ReplanningTrigger(BaseModel):
    """Event triggering the localized replanning loop."""
    trigger_type: ReplanningTriggerType
    node_id: Optional[str] = None
    metric_value: Optional[float] = None
    threshold: Optional[float] = None
    context: Dict[str, Any] = Field(default_factory=dict)
    rationale: str = ""


class SubGraphReplanningResult(BaseModel):
    """Result of adaptive replanning, describing modified sub-graph while preserving validated work."""
    mission_id: str
    trigger: ReplanningTrigger
    affected_node_ids: List[str]
    preserved_node_ids: List[str]
    new_nodes_added: List[DAGNode] = Field(default_factory=list)
    strategy_adaptation: str
    replan_version: int


class AdaptiveReplanningEngine:
    """Isolates sub-graphs and safely mutates execution topology during runtime."""

    def __init__(self, capability_discovery: CapabilityDiscoveryEngine) -> None:
        self.capability_discovery = capability_discovery

    def handle_trigger(
        self,
        dag: MutableExecutionDAG,
        trigger: ReplanningTrigger,
    ) -> SubGraphReplanningResult:
        preserved_nodes = [
            nid for nid, node in dag.nodes.items()
            if node.status == DAGNodeStatus.COMPLETED
        ]

        affected_nodes: List[str] = []
        new_nodes: List[DAGNode] = []
        adaptation = ""

        if trigger.trigger_type == ReplanningTriggerType.LOW_CONFIDENCE:
            # Low confidence in OCR or extraction -> Replace capability with high-precision model
            target_id = trigger.node_id
            if target_id and target_id in dag.nodes:
                target_node = dag.nodes[target_id]
                affected_nodes.append(target_id)
                if "ocr" in target_node.capability_id:
                    dag.replace_node_capability(
                        target_node_id=target_id,
                        new_capability_id="ocr_cloud_vision",
                        new_provider="google_cloud_vision",
                        rationale=f"Upgraded to Cloud Vision due to low confidence ({trigger.metric_value:.3f} < {trigger.threshold:.3f})",
                    )
                    adaptation = "Escalated OCR engine from local Tesseract to Google Cloud Neural Vision."
                else:
                    dag.replace_node_capability(
                        target_node_id=target_id,
                        new_capability_id="llm_pro_reasoner",
                        new_provider="gemini_pro",
                        rationale=f"Escalated to Gemini Pro Reasoner due to low confidence ({trigger.metric_value:.3f} < {trigger.threshold:.3f})",
                    )
                    adaptation = "Escalated extraction model to Gemini Pro Deep Reasoner."

        elif trigger.trigger_type == ReplanningTriggerType.NODE_FAILURE:
            # Node execution crashed -> Retry or clone with fallback
            target_id = trigger.node_id
            if target_id and target_id in dag.nodes:
                affected_nodes.append(target_id)
                target_node = dag.nodes[target_id]
                target_node.retry_count += 1
                if target_node.retry_count <= target_node.max_retries:
                    target_node.status = DAGNodeStatus.RETRYING
                    adaptation = f"Scheduled retry #{target_node.retry_count} with backoff."
                else:
                    # Switch to fallback capability
                    dag.replace_node_capability(
                        target_node_id=target_id,
                        new_capability_id="llm_pro_reasoner",
                        new_provider="gemini_pro",
                        rationale="Exceeded retries; switching to fallback deep reasoning provider.",
                    )
                    adaptation = "Exceeded max retries on node; auto-swapped to fallback engine."

        elif trigger.trigger_type == ReplanningTriggerType.LATENCY_DRIFT:
            # Split remaining pending nodes to run concurrently
            pending_nodes = [nid for nid, n in dag.nodes.items() if n.status == DAGNodeStatus.PENDING]
            if pending_nodes:
                target_id = pending_nodes[0]
                affected_nodes.append(target_id)
                shards = dag.split_node(
                    target_node_id=target_id,
                    split_count=2,
                    rationale="Parallelizing workload to recover latency SLA buffer.",
                )
                new_nodes.extend(shards)
                adaptation = f"Split pending node {target_id} into 2 parallel execution shards."

        elif trigger.trigger_type == ReplanningTriggerType.HUMAN_INTERVENTION:
            # Human operator requested manual review or rule adjustment
            adaptation = f"Applied operator directive: {trigger.rationale}"

        return SubGraphReplanningResult(
            mission_id=dag.mission_id,
            trigger=trigger,
            affected_node_ids=affected_nodes,
            preserved_node_ids=preserved_nodes,
            new_nodes_added=new_nodes,
            strategy_adaptation=adaptation or "Dynamic sub-graph adjusted.",
            replan_version=dag.version,
        )
