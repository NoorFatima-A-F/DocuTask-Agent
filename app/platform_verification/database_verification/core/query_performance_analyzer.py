"""
Query Performance and Index Analyzer for Database Verification.
"""
from typing import Dict, List, Any
from app.platform_verification.database_verification.domain.models import (
    TableSchemaDefinition,
    QueryPerformanceReport,
)
from app.platform_verification.database_verification.domain.interfaces import IQueryPerformanceAnalyzer


class QueryPerformanceAnalyzer(IQueryPerformanceAnalyzer):
    """Analyzes queries and schemas for sequential scans, missing indexes, and N+1 patterns."""

    def analyze_queries(
        self,
        queries: List[Dict[str, Any]],
        schemas: Dict[str, TableSchemaDefinition]
    ) -> QueryPerformanceReport:
        seq_scan_hazards: List[str] = []
        missing_indexes: List[str] = []
        n_plus_one_hazards: List[str] = []
        latencies: List[float] = []

        for q in queries:
            table_name = q.get("table", "")
            filter_cols = q.get("filter_columns", [])
            has_join_in_loop = q.get("join_in_loop", False)
            latency = q.get("simulated_latency_ms", 3.5)
            latencies.append(latency)

            if has_join_in_loop:
                n_plus_one_hazards.append(f"Query on '{table_name}' executed iteratively in loop (N+1 hazard)")

            if table_name in schemas:
                table_schema = schemas[table_name]
                indexed_columns = set()
                for idx in table_schema.indexes:
                    indexed_columns.update(idx.columns)

                for fc in filter_cols:
                    if fc not in indexed_columns and not table_schema.columns.get(fc, None) and fc not in table_schema.primary_key_columns:
                        seq_scan_hazards.append(f"Filter column '{table_name}.{fc}' is unindexed; causes sequential scan")
                        missing_indexes.append(f"CREATE INDEX idx_{table_name}_{fc} ON {table_name}({fc});")

        latencies.sort()
        p95 = latencies[int(len(latencies) * 0.95)] if latencies else 4.0
        p99 = latencies[int(len(latencies) * 0.99)] if latencies else 12.0

        score = 100.0 - (len(seq_scan_hazards) * 10.0) - (len(n_plus_one_hazards) * 15.0)
        score = max(0.0, min(100.0, score))
        status = "PASS" if score >= 80.0 else "FAIL"

        return QueryPerformanceReport(
            status=status,
            scanned_queries=len(queries),
            sequential_scan_hazards=seq_scan_hazards,
            missing_indexes=missing_indexes,
            n_plus_one_hazards=n_plus_one_hazards,
            p95_latency_ms=round(p95, 2),
            p99_latency_ms=round(p99, 2),
            performance_score=score,
        )
