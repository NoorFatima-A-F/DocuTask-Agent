"""
Evidence generator for Phase V11 Enterprise Business Value, ROI Intelligence & Operational Impact Verification Program.
"""

import os
import json
import hashlib
from datetime import datetime, timezone
from typing import Dict, Any, List


class BusinessValueEvidenceGenerator:
    """Exports all JSON telemetry datasets, Markdown executive audit reports, and SHA-256 manifests."""

    @staticmethod
    def calculate_sha256(file_path: str) -> str:
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    @classmethod
    def export_all_evidence(
        cls,
        base_dir: str,
        automation_metrics: Any,
        productivity_impact: Any,
        accuracy_comp: Any,
        roi_result: Any,
        tco_result: Any,
        workflow_comparisons: List[Any],
        simulations: List[Any],
        adoption_metrics: List[Any],
        case_studies: List[Any],
        optimizations: List[Dict[str, Any]],
        master_score: Any,
    ) -> Dict[str, Any]:
        docs_dir = os.path.join(base_dir, "docs")
        evidence_dir = os.path.join(base_dir, "business_value_verification_evidence")
        os.makedirs(docs_dir, exist_ok=True)
        os.makedirs(evidence_dir, exist_ok=True)

        generated_files = {}

        # 1. ROI Analysis JSON
        roi_data = {
            "roi_analysis": roi_result.to_dict() if hasattr(roi_result, "to_dict") else roi_result,
            "productivity_impact": productivity_impact.to_dict() if hasattr(productivity_impact, "to_dict") else productivity_impact,
        }
        roi_path = os.path.join(docs_dir, "phase_V11_roi_analysis.json")
        with open(roi_path, "w", encoding="utf-8") as f:
            json.dump(roi_data, f, indent=2)
        generated_files["phase_V11_roi_analysis.json"] = roi_path

        # 2. Automation Metrics JSON
        auto_data = {
            "automation_metrics": automation_metrics.to_dict() if hasattr(automation_metrics, "to_dict") else automation_metrics,
            "accuracy_comparison": accuracy_comp.to_dict() if hasattr(accuracy_comp, "to_dict") else accuracy_comp,
            "optimizations": optimizations,
        }
        auto_path = os.path.join(docs_dir, "phase_V11_automation_metrics.json")
        with open(auto_path, "w", encoding="utf-8") as f:
            json.dump(auto_data, f, indent=2)
        generated_files["phase_V11_automation_metrics.json"] = auto_path

        # 3. Workflow Comparisons JSON
        wf_data = {
            "workflow_comparisons": [w.to_dict() if hasattr(w, "to_dict") else w for w in workflow_comparisons]
        }
        wf_path = os.path.join(docs_dir, "phase_V11_workflow_comparison.json")
        with open(wf_path, "w", encoding="utf-8") as f:
            json.dump(wf_data, f, indent=2)
        generated_files["phase_V11_workflow_comparison.json"] = wf_path

        # 4. Simulation Results JSON
        sim_data = {
            "enterprise_tier_simulations": [s.to_dict() if hasattr(s, "to_dict") else s for s in simulations],
            "role_adoption_simulations": [a.to_dict() if hasattr(a, "to_dict") else a for a in adoption_metrics],
        }
        sim_path = os.path.join(docs_dir, "phase_V11_simulation_results.json")
        with open(sim_path, "w", encoding="utf-8") as f:
            json.dump(sim_data, f, indent=2)
        generated_files["phase_V11_simulation_results.json"] = sim_path

        # 5. TCO Report JSON
        tco_data = {
            "3_year_tco_comparison": tco_result.to_dict() if hasattr(tco_result, "to_dict") else tco_result
        }
        tco_path = os.path.join(docs_dir, "phase_V11_tco_report.json")
        with open(tco_path, "w", encoding="utf-8") as f:
            json.dump(tco_data, f, indent=2)
        generated_files["phase_V11_tco_report.json"] = tco_path

        # 6. Case Studies JSON
        case_data = {
            "case_studies": [c.to_dict() if hasattr(c, "to_dict") else c for c in case_studies]
        }
        case_path = os.path.join(docs_dir, "phase_V11_case_studies.json")
        with open(case_path, "w", encoding="utf-8") as f:
            json.dump(case_data, f, indent=2)
        generated_files["phase_V11_case_studies.json"] = case_path

        # 7. Business Score JSON
        score_data = {
            "business_score": master_score.to_dict() if hasattr(master_score, "to_dict") else master_score
        }
        score_path = os.path.join(docs_dir, "phase_V11_business_score.json")
        with open(score_path, "w", encoding="utf-8") as f:
            json.dump(score_data, f, indent=2)
        generated_files["phase_V11_business_score.json"] = score_path

        # 8. Human-Readable Audit Report Markdown
        md_path = os.path.join(docs_dir, "phase_V11_business_value_report.md")
        cls._write_markdown_report(
            md_path,
            master_score,
            automation_metrics,
            productivity_impact,
            accuracy_comp,
            roi_result,
            tco_result,
            workflow_comparisons,
            simulations,
            adoption_metrics,
            case_studies,
            optimizations,
        )
        generated_files["phase_V11_business_value_report.md"] = md_path

        # 9. Cryptographic Manifest JSON
        manifest = {
            "program": "Phase V11 — Enterprise Business Value, ROI Intelligence & Operational Impact Verification Program (EBV-OIVP)",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "validation_status": master_score.validation_status,
            "overall_score": master_score.overall_business_score,
            "grade": master_score.grade,
            "artifacts": {},
        }

        for filename, path in generated_files.items():
            manifest["artifacts"][filename] = {
                "path": path,
                "sha256": cls.calculate_sha256(path),
                "size_bytes": os.path.getsize(path),
            }

        manifest_path = os.path.join(evidence_dir, "manifest.json")
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)

        return manifest

    @classmethod
    def _write_markdown_report(
        cls,
        path: str,
        score: Any,
        auto_metrics: Any,
        productivity: Any,
        accuracy: Any,
        roi: Any,
        tco: Any,
        workflows: List[Any],
        sims: List[Any],
        adoptions: List[Any],
        cases: List[Any],
        optimizations: List[Dict[str, Any]],
    ):
        with open(path, "w", encoding="utf-8") as f:
            f.write("# Enterprise Business Value, ROI Intelligence & Operational Impact Verification Report (Phase V11)\n\n")
            f.write("## Executive Scorecard & Verification Summary\n\n")
            f.write(f"- **Master Business Value Score**: `{score.overall_business_score} / 100.0` (**Grade {score.grade} / {score.validation_status}**)\n")
            f.write(f"- **Automation Impact Score (25%)**: `{score.automation_score}/100`\n")
            f.write(f"- **Financial ROI Score (30%)**: `{score.roi_score}/100`\n")
            f.write(f"- **Operational Efficiency Score (25%)**: `{score.efficiency_score}/100`\n")
            f.write(f"- **Enterprise Adoption Score (20%)**: `{score.adoption_score}/100`\n\n")
            f.write("---\n\n")

            f.write("## 1. Baseline vs. Autonomous AI Workflow Comparisons\n\n")
            f.write("| Workflow Vertical | Baseline Duration | AI Duration | Speedup | Baseline Cost | AI Cost | Cost Reduction | Accuracy Δ |\n")
            f.write("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n")
            for w in workflows:
                f.write(f"| {w.workflow_name} | {w.baseline.total_duration_minutes:.1f} min | {w.ai_system.total_duration_minutes*60:.1f} sec | **{w.speedup_multiplier:.0f}x** | ${w.baseline.total_cost_usd:.2f} | **${w.ai_system.total_cost_usd:.4f}** | **{w.cost_reduction_pct:.2f}%** | +{w.accuracy_improvement_pct:.2f}% |\n")
            f.write("\n---\n\n")

            f.write("## 2. Automation Impact & Labor Hour Liberation\n\n")
            f.write(f"- **Task Automation Rate**: `{auto_metrics.automation_rate_pct:.1f}%` ({auto_metrics.fully_automated_tasks} / {auto_metrics.total_workflow_tasks} workflow tasks fully automated)\n")
            f.write(f"- **Straight-Through Processing (STP)**: `{auto_metrics.straight_through_processing_pct:.1f}%` autonomous auto-approval without human touch\n")
            f.write(f"- **Exception Routing Rate**: `{auto_metrics.exception_routing_pct:.1f}%` directed to Human-in-the-Loop review\n")
            f.write(f"- **Annual Human Hours Liberated**: **`{productivity.hours_liberated_annual:,.0f} hours / year`**\n")
            f.write(f"- **FTE Capacity Liberated**: **`{productivity.fte_capacity_liberated:.1f} FTEs`** redirected to high-value strategic work\n")
            f.write(f"- **Throughput Capacity Expansion**: **`{productivity.throughput_expansion_multiplier:.1f}x`** throughput acceleration\n\n")
            f.write("---\n\n")

            f.write("## 3. Financial ROI & 3-Year TCO Modeling\n\n")
            f.write(f"### Annual ROI Model (10,000 docs/month benchmark)\n")
            f.write(f"- **Baseline Monthly Labor Cost**: `${roi.baseline_monthly_cost:,.2f}`\n")
            f.write(f"- **AI Monthly Operating Cost**: `${roi.ai_monthly_cost:,.2f}`\n")
            f.write(f"- **Net Annual Financial Savings**: **`${roi.annual_net_savings:,.2f} / year`**\n")
            f.write(f"- **Annual Net ROI**: **`{roi.net_annual_roi_pct:,.1f}%`**\n")
            f.write(f"- **Payback Period**: **`{roi.payback_period_months:.1f} months`**\n")
            f.write(f"- **ROI Multiple**: **`{roi.roi_multiple:.1f}x`**\n\n")

            f.write(f"### 3-Year Total Cost of Ownership (TCO) Comparison\n\n")
            f.write(f"| Year | Human Operations TCO | AI Platform TCO | Net Annual Savings |\n")
            f.write(f"| :--- | :--- | :--- | :--- |\n")
            f.write(f"| Year 1 | ${tco.year_1_human_tco:,.2f} | ${tco.year_1_ai_tco:,.2f} | ${tco.year_1_human_tco - tco.year_1_ai_tco:,.2f} |\n")
            f.write(f"| Year 2 | ${tco.year_2_human_tco:,.2f} | ${tco.year_2_ai_tco:,.2f} | ${tco.year_2_human_tco - tco.year_2_ai_tco:,.2f} |\n")
            f.write(f"| Year 3 | ${tco.year_3_human_tco:,.2f} | ${tco.year_3_ai_tco:,.2f} | ${tco.year_3_human_tco - tco.year_3_ai_tco:,.2f} |\n")
            f.write(f"| **3-Year Cumulative** | **${tco.cumulative_3yr_human_tco:,.2f}** | **${tco.cumulative_3yr_ai_tco:,.2f}** | **${tco.cumulative_3yr_net_savings:,.2f}** |\n\n")
            f.write(f"*Scaling Elasticity: {tco.scaling_elasticity}*\n\n")
            f.write("---\n\n")

            f.write("## 4. Multi-Tier Enterprise Scale Simulations\n\n")
            f.write("| Organization Tier | Monthly Volume | Baseline Cost | AI Cost | Net Annual Savings | FTEs Reallocated | Cycle Time Compression |\n")
            f.write("| :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n")
            for s in sims:
                f.write(f"| {s.tier_name} | {s.monthly_docs:,} docs/mo | ${s.baseline_annual_cost:,.0f} | ${s.ai_annual_cost:,.0f} | **${s.annual_net_savings:,.0f}** | {s.ftes_reallocated:.1f} FTEs | {s.cycle_time_compression_pct:.1f}% |\n")
            f.write("\n---\n\n")

            f.write("## 5. Enterprise User Adoption Simulation\n\n")
            f.write("| Organizational Role | Primary Business Value | Satisfaction Score | Time to Adoption | Active Engagement |\n")
            f.write("| :--- | :--- | :--- | :--- | :--- |\n")
            for a in adoptions:
                f.write(f"| **{a.role}** | {a.primary_benefit} | **{a.satisfaction_score}/100** | {a.adoption_velocity_days} days | {a.active_engagement_pct:.1f}% |\n")
            f.write("\n---\n\n")

            f.write("## 6. Portfolio Case Studies\n\n")
            for c in cases:
                f.write(f"### Case Study: {c.title}\n")
                f.write(f"- **Industry**: {c.client_industry}\n")
                f.write(f"- **Profile**: {c.organization_profile}\n")
                f.write(f"- **Problem**: {c.problem_statement}\n")
                f.write(f"- **Solution**: {c.solution_architecture}\n")
                f.write(f"- **Results**:\n")
                for k, v in c.quantified_results.items():
                    f.write(f"  - `{k}`: {v}\n")
                f.write(f"- **Testimonial**: *{c.executive_testimonial}*\n\n")
