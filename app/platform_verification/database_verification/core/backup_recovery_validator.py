"""
Backup and Recovery RPO/RTO Validator for Enterprise Database Verification.
"""
from typing import Dict, Any
from app.platform_verification.database_verification.domain.models import BackupRecoveryReport
from app.platform_verification.database_verification.domain.interfaces import IBackupRecoveryValidator


class BackupRecoveryValidator(IBackupRecoveryValidator):
    """Validates automated backup integrity, point-in-time recovery, RPO and RTO compliance."""

    def validate_backup_recovery(self, backup_metadata: Dict[str, Any]) -> BackupRecoveryReport:
        backup_verified = backup_metadata.get("checksum_verified", True)
        pitr_supported = backup_metadata.get("point_in_time_recovery_supported", True)
        rpo = backup_metadata.get("measured_rpo_minutes", 5.0)
        rto = backup_metadata.get("measured_rto_minutes", 15.0)
        max_rpo = backup_metadata.get("max_acceptable_rpo_minutes", 15.0)
        max_rto = backup_metadata.get("max_acceptable_rto_minutes", 60.0)

        score = 100.0
        if not backup_verified:
            score -= 40.0
        if not pitr_supported:
            score -= 20.0
        if rpo > max_rpo:
            score -= 20.0
        if rto > max_rto:
            score -= 20.0

        score = max(0.0, min(100.0, score))
        status = "PASS" if score >= 80.0 else "FAIL"

        return BackupRecoveryReport(
            status=status,
            backup_integrity_verified=backup_verified,
            point_in_time_recovery_supported=pitr_supported,
            rpo_minutes=rpo,
            rto_minutes=rto,
            max_acceptable_rpo_minutes=max_rpo,
            max_acceptable_rto_minutes=max_rto,
            recovery_score=score,
        )
