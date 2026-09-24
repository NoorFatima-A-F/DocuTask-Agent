"""
Automated Report Generation Subsystem.
Exports comprehensive AI evaluation reports in Markdown, JSON, and HTML formats.
"""

import json
from pathlib import Path
from typing import Dict, List
from app.core.logging import logger
from app.validation.schemas import EvidenceRecord, RegressionComparison


class ReportGenerator:
    """Report generator compiling evaluation evidence into Markdown, JSON, and HTML artifacts."""

    REPORT_DIR = Path("docs/audits/reports")

    @classmethod
    def generate_all_reports(
        cls,
        evidence_records: List[EvidenceRecord],
        regression: RegressionComparison,
        report_title: str = "Enterprise AI Validation & Metric Report"
    ) -> Dict[str, str]:
        """
        Generates JSON, Markdown, and HTML report files.
        :return: Dict mapping format name to file path string
        """
        cls.REPORT_DIR.mkdir(parents=True, exist_ok=True)

        json_path = cls.REPORT_DIR / "ai_validation_report.json"
        md_path = cls.REPORT_DIR / "ai_validation_report.md"
        html_path = cls.REPORT_DIR / "ai_validation_report.html"

        # Calculate aggregated metrics
        avg_acc = sum(r.metrics.field_accuracy for r in evidence_records) / len(evidence_records) if evidence_records else 1.0
        avg_f1 = sum(r.metrics.f1_score for r in evidence_records) / len(evidence_records) if evidence_records else 1.0

        # 1. JSON Report
        report_dict = {
            "title": report_title,
            "total_evaluations": len(evidence_records),
            "average_field_accuracy": round(avg_acc, 4),
            "average_f1_score": round(avg_f1, 4),
            "regression_comparison": regression.model_dump(),
            "evidence_records": [r.model_dump() for r in evidence_records]
        }
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(report_dict, f, indent=2, default=str)

        # 2. Markdown Report
        md_content = cls._build_markdown(report_title, evidence_records, regression, avg_acc, avg_f1)
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content)

        # 3. HTML Report
        html_content = cls._build_html(report_title, evidence_records, regression, avg_acc, avg_f1)
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        logger.info(f"Generated evaluation reports: JSON='{json_path}', MD='{md_path}', HTML='{html_path}'")

        return {
            "json": str(json_path),
            "markdown": str(md_path),
            "html": str(html_path)
        }

    @classmethod
    def _build_markdown(
        cls,
        title: str,
        records: List[EvidenceRecord],
        regression: RegressionComparison,
        avg_acc: float,
        avg_f1: float
    ) -> str:
        lines = [
            f"# {title}",
            "",
            "## Executive Summary",
            f"- **Total Documents Evaluated**: {len(records)}",
            f"- **Average Field Accuracy**: **{avg_acc * 100:.1f}%**",
            f"- **Average F1 Score**: **{avg_f1 * 100:.1f}%**",
            f"- **Regression Status**: **{regression.regression_severity}** (Delta: {regression.accuracy_delta * 100:+.1f}%)",
            "",
            "## Evidence Records Matrix",
            "",
            "| Artifact ID | Model / Provider | Total Fields | Correct | Accuracy | F1 Score | Status | Evidence Path |",
            "|-------------|------------------|--------------|---------|----------|----------|--------|---------------|"
        ]

        for r in records:
            lines.append(
                f"| `{r.input_artifact}` | `{r.model_version}` | {r.metrics.total_fields} | {r.metrics.correct_fields} | "
                f"**{r.metrics.field_accuracy * 100:.1f}%** | {r.metrics.f1_score * 100:.1f}% | `{r.pass_fail}` | [`{Path(r.evidence_location).name}`]({r.evidence_location}) |"
            )

        lines.extend([
            "",
            "## Regression Baseline Comparison",
            f"- **Baseline Version**: `{regression.baseline_version}` ({regression.baseline_accuracy * 100:.1f}%)",
            f"- **Current Version**: `{regression.current_version}` ({regression.current_accuracy * 100:.1f}%)",
            f"- **Quality Severity**: `{regression.regression_severity}`",
            ""
        ])
        return "\n".join(lines)

    @classmethod
    def _build_html(
        cls,
        title: str,
        records: List[EvidenceRecord],
        regression: RegressionComparison,
        avg_acc: float,
        avg_f1: float
    ) -> str:
        rows = ""
        for r in records:
            rows += f"""
            <tr>
                <td><code>{r.input_artifact}</code></td>
                <td><code>{r.model_version}</code></td>
                <td>{r.metrics.total_fields}</td>
                <td>{r.metrics.correct_fields}</td>
                <td><b>{r.metrics.field_accuracy * 100:.1f}%</b></td>
                <td>{r.metrics.f1_score * 100:.1f}%</td>
                <td><span style="color: {'green' if r.pass_fail == 'PASS' else 'red'};">{r.pass_fail}</span></td>
            </tr>
            """

        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f4f6f9; }}
        h1 {{ color: #1a252f; }}
        .card {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 20px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
        th, td {{ padding: 12px; border: 1px solid #ddd; text-align: left; }}
        th {{ background-color: #2c3e50; color: white; }}
        tr:nth-child(even) {{ background-color: #f8f9fa; }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <div class="card">
        <h2>Executive Summary</h2>
        <p><b>Total Documents Evaluated:</b> {len(records)}</p>
        <p><b>Average Field Accuracy:</b> {avg_acc * 100:.1f}%</p>
        <p><b>Average F1 Score:</b> {avg_f1 * 100:.1f}%</p>
        <p><b>Regression Severity:</b> {regression.regression_severity}</p>
    </div>
    <div class="card">
        <h2>Evaluation Evidence Matrix</h2>
        <table>
            <thead>
                <tr>
                    <th>Artifact</th>
                    <th>Model</th>
                    <th>Fields</th>
                    <th>Correct</th>
                    <th>Accuracy</th>
                    <th>F1 Score</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                {rows}
            </tbody>
        </table>
    </div>
</body>
</html>
"""
        return html
