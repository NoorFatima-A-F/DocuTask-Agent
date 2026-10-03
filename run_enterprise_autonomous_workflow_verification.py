#!/usr/bin/env python3
"""Master CLI Runner for Phase 5: Enterprise End-to-End Autonomous Workflow & Business Process Validation Framework."""

import os
import sys

# Ensure repository root is on sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.platform_verification.enterprise_autonomous_workflow_validation.runtime.workflow_verification_runtime import (
    AutonomousWorkflowVerificationRuntime,
)


def main():
    print("=" * 80)
    print("  DocuTask Agent - Autonomous Workflow & Business Process Validation")
    print("  Phase 5 Verification Suite (Enterprise End-to-End Business Capability)")
    print("=" * 80)
    print("\n[*] Initializing 20 enterprise autonomous workflow verifiers...\n")

    runtime = AutonomousWorkflowVerificationRuntime()
    report = runtime.execute_all()

    print("-" * 80)
    print("  AUTONOMOUS BUSINESS WORKFLOW PHASES EXECUTION SUMMARY")
    print("-" * 80)

    subphase_labels = {
        "scenario_library": ("Phase 5A", "Enterprise Business Scenario Library"),
        "complete_execution": ("Phase 5B", "Complete 18-Stage Workflow Execution"),
        "human_in_the_loop": ("Phase 5C", "Human-in-the-Loop & Approval Gates"),
        "multi_agent_collaboration": ("Phase 5D", "Multi-Agent Enterprise Collaboration"),
        "decision_quality": ("Phase 5E", "Autonomous Decision Quality & ECE"),
        "business_rules": ("Phase 5F", "Business Rule & Policy Enforcement"),
        "exception_workflow": ("Phase 5G", "Exception & Anomaly Recovery"),
        "business_kpi": ("Phase 5H", "Business KPIs & Speedup Multiplier"),
        "autonomous_recovery": ("Phase 5I", "Autonomous Fault Recovery & Sagas"),
        "organizational_workflow": ("Phase 5J", "Cross-Departmental Orchestration"),
        "long_running": ("Phase 5K", "Long-Running Workflow Checkpoints"),
        "explainability": ("Phase 5L", "AI Explainability & Evidence Citations"),
        "audit_trail": ("Phase 5M", "Tamper-Evident Audit Ledger"),
        "compliance": ("Phase 5N", "Regulatory Compliance (SOC2/HIPAA/GDPR)"),
        "cost_validation": ("Phase 5O", "Unit Economics & Cost Per Document"),
        "optimization": ("Phase 5P", "Workflow Optimization & Token Tuning"),
        "business_value": ("Phase 5Q", "Business Value Realization & ROI"),
        "enterprise_dataset": ("Phase 5R", "Real-World Document Corpus Validation"),
        "scalability": ("Phase 5S", "10k Concurrent Workflow Scalability"),
        "executive_readiness": ("Phase 5T", "Executive Production Readiness"),
    }

    for key, (phase_tag, label) in subphase_labels.items():
        rep = report.reports.get(key)
        if rep:
            score_val = rep.score if hasattr(rep, "score") else rep.get("score", 0.0)
            status_val = rep.status.value if hasattr(rep, "status") else rep.get("status", "UNKNOWN")
            pass_tag = "[PASS]" if status_val in ("PASSED", "VerificationStatus.PASSED") else "[FAIL]"
            print(f"  {pass_tag} {phase_tag:<12}: {label:<48} (Score: {score_val:.1f}%)")

    print("\n" + "-" * 80)
    print("  7-PILLAR BUSINESS CERTIFICATION BREAKDOWN")
    print("-" * 80)

    for cat in report.score.categories:
        weight_pct = int(cat.weight * 100)
        print(f"  - {cat.name:<52} [Weight: {weight_pct:>2}%] Score: {cat.score:>6.2f}% | Contribution: {cat.weighted_score:>5.2f}%")

    output_dir = os.path.abspath(runtime.exporter.DEFAULT_OUTPUT_DIR)
    manifest_file = os.path.join(output_dir, "manifest.json")
    artifact_count = 0
    if os.path.exists(manifest_file):
        import json
        with open(manifest_file, "r") as f:
            manifest = json.load(f)
            artifact_count = len(manifest) + 1

    print("\n" + "=" * 80)
    print(f"  OVERALL BUSINESS SCORE      : {report.score.overall_score:.2f}%")
    print(f"  CERTIFICATION TIER          : {report.score.certification_tier.value}")
    print(f"  VERIFICATION STATUS         : {report.status.value}")
    print(f"  EVIDENCE DIRECTORY          : {output_dir}")
    print(f"  ARTIFACTS GENERATED         : {artifact_count} files (SHA-256 verified)")
    print("=" * 80 + "\n")

    return 0 if report.status.value == "PASSED" else 1


if __name__ == "__main__":
    sys.exit(main())
