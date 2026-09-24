"""Visual Workflow Composer Graph Models."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class WorkflowNode:
    node_id: str
    capability_name: str
    label: str
    config: Dict[str, Any] = field(default_factory=dict)
    position: Dict[str, float] = field(default_factory=lambda: {"x": 0.0, "y": 0.0})

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_id": self.node_id,
            "capability_name": self.capability_name,
            "label": self.label,
            "config": self.config,
            "position": self.position,
        }


@dataclass
class WorkflowEdge:
    edge_id: str
    source_node_id: str
    target_node_id: str
    condition: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "edge_id": self.edge_id,
            "source_node_id": self.source_node_id,
            "target_node_id": self.target_node_id,
            "condition": self.condition,
        }


@dataclass
class WorkflowDefinition:
    workflow_id: str
    name: str
    description: str
    nodes: Dict[str, WorkflowNode] = field(default_factory=dict)
    edges: List[WorkflowEdge] = field(default_factory=list)
    version: str = "1.0.0"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "workflow_id": self.workflow_id,
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "nodes": [n.to_dict() for n in self.nodes.values()],
            "edges": [e.to_dict() for e in self.edges],
        }
