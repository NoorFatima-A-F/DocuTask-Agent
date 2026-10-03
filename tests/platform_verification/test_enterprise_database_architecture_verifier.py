"""
Comprehensive Test Suite for Part 2F: Enterprise Database Architecture Verification Framework.
"""
import pytest
from app.platform_verification.database_verification.runtime.database_verification_runtime import DatabaseVerificationRuntime
from app.platform_verification.database_verification.domain.models import (
    DatabaseCertificationTier,
    TableSchemaDefinition,
    ColumnDefinition,
    IndexDefinition,
    MigrationStep,
)


@pytest.fixture
def db_runtime():
    return DatabaseVerificationRuntime()


def test_schema_analyzer_and_normalization(db_runtime):
    """Verifies schema quality calculation, primary key checks, foreign keys and 3NF normalization."""
    tables = {
        "valid_table": TableSchemaDefinition(
            table_name="valid_table",
            columns={
                "id": ColumnDefinition(name="id", data_type="uuid", is_primary_key=True),
                "tenant_id": ColumnDefinition(name="tenant_id", data_type="uuid", is_foreign_key=True, foreign_target="tenants.id", is_indexed=True),
                "status": ColumnDefinition(name="status", data_type="varchar", is_nullable=False),
            },
            primary_key_columns=["id"],
            indexes=[IndexDefinition(name="idx_valid_tenant", table_name="valid_table", columns=["tenant_id"])],
        ),
        "tbl_bad_table": TableSchemaDefinition(
            table_name="tbl_bad_table",
            columns={
                "email": ColumnDefinition(name="email", data_type="varchar", is_nullable=True),
                "author_id": ColumnDefinition(name="author_id", data_type="uuid", is_foreign_key=False),
                "user_name": ColumnDefinition(name="user_name", data_type="varchar"),  # Denormalized 3NF violation
            },
            normalization_level="2NF",
            primary_key_columns=[],  # Missing PK
        ),
    }

    report = db_runtime.schema_analyzer.analyze_schemas(tables)
    assert report.total_tables == 2
    assert "valid_table" in report.table_reports
    assert report.table_reports["valid_table"].schema_score >= 90.0
    assert not report.normalization_passed
    assert len(report.unnormalized_columns) > 0


def test_migration_safety_and_rollback(db_runtime):
    """Verifies migration downgrade/rollback safety and flags destructive or unindexed migrations."""
    safe_migrations = [
        MigrationStep(version="001", description="Initial setup", has_upgrade=True, has_downgrade=True),
        MigrationStep(version="002", description="Add table", has_upgrade=True, has_downgrade=True),
    ]
    safe_rep = db_runtime.migration_validator.validate_migrations(safe_migrations)
    assert safe_rep.status == "PASS"
    assert safe_rep.all_rollbacks_tested

    unsafe_migrations = [
        MigrationStep(version="003", description="Drop legacy columns", has_upgrade=True, has_downgrade=False, is_destructive=True),
    ]
    unsafe_rep = db_runtime.migration_validator.validate_migrations(unsafe_migrations)
    assert unsafe_rep.status == "FAIL"
    assert not unsafe_rep.all_rollbacks_tested
    assert len(unsafe_rep.destructive_operations) == 1


def test_transaction_safety_and_acid_rollback(db_runtime):
    """Tests ACID transaction rollback when workflow steps fail and optimistic locking."""
    workflows = [
        {
            "name": "ai_document_processing",
            "atomic_transaction": True,
            "uses_optimistic_locking": True,
            "steps": [
                {"action": "create_row"},
                {"action": "ocr_extraction"},
                {"action": "ai_reasoning", "should_fail": False},
            ],
        },
        {
            "name": "unsafe_non_atomic_workflow",
            "atomic_transaction": False,
            "uses_optimistic_locking": False,
            "steps": [{"action": "direct_write"}],
        },
    ]

    report = db_runtime.transaction_engine.evaluate_transaction_safety(workflows)
    assert report.status == "FAIL"
    assert not report.rollback_on_failure_verified
    assert "unsafe_non_atomic_workflow" in report.unprotected_mutation_paths


