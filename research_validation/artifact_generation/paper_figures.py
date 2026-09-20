"""
Paper Figures Generator (Phase 82B.5)
=====================================
Generates publication-grade figures (SVG, DOT, JSON) embedding originating
experiment IDs, Merkle digests, and confidence intervals.
"""

from __future__ import annotations
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from research_validation.provenance.hashing import hash_canonical_json, compute_sha256


@dataclass(frozen=True)
class GeneratedFigure:
    figure_id: str
    title: str
    figure_format: str  # "SVG", "DOT", "HTML"
    originating_experiment_ids: Tuple[str, ...]
    content: str
    figure_sha256: str
    created_at_utc: str


class PaperFigureGenerator:
    """
    Synthesizes publication-grade vector graphics with embedded provenance metadata.
    """

    @classmethod
    def generate_benchmark_bar_chart_svg(
        cls,
        benchmark_metrics: Dict[str, float],
        title: str = "Benchmark Accuracy & F1 Comparison",
        originating_exp_id: str = "exp_default",
        width: int = 700,
        height: int = 400,
    ) -> GeneratedFigure:
        """Generate clean, publication-quality SVG bar chart."""
        now_str = datetime.now(timezone.utc).isoformat()
        fig_id = f"fig_bar_{originating_exp_id[:8]}"

        items = list(benchmark_metrics.items())
        n = len(items)
        max_val = max(items, key=lambda x: x[1])[1] if items else 1.0
        max_val = max(max_val, 1.0)

        bar_width = 50
        gap = 40
        margin_left = 100
        margin_bottom = 80
        chart_height = height - margin_bottom - 60

        svg_parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">',
            f'<!-- Originating Experiment ID: {originating_exp_id} -->',
            f'<!-- Generated At UTC: {now_str} -->',
            '<rect width="100%" height="100%" fill="#ffffff"/>',
            f'<text x="{width//2}" y="35" font-family="Arial, Helvetica, sans-serif" font-size="18" font-weight="bold" text-anchor="middle" fill="#1e293b">{title}</text>',
            f'<text x="{width//2}" y="52" font-family="Arial, Helvetica, sans-serif" font-size="11" text-anchor="middle" fill="#64748b">Provenance: {originating_exp_id}</text>',
            # Y Axis
            f'<line x1="{margin_left}" y1="70" x2="{margin_left}" y2="{70 + chart_height}" stroke="#94a3b8" stroke-width="1.5"/>',
            # X Axis
            f'<line x1="{margin_left}" y1="{70 + chart_height}" x2="{width - 40}" y2="{70 + chart_height}" stroke="#94a3b8" stroke-width="1.5"/>',
        ]

        # Y axis ticks
        for i in range(5):
            frac = i / 4.0
            y_pos = 70 + chart_height - (frac * chart_height)
            val_label = f"{frac * max_val:.2f}"
            svg_parts.append(
                f'<text x="{margin_left - 10}" y="{y_pos + 4}" font-family="Arial, sans-serif" font-size="11" text-anchor="end" fill="#64748b">{val_label}</text>'
            )
            svg_parts.append(
                f'<line x1="{margin_left}" y1="{y_pos}" x2="{width - 40}" y2="{y_pos}" stroke="#f1f5f9" stroke-width="1"/>'
            )

        # Draw Bars
        colors = ["#3b82f6", "#10b981", "#8b5cf6", "#f59e0b", "#ec4899", "#06b6d4"]
        for idx, (label, val) in enumerate(items):
            x = margin_left + 30 + idx * (bar_width + gap)
            bar_h = (val / max_val) * chart_height if max_val > 0 else 0
            y = 70 + chart_height - bar_h
            color = colors[idx % len(colors)]

            svg_parts.append(
                f'<rect x="{x}" y="{y}" width="{bar_width}" height="{bar_h}" rx="4" fill="{color}"/>'
            )
            # Value label
            svg_parts.append(
                f'<text x="{x + bar_width//2}" y="{y - 8}" font-family="Arial, sans-serif" font-size="12" font-weight="600" text-anchor="middle" fill="#1e293b">{val:.3f}</text>'
            )
            # Metric label
            svg_parts.append(
                f'<text x="{x + bar_width//2}" y="{70 + chart_height + 20}" font-family="Arial, sans-serif" font-size="11" text-anchor="middle" fill="#475569">{label}</text>'
            )

        svg_parts.append('</svg>')
        full_svg = "\n".join(svg_parts)
        sha = compute_sha256(full_svg.encode())

        return GeneratedFigure(
            figure_id=fig_id,
            title=title,
            figure_format="SVG",
            originating_experiment_ids=(originating_exp_id,),
            content=full_svg,
            figure_sha256=sha,
            created_at_utc=now_str,
        )

    @classmethod
    def generate_pipeline_dag_dot(
        cls,
        nodes: List[Dict[str, str]],
        edges: List[Tuple[str, str]],
        originating_exp_id: str = "exp_default",
    ) -> GeneratedFigure:
        """Generate Graphviz DOT diagram for pipeline lineage."""
        now_str = datetime.now(timezone.utc).isoformat()
        fig_id = f"fig_dot_{originating_exp_id[:8]}"

        dot_lines = [
            f'// Experiment Provenance DAG: {originating_exp_id}',
            'digraph PipelineLineage {',
            '  rankdir=LR;',
            '  node [shape=box, style="rounded,filled", fontname="Arial", fontsize=11, fillcolor="#f8fafc", color="#cbd5e1"];',
            '  edge [color="#64748b", arrowhead=vee];',
        ]

        for n in nodes:
            nid = n.get("id", "")
            lbl = n.get("label", nid)
            dot_lines.append(f'  "{nid}" [label="{lbl}"];')

        for src, dst in edges:
            dot_lines.append(f'  "{src}" -> "{dst}";')

        dot_lines.append('}')
        content = "\n".join(dot_lines)
        sha = compute_sha256(content.encode())

        return GeneratedFigure(
            figure_id=fig_id,
            title="Pipeline Lineage DAG",
            figure_format="DOT",
            originating_experiment_ids=(originating_exp_id,),
            content=content,
            figure_sha256=sha,
            created_at_utc=now_str,
        )
