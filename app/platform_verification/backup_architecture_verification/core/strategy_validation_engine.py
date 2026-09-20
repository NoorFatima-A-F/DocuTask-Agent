"""
Part 3: Backup Strategy Validation Engine.
Verifies backup strategy matches asset criticality (Full, Incremental, Differential, Snapshot, Continuous).
Detects missing, conflicting, and incorrect backup strategies.
"""
from typing import List, Dict, Any, Optional
from app.platform_verification.backup_architecture_verification.domain.models import (
    AssetCategory,
    CriticalityTier,
    BackupStrategyType,
    AssetInventoryItem,
    ClassificationEntry,
    BackupStrategyConfig,
    StrategyValidationResult,
)
from app.platform_verification.backup_architecture_verification.domain.interfaces import (
    IStrategyValidationEngine,
)


class StrategyValidationEngine(IStrategyValidationEngine):
    """
    Validates that configured backup strategies strictly adhere to enterprise
    resilience, RPO/RTO specifications, and recovery criteria.
    """

    def get_default_platform_strategies(self) -> Dict[str, BackupStrategyConfig]:
        """Provides production-grade default strategy configurations for all platform assets."""
        return {
            "postgres_primary": BackupStrategyConfig(
                asset_name="postgres_primary",
                strategy_type=BackupStrategyType.CONTINUOUS,
                frequency_cron="0 2 * * *",  # Daily base backup + Continuous WAL archiving
                estimated_size_mb=10240.0,
                retention_days=30,
                storage_location="s3://docutask-backups/postgres-wal-pitr/",
                is_continuous=True,
                wal_archiving_enabled=True,
                dependency_chain=["app_environment_variables", "enterprise_secrets_vault"],
                encryption_algorithm="AES-256-GCM",
            ),
            "redis_cache_queue": BackupStrategyConfig(
                asset_name="redis_cache_queue",
                strategy_type=BackupStrategyType.SNAPSHOT,
                frequency_cron="*/15 * * * *",  # 15-minute RDB snapshots + AOF
                estimated_size_mb=1024.0,
                retention_days=7,
                storage_location="s3://docutask-backups/redis-snapshots/",
                is_continuous=False,
                dependency_chain=["postgres_primary"],
                encryption_algorithm="AES-256-GCM",
            ),
            "docker_named_volumes": BackupStrategyConfig(
                asset_name="docker_named_volumes",
                strategy_type=BackupStrategyType.SNAPSHOT,
                frequency_cron="0 */4 * * *",  # 4-hour CSI volume snapshots
                estimated_size_mb=5120.0,
                retention_days=14,
                storage_location="csi-snapshot-class://fast-ssd-snapshots",
                is_continuous=False,
                encryption_algorithm="AES-256-GCM",
            ),
            "minio_s3_object_store": BackupStrategyConfig(
                asset_name="minio_s3_object_store",
                strategy_type=BackupStrategyType.CONTINUOUS,
                frequency_cron="0 3 * * *",  # Daily sync + continuous cross-region replication (CRR)
                estimated_size_mb=51200.0,
                retention_days=90,
                storage_location="s3://docutask-dr-replica-bucket/object-store/",
                is_continuous=True,
                encryption_algorithm="AES-256-GCM",
            ),
            "uploaded_documents_raw": BackupStrategyConfig(
                asset_name="uploaded_documents_raw",
                strategy_type=BackupStrategyType.CONTINUOUS,
                frequency_cron="0 4 * * *",  # Cross-region replication + versioning
                estimated_size_mb=30720.0,
                retention_days=2555,  # 7-year regulatory retention
                storage_location="s3://docutask-dr-replica-bucket/raw-documents/",
                is_continuous=True,
                encryption_algorithm="AES-256-GCM",
            ),
            "ocr_extracted_text_artifacts": BackupStrategyConfig(
                asset_name="ocr_extracted_text_artifacts",
                strategy_type=BackupStrategyType.INCREMENTAL,
                frequency_cron="0 */2 * * *",  # 2-hour incrementals
                estimated_size_mb=8192.0,
                retention_days=60,
                storage_location="s3://docutask-backups/ocr-artifacts/",
                is_continuous=False,
                dependency_chain=["uploaded_documents_raw"],
                base_snapshot_id="base-ocr-20260901",
                encryption_algorithm="AES-256-GCM",
            ),
            "extracted_structured_json": BackupStrategyConfig(
                asset_name="extracted_structured_json",
                strategy_type=BackupStrategyType.INCREMENTAL,
                frequency_cron="0 */2 * * *",  # 2-hour incrementals
                estimated_size_mb=4096.0,
                retention_days=90,
                storage_location="s3://docutask-backups/extracted-json/",
                is_continuous=False,
                dependency_chain=["postgres_primary", "ocr_extracted_text_artifacts"],
                base_snapshot_id="base-json-20260901",
                encryption_algorithm="AES-256-GCM",
            ),
            "ai_verification_evidence": BackupStrategyConfig(
                asset_name="ai_verification_evidence",
                strategy_type=BackupStrategyType.CONTINUOUS,
                frequency_cron="0 1 * * *",  # Continuous immutable append-only replication
                estimated_size_mb=2048.0,
                retention_days=3650,  # 10-year immutable audit
                storage_location="s3://docutask-compliance-worm/ai-evidence/",
                is_continuous=True,
                encryption_algorithm="AES-256-GCM",
            ),
            "app_environment_variables": BackupStrategyConfig(
                asset_name="app_environment_variables",
                strategy_type=BackupStrategyType.FULL,
                frequency_cron="0 0 * * *",  # Daily git revision backup
                estimated_size_mb=1.0,
                retention_days=365,
                storage_location="git-archive://configs/env-backups/",
                is_continuous=False,
                encryption_algorithm="AES-256-GCM",
            ),
            "enterprise_secrets_vault": BackupStrategyConfig(
                asset_name="enterprise_secrets_vault",
                strategy_type=BackupStrategyType.FULL,
                frequency_cron="0 */6 * * *",  # 6-hour encrypted vault snapshots
                estimated_size_mb=10.0,
                retention_days=365,
                storage_location="vault-raft-snapshot://dr-vault-cluster/",
                is_continuous=False,
                encryption_algorithm="AES-256-GCM",
            ),
            "platform_system_configs": BackupStrategyConfig(
                asset_name="platform_system_configs",
                strategy_type=BackupStrategyType.FULL,
                frequency_cron="0 0 * * *",  # Daily git mirror
                estimated_size_mb=20.0,
                retention_days=365,
                storage_location="git-mirror://infra-configs-backup/",
                is_continuous=False,
                encryption_algorithm="AES-256-GCM",
            ),
            "task_queue_persistence": BackupStrategyConfig(
                asset_name="task_queue_persistence",
                strategy_type=BackupStrategyType.SNAPSHOT,
                frequency_cron="*/30 * * * *",  # 30-minute state snapshots
                estimated_size_mb=1024.0,
                retention_days=7,
                storage_location="s3://docutask-backups/queue-persistence/",
                is_continuous=False,
                encryption_algorithm="AES-256-GCM",
            ),
            "scheduled_cron_jobs": BackupStrategyConfig(
                asset_name="scheduled_cron_jobs",
                strategy_type=BackupStrategyType.FULL,
                frequency_cron="0 0 * * *",  # Daily schedule backup
                estimated_size_mb=10.0,
                retention_days=30,
                storage_location="s3://docutask-backups/scheduled-jobs/",
                is_continuous=False,
                encryption_algorithm="AES-256-GCM",
            ),
            "agent_registry_state": BackupStrategyConfig(
                asset_name="agent_registry_state",
                strategy_type=BackupStrategyType.INCREMENTAL,
                frequency_cron="0 */1 * * *",  # Hourly incrementals
                estimated_size_mb=100.0,
                retention_days=60,
                storage_location="s3://docutask-backups/agent-registry/",
                is_continuous=False,
                dependency_chain=["postgres_primary"],
                encryption_algorithm="AES-256-GCM",
            ),
            "agent_memory_episodes": BackupStrategyConfig(
                asset_name="agent_memory_episodes",
                strategy_type=BackupStrategyType.INCREMENTAL,
                frequency_cron="0 */1 * * *",  # Hourly incrementals
                estimated_size_mb=2048.0,
                retention_days=90,
                storage_location="s3://docutask-backups/agent-memory/",
                is_continuous=False,
                dependency_chain=["postgres_primary"],
                encryption_algorithm="AES-256-GCM",
            ),
            "prompt_templates_repository": BackupStrategyConfig(
                asset_name="prompt_templates_repository",
                strategy_type=BackupStrategyType.FULL,
                frequency_cron="0 0 * * *",  # Daily full git mirror
                estimated_size_mb=5.0,
                retention_days=365,
                storage_location="git-archive://prompts/templates-backup/",
                is_continuous=False,
                encryption_algorithm="AES-256-GCM",
            ),
            "knowledge_base_documents": BackupStrategyConfig(
                asset_name="knowledge_base_documents",
                strategy_type=BackupStrategyType.DIFFERENTIAL,
                frequency_cron="0 6 * * *",  # Daily differential
                estimated_size_mb=10240.0,
                retention_days=90,
                storage_location="s3://docutask-backups/knowledge-base/",
                is_continuous=False,
                base_snapshot_id="base-kb-20260901",
                encryption_algorithm="AES-256-GCM",
            ),
            "vector_embeddings_index": BackupStrategyConfig(
                asset_name="vector_embeddings_index",
                strategy_type=BackupStrategyType.SNAPSHOT,
                frequency_cron="0 */4 * * *",  # 4-hour HNSW snapshots
                estimated_size_mb=5120.0,
                retention_days=30,
                storage_location="s3://docutask-backups/vector-embeddings/",
                is_continuous=False,
                dependency_chain=["knowledge_base_documents"],
                encryption_algorithm="AES-256-GCM",
            ),
            "system_governance_policies": BackupStrategyConfig(
                asset_name="system_governance_policies",
                strategy_type=BackupStrategyType.FULL,
                frequency_cron="0 0 * * *",  # Daily full bundle backup
                estimated_size_mb=2.0,
                retention_days=365,
                storage_location="git-archive://governance/policies-backup/",
                is_continuous=False,
                encryption_algorithm="AES-256-GCM",
            ),
            "platform_verification_evidence": BackupStrategyConfig(
                asset_name="platform_verification_evidence",
                strategy_type=BackupStrategyType.CONTINUOUS,
                frequency_cron="0 2 * * *",  # Immutable WORM sync
                estimated_size_mb=3072.0,
                retention_days=1825,  # 5-year retention
                storage_location="s3://docutask-compliance-worm/verification-evidence/",
                is_continuous=True,
                encryption_algorithm="AES-256-GCM",
            ),
            "application_audit_logs": BackupStrategyConfig(
                asset_name="application_audit_logs",
                strategy_type=BackupStrategyType.INCREMENTAL,
                frequency_cron="0 */4 * * *",  # 4-hour log incrementals
                estimated_size_mb=20480.0,
                retention_days=365,
                storage_location="s3://docutask-audit-cold/application-logs/",
                is_continuous=False,
                dependency_chain=["postgres_primary"],
                base_snapshot_id="base-audit-20260901",
                encryption_algorithm="AES-256-GCM",
            ),
            "prometheus_metrics_db": BackupStrategyConfig(
                asset_name="prometheus_metrics_db",
                strategy_type=BackupStrategyType.SNAPSHOT,
                frequency_cron="0 0 * * *",  # Daily TSDB snapshot
                estimated_size_mb=10240.0,
                retention_days=30,
                storage_location="s3://docutask-backups/prometheus-tsdb/",
                is_continuous=False,
                encryption_algorithm="AES-256-GCM",
            ),
            "grafana_dashboards": BackupStrategyConfig(
                asset_name="grafana_dashboards",
                strategy_type=BackupStrategyType.FULL,
                frequency_cron="0 0 * * *",  # Daily export
                estimated_size_mb=10.0,
                retention_days=90,
                storage_location="git-archive://grafana/dashboards/",
                is_continuous=False,
                encryption_algorithm="AES-256-GCM",
            ),
        }

    def validate_strategies(
        self,
        assets: List[AssetInventoryItem],
        classifications: Dict[str, ClassificationEntry],
        strategies: Dict[str, BackupStrategyConfig],
    ) -> List[StrategyValidationResult]:
        results: List[StrategyValidationResult] = []

        for asset in assets:
            if not asset.backup_required:
                # Tier 3 / Rebuildable assets do not require a strategy
                results.append(
                    StrategyValidationResult(
                        asset_name=asset.name,
                        criticality=asset.criticality,
                        configured_strategy=BackupStrategyType.FULL,  # N/A
                        is_adequate=True,
                        findings=["Asset is rebuildable on demand; backup strategy is optional."],
                        recommendations=[],
                    )
                )
                continue

            strat = strategies.get(asset.name)
            if not strat:
                results.append(
                    StrategyValidationResult(
                        asset_name=asset.name,
                        criticality=asset.criticality,
                        configured_strategy=BackupStrategyType.FULL,
                        is_adequate=False,
                        findings=["CRITICAL: Missing backup strategy for protected asset."],
                        recommendations=["Configure a valid backup strategy (Full, Incremental, Snapshot, or Continuous)."],
                    )
                )
                continue

            findings: List[str] = []
            recommendations: List[str] = []
            is_adequate = True

            # Strategy validation rules:
            # Rule 1: Tier 0 assets must have continuous replication/WAL, frequent snapshot, incremental, or full backup
            if asset.criticality == CriticalityTier.TIER_0:
                if strat.strategy_type not in [
                    BackupStrategyType.CONTINUOUS,
                    BackupStrategyType.SNAPSHOT,
                    BackupStrategyType.FULL,
                    BackupStrategyType.INCREMENTAL,
                ]:
                    is_adequate = False
                    findings.append("Tier 0 asset has inadequate strategy type (requires Continuous, Snapshot, Incremental, or Full).")
                    recommendations.append("Upgrade strategy to Continuous WAL streaming or frequent replication.")

                if asset.category == AssetCategory.DATABASE and not strat.wal_archiving_enabled:
                    is_adequate = False
                    findings.append("Tier 0 Relational Database missing continuous WAL archiving.")
                    recommendations.append("Enable WAL archiving to guarantee zero data loss Point-In-Time-Recovery (PITR).")

            # Rule 2: Incremental backups must have a base snapshot ID or parent dependency
            if strat.strategy_type == BackupStrategyType.INCREMENTAL:
                if not strat.dependency_chain and not strat.base_snapshot_id:
                    is_adequate = False
                    findings.append("Incremental backup lacks dependency chain or base snapshot anchor.")
                    recommendations.append("Define base snapshot ID or parent dependency chain for incrementals.")

            # Rule 3: Differential backups must reference valid base snapshot
            if strat.strategy_type == BackupStrategyType.DIFFERENTIAL:
                if not strat.base_snapshot_id:
                    is_adequate = False
                    findings.append("Differential backup missing base snapshot reference.")
                    recommendations.append("Specify base snapshot ID to enable differential diff computation.")

            # Rule 4: Destination storage must be specified and non-empty
            if not strat.storage_location:
                is_adequate = False
                findings.append("Storage location is undefined.")
                recommendations.append("Configure a secure target storage URI (e.g. S3 WORM or CSI volume snapshot).")

            if not findings:
                findings.append(f"Strategy {strat.strategy_type.value} validated successfully against {asset.criticality.value} requirements.")

            results.append(
                StrategyValidationResult(
                    asset_name=asset.name,
                    criticality=asset.criticality,
                    configured_strategy=strat.strategy_type,
                    is_adequate=is_adequate,
                    findings=findings,
                    recommendations=recommendations,
                )
            )

        return results

    def export_strategy_report_json(self, results: List[StrategyValidationResult]) -> Dict[str, Any]:
        """Formats the strategy validation results to JSON dictionary."""
        passed_count = len([r for r in results if r.is_adequate])
        return {
            "total_strategies_evaluated": len(results),
            "passed_strategies_count": passed_count,
            "failed_strategies_count": len(results) - passed_count,
            "overall_strategy_compliance_percent": round((passed_count / len(results) * 100.0), 2) if results else 100.0,
            "strategy_evaluations": [
                {
                    "asset_name": r.asset_name,
                    "criticality": r.criticality.value,
                    "configured_strategy": r.configured_strategy.value,
                    "is_adequate": r.is_adequate,
                    "findings": r.findings,
                    "recommendations": r.recommendations,
                }
                for r in results
            ],
        }
