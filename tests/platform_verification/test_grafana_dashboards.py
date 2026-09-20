"""Comprehensive Unit and Integration Tests for Phase 3H.4.4 — Grafana Dashboard Verification Framework."""

import os
import json
import pytest

from app.platform_verification.grafana_verification.domain.models import (
    DashboardCertificationTier,
    DashboardCategory,
    UserRole,
)
from app.platform_verification.grafana_verification.verifiers.grafana_configuration_verifier import (
    GrafanaConfigurationVerifier,
)
from app.platform_verification.grafana_verification.verifiers.dashboard_provisioning_verifier import (
    DashboardProvisioningVerifier,
)
from app.platform_verification.grafana_verification.verifiers.system_health_verifier import (
    SystemHealthDashboardVerifier,
)
from app.platform_verification.grafana_verification.verifiers.ai_processing_verifier import (
    AIProcessingDashboardVerifier,
)
from app.platform_verification.grafana_verification.verifiers.agent_runtime_verifier import (
    AgentRuntimeDashboardVerifier,
)
from app.platform_verification.grafana_verification.verifiers.infrastructure_verifier import (
    InfrastructureDashboardVerifier,
)
from app.platform_verification.grafana_verification.verifiers.incident_dashboard_verifier import (
    IncidentDashboardVerifier,
)
from app.platform_verification.grafana_verification.usability.dashboard_usability_verifier import (
    DashboardUsabilityVerifier,
)
from app.platform_verification.grafana_verification.performance.dashboard_performance_verifier import (
    DashboardPerformanceVerifier,
)
from app.platform_verification.grafana_verification.security.dashboard_security_auditor import (
    DashboardSecurityAuditor,
)
from app.platform_verification.grafana_verification.scoring.dashboard_quality_scorer import (
    DashboardQualityScorer,
)
from app.platform_verification.grafana_verification.exporter.grafana_evidence_exporter import (
    GrafanaEvidenceExporter,
)
from app.platform_verification.grafana_verification.runtime.grafana_verification_runtime import (
    GrafanaVerificationRuntime,
)


