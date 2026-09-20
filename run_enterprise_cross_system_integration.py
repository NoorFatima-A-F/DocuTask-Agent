#!/usr/bin/env python3
"""Master CLI Runner for Phase 4: Enterprise Cross-System Integration & End-to-End Platform Validation Framework."""

import os
import sys

# Ensure repository root is on sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.platform_verification.enterprise_cross_system_integration.runtime.integration_verification_runtime import (
    CrossSystemIntegrationVerificationRuntime,
)


def main():
    print("=" * 80)
    print("  DocuTask Agent - Enterprise Cross-System Integration Framework")
    print("  Phase 4 Verification Suite (End-to-End Cross-Subsystem Platform Validation)")
    print("=" * 80)
    print("\n[*] Initializing 22 enterprise cross-system verifiers...\n")

    runtime = CrossSystemIntegrationVerificationRuntime()
    report = runtime.execute_all()

    print("-" * 80)
    print("  CROSS-SYSTEM INTEGRATION PHASES EXECUTION SUMMARY")
    print("-" * 80)

    subphase_labels = {
        "dependency_mapping": ("Phase 4A", "Enterprise Dependency Mapping & DAG"),
        "interface_contract": ("Phase 4B", "Cross-System Interface Contracts"),
        "api_chain": ("Phase 4C", "API Request Chain Integrity"),
        "state_propagation": ("Phase 4D", "Distributed State Propagation"),
        "knowledge_flow": ("Phase 4E", "Knowledge Flow & Data Pipeline"),
        "memory_interaction": ("Phase 4F", "Multi-Tier Memory Interaction"),
        "planning_pipeline": ("Phase 4G", "Planning Pipeline & Execution Engine"),
        "agent_collaboration": ("Phase 4H", "Multi-Agent Collaboration & Consensus"),
        "cognitive_integration": ("Phase 4I", "Knowledge & Cognitive Integration"),
        "security_boundary": ("Phase 4J", "Security Boundaries & Tenant Isolation"),
        "lifecycle_integration": ("Phase 4K", "Artifact & System Lifecycle"),
        "deployment_integration": ("Phase 4L", "Deployment, Canary & Rollback"),
        "marketplace_validation": ("Phase 4M", "AI Marketplace & Packaging"),
        "event_bus": ("Phase 4N", "Event Bus & Stream Processing"),
        "scheduler": ("Phase 4O", "Distributed Scheduler & Cron Engine"),
        "observability_integration": ("Phase 4P", "Unified Observability & Tracing"),
        "data_integrity": ("Phase 4Q", "Data Integrity & Corruption Recovery"),
        "failure_propagation": ("Phase 4R", "Failure Propagation & Blast Radius"),
        "cross_system_performance": ("Phase 4S", "Cross-System Performance & Latency"),
        "enterprise_workflows": ("Phase 4T", "Large End-to-End Enterprise Workflows"),
        "integration_regression": ("Phase 4U", "Integration Regression Suite"),
        "evidence_generation": ("Phase 4V", "Cryptographic Evidence Generation"),
    }

    for key, (phase_tag, label) in subphase_labels.items():
        rep = report.reports.get(key)
        if rep:
            score_val = rep.score if hasattr(rep, "score") else rep.get("score", 0.0)
            status_val = rep.status.value if hasattr(rep, "status") else rep.get("status", "UNKNOWN")
            pass_tag = "[PASS]" if status_val in ("PASSED", "VerificationStatus.PASSED") else "[FAIL]"
            print(f"  {pass_tag} {phase_tag:<12}: {label:<48} (Score: {score_val:.1f}%)")

    print("\n" + "-" * 80)
    print("  7-PILLAR INTEGRATION QUALITY BREAKDOWN")
    print("-" * 80)

    for cat in report.score.categories:
        weight_pct = int(cat.weight * 100)
        print(f"  - {cat.name:<48} [Weight: {weight_pct:>2}%] Score: {cat.score:>6.2f}% | Contribution: {cat.weighted_score:>5.2f}%")

    output_dir = os.path.abspath(runtime.exporter.DEFAULT_OUTPUT_DIR)
    manifest_file = os.path.join(output_dir, "manifest.json")
    artifact_count = 0
    if os.path.exists(manifest_file):
        import json
        with open(manifest_file, "r") as f:
            manifest = json.load(f)
            artifact_count = len(manifest) + 1

    print("\n" + "=" * 80)
    print(f"  OVERALL INTEGRATION SCORE   : {report.score.overall_score:.2f}%")
    print(f"  CERTIFICATION TIER          : {report.score.certification_tier.value}")
    print(f"  VERIFICATION STATUS         : {report.status.value}")
    print(f"  EVIDENCE DIRECTORY          : {output_dir}")
    print(f"  ARTIFACTS GENERATED         : {artifact_count} files (SHA-256 verified)")
    print("=" * 80 + "\n")

    return 0 if report.status.value == "PASSED" else 1


if __name__ == "__main__":
    sys.exit(main())
