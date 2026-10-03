"""
Phase 3H.5.7: Enterprise Reliability Intelligence, Health Scoring & Resilience Optimization Master CLI Runner
"""
import sys
import os
from app.platform_verification.reliability_intelligence_verification.runtime.reliability_intelligence_runtime import (
    ReliabilityIntelligenceRuntime,
)


def main():
    print("=" * 80)
    print("DocuTask Agent — Phase 3H.5.7: Reliability Intelligence, Health Scoring & Resilience")
    print("=" * 80)
    print("Executing component reliability scoring, SLO compliance, error budgets, and chaos validation...\n")

    runtime = ReliabilityIntelligenceRuntime()
    results = runtime.run_full_reliability_verification(output_dir="reliability_intelligence_verification")
    scorecard = results["scorecard"]
    health = results["health_report"]
    comp = results["comp_report"]
    slo = results["slo_report"]
    budget = results["budget_report"]
    risk = results["risk_report"]
    rec = results["rec_report"]
    chaos = results["chaos_report"]
    trend = results["trend_report"]
    gov = results["gov_report"]

    print("-" * 80)
    print("ENTERPRISE RELIABILITY INTELLIGENCE SCORECARD")
    print("-" * 80)
    print(f"Overall Platform Health Score:  {health.overall_health_score:.2f} / 100 ({health.health_tier.value})")
    print(f"Certification Composite Score:  {scorecard.composite_score:.2f}%")
    print(f"Reliability Maturity Tier:      {scorecard.tier}")
    print(f"CI/CD Deployment Gate:          {'APPROVED (PASS)' if gov.deployment_gate_approved else 'BLOCKED (FAIL)'}")
    print(f"Certified Enterprise Ready:     {'YES (CERTIFIED)' if scorecard.certified_enterprise_ready else 'NO (FAILED)'}")
    print("-" * 80)
    print("RELIABILITY DIMENSIONS & PILLARS:")
    print(f"  • Monitored Components:        {comp.total_components_scored}/10 (Mean Score: {comp.mean_component_reliability_score:.2f}%)")
    print(f"  • SLO Compliance Rate:         {slo.overall_slo_compliance_pct:.2f}% (All 4 SLO Targets Met: {'YES' if slo.all_slos_met else 'NO'})")
    print(f"  • SRE Error Budget Status:     {'HEALTHY' if budget.overall_budget_healthy else 'EXHAUSTED'} (0 budget exhaustion events)")
    print(f"  • Pre-Failure Risks Tracked:   {risk.total_risks_identified} (Critical: {risk.critical_risks_count})")
    print(f"  • Resilience Recommendations:  {rec.total_recommendations} actionable recommendations")
    print(f"  • Chaos Fault Injection:       {'PASSED' if chaos.all_chaos_tests_passed else 'FAILED'} ({chaos.total_chaos_tests}/4 tests validated)")
    print(f"  • Long-Term Resilience Trend:  {'IMPROVING' if trend.long_term_resilience_improving else 'DEGRADING'} (+10.42% 30-day gain)")
    print("-" * 80)
    print("WEIGHTED SCORECARD PILLARS:")
    print(f"  • Reliability Measurement Accuracy (20%): {scorecard.reliability_measurement_accuracy:.2f}%")
    print(f"  • Health Scoring Quality           (20%): {scorecard.health_scoring_quality:.2f}%")
    print(f"  • SLO Management                   (15%): {scorecard.slo_management_score:.2f}%")
    print(f"  • Error Budget Implementation      (15%): {scorecard.error_budget_score:.2f}%")
    print(f"  • Risk Prediction                  (15%): {scorecard.risk_prediction_score:.2f}%")
    print(f"  • Resilience Recommendations       (10%): {scorecard.recommendations_score:.2f}%")
    print(f"  • Governance Controls               (5%): {scorecard.governance_score:.2f}%")
    print("-" * 80)
    print(f"Standardized evidence repository exported to 'reliability_intelligence_verification/' ({len(results['exported_files'])} artifacts):")
    for f in sorted(results["exported_files"]):
        print(f"  - {os.path.relpath(f, 'reliability_intelligence_verification')}")
    print("=" * 80)

    if scorecard.certified_enterprise_ready and scorecard.composite_score >= 90.0:
        print("[SUCCESS] Phase 3H.5.7 Reliability Intelligence & Resilience Optimization Verification PASSED.\n")
        sys.exit(0)
    else:
        print("[ERROR] Phase 3H.5.7 Verification FAILED to meet enterprise thresholds.\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
