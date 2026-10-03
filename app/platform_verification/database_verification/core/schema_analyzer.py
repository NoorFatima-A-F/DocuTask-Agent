"""
Schema and Normalization Analyzer for Enterprise Database Verification.
"""
import re
from typing import Dict, List
from app.platform_verification.database_verification.domain.models import (
    TableSchemaDefinition,
    ColumnDefinition,
    TableQualityReport,
    TableQualityGrade,
    SchemaQualityReport,
)
from app.platform_verification.database_verification.domain.interfaces import ISchemaAnalyzer


class SchemaAnalyzer(ISchemaAnalyzer):
    """Analyzes relational database schema definitions against enterprise standards."""

    VALID_TABLE_NAME_PATTERN = re.compile(r"^[a-z][a-z0-9_]*[a-z0-9]$")

    def analyze_schemas(self, tables: Dict[str, TableSchemaDefinition]) -> SchemaQualityReport:
        table_reports: Dict[str, TableQualityReport] = {}
        total_score = 0.0
        unnormalized_columns: List[str] = []

        for name, table in tables.items():
            report = self._analyze_table(name, table, tables)
            table_reports[name] = report
            total_score += report.schema_score

            # Check 3NF denormalization flags
            if table.normalization_level != "3NF":
                for col_name, col in table.columns.items():
                    if any(prefix in col_name for prefix in ["user_name", "user_email", "tenant_name", "author_name"]):
                        unnormalized_columns.append(f"{name}.{col_name}")

        avg_score = total_score / max(len(tables), 1)
        normalization_passed = len(unnormalized_columns) == 0

        return SchemaQualityReport(
            total_tables=len(tables),
            average_schema_score=round(avg_score, 2),
            table_reports=table_reports,
            normalization_passed=normalization_passed,
            unnormalized_columns=unnormalized_columns,
        )

    def _analyze_table(
        self,
        name: str,
        table: TableSchemaDefinition,
        all_tables: Dict[str, TableSchemaDefinition]
    ) -> TableQualityReport:
        issues: List[str] = []
        score = 100.0

        # 1. Primary Key check
        has_pk = len(table.primary_key_columns) > 0
        if not has_pk:
            issues.append("Missing primary key")
            score -= 30.0

        # 2. Naming standard
        naming_passed = bool(self.VALID_TABLE_NAME_PATTERN.match(name)) and not name.startswith("tbl_") and not name.startswith("data")
        if not naming_passed:
            issues.append(f"Table name '{name}' violates snake_case convention or uses forbidden prefixes")
            score -= 10.0

        # 3. Foreign Key Checks
        missing_fks: List[str] = []
        unindexed_fks: List[str] = []
        indexed_cols = set()
        for idx in table.indexes:
            indexed_cols.update(idx.columns)

        for col_name, col in table.columns.items():
            if col_name.endswith("_id") and not col.is_primary_key and col_name != "tenant_id":
                if not col.is_foreign_key or not col.foreign_target:
                    missing_fks.append(col_name)
                    issues.append(f"Column '{col_name}' appears to be a relationship but lacks FK constraint")
                    score -= 10.0
                else:
                    target_tbl = col.foreign_target.split(".")[0]
                    if target_tbl not in all_tables:
                        missing_fks.append(col_name)
                        issues.append(f"FK '{col_name}' references non-existent table '{target_tbl}'")
                        score -= 15.0

                if col_name not in indexed_cols and not col.is_indexed:
                    unindexed_fks.append(col_name)
                    issues.append(f"Foreign key '{col_name}' lacks dedicated index")
                    score -= 5.0

        # 4. Bad Nullable Columns
        bad_nullable: List[str] = []
        for col_name, col in table.columns.items():
            if col_name in ["email", "username", "status", "created_at"] and col.is_nullable:
                bad_nullable.append(col_name)
                issues.append(f"Critical field '{col_name}' is marked nullable")
                score -= 5.0

        final_score = max(0.0, min(100.0, score))
        if final_score >= 95.0:
            grade = TableQualityGrade.A_EXCELLENT
        elif final_score >= 85.0:
            grade = TableQualityGrade.B_GOOD
        elif final_score >= 75.0:
            grade = TableQualityGrade.C_ACCEPTABLE
        elif final_score >= 60.0:
            grade = TableQualityGrade.D_DEFICIENT
        else:
            grade = TableQualityGrade.F_FAILED

        return TableQualityReport(
            table_name=name,
            schema_score=final_score,
            grade=grade,
            has_pk=has_pk,
            missing_fks=missing_fks,
            unindexed_fks=unindexed_fks,
            bad_nullable_columns=bad_nullable,
            naming_standard_passed=naming_passed,
            issues=issues,
        )