class TestGrafanaDashboardVerification:
    """Test suite for validating Grafana dashboard verification components."""

    def test_grafana_configuration_verification(self):
        """3H.4.4.1: Verify Grafana configuration (datasources, storage, ports, auth)."""
        verifier = GrafanaConfigurationVerifier()
        report = verifier.verify_configuration()
        assert report.status == "PASS"
        assert report.datasource_type == "prometheus"
        assert report.authentication_enabled is True
        assert report.persistent_storage_enabled is True
        assert report.grafana_version == "11.2.0"

    def test_dashboard_provisioning_and_recovery(self):
        """3H.4.4.2: Verify dashboard provisioning from file definitions and teardown recovery."""
        verifier = DashboardProvisioningVerifier()
        report = verifier.verify_provisioning()
        assert report.status == "PASS"
        assert report.provisioned_dashboards_count >= 5
        assert report.tear_down_recovery_verified is True
        assert report.iac_format == "JSON"

    def test_system_health_dashboard(self):
        """3H.4.4.3: Verify System Health dashboard panels, metrics, and traffic lights."""
        verifier = SystemHealthDashboardVerifier()
        report = verifier.verify_dashboard()
        assert report.status == "PASS"
        assert report.category == DashboardCategory.SYSTEM_HEALTH
        assert report.total_panels == 8
        assert report.all_queries_valid is True

    def test_ai_processing_dashboard(self):
        """3H.4.4.4: Verify AI Processing dashboard (throughput, latency percentiles, tokens)."""
        verifier = AIProcessingDashboardVerifier()
        report = verifier.verify_dashboard()
        assert report.status == "PASS"
        assert report.category == DashboardCategory.AI_PROCESSING
        assert report.total_panels == 5
        assert report.all_queries_valid is True

    def test_agent_runtime_dashboard(self):
        """3H.4.4.5: Verify Agent Runtime dashboard (tasks, planner duration, tool calls)."""
        verifier = AgentRuntimeDashboardVerifier()
        report = verifier.verify_dashboard()
        assert report.status == "PASS"
        assert report.category == DashboardCategory.AGENT_RUNTIME
        assert report.total_panels == 5
        assert report.all_queries_valid is True

    def test_infrastructure_dashboard(self):
        """3H.4.4.6: Verify Infrastructure dashboard (CPU, RAM, Postgres, Redis, Disk)."""
        verifier = InfrastructureDashboardVerifier()
        report = verifier.verify_dashboard()
        assert report.status == "PASS"
        assert report.category == DashboardCategory.INFRASTRUCTURE
        assert report.total_panels == 4
        assert report.all_queries_valid is True

    def test_incident_response_dashboard(self):
        """3H.4.4.7: Verify Incident Investigation dashboard (alerts, exceptions, MTTR)."""
        verifier = IncidentDashboardVerifier()
        report = verifier.verify_dashboard()
        assert report.status == "PASS"
        assert report.category == DashboardCategory.INCIDENT_INVESTIGATION
        assert report.total_panels == 4
        assert report.all_queries_valid is True

    def test_dashboard_usability_scenarios(self):
        """3H.4.4.8: Verify operational workflows (routine check, failure diagnosis, deployment attribution)."""
        verifier = DashboardUsabilityVerifier()
        report = verifier.verify_usability()
        assert report.status == "PASS"
        assert report.total_scenarios_tested == 3
        assert report.passed_scenarios == 3
        assert report.avg_identification_time_seconds < 30.0

    def test_dashboard_performance_benchmarks(self):
        """3H.4.4.9: Verify performance under 100k data points (<3s load, <1s query)."""
        verifier = DashboardPerformanceVerifier()
        report = verifier.verify_performance()
        assert report.status == "PASS"
        assert report.load_time_target_met is True
        assert report.query_response_target_met is True
        assert report.avg_dashboard_load_time_seconds < 3.0

    def test_dashboard_security_auditor(self):
        """3H.4.4.10: Audit for secret leaks, PII, auth enforcement, and RBAC matrix."""
        auditor = DashboardSecurityAuditor()
        report = auditor.audit_security()
        assert report.status == "PASS"
        assert report.auth_login_enforced is True
        assert report.zero_leak_verified is True
        assert report.api_key_exposure_found == 0
        assert report.pii_customer_data_exposure_found == 0

    def test_quality_scorecard_calculation(self):
        """3H.4.4.11: Verify quality scorecard calculation and enterprise tier certification."""
        runtime = GrafanaVerificationRuntime()
        scorecard, _ = runtime.execute_full_verification()
        assert scorecard.overall_score >= 95.0
        assert scorecard.certification_tier == DashboardCertificationTier.ENTERPRISE_DASHBOARD_READY
        assert scorecard.passed is True
        assert scorecard.system_visibility_score == 100.0
        assert scorecard.ai_workload_visibility_score == 100.0

    def test_evidence_exporter_and_manifests(self, tmp_path):
        """3H.4.4.12: Verify exporting all 12 evidence manifests."""
        runtime = GrafanaVerificationRuntime(output_dir=str(tmp_path))
        scorecard, manifests = runtime.execute_full_verification()
        assert scorecard.passed is True
        assert len(manifests) == 12

        expected_files = [
            "configuration_report.json",
            "provisioning_report.json",
            "system_dashboard_report.json",
            "ai_dashboard_report.json",
            "agent_dashboard_report.json",
            "infrastructure_dashboard_report.json",
            "incident_dashboard_report.json",
            "usability_report.json",
            "performance_report.json",
            "security_report.json",
            "certification_report.json",
            "metadata.json",
        ]

        for fname in expected_files:
            fpath = tmp_path / fname
            assert fpath.exists(), f"Missing manifest: {fname}"
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
                assert isinstance(data, dict)
