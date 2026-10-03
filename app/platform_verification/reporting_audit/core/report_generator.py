"""
Audit Report Generator with SHA-256 integrity digest generation.
"""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid
from app.platform_verification.reporting_audit.domain.interfaces import IAuditReportGenerator
from app.platform_verification.reporting_audit.domain.models import (
    AuditReportRecord,
    ReportFormat,
    ReportType,
)


class EnterpriseAuditReportGenerator(IAuditReportGenerator):
    """Compiles and signs formal compliance and verification reports."""

    def __init__(self):
        self._reports: Dict[str, AuditReportRecord] = {}

    def generate_report(
        self,
        report_type: ReportType,
        title: str,
        scope: str,
        data: Dict[str, Any],
        evidence_refs: List[str],
        generated_by: str,
        report_format: ReportFormat = ReportFormat.JSON,
    ) -> AuditReportRecord:
        report_id = f"RPT-{report_type.value[:4]}-{uuid.uuid4().hex[:8].upper()}"
        generated_at = datetime.now(timezone.utc).isoformat()

        record = AuditReportRecord(
            report_id=report_id,
            report_type=report_type,
            title=title,
            scope=scope,
            generated_by=generated_by,
            generated_at=generated_at,
            evidence_references=evidence_refs,
            content=data,
            generator_version="v1.0.0",
        )
        record.sha256_digest = record.compute_sha256()

        self._reports[report_id] = record
        return record

    def get_report(self, report_id: str) -> Optional[AuditReportRecord]:
        return self._reports.get(report_id)

    def search_reports(self, query: str) -> List[AuditReportRecord]:
        q = query.lower()
        return [
            r for r in self._reports.values()
            if q in r.title.lower() or q in r.scope.lower() or q in r.report_type.value.lower()
        ]
