"""
Evidence Provenance & Scientific Lineage Framework
Module: provenance_visualizer.py

Renders multi-format visualizations of scientific evidence graphs:
- SVG standalone diagrams
- Interactive standalone HTML with hover tooltips and metadata inspectors
- Graphviz DOT graph notation
- Mermaid flowchart markdown diagrams
"""

from __future__ import annotations

import json

from research_validation.provenance.evidence_graph import EvidenceGraph
from research_validation.provenance.provenance_models import LineageStage


class ProvenanceVisualizer:
    """
    Generates publication-ready visualizations for scientific peer-review.
    """

    STAGE_COLORS = {
        LineageStage.RAW_OBSERVATION: "#7aa2f7",      # Blue
        LineageStage.TRANSFORMATION: "#bb9af7",        # Purple
        LineageStage.INTERMEDIATE_ARTIFACT: "#7dcfff", # Cyan
        LineageStage.AGGREGATION: "#e0af68",          # Orange
        LineageStage.FINAL_METRIC: "#9ece6a",         # Green
        LineageStage.SCIENTIFIC_REPORT: "#2ac3de",    # Teal
        LineageStage.DIGITAL_SIGNATURE: "#f7768e",    # Red/Gold
    }

    @classmethod
    def to_mermaid(cls, graph: EvidenceGraph) -> str:
        """Generate Mermaid flowchart diagram."""
        lines = ["flowchart TD"]
        for node_id, node in graph.merkle_dag.nodes.items():
            clean_name = node.name.replace('"', "'")
            color = cls.STAGE_COLORS.get(node.stage, "#c0caf5")
            label = f"<b>{node.stage.value}</b><br/>{clean_name}<br/><code>{node.node_hash[:8]}</code>"
            lines.append(f'    {node_id}["{label}"]')
            lines.append(f'    style {node_id} fill:{color}22,stroke:{color},stroke-width:2px')

        for parent_id, children in graph.merkle_dag.children_map.items():
            for child_id in children:
                lines.append(f"    {parent_id} --> {child_id}")

        return "\n".join(lines)

    @classmethod
    def to_graphviz_dot(cls, graph: EvidenceGraph) -> str:
        """Generate Graphviz DOT representation."""
        lines = [
            "digraph ProvenanceLineage {",
            '  rankdir="TB";',
            '  node [shape=box, style="filled,rounded", fontname="Helvetica", fontsize=10];',
            '  edge [color="#565f89", arrowsize=0.8];'
        ]

        for node_id, node in graph.merkle_dag.nodes.items():
            color = cls.STAGE_COLORS.get(node.stage, "#7aa2f7")
            label = f"{node.stage.value}\\n{node.name}\\n[{node.node_hash[:8]}]"
            lines.append(f'  "{node_id}" [label="{label}", fillcolor="{color}33", color="{color}"];')

        for parent_id, children in graph.merkle_dag.children_map.items():
            for child_id in children:
                lines.append(f'  "{parent_id}" -> "{child_id}";')

        lines.append("}")
        return "\n".join(lines)

    @classmethod
    def to_svg(cls, graph: EvidenceGraph, width: int = 800, height: int = 400) -> str:
        """Render publication-quality standalone SVG diagram."""
        nodes = list(graph.merkle_dag.nodes.values())
        if not nodes:
            return f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}"><text x="20" y="40">Empty Evidence Graph</text></svg>'

        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
            '  <rect width="100%" height="100%" fill="#1a1b26" rx="8"/>',
            '  <text x="25" y="35" fill="#7aa2f7" font-family="sans-serif" font-size="16" font-weight="bold">Scientific Lineage Merkle DAG</text>',
            f'  <text x="25" y="55" fill="#a9b1d6" font-family="sans-serif" font-size="12">Root Digest: {graph.merkle_dag.compute_root_digest()[:16]}... | Total Nodes: {len(nodes)}</text>',
            '  <line x1="25" y1="65" x2="775" y2="65" stroke="#414868" stroke-width="1"/>'
        ]

        # Layout nodes horizontally or vertically
        y_step = max(35, min(50, (height - 90) // max(1, len(nodes))))
        y = 90
        for idx, node in enumerate(nodes):
            color = cls.STAGE_COLORS.get(node.stage, "#7aa2f7")
            svg_parts.append(f'  <rect x="25" y="{y}" width="180" height="28" fill="{color}22" stroke="{color}" rx="4" stroke-width="1.5"/>')
            svg_parts.append(f'  <text x="35" y="{y+18}" fill="#c0caf5" font-family="sans-serif" font-size="11" font-weight="bold">{node.stage.value[:14]}</text>')
            svg_parts.append(f'  <text x="220" y="{y+18}" fill="#a9b1d6" font-family="monospace" font-size="11">{node.name[:35]} [{node.node_hash[:8]}]</text>')
            svg_parts.append(f'  <text x="650" y="{y+18}" fill="{color}" font-family="sans-serif" font-size="11" font-weight="bold">{node.quality_level.value}</text>')
            y += y_step

        svg_parts.append('</svg>')
        return "\n".join(svg_parts)

    @classmethod
    def to_interactive_html(cls, graph: EvidenceGraph, title: str = "Scientific Lineage Explorer") -> str:
        """Generate interactive standalone HTML document for reviewers."""
        nodes_json = json.dumps([n.to_dict() for n in graph.merkle_dag.nodes.values()], indent=2)
        mermaid_code = cls.to_mermaid(graph)

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{title}</title>
  <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
  <style>
    body {{ background-color: #1a1b26; color: #c0caf5; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; margin: 20px; }}
    h1 {{ color: #7aa2f7; border-bottom: 1px solid #414868; padding-bottom: 10px; }}
    .card {{ background: #24283b; padding: 15px; border-radius: 8px; margin-bottom: 20px; border: 1px solid #414868; }}
    pre {{ background: #13141c; padding: 12px; border-radius: 6px; overflow-x: auto; color: #7dcfff; }}
  </style>
</head>
<body>
  <h1>{title}</h1>
  <div class="card">
    <h3>Lineage Merkle Graph</h3>
    <pre class="mermaid">
{mermaid_code}
    </pre>
  </div>
  <div class="card">
    <h3>Evidence Nodes Manifest</h3>
    <pre>{nodes_json}</pre>
  </div>
  <script>mermaid.initialize({{startOnLoad:true, theme: 'dark'}});</script>
</body>
</html>"""
