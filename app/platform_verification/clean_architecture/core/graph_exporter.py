"""
Dependency Graph Exporter generating JSON, DOT, and HTML visual representations.
"""
from __future__ import annotations
import json
from typing import Any, Dict, List
from app.platform_verification.clean_architecture.domain.models import CleanArchDependencyEdge


class EnterpriseGraphExporter:
    """Exports dependency graphs for architecture documentation and audits."""

    @staticmethod
    def export_to_json(edges: List[CleanArchDependencyEdge]) -> str:
        data = [
            {
                "source": e.source_module,
                "source_layer": e.source_layer.value,
                "target": e.target_module,
                "target_layer": e.target_layer.value,
                "type": e.import_type.value,
                "allowed": e.is_allowed,
                "waived": e.is_waived,
            }
            for e in edges
        ]
        return json.dumps(data, indent=2)

    @staticmethod
    def export_to_dot(edges: List[CleanArchDependencyEdge]) -> str:
        lines = ["digraph CleanArchitectureDependencies {", "  rankdir=LR;", "  node [shape=box];"]
        for e in edges:
            color = "green" if e.is_allowed else "red"
            lines.append(f'  "{e.source_module}" -> "{e.target_module}" [color="{color}"];')
        lines.append("}")
        return "\n".join(lines)
