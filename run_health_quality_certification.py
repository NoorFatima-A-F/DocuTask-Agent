"""
Phase 3H.5.11: Enterprise Health Quality Scoring & Operational Certification Framework Master CLI Runner
"""
import sys
import os
from app.platform_verification.health_quality_certification.runtime.health_quality_runtime import (
    HealthQualityRuntime,
)
from app.platform_verification.health_quality_certification.domain.models import (
    CertificationStatus,
    DeploymentDecision,
)


def main():
    print("=" * 80)
    print("DocuTask Agent — Phase 3H.5.11: Health Quality Scoring & Enterprise Certification")
    print("=" * 80)
    print("Collecting 8-dimension health quality evidence, evaluating SRE metrics, and running gate...\n")

    runtime = HealthQualityRuntime(output_dir="health_quality_certification")
    results = runtime.run_full_certification()
    scorecard = results["scorecard"]
    sre = results["sre_metrics"]
    regression = results["regression_report"]
    gate = results["deployment_gate"]

    print("-" * 80)
    print("HEALTH QUALITY & OPERATIONAL CERTIFICATION SCORECARD")
    print("-" * 80)
    print(f"Verification ID:                {scorecard.verification_id}")
    print(f"Overall Quality Score:          {scorecard.overall_score:.2f}%")
    print(f"Health Maturity Level:          Level 4 — {scorecard.maturity_level.value}")
    print(f"Certification Status:           {scorecard.certification_status.value}")
    print(f"CI/CD Deployment Gate:          {gate.decision.value} (Actual: {gate.actual_score:.2f}%, Min: {gate.minimum_score_required:.0f}%)")
    print(f"Certified Enterprise Ready:     {'YES (CERTIFIED)' if scorecard.passed else 'NO (FAILED)'}")
    print("-" * 80)
    print("SRE RELIABILITY METRICS:")
    print(f"  • Availability:                {sre.availability_pct:.2f}% (Uptime: {sre.uptime_seconds:.0f}s / {sre.total_time_seconds:.0f}s) [{'COMPLIANT' if sre.slo_compliant else 'NON-COMPLIANT'}]")
    print(f"  • Mean Time To Detect (MTTD):  {sre.mttd_seconds:.1f}s")
    print(f"  • Mean Time To Recover (MTTR): {sre.mttr_seconds:.1f}s")
    print(f"  • Mean Time Between Failures:  {sre.mtbf_hours:.1f} hours")
    print(f"  • Incidents (Last 30 Days):    {sre.incident_count_last_30d}")
    print("-" * 80)
    print("8-CATEGORY WEIGHTED HEALTH QUALITY PILLARS:")
    for cat in scorecard.category_scores:
        print(f"  • {cat.category_name:<34} ({cat.weight * 100:.0f}%): {cat.raw_score:.2f}% (Weighted: {cat.weighted_score:.2f}%) [{cat.status}]")
    print("-" * 80)
    print("REGRESSION HEALTH ANALYSIS & DEPLOYMENT GATE:")
    print(f"  • Baseline Comparison:         Previous: {regression.previous_overall_score:.2f}% -> Current: {regression.current_overall_score:.2f}% (Delta: {regression.overall_delta:+.2f}%)")
    print(f"  • Regression Policy:           {'PASSED (No regression detected)' if regression.regression_policy_passed else 'FAILED (Regression detected)'}")
    print(f"  • Critical Readiness Checks:   {'ALL PASSED' if gate.critical_requirements_met else 'FAILED'}")
    print("-" * 80)
    print(f"Standardized evidence repository exported to 'health_quality_certification/' ({len(results['exported_files'])} artifacts):")
    for filename in sorted(results["exported_files"].keys()):
        print(f"  - {filename}")
    print("=" * 80)

    if scorecard.passed and scorecard.overall_score >= 90.0 and gate.decision == DeploymentDecision.APPROVED:
        print("[SUCCESS] Phase 3H.5.11 Health Quality Scoring & Operational Certification PASSED.\n")
        sys.exit(0)
    else:
        print("[ERROR] Phase 3H.5.11 Certification FAILED to meet enterprise thresholds.\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
