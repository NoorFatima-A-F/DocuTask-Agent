"""
LaTeX Export (Phase 82B.5)
==========================
Transforms Publication Tables and figure metadata into clean, compilable LaTeX
code utilizing booktabs and standard academic formatting.
"""

from __future__ import annotations
from typing import Optional

from research_validation.artifact_generation.publication_tables import PublicationTable


class LatexExporter:
    """
    Exports publication tables and figures to LaTeX.
    """

    @classmethod
    def export_table(cls, table: PublicationTable, label: Optional[str] = None) -> str:
        """Render publication table as LaTeX booktabs code."""
        tbl_label = label or f"tab:{table.table_id}"
        col_aligns = "".join("l" if c.alignment == "left" else "r" if c.alignment == "right" else "c" for c in table.columns)

        lines = [
            f"% LaTeX Table generated for Experiment(s): {', '.join(table.originating_experiment_ids)}",
            f"% Digest: {table.table_digest_sha256}",
            r"\begin{table}[htbp]",
            r"\centering",
            f"\\caption{{{table.caption}}}",
            f"\\label{{{tbl_label}}}",
            f"\\begin{{tabular}}{{{col_aligns}}}",
            r"\toprule",
        ]

        # Header
        headers = [f"\\textbf{{{c.header}}}" for c in table.columns]
        lines.append(" & ".join(headers) + r" \\")
        lines.append(r"\midrule")

        # Rows
        for row in table.rows:
            row_vals = []
            for col in table.columns:
                val = row.get(col.key, "")
                if isinstance(val, float):
                    row_vals.append(f"{val:.4f}")
                else:
                    row_vals.append(str(val))
            lines.append(" & ".join(row_vals) + r" \\")

        lines.extend([
            r"\bottomrule",
            r"\end{tabular}",
            r"\end{table}",
        ])

        return "\n".join(lines)

    @classmethod
    def export_figure(cls, figure_filename: str, caption: str, label: str) -> str:
        """Render LaTeX figure inclusion snippet."""
        return f"""\\begin{{figure}}[htbp]
\\centering
\\includegraphics[width=0.9\\linewidth]{{{figure_filename}}}
\\caption{{{caption}}}
\\label{{{label}}}
\\end{{figure}}"""
