"""Tests for Governance Reporting Engine, Templates, and Multi-Format Exporters."""

import pytest
import json
from app.governance.analytics.warehouse.repositories import GovernanceDataWarehouseRepository
from app.governance.analytics.core.engine import GovernanceMetricsEngine
from app.governance.analytics.reporting.templates import ReportType, ReportFormat
from app.governance.analytics.reporting.generator import ReportGenerator
from app.governance.analytics.reporting.exporters import ReportExporter


def test_report_generation_and_export():
    repo = GovernanceDataWarehouseRepository()
    metrics = GovernanceMetricsEngine(repo)
    gen = ReportGenerator(metrics_engine=metrics)

    # 1. Executive Report
    rep_exec = gen.generate_report(ReportType.MONTHLY_EXECUTIVE, tenant_id="tenant_rep")
    assert rep_exec.report_id.startswith("rep_")
    assert rep_exec.governance_score >= 0.0
    assert len(rep_exec.sections) >= 1

    # 2. Export JSON
    json_out = ReportExporter.export(rep_exec, format=ReportFormat.JSON)
    parsed = json.loads(json_out)
    assert parsed["report_id"] == rep_exec.report_id

    # 3. Export CSV
    csv_out = ReportExporter.export(rep_exec, format=ReportFormat.CSV)
    assert "Report ID" in csv_out

    # 4. Export PDF (text formatted)
    pdf_out = ReportExporter.export(rep_exec, format=ReportFormat.PDF)
    assert "EXECUTIVE SUMMARY:" in pdf_out

    # 5. Export Excel (TSV)
    excel_out = ReportExporter.export(rep_exec, format=ReportFormat.EXCEL)
    assert "Section\tMetric\tValue" in excel_out
