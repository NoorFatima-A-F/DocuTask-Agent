"""
Phase 3H.5.6: Enterprise Failure Learning, RCA & Recovery Optimization Master CLI Runner
"""
import sys
import os
from app.platform_verification.failure_learning_verification.runtime.failure_learning_runtime import (
    FailureLearningRuntime,
)


def main():
    print("=" * 80)
    print("DocuTask Agent — Phase 3H.5.6: Failure Learning, RCA & Recovery Optimization")
    print("=" * 80)
    print("Executing failure event analysis, RCA, pattern recognition, and policy evolution...\n")

    runtime = FailureLearningRuntime()
    results = runtime.run_full_failure_learning_verification(output_dir="failure_learning_verification")
    scorecard = results["scorecard"]
    rca_report = results["rca_report"]
    pattern_report = results["pattern_report"]
    kb_report = results["kb_report"]
    opt_report = results["optimization_report"]
    prev_report = results["prevention_report"]
    sim_report = results["simulation_report"]

    print("-" * 80)
    print("ENTERPRISE ADAPTIVE RELIABILITY INTELLIGENCE SCORECARD")
    print("-" * 80)
    print(f"Overall Composite Score:        {scorecard.composite_score:.2f}%")
    print(f"Intelligence Maturity Tier:     {scorecard.tier.value}")
    print(f"Certified Enterprise Ready:     {'YES (CERTIFIED)' if scorecard.certified_enterprise_ready else 'NO (FAILED)'}")
    print("-" * 80)
    print("RELIABILITY INTELLIGENCE SUMMARY:")
    print(f"  • RCA Pipeline Accuracy:       {rca_report.mean_rca_accuracy_pct:.2f}% ({rca_report.total_incidents_analyzed} incidents analyzed)")
    print(f"  • Patterns Detected:           {pattern_report.total_patterns_detected} ({pattern_report.repeated_patterns_identified} repeated patterns)")
    print(f"  • Knowledge Base Articles:     {kb_report.total_knowledge_articles} across {len(kb_report.categories_covered)} categories")
    print(f"  • Mean MTTR Reduction:         {opt_report.average_mttr_reduction_pct:.2f}% (Success Rate: {opt_report.recovery_success_rate_pct:.1f}%)")
    print(f"  • Failure Prevention Rate:     {prev_report.prevention_rate_pct:.2f}% ({prev_report.total_early_warnings_evaluated} early warnings)")
    print(f"  • Learning Simulation Tests:   {'PASSED' if sim_report.all_scenarios_passed else 'FAILED'} ({sim_report.total_scenarios_simulated}/4 scenarios)")
    print("-" * 80)
    print("WEIGHTED SCORECARD PILLARS:")
    print(f"  • Failure Analysis Accuracy (25%): {scorecard.failure_analysis_accuracy:.2f}%")
    print(f"  • Root Cause Identification (20%): {scorecard.root_cause_score:.2f}%")
    print(f"  • Knowledge Retention       (15%): {scorecard.knowledge_retention_score:.2f}%")
    print(f"  • Recovery Optimization     (20%): {scorecard.recovery_optimization_score:.2f}%")
    print(f"  • Prevention Capability     (15%): {scorecard.prevention_capability_score:.2f}%")
    print(f"  • Safety Controls            (5%): {scorecard.safety_controls_score:.2f}%")
    print("-" * 80)
    print(f"Standardized evidence repository exported to 'failure_learning_verification/' ({len(results['exported_files'])} artifacts):")
    for f in sorted(results["exported_files"]):
        print(f"  - {os.path.relpath(f, 'failure_learning_verification')}")
    print("=" * 80)

    if scorecard.certified_enterprise_ready and scorecard.composite_score >= 90.0:
        print("[SUCCESS] Phase 3H.5.6 Failure Learning & Recovery Optimization Verification PASSED.\n")
        sys.exit(0)
    else:
        print("[ERROR] Phase 3H.5.6 Verification FAILED to meet enterprise thresholds.\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
