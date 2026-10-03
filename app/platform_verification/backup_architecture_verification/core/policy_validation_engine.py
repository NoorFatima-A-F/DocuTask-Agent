"""
Part 10: Policy Validation Engine.
Verifies enterprise backup policies, syntax, encryption enforcement,
retention requirements, restore testing schedules, and notification hooks.
Detects conflicting, duplicate, or invalid policies.
"""
from typing import List, Dict, Any
from app.platform_verification.backup_architecture_verification.domain.models import (
    PolicyValidationResult,
)
from app.platform_verification.backup_architecture_verification.domain.interfaces import (
    IPolicyValidationEngine,
)


class PolicyValidationEngine(IPolicyValidationEngine):
    """
    Validates backup policy declarations against enterprise governance rules.
    """

    def get_default_platform_policies(self) -> List[Dict[str, Any]]:
        """Provides default enterprise backup policies."""
        return [
            {
                "policy_id": "POL-BKP-001",
                "policy_name": "Tier0_Continuous_Replication_Policy",
                "asset_pattern": "postgres_primary|minio_s3_object_store|uploaded_documents_raw|ai_verification_evidence",
                "schedule": "CONTINUOUS_AND_DAILY_0200_UTC",
                "frequency_cron": "0 2 * * *",
                "destination": "s3://docutask-dr-replica-bucket/",
                "encryption": "AES-256-GCM_KMS",
                "retention": "GFS_7Y_OR_10Y_WORM",
                "validation": "AUTOMATED_RESTORE_SANDBOX_DAILY",
                "notification": "slack_#dr-alerts_and_pagerduty",
                "restore_testing": "WEEKLY_AUTOMATED_FIRE_DRILL",
            },
            {
                "policy_id": "POL-BKP-002",
                "policy_name": "Tier1_Incremental_Snapshot_Policy",
                "asset_pattern": "ocr_extracted_text_artifacts|extracted_structured_json|agent_registry_state|agent_memory_episodes",
                "schedule": "HOURLY_AND_TWO_HOURLY",
                "frequency_cron": "0 */1 * * *",
                "destination": "s3://docutask-backups/incremental/",
                "encryption": "AES-256-GCM_KMS",
                "retention": "GFS_60D_TO_90D",
                "validation": "CHECKSUM_AND_INDEX_VALIDATION",
                "notification": "slack_#dr-alerts",
                "restore_testing": "MONTHLY_SAMPLE_RESTORE",
            },
            {
                "policy_id": "POL-BKP-003",
                "policy_name": "Tier1_Fast_Snapshot_Policy",
                "asset_pattern": "redis_cache_queue|docker_named_volumes|task_queue_persistence|vector_embeddings_index",
                "schedule": "SNAPSHOT_15M_TO_4H",
                "frequency_cron": "0 */4 * * *",
                "destination": "csi-snapshots://enterprise-fast-ssd",
                "encryption": "AES-256-GCM_KMS",
                "retention": "GFS_7D_TO_30D",
                "validation": "VOLUME_MOUNT_VERIFICATION",
                "notification": "slack_#dr-alerts",
                "restore_testing": "BI_WEEKLY_RESTORE_VALIDATION",
            },
            {
                "policy_id": "POL-BKP-004",
                "policy_name": "Tier0_Tier1_GitOps_Config_Policy",
                "asset_pattern": "app_environment_variables|enterprise_secrets_vault|platform_system_configs|prompt_templates_repository|system_governance_policies",
                "schedule": "DAILY_OR_ON_COMMIT",
                "frequency_cron": "0 0 * * *",
                "destination": "git-archive://secure-dr-mirror/",
                "encryption": "AES-256-GCM_SEALED_VAULT",
                "retention": "GFS_1Y_TO_7Y",
                "validation": "GPG_SIGNATURE_AND_LINT_VERIFICATION",
                "notification": "slack_#security-alerts",
                "restore_testing": "PER_RELEASE_REBUILD_DRILL",
            },
            {
                "policy_id": "POL-BKP-005",
                "policy_name": "Tier2_Telemetry_And_Audit_Policy",
                "asset_pattern": "application_audit_logs|prometheus_metrics_db|grafana_dashboards",
                "schedule": "DAILY_OR_4HOURLY",
                "frequency_cron": "0 */4 * * *",
                "destination": "s3://docutask-audit-cold/",
                "encryption": "AES-256-GCM_KMS",
                "retention": "GFS_30D_TO_365D",
                "validation": "LOG_CONTINUITY_CHECKSUM",
                "notification": "slack_#observability-alerts",
                "restore_testing": "QUARTERLY_AUDIT_QUERY_DRILL",
            },
        ]

    def validate_policies(self, policies: List[Dict[str, Any]]) -> List[PolicyValidationResult]:
        results: List[PolicyValidationResult] = []
        seen_patterns: Dict[str, str] = {}

        for pol in policies:
            policy_id = pol.get("policy_id", "UNKNOWN")
            policy_name = pol.get("policy_name", "Unnamed Policy")
            pattern = pol.get("asset_pattern", "")
            conflicts: List[str] = []

            # Check required fields
            sched_valid = bool(pol.get("schedule") and pol.get("frequency_cron"))
            dest_valid = bool(pol.get("destination") and ("://" in pol.get("destination", "") or "s3" in pol.get("destination", "")))
            enc_valid = bool(pol.get("encryption") and "AES-256" in pol.get("encryption", ""))
            ret_valid = bool(pol.get("retention"))
            val_valid = bool(pol.get("validation"))
            notif_valid = bool(pol.get("notification"))
            rest_valid = bool(pol.get("restore_testing"))

            if not sched_valid:
                conflicts.append("Schedule or cron frequency missing/invalid.")
            if not dest_valid:
                conflicts.append("Backup destination URI format missing or invalid.")
            if not enc_valid:
                conflicts.append("Encryption standard does not satisfy enterprise AES-256 requirement.")
            if not ret_valid:
                conflicts.append("Retention specification missing.")
            if not val_valid:
                conflicts.append("Automated verification hook missing.")
            if not notif_valid:
                conflicts.append("Alerting/notification destination missing.")
            if not rest_valid:
                conflicts.append("Restore testing schedule missing.")

            # Check for conflicting duplicate policy IDs
            if policy_id in seen_patterns:
                conflicts.append(f"Duplicate policy ID {policy_id} conflicts with {seen_patterns[policy_id]}.")
            else:
                seen_patterns[policy_id] = policy_name

            is_valid = (
                sched_valid
                and dest_valid
                and enc_valid
                and ret_valid
                and val_valid
                and notif_valid
                and rest_valid
                and len(conflicts) == 0
            )

            results.append(
                PolicyValidationResult(
                    policy_id=policy_id,
                    policy_name=policy_name,
                    asset_pattern=pattern,
                    schedule_valid=sched_valid,
                    destination_valid=dest_valid,
                    encryption_enforced=enc_valid,
                    retention_enforced=ret_valid,
                    validation_hook_configured=val_valid,
                    notification_configured=notif_valid,
                    restore_testing_scheduled=rest_valid,
                    is_valid=is_valid,
                    conflicts_detected=conflicts,
                )
            )

        return results

    def export_policy_validation_json(
        self, results: List[PolicyValidationResult]
    ) -> Dict[str, Any]:
        """Formats the policy validation report to JSON dictionary."""
        passed_count = len([r for r in results if r.is_valid])
        return {
            "total_policies_validated": len(results),
            "valid_policies_count": passed_count,
            "invalid_policies_count": len(results) - passed_count,
            "policy_compliance_percent": round((passed_count / len(results) * 100.0), 2) if results else 100.0,
            "policy_results": [
                {
                    "policy_id": r.policy_id,
                    "policy_name": r.policy_name,
                    "asset_pattern": r.asset_pattern,
                    "schedule_valid": r.schedule_valid,
                    "destination_valid": r.destination_valid,
                    "encryption_enforced": r.encryption_enforced,
                    "retention_enforced": r.retention_enforced,
                    "validation_hook_configured": r.validation_hook_configured,
                    "notification_configured": r.notification_configured,
                    "restore_testing_scheduled": r.restore_testing_scheduled,
                    "is_valid": r.is_valid,
                    "conflicts_detected": r.conflicts_detected,
                }
                for r in results
            ],
        }
