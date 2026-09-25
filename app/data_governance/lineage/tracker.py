"""Data Lineage Runtime Tracker (Phase 8B).

Provides automatic lineage recording and context management during data processing.
"""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional
from app.data_governance.lineage.graph import LineageGraphEngine
from app.data_governance.lineage.nodes import LineageNode, LineageNodeType
from app.data_governance.lineage.edges import LineageEdge, LineageEdgeType


class LineageTrackerContext:
    """Context manager for tracing step transformations."""

    def __init__(
        self,
        tracker: LineageTracker,
        transformation_name: str,
        input_node_ids: List[str],
        output_node_ids: List[str],
        organization_id: str,
        actor_id: str = "system",
        properties: Optional[Dict[str, Any]] = None,
    ):
        self.tracker = tracker
        self.transformation_name = transformation_name
        self.input_node_ids = input_node_ids
        self.output_node_ids = output_node_ids
        self.organization_id = organization_id
        self.actor_id = actor_id
        self.properties = properties or {}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.tracker.record_transformation(
                transformation_name=self.transformation_name,
                input_node_ids=self.input_node_ids,
                output_node_ids=self.output_node_ids,
                organization_id=self.organization_id,
                actor_id=self.actor_id,
                properties=self.properties,
            )


class LineageTracker:
    """Orchestrates runtime lineage capture."""

    def __init__(self, graph_engine: Optional[LineageGraphEngine] = None):
        self.graph = graph_engine or LineageGraphEngine()

    def register_node(
        self,
        node_id: str,
        node_type: LineageNodeType,
        label: str,
        organization_id: str,
        properties: Optional[Dict[str, Any]] = None,
    ) -> LineageNode:
        """Register or update a node in the lineage graph."""
        node = LineageNode(
            node_id=node_id,
            node_type=node_type,
            label=label,
            organization_id=organization_id,
            properties=properties or {},
        )
        return self.graph.add_node(node)

    def record_transformation(
        self,
        transformation_name: str,
        input_node_ids: List[str],
        output_node_ids: List[str],
        organization_id: str,
        actor_id: str = "system",
        properties: Optional[Dict[str, Any]] = None,
    ) -> LineageNode:
        """Create a transformation task node and wire input -> task -> output edges."""
        task_node_id = f"trans_{uuid.uuid4().hex[:10]}"
        task_node = self.register_node(
            node_id=task_node_id,
            node_type=LineageNodeType.TASK,
            label=transformation_name,
            organization_id=organization_id,
            properties=properties or {},
        )

        # Wire inputs -> task
        for inp_id in input_node_ids:
            self.graph.add_edge(
                LineageEdge(
                    edge_id=f"edge_{uuid.uuid4().hex[:8]}",
                    source_node_id=inp_id,
                    target_node_id=task_node_id,
                    edge_type=LineageEdgeType.READ,
                    organization_id=organization_id,
                    actor_id=actor_id,
                )
            )

        # Wire task -> outputs
        for out_id in output_node_ids:
            self.graph.add_edge(
                LineageEdge(
                    edge_id=f"edge_{uuid.uuid4().hex[:8]}",
                    source_node_id=task_node_id,
                    target_node_id=out_id,
                    edge_type=LineageEdgeType.GENERATED_BY,
                    organization_id=organization_id,
                    actor_id=actor_id,
                )
            )

        return task_node

    def track(
        self,
        transformation_name: str,
        input_node_ids: List[str],
        output_node_ids: List[str],
        organization_id: str,
        actor_id: str = "system",
        properties: Optional[Dict[str, Any]] = None,
    ) -> LineageTrackerContext:
        """Return context manager for automatic transformation tracking."""
        return LineageTrackerContext(
            tracker=self,
            transformation_name=transformation_name,
            input_node_ids=input_node_ids,
            output_node_ids=output_node_ids,
            organization_id=organization_id,
            actor_id=actor_id,
            properties=properties,
        )
