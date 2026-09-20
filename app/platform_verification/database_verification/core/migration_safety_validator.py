"""
Migration Safety and Rollback Validator for Enterprise Database Verification.
"""
from typing import List
from app.platform_verification.database_verification.domain.models import (
    MigrationStep,
    MigrationSafetyReport,
)
from app.platform_verification.database_verification.domain.interfaces import IMigrationSafetyValidator


class MigrationSafetyValidator(IMigrationSafetyValidator):
    """Verifies forward migrations and rollbacks for reversibility and stability."""

    def validate_migrations(self, migrations: List[MigrationStep]) -> MigrationSafetyReport:
        reversible_count = 0
        irreversible_count = 0
        destructive_ops: List[str] = []
        issues: List[str] = []

        for step in migrations:
            if not step.has_downgrade or not step.is_reversible:
                irreversible_count += 1
                issues.append(f"Migration {step.version} ({step.description}) lacks a valid downgrade/rollback script")
            else:
                reversible_count += 1

            if step.is_destructive:
                destructive_ops.append(f"{step.version}: {step.description}")
                issues.append(f"Migration {step.version} contains destructive operation (e.g. drop column/table without deprecation)")

            if step.unindexed_foreign_keys_added:
                for fk in step.unindexed_foreign_keys_added:
                    issues.append(f"Migration {step.version} adds foreign key '{fk}' without creating a supporting index")

        all_rollbacks_tested = (irreversible_count == 0)
        status = "PASS" if all_rollbacks_tested and len(destructive_ops) == 0 else "FAIL"

        return MigrationSafetyReport(
            status=status,
            total_migrations=len(migrations),
            reversible_count=reversible_count,
            irreversible_count=irreversible_count,
            destructive_operations=destructive_ops,
            all_rollbacks_tested=all_rollbacks_tested,
            issues=issues,
        )
