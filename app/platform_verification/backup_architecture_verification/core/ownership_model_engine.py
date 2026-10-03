"""
Part 8: Backup Ownership Model Engine.
Enforces that every recoverable asset has defined engineering ownership,
automation systems, restore owners, and verification owners.
"""
from typing import List, Dict, Any
from app.platform_verification.backup_architecture_verification.domain.models import (
    AssetInventoryItem,
    BackupOwnershipRecord,
)
from app.platform_verification.backup_architecture_verification.domain.interfaces import (
    IOwnershipModelEngine,
)


class OwnershipModelEngine(IOwnershipModelEngine):
    """
    Validates ownership mappings and fails verification if any protected asset
    lacks clear team ownership or restore responsibility.
    """

    def __init__(self):
        self._default_ownership_table: Dict[str, Dict[str, str]] = {
            "postgres_primary": {
                "owner_team": "database_reliability_engineering",
                "subsystem": "core_database",
                "automation_system": "patroni_and_pgbackrest",
                "schedule_expression": "0 2 * * *",
                "restore_owner_team": "sre_platform_team",
                "verification_owner_team": "data_governance_team",
                "escalation_contact": "dbre-oncall@docutask.internal",
            },
            "redis_cache_queue": {
                "owner_team": "message_broker_team",
                "subsystem": "broker_queue",
                "automation_system": "redis_sentinel_backup_operator",
                "schedule_expression": "*/15 * * * *",
                "restore_owner_team": "sre_platform_team",
                "verification_owner_team": "sre_platform_team",
                "escalation_contact": "broker-oncall@docutask.internal",
            },
            "docker_named_volumes": {
                "owner_team": "kubernetes_platform_team",
                "subsystem": "storage_orchestration",
                "automation_system": "velero_csi_snapshotter",
                "schedule_expression": "0 */4 * * *",
                "restore_owner_team": "kubernetes_platform_team",
                "verification_owner_team": "qa_automation_team",
                "escalation_contact": "k8s-oncall@docutask.internal",
            },
            "minio_s3_object_store": {
                "owner_team": "storage_infrastructure_team",
                "subsystem": "blob_storage",
                "automation_system": "minio_mirror_daemon",
                "schedule_expression": "0 3 * * *",
                "restore_owner_team": "sre_platform_team",
                "verification_owner_team": "compliance_audit_team",
                "escalation_contact": "storage-oncall@docutask.internal",
            },
            "uploaded_documents_raw": {
                "owner_team": "document_platform_team",
                "subsystem": "ingestion_storage",
                "automation_system": "aws_s3_cross_region_replication",
                "schedule_expression": "0 4 * * *",
                "restore_owner_team": "sre_platform_team",
                "verification_owner_team": "compliance_audit_team",
                "escalation_contact": "doc-platform@docutask.internal",
            },
            "ocr_extracted_text_artifacts": {
                "owner_team": "ocr_engineering_team",
                "subsystem": "ocr_pipeline",
                "automation_system": "argo_workflows_backup_cron",
                "schedule_expression": "0 */2 * * *",
                "restore_owner_team": "ocr_engineering_team",
                "verification_owner_team": "qa_automation_team",
                "escalation_contact": "ocr-team@docutask.internal",
            },
            "extracted_structured_json": {
                "owner_team": "ai_extraction_team",
                "subsystem": "structured_data",
                "automation_system": "argo_workflows_backup_cron",
                "schedule_expression": "0 */2 * * *",
                "restore_owner_team": "ai_extraction_team",
                "verification_owner_team": "data_governance_team",
                "escalation_contact": "extraction-team@docutask.internal",
            },
            "ai_verification_evidence": {
                "owner_team": "compliance_and_governance_team",
                "subsystem": "evidence_vault",
                "automation_system": "worm_immutable_sync_operator",
                "schedule_expression": "0 1 * * *",
                "restore_owner_team": "security_operations_team",
                "verification_owner_team": "compliance_audit_team",
                "escalation_contact": "compliance-audit@docutask.internal",
            },
            "app_environment_variables": {
                "owner_team": "devops_platform_team",
                "subsystem": "gitops_config",
                "automation_system": "argocd_gitops_engine",
                "schedule_expression": "0 0 * * *",
                "restore_owner_team": "devops_platform_team",
                "verification_owner_team": "security_operations_team",
                "escalation_contact": "devops-oncall@docutask.internal",
            },
            "enterprise_secrets_vault": {
                "owner_team": "enterprise_security_team",
                "subsystem": "secrets_management",
                "automation_system": "vault_raft_auto_snapshot",
                "schedule_expression": "0 */6 * * *",
                "restore_owner_team": "enterprise_security_team",
                "verification_owner_team": "security_audit_team",
                "escalation_contact": "security-oncall@docutask.internal",
            },
            "platform_system_configs": {
                "owner_team": "devops_platform_team",
                "subsystem": "infrastructure_code",
                "automation_system": "terraform_cloud_mirror",
                "schedule_expression": "0 0 * * *",
                "restore_owner_team": "devops_platform_team",
                "verification_owner_team": "qa_automation_team",
                "escalation_contact": "devops-oncall@docutask.internal",
            },
            "task_queue_persistence": {
                "owner_team": "async_workers_team",
                "subsystem": "worker_runtime",
                "automation_system": "celery_state_backup_daemon",
                "schedule_expression": "*/30 * * * *",
                "restore_owner_team": "async_workers_team",
                "verification_owner_team": "sre_platform_team",
                "escalation_contact": "workers-team@docutask.internal",
            },
            "scheduled_cron_jobs": {
                "owner_team": "backend_platform_team",
                "subsystem": "scheduler",
                "automation_system": "k8s_cron_backup_operator",
                "schedule_expression": "0 0 * * *",
                "restore_owner_team": "backend_platform_team",
                "verification_owner_team": "qa_automation_team",
                "escalation_contact": "backend-team@docutask.internal",
            },
            "agent_registry_state": {
                "owner_team": "agent_intelligence_team",
                "subsystem": "agent_runtime",
                "automation_system": "agent_state_checkpoint_operator",
                "schedule_expression": "0 */1 * * *",
                "restore_owner_team": "agent_intelligence_team",
                "verification_owner_team": "qa_automation_team",
                "escalation_contact": "agent-core@docutask.internal",
            },
            "agent_memory_episodes": {
                "owner_team": "agent_intelligence_team",
                "subsystem": "agent_memory",
                "automation_system": "vector_pg_snapshot_operator",
                "schedule_expression": "0 */1 * * *",
                "restore_owner_team": "agent_intelligence_team",
                "verification_owner_team": "data_governance_team",
                "escalation_contact": "agent-core@docutask.internal",
            },
            "prompt_templates_repository": {
                "owner_team": "prompt_engineering_team",
                "subsystem": "prompt_registry",
                "automation_system": "git_sync_daemon",
                "schedule_expression": "0 0 * * *",
                "restore_owner_team": "prompt_engineering_team",
                "verification_owner_team": "qa_automation_team",
                "escalation_contact": "prompts@docutask.internal",
            },
            "knowledge_base_documents": {
                "owner_team": "rag_knowledge_team",
                "subsystem": "knowledge_store",
                "automation_system": "rag_backup_operator",
                "schedule_expression": "0 6 * * *",
                "restore_owner_team": "rag_knowledge_team",
                "verification_owner_team": "data_governance_team",
                "escalation_contact": "rag-team@docutask.internal",
            },
            "vector_embeddings_index": {
                "owner_team": "rag_knowledge_team",
                "subsystem": "vector_index",
                "automation_system": "qdrant_snapshot_daemon",
                "schedule_expression": "0 */4 * * *",
                "restore_owner_team": "rag_knowledge_team",
                "verification_owner_team": "qa_automation_team",
                "escalation_contact": "rag-team@docutask.internal",
            },
            "system_governance_policies": {
                "owner_team": "enterprise_security_team",
                "subsystem": "policy_enforcement",
                "automation_system": "opa_bundle_backup_cron",
                "schedule_expression": "0 0 * * *",
                "restore_owner_team": "enterprise_security_team",
                "verification_owner_team": "security_audit_team",
                "escalation_contact": "security-oncall@docutask.internal",
            },
            "platform_verification_evidence": {
                "owner_team": "compliance_and_governance_team",
                "subsystem": "verification_audit",
                "automation_system": "evidence_worm_backup_job",
                "schedule_expression": "0 2 * * *",
                "restore_owner_team": "sre_platform_team",
                "verification_owner_team": "compliance_audit_team",
                "escalation_contact": "compliance-audit@docutask.internal",
            },
            "application_audit_logs": {
                "owner_team": "security_operations_team",
                "subsystem": "audit_logs",
                "automation_system": "fluentd_cold_s3_shipper",
                "schedule_expression": "0 */4 * * *",
                "restore_owner_team": "security_operations_team",
                "verification_owner_team": "security_audit_team",
                "escalation_contact": "secops@docutask.internal",
            },
            "prometheus_metrics_db": {
                "owner_team": "sre_platform_team",
                "subsystem": "observability_metrics",
                "automation_system": "thanos_sidecar_s3_shipper",
                "schedule_expression": "0 0 * * *",
                "restore_owner_team": "sre_platform_team",
                "verification_owner_team": "sre_platform_team",
                "escalation_contact": "sre-oncall@docutask.internal",
            },
            "grafana_dashboards": {
                "owner_team": "sre_platform_team",
                "subsystem": "observability_dashboards",
                "automation_system": "grafana_gitops_sync",
                "schedule_expression": "0 0 * * *",
                "restore_owner_team": "sre_platform_team",
                "verification_owner_team": "qa_automation_team",
                "escalation_contact": "sre-oncall@docutask.internal",
            },
            "temporary_processing_cache": {
                "owner_team": "worker_runtime_team",
                "subsystem": "scratch_disk",
                "automation_system": "k8s_empty_dir_lifecycle",
                "schedule_expression": "NONE",
                "restore_owner_team": "worker_runtime_team",
                "verification_owner_team": "worker_runtime_team",
                "escalation_contact": "worker-runtime@docutask.internal",
            },
            "user_session_cache": {
                "owner_team": "auth_platform_team",
                "subsystem": "session_cache",
                "automation_system": "redis_ttl_rebuilder",
                "schedule_expression": "NONE",
                "restore_owner_team": "auth_platform_team",
                "verification_owner_team": "auth_platform_team",
                "escalation_contact": "auth-team@docutask.internal",
            },
            "generated_pdf_thumbnails": {
                "owner_team": "document_platform_team",
                "subsystem": "thumbnail_cache",
                "automation_system": "on_demand_thumbnail_worker",
                "schedule_expression": "NONE",
                "restore_owner_team": "document_platform_team",
                "verification_owner_team": "qa_automation_team",
                "escalation_contact": "doc-platform@docutask.internal",
            },
        }

    def verify_ownership(self, assets: List[AssetInventoryItem]) -> List[BackupOwnershipRecord]:
        records: List[BackupOwnershipRecord] = []

        for asset in assets:
            info = self._default_ownership_table.get(asset.name)
            if not info:
                # Missing ownership -> failure
                records.append(
                    BackupOwnershipRecord(
                        asset_name=asset.name,
                        owner_team="UNASSIGNED",
                        subsystem="UNKNOWN",
                        automation_system="NONE",
                        schedule_expression="NONE",
                        restore_owner_team="UNASSIGNED",
                        verification_owner_team="UNASSIGNED",
                        escalation_contact="UNASSIGNED",
                        has_assigned_owners=False,
                    )
                )
                continue

            has_valid_owners = bool(
                info.get("owner_team") and info.get("owner_team") != "UNASSIGNED"
                and info.get("restore_owner_team") and info.get("restore_owner_team") != "UNASSIGNED"
                and info.get("verification_owner_team") and info.get("verification_owner_team") != "UNASSIGNED"
            )

            record = BackupOwnershipRecord(
                asset_name=asset.name,
                owner_team=info["owner_team"],
                subsystem=info["subsystem"],
                automation_system=info["automation_system"],
                schedule_expression=info["schedule_expression"],
                restore_owner_team=info["restore_owner_team"],
                verification_owner_team=info["verification_owner_team"],
                escalation_contact=info["escalation_contact"],
                has_assigned_owners=has_valid_owners,
            )
            records.append(record)

        return records

    def export_ownership_report_json(
        self, records: List[BackupOwnershipRecord]
    ) -> Dict[str, Any]:
        """Formats the ownership report to JSON dictionary."""
        valid_count = len([r for r in records if r.has_assigned_owners])
        return {
            "total_assets_evaluated": len(records),
            "fully_owned_assets_count": valid_count,
            "unassigned_ownership_count": len(records) - valid_count,
            "ownership_compliance_percent": round((valid_count / len(records) * 100.0), 2) if records else 100.0,
            "ownership_records": [
                {
                    "asset_name": r.asset_name,
                    "owner_team": r.owner_team,
                    "subsystem": r.subsystem,
                    "automation_system": r.automation_system,
                    "schedule_expression": r.schedule_expression,
                    "restore_owner_team": r.restore_owner_team,
                    "verification_owner_team": r.verification_owner_team,
                    "escalation_contact": r.escalation_contact,
                    "has_assigned_owners": r.has_assigned_owners,
                }
                for r in records
            ],
        }
