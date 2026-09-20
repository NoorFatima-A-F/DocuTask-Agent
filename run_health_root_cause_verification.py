"""Master CLI Runner for Phase 3H.4.2 - Health Root Cause Analysis & Failure Attribution Framework.

Executes all 14 sub-parts of Phase 3H.4.2 verification:
1. Dependency Graph Modeling
2. Health Event Correlation
3. Failure Classification (5 Categories)
4. Root Cause Scoring Engine
5. Impact Analysis Engine
6. Incident Severity Classification (SEV-1 to SEV-4)
7. Failure Timeline Reconstruction
8. Cascading Failure Detection
9. False Positive Reduction
10. Historical Incident Memory & Learning
11. Health API Diagnosis Extensions
12. 5 Automated Failure Scenarios
13. Evidence Generation (8 JSON manifests in health_root_cause_verification/)
14. Quality Scoring (6-dimension weighted scorecard)
"""

import sys
import os
import io

# Enforce UTF-8 stdout for Windows terminals
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.platform_verification.health_root_cause.runtime.health_root_cause_runtime import (
    HealthRootCauseRuntime,
)


def main() -> int:
    print("=" * 100)
    print(" DOCUTASK AGENT - ENTERPRISE HEALTH ROOT CAUSE ANALYSIS & FAILURE ATTRIBUTION")
    print(" PHASE 3H.4.2: TOPOLOGY, EVENT CORRELATION, CASCADE ISOLATION & OPERATIONAL DIAGNOSIS")
    print("=" * 100)

    runtime = HealthRootCauseRuntime()
    print("\n[*] Initializing Phase 3H.4.2 Health Root Cause Analysis verification engine...")
    results = runtime.run_full_verification()

    dep_rep = results["dependency_report"]
    corr_rep = results["correlation_report"]
    rc_rep = results["root_cause_report"]
    imp_rep = results["impact_report"]
    time_rep = results["timeline_report"]
    casc_rep = results["cascade_report"]
    fp_rep = results["false_positive_report"]
    mem_rep = results["memory_report"]
    scen_rep = results["scenarios_report"]
    scorecard = results["scorecard"]
    manifests = results["exported_manifests"]

    # 1. Dependency Graph Topology Table
    print("\n" + "-" * 100)
    print(" 1. RUNTIME DEPENDENCY GRAPH TOPOLOGY (DAG)")
    print("-" * 100)
    print(f" {'COMPONENT':<20} | {'TYPE':<16} | {'CRITICALITY':<12} | {'DEPENDS ON':<24} | {'DEPENDENTS':<20}")
    print("-" * 100)
    for name, node in dep_rep.nodes.items():
        deps_str = ", ".join(node.depends_on) or "none (root)"
        dept_str = ", ".join(node.dependents) or "none (leaf)"
        print(f" {node.name:<20} | {node.component_type:<16} | {node.criticality.value:<12} | {deps_str:<24} | {dept_str:<20}")

    # 2. Correlated Event Clusters Table
    print("\n" + "-" * 100)
    print(" 2. MULTI-SIGNAL HEALTH EVENT CORRELATION")
    print("-" * 100)
    print(f" {'CLUSTER ID':<24} | {'COMPONENT':<16} | {'SIGNALS':<8} | {'CONFIDENCE':<12} | {'CORRELATED SUMMARY':<34}")
    print("-" * 100)
    for c in corr_rep.clusters:
        print(f" {c.cluster_id:<24} | {c.primary_component:<16} | {c.correlated_signals_count:>7} | {c.correlation_score:>10.2f} | {c.summary[:32]:<34}")

    # 3. Root Cause Scoring Table
    print("\n" + "-" * 100)
    print(" 3. ROOT CAUSE ATTRIBUTION & CONFIDENCE SCORING")
    print("-" * 100)
    pr = rc_rep.primary_root_cause
    print(f" Primary Root Cause:   {pr.component} -> {pr.reason} ({pr.category.value})")
    print(f" Attribution Score:    {pr.confidence:.2f} (Signal: {pr.signal_strength:.2f}, Topology: {pr.topological_score:.2f}, History: {pr.historical_match_score:.2f})")
    print(f" Diagnostic Summary:   {pr.evidence_summary}")
    print(f" Recovery Action:      {pr.recommended_action}")

    # 4. Impact Assessment Table
    print("\n" + "-" * 100)
    print(" 4. BLAST RADIUS & SERVICE IMPACT ANALYSIS")
    print("-" * 100)
    for imp in imp_rep.assessments:
        aff_str = ", ".join(imp.affected_services)
        unaff_str = ", ".join(imp.unaffected_services)
        print(f" [!] Root Cause: {imp.root_cause_component} | Severity: {imp.severity.value} | Blast Radius: {imp.estimated_blast_radius_pct:.1f}%")
        print(f"     Affected:   {aff_str}")
        print(f"     Unaffected: {unaff_str}")
        print(f"     Business:   {imp.business_impact}")

    # 5. Cascading Failure Isolation Table
    print("\n" + "-" * 100)
    print(" 5. CASCADING PROPAGATION ISOLATION")
    print("-" * 100)
    print(f" Primary Origin: {casc_rep.primary_origin_component} | Propagation Depth: {casc_rep.propagation_depth}")
    for node in casc_rep.cascade_chain:
        flag = "[PRIMARY ROOT CAUSE]" if node.is_primary_root_cause else "[SECONDARY SYMPTOM]"
        print(f"   Step {node.step_order}: {node.component:<18} {flag:<22} -> {node.symptom}")

    # 6. Failure Timeline Table
    print("\n" + "-" * 100)
    print(" 6. FAILURE ONSET & PROPAGATION TIMELINE")
    print("-" * 100)
    for m in time_rep.milestones:
        print(f" [{m.time_offset}] ({m.severity:<8}) {m.component:<16} | State: {m.state_change:<24} | {m.event}")

    # 7. False Positive & Memory Table
    print("\n" + "-" * 100)
    print(" 7. FALSE POSITIVE DAMPING & HISTORICAL MEMORY")
    print("-" * 100)
    print(f" Total Evaluated Signals:    {fp_rep.total_signals_evaluated} | Damped Transient Spikes: {fp_rep.transient_spikes_damped}")
    print(f" False Positive Rate:        {fp_rep.false_positive_rate_pct:.2f}% (Target: 0.00%)")
    print(f" Known Historical Signatures: {mem_rep.total_known_signatures}")
    for sig in mem_rep.signatures:
        print(f"   - {sig.signature_id:<20}: {sig.root_cause} (Occurrences: {sig.historical_occurrences})")

    # 8. 5 Verification Scenarios Table
    print("\n" + "-" * 100)
    print(" 8. 5 AUTOMATED ROOT CAUSE DIAGNOSIS SCENARIOS")
    print("-" * 100)
    for s in scen_rep.scenarios:
        print(f" [✓] {s.scenario_id:<26} | Correct: {s.attributed_correctly} | Cascade Isolated: {s.cascade_isolated} | Conf: {s.confidence:.2f}")

    # 9. Composite Scorecard
    print("\n" + "=" * 100)
    print(" ENTERPRISE HEALTH ROOT CAUSE ANALYSIS SCORECARD")
    print("=" * 100)
    print(f" 1. Root Cause Accuracy (Weight 30%):        {scorecard.root_cause_accuracy_score:>6.2f} / 100")
    print(f" 2. Dependency Analysis (Weight 20%):        {scorecard.dependency_analysis_score:>6.2f} / 100")
    print(f" 3. Impact Prediction (Weight 15%):          {scorecard.impact_prediction_score:>6.2f} / 100")
    print(f" 4. Event Correlation (Weight 15%):          {scorecard.event_correlation_score:>6.2f} / 100")
    print(f" 5. False Positive Control (Weight 10%):     {scorecard.false_positive_control_score:>6.2f} / 100")
    print(f" 6. Evidence Quality (Weight 10%):           {scorecard.evidence_quality_score:>6.2f} / 100")
    print("-" * 100)
    print(f" OVERALL WEIGHTED DIAGNOSIS SCORE:           {scorecard.overall_score:>6.2f}%")
    print(f" CERTIFICATION TIER:                         {scorecard.certification_tier.value}")
    print(f" VERDICT:                                    {scorecard.certification_verdict}")
    print("=" * 100)

    # 10. Manifests Export List
    print("\n[+] Exported 8 Structured Audit Evidence Manifests (health_root_cause_verification/):")
    for fname, path in manifests.items():
        print(f"    - {fname:<34} -> {path}")

    if scorecard.passed and scorecard.overall_score >= 95.0:
        print("\n[SUCCESS] Phase 3H.4.2 Health Root Cause Analysis Verification PASSED with Tier 'Enterprise Incident Diagnosis Ready' (>= 95.00%).")
        return 0
    else:
        print(f"\n[FAILURE] Phase 3H.4.2 Verification did not meet target (Score: {scorecard.overall_score}%).")
        return 1


if __name__ == "__main__":
    sys.exit(main())
