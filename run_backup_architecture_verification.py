"""
Enterprise Backup Strategy & Architecture Verification Runner (Part 3G.2A).
Executes the full automated 14-part verification engine and exports audit artifacts.
"""
import sys
import logging
from pathlib import Path

from app.platform_verification.backup_architecture_verification.runtime.backup_verification_runtime import (
    BackupArchitectureVerificationRuntime,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("BackupArchitectureVerifier")


def main() -> int:
    workspace_root = Path(__file__).resolve().parent
    evidence_dir = workspace_root / "evidence" / "backup_architecture_verification"

    logger.info("Initializing Enterprise Backup Architecture Verification Framework (Part 3G.2A)...")
    runtime = BackupArchitectureVerificationRuntime()

    logger.info("Executing 14-phase automated verification pipeline across all platform assets...")
    result = runtime.run_full_verification(export_evidence=True, output_dir=str(evidence_dir))

    scorecard = result["scorecard"]
    verification_data = result["verification_data"]
    artifacts = result["exported_artifacts"]

    print("\n" + "=" * 90)
    print("  ENTERPRISE BACKUP STRATEGY & ARCHITECTURE VERIFICATION REPORT (PART 3G.2A)")
    print("=" * 90)
    print(f"  Platform Version            : {runtime.platform_version}")
    print(f"  Environment                 : {runtime.environment}")
    print(f"  Git Commit SHA              : {runtime.git_commit_sha}")
    print(f"  Execution Duration          : {scorecard.execution_duration_ms:.2f} ms")
    print("-" * 90)
    print(f"  [Part 1] Discovered Assets   : {verification_data['asset_inventory']['total_assets_discovered']} assets")
    print(f"  [Part 2] Classified Matrix   : Tier0: {verification_data['classification_matrix']['tier_summary']['Tier0_Mission_Critical']}, "
          f"Tier1: {verification_data['classification_matrix']['tier_summary']['Tier1_Business_Critical']}, "
          f"Tier2: {verification_data['classification_matrix']['tier_summary']['Tier2_Operational']}, "
          f"Tier3: {verification_data['classification_matrix']['tier_summary']['Tier3_Rebuildable']}")
    print(f"  [Part 3] Strategy Compliance : {verification_data['strategy_report']['overall_strategy_compliance_percent']}%")
    print(f"  [Part 4] Recovery DAG Valid  : {verification_data['dependency_graph']['is_valid_dag']} (Topological Stages: {len(verification_data['dependency_graph']['topological_recovery_order'])})")
    print(f"  [Part 5] Backup Coverage     : Tier0: {verification_data['coverage_report']['tier0_coverage_percent']}%, "
          f"Tier1: {verification_data['coverage_report']['tier1_coverage_percent']}%, "
          f"Tier2: {verification_data['coverage_report']['tier2_coverage_percent']}%, "
          f"Overall: {verification_data['coverage_report']['total_coverage_percent']}%")
    print(f"  [Part 6] Retention GFS Check : {verification_data['retention_report']['retention_compliance_percent']}% compliant")
    print(f"  [Part 7] 8-Stage Lifecycle   : {verification_data['lifecycle_report']['lifecycle_compliance_percent']}% compliant")
    print(f"  [Part 8] Ownership Mapping   : {verification_data['ownership_report']['ownership_compliance_percent']}% assigned")
    print(f"  [Part 9] Cryptographic Meta : {verification_data['metadata_registry']['total_backups_registered']} verified entries")
    print(f"  [Part 10] Policy Validation  : {verification_data['policy_validation']['policy_compliance_percent']}% compliant")
    print(f"  [Part 11] Consistency Passed : {result['consistency_passed']}")
    print(f"  [Part 12] Prometheus/OTel/GF : Exporters Active (Success Rate: {verification_data['metrics']['summary_metrics']['backup_success_rate_percent']}%)")
    print("-" * 90)
    print("  CATEGORY SCORE BREAKDOWN:")
    print(f"    - Asset Discovery    (10%) : {scorecard.asset_discovery_score:.1f} / 100")
    print(f"    - Classification     (10%) : {scorecard.classification_score:.1f} / 100")
    print(f"    - Strategy Quality   (20%) : {scorecard.strategy_quality_score:.1f} / 100")
    print(f"    - Coverage           (20%) : {scorecard.coverage_score:.1f} / 100")
    print(f"    - Retention Policy   (10%) : {scorecard.retention_score:.1f} / 100")
    print(f"    - Lifecycle Validation(10%): {scorecard.lifecycle_score:.1f} / 100")
    print(f"    - Metadata Registry  (10%) : {scorecard.metadata_score:.1f} / 100")
    print(f"    - Observability       (5%) : {scorecard.observability_score:.1f} / 100")
    print(f"    - Policy Validation   (5%) : {scorecard.policy_validation_score:.1f} / 100")
    print("-" * 90)
    print(f"  OVERALL BACKUP READINESS SCORE: {scorecard.readiness_composite_score:.2f} / 100.00")
    print(f"  ENTERPRISE CERTIFICATION TIER : [{scorecard.certification_tier.value.upper()}]")
    print(f"  AUDIT PASS STATUS             : {'PASSED [OK]' if scorecard.passed else 'FAILED [NON-COMPLIANT]'}")
    print("-" * 90)
    print(f"  Evidence Artifacts Generated ({len(artifacts)} files):")
    for name, path in artifacts.items():
        print(f"    • {name} -> {path}")
    print("=" * 90 + "\n")

    return 0 if scorecard.passed else 1


if __name__ == "__main__":
    sys.exit(main())
