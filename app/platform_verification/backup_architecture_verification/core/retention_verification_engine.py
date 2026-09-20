"""
Part 6: Retention Policy Verification Engine.
Validates retention policies, Grandfather-Father-Son (GFS) schemes, legal holds,
and detects infinite retention, missing retention, and accidental purge risks.
"""
from typing import List, Dict, Any
from app.platform_verification.backup_architecture_verification.domain.models import (
    CriticalityTier,
    AssetInventoryItem,
    RetentionPolicyConfig,
    RetentionValidationResult,
)
from app.platform_verification.backup_architecture_verification.domain.interfaces import (
    IRetentionVerificationEngine,
)


class RetentionVerificationEngine(IRetentionVerificationEngine):
    """
    Verifies retention compliance according to enterprise data governance,
    SOC 2, ISO 27001, and regulatory compliance guidelines.
    """

    def get_default_platform_retention_policies(self) -> Dict[str, RetentionPolicyConfig]:
        """Provides enterprise default GFS retention policies for platform assets."""
        return {
            "postgres_primary": RetentionPolicyConfig(
                asset_name="postgres_primary",
                daily_retention_days=30,
                weekly_retention_weeks=12,
                monthly_retention_months=12,
                yearly_retention_years=7,
                archival_tier="glacier_deep_archive",
                legal_hold_supported=True,
                immutability_enabled=True,
                auto_expiration_enabled=True,
                secure_deletion_method="crypto_shredding_and_nist_800_88",
            ),
            "redis_cache_queue": RetentionPolicyConfig(
                asset_name="redis_cache_queue",
                daily_retention_days=7,
                weekly_retention_weeks=2,
                monthly_retention_months=0,
                yearly_retention_years=0,
                archival_tier="standard_ia",
                legal_hold_supported=False,
                immutability_enabled=False,
                auto_expiration_enabled=True,
                secure_deletion_method="automated_purge",
            ),
            "docker_named_volumes": RetentionPolicyConfig(
                asset_name="docker_named_volumes",
                daily_retention_days=14,
                weekly_retention_weeks=4,
                monthly_retention_months=0,
                yearly_retention_years=0,
                archival_tier="csi_snapshot_store",
                legal_hold_supported=False,
                immutability_enabled=False,
                auto_expiration_enabled=True,
                secure_deletion_method="csi_volume_deletion",
            ),
            "minio_s3_object_store": RetentionPolicyConfig(
                asset_name="minio_s3_object_store",
                daily_retention_days=90,
                weekly_retention_weeks=26,
                monthly_retention_months=24,
                yearly_retention_years=7,
                archival_tier="glacier_instant_retrieval",
                legal_hold_supported=True,
                immutability_enabled=True,
                auto_expiration_enabled=True,
                secure_deletion_method="crypto_shredding",
            ),
            "uploaded_documents_raw": RetentionPolicyConfig(
                asset_name="uploaded_documents_raw",
                daily_retention_days=90,
                weekly_retention_weeks=52,
                monthly_retention_months=84,
                yearly_retention_years=7,
                archival_tier="glacier_deep_archive",
                legal_hold_supported=True,
                immutability_enabled=True,
                auto_expiration_enabled=True,
                secure_deletion_method="crypto_shredding",
            ),
            "ocr_extracted_text_artifacts": RetentionPolicyConfig(
                asset_name="ocr_extracted_text_artifacts",
                daily_retention_days=60,
                weekly_retention_weeks=12,
                monthly_retention_months=6,
                yearly_retention_years=1,
                archival_tier="standard_ia",
                legal_hold_supported=False,
                immutability_enabled=False,
                auto_expiration_enabled=True,
                secure_deletion_method="automated_purge",
            ),
            "extracted_structured_json": RetentionPolicyConfig(
                asset_name="extracted_structured_json",
                daily_retention_days=90,
                weekly_retention_weeks=26,
                monthly_retention_months=12,
                yearly_retention_years=3,
                archival_tier="glacier_flexible_retrieval",
                legal_hold_supported=True,
                immutability_enabled=True,
                auto_expiration_enabled=True,
                secure_deletion_method="crypto_shredding",
            ),
            "ai_verification_evidence": RetentionPolicyConfig(
                asset_name="ai_verification_evidence",
                daily_retention_days=365,
                weekly_retention_weeks=52,
                monthly_retention_months=120,
                yearly_retention_years=10,
                archival_tier="worm_compliance_vault",
                legal_hold_supported=True,
                immutability_enabled=True,
                auto_expiration_enabled=False,  # Indefinite compliance retention under active legal hold
                secure_deletion_method="nist_800_88_sanitization",
            ),
            "app_environment_variables": RetentionPolicyConfig(
                asset_name="app_environment_variables",
                daily_retention_days=30,
                weekly_retention_weeks=12,
                monthly_retention_months=12,
                yearly_retention_years=3,
                archival_tier="git_historical_store",
                legal_hold_supported=True,
                immutability_enabled=True,
                auto_expiration_enabled=True,
                secure_deletion_method="git_purge",
            ),
            "enterprise_secrets_vault": RetentionPolicyConfig(
                asset_name="enterprise_secrets_vault",
                daily_retention_days=30,
                weekly_retention_weeks=12,
                monthly_retention_months=12,
                yearly_retention_years=7,
                archival_tier="encrypted_vault_archive",
                legal_hold_supported=True,
                immutability_enabled=True,
                auto_expiration_enabled=True,
                secure_deletion_method="crypto_shredding_and_key_destruction",
            ),
            "platform_system_configs": RetentionPolicyConfig(
                asset_name="platform_system_configs",
                daily_retention_days=30,
                weekly_retention_weeks=12,
                monthly_retention_months=12,
                yearly_retention_years=3,
                archival_tier="git_historical_store",
                legal_hold_supported=False,
                immutability_enabled=True,
                auto_expiration_enabled=True,
                secure_deletion_method="git_purge",
            ),
            "task_queue_persistence": RetentionPolicyConfig(
                asset_name="task_queue_persistence",
                daily_retention_days=7,
                weekly_retention_weeks=2,
                monthly_retention_months=0,
                yearly_retention_years=0,
                archival_tier="standard_ia",
                legal_hold_supported=False,
                immutability_enabled=False,
                auto_expiration_enabled=True,
                secure_deletion_method="automated_purge",
            ),
            "scheduled_cron_jobs": RetentionPolicyConfig(
                asset_name="scheduled_cron_jobs",
                daily_retention_days=30,
                weekly_retention_weeks=4,
                monthly_retention_months=3,
                yearly_retention_years=0,
                archival_tier="standard_ia",
                legal_hold_supported=False,
                immutability_enabled=False,
                auto_expiration_enabled=True,
                secure_deletion_method="automated_purge",
            ),
            "agent_registry_state": RetentionPolicyConfig(
                asset_name="agent_registry_state",
                daily_retention_days=60,
                weekly_retention_weeks=12,
                monthly_retention_months=6,
                yearly_retention_years=1,
                archival_tier="standard_ia",
                legal_hold_supported=True,
                immutability_enabled=True,
                auto_expiration_enabled=True,
                secure_deletion_method="automated_purge",
            ),
            "agent_memory_episodes": RetentionPolicyConfig(
                asset_name="agent_memory_episodes",
                daily_retention_days=90,
                weekly_retention_weeks=24,
                monthly_retention_months=12,
                yearly_retention_years=2,
                archival_tier="glacier_instant_retrieval",
                legal_hold_supported=True,
                immutability_enabled=True,
                auto_expiration_enabled=True,
                secure_deletion_method="crypto_shredding",
            ),
            "prompt_templates_repository": RetentionPolicyConfig(
                asset_name="prompt_templates_repository",
                daily_retention_days=30,
                weekly_retention_weeks=12,
                monthly_retention_months=12,
                yearly_retention_years=3,
                archival_tier="git_historical_store",
                legal_hold_supported=False,
                immutability_enabled=True,
                auto_expiration_enabled=True,
                secure_deletion_method="git_purge",
            ),
            "knowledge_base_documents": RetentionPolicyConfig(
                asset_name="knowledge_base_documents",
                daily_retention_days=90,
                weekly_retention_weeks=24,
                monthly_retention_months=12,
                yearly_retention_years=3,
                archival_tier="glacier_instant_retrieval",
                legal_hold_supported=True,
                immutability_enabled=True,
                auto_expiration_enabled=True,
                secure_deletion_method="crypto_shredding",
            ),
            "vector_embeddings_index": RetentionPolicyConfig(
                asset_name="vector_embeddings_index",
                daily_retention_days=30,
                weekly_retention_weeks=8,
                monthly_retention_months=3,
                yearly_retention_years=0,
                archival_tier="standard_ia",
                legal_hold_supported=False,
                immutability_enabled=False,
                auto_expiration_enabled=True,
                secure_deletion_method="automated_purge",
            ),
            "system_governance_policies": RetentionPolicyConfig(
                asset_name="system_governance_policies",
                daily_retention_days=30,
                weekly_retention_weeks=12,
                monthly_retention_months=12,
                yearly_retention_years=7,
                archival_tier="git_historical_store",
                legal_hold_supported=True,
                immutability_enabled=True,
                auto_expiration_enabled=True,
                secure_deletion_method="git_purge",
            ),
            "platform_verification_evidence": RetentionPolicyConfig(
                asset_name="platform_verification_evidence",
                daily_retention_days=365,
                weekly_retention_weeks=52,
                monthly_retention_months=60,
                yearly_retention_years=5,
                archival_tier="worm_compliance_vault",
                legal_hold_supported=True,
                immutability_enabled=True,
                auto_expiration_enabled=True,
                secure_deletion_method="nist_800_88_sanitization",
            ),
            "application_audit_logs": RetentionPolicyConfig(
                asset_name="application_audit_logs",
                daily_retention_days=365,
                weekly_retention_weeks=52,
                monthly_retention_months=36,
                yearly_retention_years=3,
                archival_tier="cold_s3_worm",
                legal_hold_supported=True,
                immutability_enabled=True,
                auto_expiration_enabled=True,
                secure_deletion_method="crypto_shredding",
            ),
            "prometheus_metrics_db": RetentionPolicyConfig(
                asset_name="prometheus_metrics_db",
                daily_retention_days=30,
                weekly_retention_weeks=4,
                monthly_retention_months=0,
                yearly_retention_years=0,
                archival_tier="standard_ia",
                legal_hold_supported=False,
                immutability_enabled=False,
                auto_expiration_enabled=True,
                secure_deletion_method="automated_purge",
            ),
            "grafana_dashboards": RetentionPolicyConfig(
                asset_name="grafana_dashboards",
                daily_retention_days=90,
                weekly_retention_weeks=12,
                monthly_retention_months=6,
                yearly_retention_years=1,
                archival_tier="git_historical_store",
                legal_hold_supported=False,
                immutability_enabled=True,
                auto_expiration_enabled=True,
                secure_deletion_method="git_purge",
            ),
        }

    def verify_retention_policies(
        self,
        assets: List[AssetInventoryItem],
        retentions: Dict[str, RetentionPolicyConfig],
    ) -> List[RetentionValidationResult]:
        results: List[RetentionValidationResult] = []

        for asset in assets:
            if not asset.backup_required:
                results.append(
                    RetentionValidationResult(
                        asset_name=asset.name,
                        retention_defined=True,
                        has_infinite_retention=False,
                        has_accidental_purge_risk=False,
                        legal_hold_compliant=True,
                        immutability_verified=True,
                        is_valid=True,
                        details=["Rebuildable asset; no retention policy required."],
                    )
                )
                continue

            policy = retentions.get(asset.name)
            if not policy:
                results.append(
                    RetentionValidationResult(
                        asset_name=asset.name,
                        retention_defined=False,
                        has_infinite_retention=False,
                        has_accidental_purge_risk=True,
                        legal_hold_compliant=False,
                        immutability_verified=False,
                        is_valid=False,
                        details=["CRITICAL: Retention policy missing for protected asset."],
                    )
                )
                continue

            details: List[str] = []
            has_infinite = False
            has_purge_risk = False
            legal_hold_ok = True
            immutability_ok = True

            # Check for missing or inadequate retention periods
            if policy.daily_retention_days <= 0:
                details.append("Daily retention days must be greater than 0.")
                has_purge_risk = True

            if asset.criticality == CriticalityTier.TIER_0:
                if policy.daily_retention_days < 14:
                    details.append("Tier 0 asset has daily retention < 14 days, risking premature purge.")
                    has_purge_risk = True
                if not policy.legal_hold_supported:
                    details.append("Tier 0 asset does not support legal holds.")
                    legal_hold_ok = False
                if not policy.immutability_enabled:
                    details.append("Tier 0 asset lacks Object Lock / WORM immutability.")
                    immutability_ok = False

            # Detect infinite retention without legal hold justification
            if not policy.auto_expiration_enabled and not policy.legal_hold_supported:
                details.append("WARNING: Auto-expiration is disabled without legal hold justification (infinite retention).")
                has_infinite = True

            is_valid = (
                not has_purge_risk
                and not has_infinite
                and legal_hold_ok
                and immutability_ok
            )

            if is_valid:
                details.append(
                    f"Retention verified: {policy.daily_retention_days}d daily, "
                    f"{policy.weekly_retention_weeks}w weekly, {policy.monthly_retention_months}m monthly, "
                    f"{policy.yearly_retention_years}y yearly (Tier: {policy.archival_tier})."
                )

            results.append(
                RetentionValidationResult(
                    asset_name=asset.name,
                    retention_defined=True,
                    has_infinite_retention=has_infinite,
                    has_accidental_purge_risk=has_purge_risk,
                    legal_hold_compliant=legal_hold_ok,
                    immutability_verified=immutability_ok,
                    is_valid=is_valid,
                    details=details,
                )
            )

        return results

    def export_retention_report_json(
        self, results: List[RetentionValidationResult]
    ) -> Dict[str, Any]:
        """Formats the retention verification results to JSON dictionary."""
        passed_count = len([r for r in results if r.is_valid])
        return {
            "total_retention_policies_checked": len(results),
            "valid_policies_count": passed_count,
            "invalid_policies_count": len(results) - passed_count,
            "retention_compliance_percent": round((passed_count / len(results) * 100.0), 2) if results else 100.0,
            "retention_verifications": [
                {
                    "asset_name": r.asset_name,
                    "retention_defined": r.retention_defined,
                    "has_infinite_retention": r.has_infinite_retention,
                    "has_accidental_purge_risk": r.has_accidental_purge_risk,
                    "legal_hold_compliant": r.legal_hold_compliant,
                    "immutability_verified": r.immutability_verified,
                    "is_valid": r.is_valid,
                    "details": r.details,
                }
                for r in results
            ],
        }
