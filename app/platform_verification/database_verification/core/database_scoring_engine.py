"""
Weighted Database Quality Scoring and Certification Engine.
"""
from app.platform_verification.database_verification.domain.models import (
    SchemaQualityReport,
    TransactionSafetyReport,
    QueryPerformanceReport,
    DatabaseSecurityReport,
    TenantIsolationReport,
    MigrationSafetyReport,
    BackupRecoveryReport,
    DatabaseQualityScorecard,
    DatabaseCertificationTier,
)
from app.platform_verification.database_verification.domain.interfaces import IDatabaseScoringEngine


class DatabaseScoringEngine(IDatabaseScoringEngine):
    """Calculates weighted composite scorecard across 5 database pillars."""

    # Weights: Schema (25%), Transaction (20%), Performance (20%), Security/Isolation (20%), Migration/Recovery (15%)
    WEIGHT_SCHEMA = 0.25
    WEIGHT_TX = 0.20
    WEIGHT_PERF = 0.20
    WEIGHT_SEC_ISO = 0.20
    WEIGHT_MIG_REC = 0.15

    def calculate_scorecard(
        self,
        schema: SchemaQualityReport,
        tx: TransactionSafetyReport,
        perf: QueryPerformanceReport,
        security: DatabaseSecurityReport,
        isolation: TenantIsolationReport,
        migration: MigrationSafetyReport,
        recovery: BackupRecoveryReport,
    ) -> DatabaseQualityScorecard:
        schema_s = schema.average_schema_score
        tx_s = tx.acid_compliance_score
        perf_s = perf.performance_score
        sec_iso_s = (security.security_score * 0.5) + (isolation.rls_or_filter_score * 0.5)

        mig_s = 100.0 if migration.status == "PASS" else 60.0
        mig_rec_s = (mig_s * 0.5) + (recovery.recovery_score * 0.5)

        composite = (
            (schema_s * self.WEIGHT_SCHEMA)
            + (tx_s * self.WEIGHT_TX)
            + (perf_s * self.WEIGHT_PERF)
            + (sec_iso_s * self.WEIGHT_SEC_ISO)
            + (mig_rec_s * self.WEIGHT_MIG_REC)
        )
        composite = round(composite, 2)

        if composite >= 92.0 and not isolation.cross_tenant_leak_detected and security.sql_injection_safe:
            tier = DatabaseCertificationTier.PRODUCTION_READY
        elif composite >= 80.0:
            tier = DatabaseCertificationTier.ACCEPTABLE
        elif composite >= 70.0:
            tier = DatabaseCertificationTier.TECHNICAL_DEBT_WARNING
        else:
            tier = DatabaseCertificationTier.FAILED

        return DatabaseQualityScorecard(
            schema_score=round(schema_s, 2),
            transaction_score=round(tx_s, 2),
            performance_score=round(perf_s, 2),
            security_isolation_score=round(sec_iso_s, 2),
            migration_recovery_score=round(mig_rec_s, 2),
            composite_score=composite,
            tier=tier,
        )
