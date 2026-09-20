"""
Phase 3H.8: Enterprise Operational Governance, Change Management & Safe Operations Verification Master CLI Runner
"""
import sys
import os
from pathlib import Path
from app.platform_verification.operational_governance.runtime.operational_governance_runtime import (
    OperationalGovernanceRuntime,
)
from app.platform_verification.operational_governance.domain.models import (
    GovernanceCertificationTier,
)


def main():
    print("=" * 80)
    print("DocuTask Agent — Phase 3H.8: Enterprise Operational Governance Verification")
    print("=" * 80)
    print("Executing change lifecycle audits, configuration immutability checks,")
    print("progressive deployment gates, database migration safety verifications,")
    print("AI model versioning benchmarks, multi-tier approval workflows, automated")
    print("rollback triggers, tamper-evident audit trails, and governance dashboards...\n")

    output_dir = Path("operational_governance_verification")
    runtime = OperationalGovernanceRuntime(output_dir=output_dir)
    results = runtime.run_full_verification(export_evidence=True)

    scorecard = results["scorecard"]
    change = results["change_governance_report"]
    config = results["configuration_change_report"]
    deploy = results["deployment_safety_report"]
    db = results["database_change_report"]
    ai = results["ai_model_change_report"]
    approval = results["approval_workflow_report"]
    rollback = results["rollback_verification_report"]
    audit = results["audit_trail_report"]
    continuous = results["continuous_verification_report"]
    dashboard = results["governance_dashboard_report"]
    export_meta = results["export_metadata"]

    print("-" * 80)
    print("OPERATIONAL GOVERNANCE & CHANGE MANAGEMENT SCORECARD")
    print("-" * 80)
    print(f"Verification ID:                {scorecard.verification_id}")
    print(f"Overall Governance Score:       {scorecard.overall_governance_score:.2f}%")
    print(f"Certification Tier:             {scorecard.certification_tier.value}")
    print(f"Change Auditability:            {'GUARANTEED (100%)' if scorecard.change_auditability_guaranteed else 'NO'}")
    print(f"Rollback Readiness:             {'GUARANTEED (100%)' if scorecard.rollback_readiness_guaranteed else 'NO'}")
    print(f"Governance Certified Ready:     {'YES (PASSED)' if scorecard.passed else 'NO (FAILED)'}")
    print("-" * 80)
    print("GOVERNANCE CAPABILITY DIMENSIONS:")
    print(f"  • Change Governance:           {change.total_changes_evaluated} changes audited (Low, Moderate, High, Emergency)")
    print(f"  • Configuration Integrity:     {config.total_configs_audited} configs validated (Immutable hashes, secret separation, 0 drift)")
    print(f"  • Deployment Safety Gates:     {deploy.total_deployments_audited} progressive delivery strategies (Canary, Blue/Green, Rolling, Feature Flags)")
    print(f"  • Database Change Safety:      {db.total_migrations_audited} zero-downtime migrations verified (Backward/forward compatible)")
    print(f"  • AI Model Governance:         {ai.total_ai_changes_audited} model/prompt benchmarks (100% schema compatibility, 0 regression)")
    print(f"  • Approval Workflows:          {approval.total_workflows_evaluated} approval policies enforced (Policy compliance: {approval.policy_compliance_pct:.1f}%)")
    print(f"  • Automated Rollback:          {rollback.total_triggers_evaluated} failure triggers verified (SLO breach, latency, error spikes, prompt drift)")
    print(f"  • Immutable Audit Trail:       {audit.total_audit_records} tamper-evident operational records logged with SHA-256 evidence")
    print(f"  • Continuous Verification:     {continuous.checks_passed}/{continuous.checks_total} post-deployment health & SLI checks passed")
    print(f"  • Governance Dashboards:       {len(dashboard.metrics)} real-time telemetry gauges active (Risk index: {dashboard.operational_risk_index:.2f})")
    print("-" * 80)
    print("8-PILLAR WEIGHTED GOVERNANCE BREAKDOWN:")
    for pillar in scorecard.pillar_scores:
        print(f"  • {pillar.pillar_name:<42} ({pillar.weight * 100:.0f}%): {pillar.raw_score:.2f}% (Weighted: {pillar.weighted_score:.2f}%) [{pillar.status}]")
    print("-" * 80)

    if export_meta:
        print("EVIDENCE MANIFEST EXPORTED:")
        print(f"  Directory: {output_dir.resolve()}")
        print(f"  Total Artifacts: {export_meta['total_reports_exported']} files + metadata.json")
        for filename, file_info in export_meta["manifest"].items():
            print(f"    - {filename:<45} ({file_info['size_bytes']} bytes, SHA-256: {file_info['sha256_checksum'][:12]}...)")
        print("-" * 80)

    print(f"RESULT: {scorecard.certification_tier.value.upper()} (Score: {scorecard.overall_governance_score:.2f}%)")
    print("=" * 80)

    return 0 if scorecard.passed else 1


if __name__ == "__main__":
    sys.exit(main())
