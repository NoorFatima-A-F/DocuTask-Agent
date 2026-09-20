"""
Multi-Tenant Isolation Validator for Enterprise Database Verification.
"""
from typing import Dict, List, Any
from app.platform_verification.database_verification.domain.models import TenantIsolationReport
from app.platform_verification.database_verification.domain.interfaces import ITenantIsolationValidator


class TenantIsolationValidator(ITenantIsolationValidator):
    """Verifies that queries and repositories strictly enforce tenant boundaries."""

    def validate_isolation(self, queries: List[Dict[str, Any]]) -> TenantIsolationReport:
        unscoped: List[str] = []
        cross_leak = False

        for q in queries:
            sql_or_name = q.get("name", "unnamed_query")
            filters = q.get("filters", {})
            target_tenant = q.get("target_tenant", "tenant_alpha")
            authenticated_tenant = q.get("authenticated_tenant", "tenant_alpha")

            # Check if tenant_id is in filter
            if "tenant_id" not in filters and not q.get("is_global_system_query", False):
                unscoped.append(sql_or_name)

            # Test cross-tenant access attempt
            if target_tenant != authenticated_tenant:
                # If query succeeded without permission check, leak occurred
                if q.get("returned_record_count", 0) > 0:
                    cross_leak = True
                    unscoped.append(f"{sql_or_name}_cross_tenant_leak")

        score = 100.0 - (len(unscoped) * 20.0) - (50.0 if cross_leak else 0.0)
        score = max(0.0, min(100.0, score))
        status = "PASS" if score >= 90.0 and not cross_leak else "FAIL"

        return TenantIsolationReport(
            status=status,
            tenant_filtering_enforced=(len(unscoped) == 0),
            cross_tenant_leak_detected=cross_leak,
            unscoped_queries=unscoped,
            rls_or_filter_score=score,
        )