def test_query_performance_and_sequential_scan_detection(db_runtime):
    """Verifies detection of unindexed filter columns and sequential scan hazards."""
    schemas = {
        "documents": TableSchemaDefinition(
            table_name="documents",
            columns={"id": ColumnDefinition(name="id", data_type="uuid", is_primary_key=True)},
            primary_key_columns=["id"],
            indexes=[],
        )
    }
    queries = [
        {"table": "documents", "filter_columns": ["status", "created_at"], "join_in_loop": True, "simulated_latency_ms": 25.0}
    ]

    report = db_runtime.query_analyzer.analyze_queries(queries, schemas)
    assert len(report.sequential_scan_hazards) >= 2
    assert len(report.n_plus_one_hazards) == 1
    assert len(report.missing_indexes) >= 2


def test_tenant_isolation_and_cross_leak_detection(db_runtime):
    """Verifies that missing tenant_id filters and cross-tenant data leaks are caught."""
    clean_queries = [
        {"name": "q1", "filters": {"tenant_id": "tenant_1"}, "target_tenant": "tenant_1", "authenticated_tenant": "tenant_1"}
    ]
    clean_rep = db_runtime.isolation_validator.validate_isolation(clean_queries)
    assert clean_rep.status == "PASS"
    assert not clean_rep.cross_tenant_leak_detected

    leaky_queries = [
        {"name": "leaky_q", "filters": {}, "target_tenant": "tenant_2", "authenticated_tenant": "tenant_1", "returned_record_count": 3}
    ]
    leaky_rep = db_runtime.isolation_validator.validate_isolation(leaky_queries)
    assert leaky_rep.status == "FAIL"
    assert leaky_rep.cross_tenant_leak_detected


def test_security_evaluator_and_sql_injection(db_runtime):
    """Tests SQL injection detection and credential leak scanning."""
    safe_queries = ["SELECT id FROM users WHERE id = :user_id"]
    safe_code = ["db_pass = os.environ.get('DB_PASS')"]
    safe_rep = db_runtime.security_evaluator.evaluate_security(safe_queries, safe_code)
    assert safe_rep.status == "PASS"
    assert safe_rep.sql_injection_safe

    insecure_queries = ["f'SELECT * FROM documents WHERE name = {user_input}'"]
    insecure_code = ["postgres_url = 'postgresql://admin:supersecretpassword@localhost:5432/docutask'"]
    insecure_rep = db_runtime.security_evaluator.evaluate_security(insecure_queries, insecure_code)
    assert insecure_rep.status == "FAIL"
    assert not insecure_rep.sql_injection_safe
    assert len(insecure_rep.hardcoded_credentials_found) > 0


def test_backup_recovery_rpo_rto_validation(db_runtime):
    """Tests backup verification and RPO/RTO compliance."""
    compliant_meta = {
        "checksum_verified": True,
        "point_in_time_recovery_supported": True,
        "measured_rpo_minutes": 5.0,
        "measured_rto_minutes": 20.0,
        "max_acceptable_rpo_minutes": 15.0,
        "max_acceptable_rto_minutes": 60.0,
    }
    rep = db_runtime.recovery_validator.validate_backup_recovery(compliant_meta)
    assert rep.status == "PASS"
    assert rep.recovery_score >= 90.0

    non_compliant = {
        "checksum_verified": False,
        "point_in_time_recovery_supported": False,
        "measured_rpo_minutes": 120.0,
        "measured_rto_minutes": 300.0,
    }
    fail_rep = db_runtime.recovery_validator.validate_backup_recovery(non_compliant)
    assert fail_rep.status == "FAIL"


def test_end_to_end_database_verification_and_rest_api(db_runtime):
    """Tests end-to-end full verification run, evidence generation, and in-process REST API."""
    package = db_runtime.run_full_verification(
        commit_sha="git-sha-f1a2b3",
        target_database="PostgreSQL-16-Enterprise",
    )

    assert package.scorecard.composite_score >= 90.0
    assert package.scorecard.tier in [DatabaseCertificationTier.PRODUCTION_READY, DatabaseCertificationTier.ACCEPTABLE]
    assert package.package_sha256 != ""

    # Test REST API
    api = db_runtime.api
    scan_res = api.post_scan({"commit_sha": "git-sha-f1a2b3", "target_database": "PostgreSQL-16-Enterprise"})
    assert scan_res["status"] == "COMPLETED"
    assert "package_id" in scan_res

    report_res = api.get_report(scan_res["package_id"])
    assert report_res is not None
    assert report_res["commit_sha"] == "git-sha-f1a2b3"
    assert "scorecard" in report_res

    metrics_res = api.get_metrics()
    assert "supported_engines" in metrics_res
