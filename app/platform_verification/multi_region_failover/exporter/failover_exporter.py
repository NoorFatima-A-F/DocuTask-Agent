"""
Multi-Region Failover Evidence Exporter (Part 3G.6M).
Exports all 9 verification manifests and certificates into multi_region_verification/
"""
import json
import os
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime, timezone

from app.platform_verification.multi_region_failover.domain.models import (
    MultiRegionArchitectureReport,
    CloudPortabilityReport,
    DatabaseReplicationReport,
    StorageReplicationReport,
    TrafficFailoverReport,
    WorkflowCheckpointReport,
    ChaosOutageReport,
    AvailabilityMetricsReport,
    MultiRegionScorecard,
)


class FailoverExporter:
    """
    Exports comprehensive multi-region failover evidence artifacts.
    """

    def __init__(self, base_dir: str = ".", output_dir_name: str = "multi_region_verification"):
        self.base_dir = Path(base_dir)
        self.output_dir = self.base_dir / output_dir_name

    def export_all_manifests(
        self,
        arch: MultiRegionArchitectureReport,
        portability: CloudPortabilityReport,
        db_rep: DatabaseReplicationReport,
        storage_rep: StorageReplicationReport,
        traffic: TrafficFailoverReport,
        workflow: WorkflowCheckpointReport,
        chaos: ChaosOutageReport,
        avail: AvailabilityMetricsReport,
        scorecard: MultiRegionScorecard,
        failover_execution: Dict[str, Any],
    ) -> Dict[str, Any]:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        files_written = []
        now_str = datetime.now(timezone.utc).isoformat()

        # 1. architecture_report.json
        arch_file = self.output_dir / "architecture_report.json"
        arch_data = {
            "primary_region": arch.primary_region.value,
            "secondary_region": arch.secondary_region.value,
            "total_critical_services": arch.total_critical_services,
            "replicated_services_count": arch.replicated_services_count,
            "passed": arch.passed,
            "services": [
                {
                    "name": s.service_name,
                    "primary_status": s.primary_status,
                    "secondary_status": s.secondary_status,
                    "mode": s.replication_mode,
                }
                for s in arch.services
            ],
            "portability": {
                "compute_portable": portability.compute_portability_verified,
                "storage_abstracted": portability.storage_abstraction_verified,
                "ai_abstracted": portability.ai_provider_abstraction_verified,
                "supported_clouds": portability.supported_clouds,
            },
        }
        arch_file.write_text(json.dumps(arch_data, indent=2), encoding="utf-8")
        files_written.append(str(arch_file))

        # 2. replication_report.json
        rep_file = self.output_dir / "replication_report.json"
        rep_data = {
            "database_replication": {
                "health": db_rep.replication_health.value,
                "lag_seconds": db_rep.replication_lag_seconds,
                "primary_lsn": db_rep.current_primary_lsn,
                "replica_lsn": db_rep.replica_replay_lsn,
            },
            "storage_replication": {
                "total_documents": storage_rep.total_documents_tested,
                "sha256_match_pct": storage_rep.sha256_checksum_match_pct,
                "sync_lag_sec": storage_rep.cross_region_sync_lag_sec,
            },
            "passed": db_rep.passed and storage_rep.passed,
        }
        rep_file.write_text(json.dumps(rep_data, indent=2), encoding="utf-8")
        files_written.append(str(rep_file))

        # 3. failover_report.json
        failover_file = self.output_dir / "failover_report.json"
        failover_file.write_text(json.dumps(failover_execution, indent=2), encoding="utf-8")
        files_written.append(str(failover_file))

        # 4. traffic_report.json
        traffic_file = self.output_dir / "traffic_report.json"
        traffic_data = {
            "global_traffic_manager": traffic.global_traffic_manager,
            "detection_time_sec": traffic.detection_time_sec,
            "dns_propagation_time_sec": traffic.dns_propagation_time_sec,
            "traffic_migration_time_sec": traffic.traffic_migration_time_sec,
            "total_failover_time_sec": traffic.total_failover_time_sec,
            "dropped_requests_pct": traffic.dropped_requests_pct,
            "passed": traffic.passed,
        }
        traffic_file.write_text(json.dumps(traffic_data, indent=2), encoding="utf-8")
        files_written.append(str(traffic_file))

        # 5. database_report.json
        db_file = self.output_dir / "database_report.json"
        db_data = {
            "replication_health": db_rep.replication_health.value,
            "current_primary_lsn": db_rep.current_primary_lsn,
            "replica_replay_lsn": db_rep.replica_replay_lsn,
            "replication_lag_seconds": db_rep.replication_lag_seconds,
            "standby_promotion_latency_sec": db_rep.standby_promotion_latency_sec,
            "data_loss_bytes": db_rep.data_loss_bytes,
            "passed": db_rep.passed,
            "details": db_rep.details,
        }
        db_file.write_text(json.dumps(db_data, indent=2), encoding="utf-8")
        files_written.append(str(db_file))

        # 6. storage_report.json
        storage_file = self.output_dir / "storage_report.json"
        storage_data = {
            "total_documents_tested": storage_rep.total_documents_tested,
            "replicated_documents_count": storage_rep.replicated_documents_count,
            "sha256_checksum_match_pct": storage_rep.sha256_checksum_match_pct,
            "cross_region_sync_lag_sec": storage_rep.cross_region_sync_lag_sec,
            "zero_data_loss_verified": storage_rep.zero_data_loss_verified,
            "passed": storage_rep.passed,
            "details": storage_rep.details,
        }
        storage_file.write_text(json.dumps(storage_data, indent=2), encoding="utf-8")
        files_written.append(str(storage_file))

        # 7. chaos_results.json
        chaos_file = self.output_dir / "chaos_results.json"
        chaos_data = {
            "simulations_executed": chaos.simulations_executed,
            "region_shutdown_passed": chaos.region_shutdown_passed,
            "network_partition_passed": chaos.network_partition_passed,
            "cloud_provider_outage_passed": chaos.cloud_provider_outage_passed,
            "zero_split_brain_verified": chaos.zero_split_brain_verified,
            "passed": chaos.passed,
            "details": chaos.details,
        }
        chaos_file.write_text(json.dumps(chaos_data, indent=2), encoding="utf-8")
        files_written.append(str(chaos_file))

        # 8. availability_metrics.json
        avail_file = self.output_dir / "availability_metrics.json"
        avail_data = {
            "annual_uptime_target_pct": avail.annual_uptime_target_pct,
            "availability_tier": avail.availability_tier.value,
            "measured_regional_rto_seconds": avail.measured_regional_rto_seconds,
            "measured_regional_rpo_seconds": avail.measured_regional_rpo_seconds,
            "rto_sla_met": avail.rto_sla_met,
            "rpo_sla_met": avail.rpo_sla_met,
            "availability_score": avail.availability_score,
            "passed": avail.passed,
            "details": avail.details,
        }
        avail_file.write_text(json.dumps(avail_data, indent=2), encoding="utf-8")
        files_written.append(str(avail_file))

        # 9. certification.json
        cert_file = self.output_dir / "certification.json"
        cert_data = {
            "certification_id": "CERT-3G6-MULTI-REGION-FAILOVER-001",
            "platform": "DocuTask Agent",
            "phase": "3G.6",
            "primary_region": arch.primary_region.value,
            "secondary_region": arch.secondary_region.value,
            "overall_failover_score": scorecard.overall_failover_score,
            "availability_tier": scorecard.availability_tier.value,
            "certification_verdict": scorecard.certification_verdict,
            "ci_cd_deployment_approved": scorecard.ci_cd_deployment_approved,
            "measured_rto_seconds": avail.measured_regional_rto_seconds,
            "measured_rpo_seconds": avail.measured_regional_rpo_seconds,
            "issued_at_utc": now_str,
            "valid_until_utc": "2027-09-15T12:00:00Z",
        }
        cert_file.write_text(json.dumps(cert_data, indent=2), encoding="utf-8")
        files_written.append(str(cert_file))

        return {
            "total_files_exported": len(files_written),
            "output_directory": str(self.output_dir),
            "files": files_written,
        }
