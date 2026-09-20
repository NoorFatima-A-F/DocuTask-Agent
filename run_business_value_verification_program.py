"""
Master CLI Runner for Phase V11 — Enterprise Business Value, ROI Intelligence & Operational Impact Verification Program (EBV-OIVP).
"""

import os
import sys
import time
from datetime import datetime, timezone

from app.business_value_verification.metrics.automation_metrics import AutomationMetricsCalculator
from app.business_value_verification.metrics.productivity_analyzer import ProductivityAnalyzer
from app.business_value_verification.metrics.accuracy_comparator import AccuracyComparator
from app.business_value_verification.roi.roi_engine import ROIAnalyzer
from app.business_value_verification.roi.tco_analyzer import TCOAnalyzer
from app.business_value_verification.workflows.baseline_workflows import WorkflowModelFactory
from app.business_value_verification.workflows.process_optimizer import ProcessOptimizer
from app.business_value_verification.simulation.enterprise_simulator import EnterpriseSimulator
from app.business_value_verification.simulation.adoption_simulator import AdoptionSimulator
from app.business_value_verification.case_studies.case_study_generator import CaseStudyGenerator
from app.business_value_verification.reporting.business_value_scorer import BusinessValueScorer
from app.business_value_verification.reporting.evidence_generator import BusinessValueEvidenceGenerator


def main():
    print("=" * 80)
    print(" DOCUTASK AGENT ENTERPRISE BUSINESS VALUE & ROI VERIFICATION PROGRAM ")
    print(" Phase V11: Business Value, ROI Intelligence & Operational Impact (EBV-OIVP)")
    print("=" * 80)

    start_time = time.perf_counter()
    base_dir = os.path.abspath(os.path.dirname(__file__))

    # 1. Baseline vs AI Workflows
    print("\n[1/6] Evaluating Baseline vs Autonomous AI Workflows Across 4 Verticals...")
    comparisons = WorkflowModelFactory.get_all_comparisons()
    for c in comparisons:
        print(f"  [OK] {c.workflow_name:<46} Speedup: {c.speedup_multiplier:5.0f}x | Cost Drop: {c.cost_reduction_pct:.2f}% | Accuracy: +{c.accuracy_improvement_pct:.2f}%")

    # 2. Automation & Productivity Metrics
    print("\n[2/6] Calculating Automation Rates, STP %, and Human Labor Liberation...")
    auto_metrics = AutomationMetricsCalculator.calculate_metrics()
    productivity = ProductivityAnalyzer.calculate_productivity()
    accuracy = AccuracyComparator.compare_accuracy()

    print(f"  [OK] Task Automation Rate: {auto_metrics.automation_rate_pct:.1f}% ({auto_metrics.fully_automated_tasks}/{auto_metrics.total_workflow_tasks} tasks)")
    print(f"  [OK] Straight-Through Processing (STP): {auto_metrics.straight_through_processing_pct:.1f}% (Exception Routing: {auto_metrics.exception_routing_pct:.1f}%)")
    print(f"  [OK] Annual Human Labor Liberated: {productivity.hours_liberated_annual:,.0f} hours/yr ({productivity.fte_capacity_liberated:.1f} FTEs capacity)")
    print(f"  [OK] Quality & Error Improvement: Human Error: {accuracy.human_field_error_rate_pct:.1f}% -> AI Error: {accuracy.ai_field_error_rate_pct:.2f}% (+{accuracy.overall_quality_improvement_pct:.2f}% improvement)")

    # 3. Financial ROI & 3-Year TCO Modeling
    print("\n[3/6] Computing Financial ROI & 3-Year Total Cost of Ownership (TCO)...")
    roi = ROIAnalyzer.calculate_roi()
    tco = TCOAnalyzer.calculate_3yr_tco()

    print(f"  [OK] Annual Net Savings (10k docs/mo): ${roi.annual_net_savings:,.2f}/yr | Net ROI: {roi.net_annual_roi_pct:,.1f}% | Payback: {roi.payback_period_months:.1f} months | Multiple: {roi.roi_multiple:.1f}x")
    print(f"  [OK] 3-Year Cumulative TCO Savings: ${tco.cumulative_3yr_net_savings:,.2f} (Human: ${tco.cumulative_3yr_human_tco:,.2f} vs AI: ${tco.cumulative_3yr_ai_tco:,.2f})")

    # 4. Enterprise Scale Simulations & Organizational Adoption
    print("\n[4/6] Running Multi-Tier Enterprise Simulations & Adoption Curves...")
    sims = EnterpriseSimulator.simulate_all_tiers()
    adoptions = AdoptionSimulator.simulate_role_adoption()
    optimizations = ProcessOptimizer.analyze_optimization_opportunities()

    for s in sims:
        print(f"  [OK] {s.tier_name:<38} Volume: {s.monthly_docs:>6,}/mo | Net Savings: ${s.annual_net_savings:>10,}/yr | FTEs: {s.ftes_reallocated:4.1f}")
    for a in adoptions:
        print(f"  [OK] Role: {a.role:<34} Satisfaction: {a.satisfaction_score:>4.1f}/100 | Adoption: {a.adoption_velocity_days} days | Engagement: {a.active_engagement_pct:.1f}%")

    # 5. Executive Case Studies & Master Score
    print("\n[5/6] Generating Executive Case Studies & Calculating Business Score...")
    case_studies = CaseStudyGenerator.generate_all_case_studies()
    master_score = BusinessValueScorer.calculate_score()

    for cs in case_studies:
        print(f"  [OK] Case Study Generated: {cs.title} ({cs.client_industry})")
    print(f"\n  [STAR] MASTER BUSINESS VALUE SCORE: {master_score.overall_business_score}/100.0 (Grade {master_score.grade} - {master_score.validation_status})")

    # 6. Export Evidence & SHA-256 Manifest
    print("\n[6/6] Exporting Evidence Artifacts & Cryptographic SHA-256 Manifest...")
    manifest = BusinessValueEvidenceGenerator.export_all_evidence(
        base_dir=base_dir,
        automation_metrics=auto_metrics,
        productivity_impact=productivity,
        accuracy_comp=accuracy,
        roi_result=roi,
        tco_result=tco,
        workflow_comparisons=comparisons,
        simulations=sims,
        adoption_metrics=adoptions,
        case_studies=case_studies,
        optimizations=optimizations,
        master_score=master_score,
    )

    elapsed_sec = time.perf_counter() - start_time
    print(f"\n================================================================================")
    print(f" VERIFICATION COMPLETE in {elapsed_sec:.2f} seconds")
    print(f" Cryptographic Manifest saved to: ./business_value_verification_evidence/manifest.json")
    print(f" Artifacts hashed: {len(manifest['artifacts'])}")
    for name, meta in manifest["artifacts"].items():
        print(f"  - {name:<36} SHA-256: {meta['sha256'][:16]}... ({meta['size_bytes']} bytes)")
    print(f"================================================================================\n")


if __name__ == "__main__":
    main()
