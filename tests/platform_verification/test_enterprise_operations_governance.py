"""
Phase 3R: Comprehensive Test Suite for Enterprise Production Operations Governance Framework.
"""

from pathlib import Path
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.platform_verification.enterprise_operations_governance.domain.models import (
    IncidentSeverity,
    MaturityCertification,
    SystemHealthStatus,
)
from app.platform_verification.enterprise_operations_governance.core import (
    AIOpsMonitor,
    AlertingEngine,
    AuditTrailEngine,
    ChangeManager,
    FinOpsMonitor,
    HealthIntelligenceEngine,
    IncidentManager,
    OperationalMaturityScorer,
    RootCauseAnalyzer,
    RunbookEngine,
    SelfHealingEngine,
    SLOManager,
)
from app.platform_verification.enterprise_operations_governance.exporter.operations_governance_exporter import (
    OperationsGovernanceExporter,
)
from app.platform_verification.enterprise_operations_governance.runtime.operations_governance_runtime import (
    OperationsGovernanceRuntime,
)
from app.platform_verification.enterprise_operations_governance.api.operations_governance_api import (
    router,
)


class TestEnterpriseOperationsGovernance:
    """Comprehensive test suite for Phase 3R Enterprise Platform Operations Governance."""

    @pytest.fixture
    def app_client(self):
        app = FastAPI()
        app.include_router(router)
        return TestClient(app)

    @pytest.fixture
    def temp_export_dir(self, tmp_path):
        export_path = tmp_path / "test_operations_verification"
        export_path.mkdir(parents=True, exist_ok=True)
        return str(export_path)

    # ──────────────────────────────────────────────────────────────────────────
    # 1. SLO Framework & Error Budget Tests (Part 3R.1, 3R.2)
    # ──────────────────────────────────────────────────────────────────────────

    def test_evaluate_slos(self):
        slo_mgr = SLOManager()
        report = slo_mgr.evaluate_slos()
        assert report.all_slos_met is True
        assert report.compliance_score == 100.0
        assert len(report.slos) == 4
        assert any(s.name == "API Availability" for s in report.slos)
        assert any(s.name == "Document Submission Latency" for s in report.slos)

    def test_calculate_error_budget(self):
        slo_mgr = SLOManager()
        budget = slo_mgr.calculate_error_budget()
        assert budget.total_budget_minutes == 216.0
        assert budget.remaining_budget_pct > 90.0
        assert budget.budget_exhausted is False
        assert budget.deployment_freeze_active is False
        assert "permitted" in budget.policy_recommendation.lower()

    # ──────────────────────────────────────────────────────────────────────────
    # 2. Production Health Intelligence Tests (Part 3R.3)
    # ──────────────────────────────────────────────────────────────────────────

    def test_assess_production_health(self):
        health_engine = HealthIntelligenceEngine()
        report = health_engine.assess_production_health()
        assert report.overall_status == SystemHealthStatus.HEALTHY
        assert report.api_health == SystemHealthStatus.HEALTHY
        assert report.worker_health == SystemHealthStatus.HEALTHY
        assert report.database_health == SystemHealthStatus.HEALTHY
        assert len(report.subsystems) >= 5
        assert report.cpu_usage_pct < 60.0
        assert report.memory_usage_pct < 70.0

    # ──────────────────────────────────────────────────────────────────────────
    # 3. Incident Management Tests (Part 3R.4)
    # ──────────────────────────────────────────────────────────────────────────

    def test_incident_summary(self):
        inc_mgr = IncidentManager()
        report = inc_mgr.get_incident_summary()
        assert report.active_incidents_count == 0
        assert report.resolved_incidents_count >= 3
        assert report.mean_time_to_recover_sec < 60.0
        assert report.incident_management_healthy is True
        assert any(i.severity == IncidentSeverity.SEV2_MAJOR for i in report.incidents)

    # ──────────────────────────────────────────────────────────────────────────
    # 4. Multi-Channel Alerting Tests (Part 3R.5)
    # ──────────────────────────────────────────────────────────────────────────

    def test_evaluate_alert_rules(self):
        alert_engine = AlertingEngine()
        report = alert_engine.evaluate_alert_rules()
        assert report.total_configured_alerts >= 6
        assert report.active_firing_alerts == 0
        assert report.pipeline_status == "ALL_ALERTS_NOMINAL"
        assert "pagerduty" in report.notification_channels
        assert "slack_ops" in report.notification_channels

    # ──────────────────────────────────────────────────────────────────────────
    # 5. Operational Runbooks Tests (Part 3R.6)
    # ──────────────────────────────────────────────────────────────────────────

    def test_validate_runbooks(self):
        rb_engine = RunbookEngine()
        report = rb_engine.validate_runbooks()
        assert report.total_runbooks == 6
        assert report.coverage_pct == 100.0
        assert report.all_runbooks_validated is True
        assert any(r.filename == "database_failure.md" for r in report.runbooks)
        assert any(r.filename == "worker_failure.md" for r in report.runbooks)
        assert any(r.filename == "recovery_procedure.md" for r in report.runbooks)

    # ──────────────────────────────────────────────────────────────────────────
    # 6. Self-Healing Automated Remediation Tests (Part 3R.7)
    # ──────────────────────────────────────────────────────────────────────────

    def test_self_healing_verification(self):
        healing_engine = SelfHealingEngine()
        report = healing_engine.execute_self_healing_verification()
        assert report.self_healing_enabled is True
        assert report.successful_remediations == report.total_remediations_executed
        assert report.failed_remediations == 0
        assert report.average_recovery_time_sec < 20.0
        assert len(report.actions) == 3

    # ──────────────────────────────────────────────────────────────────────────
    # 7. Root Cause Analysis Tests (Part 3R.8)
    # ──────────────────────────────────────────────────────────────────────────

    def test_analyze_incident(self):
        rca_engine = RootCauseAnalyzer()
        report = rca_engine.analyze_incident("INC-202609-001")
        assert report.incident_id == "INC-202609-001"
        assert report.confidence > 90.0
        assert len(report.timeline_events) >= 4
        assert len(report.hypotheses) >= 2
        assert any(h.is_primary for h in report.hypotheses)
        assert len(report.recommended_preventative_actions) >= 2

    # ──────────────────────────────────────────────────────────────────────────
    # 8. Change Management Tests (Part 3R.9)
    # ──────────────────────────────────────────────────────────────────────────

    def test_audit_changes(self):
        chg_mgr = ChangeManager()
        report = chg_mgr.audit_changes()
        assert report.total_changes_recorded >= 4
        assert report.high_risk_changes == 0
        assert report.failed_rollouts == 0
        assert report.change_discipline_score == 100.0
        assert all(c.verified_post_deploy for c in report.changes)

    # ──────────────────────────────────────────────────────────────────────────
    # 9. Production Audit Trail Tests (Part 3R.10)
    # ──────────────────────────────────────────────────────────────────────────

    def test_verify_audit_trail(self):
        audit_engine = AuditTrailEngine()
        report = audit_engine.verify_audit_trail()
        assert report.immutable_log_verified is True
        assert report.total_audit_events >= 4
        assert report.unauthorized_attempts_detected == 0
        assert "100% AUDITABLE" in report.compliance_integrity

    # ──────────────────────────────────────────────────────────────────────────
    # 10. AIOps Monitoring Tests (Part 3R.11)
    # ──────────────────────────────────────────────────────────────────────────

    def test_monitor_ai_operations(self):
        ai_ops = AIOpsMonitor()
        report = ai_ops.monitor_ai_operations()
        assert report.extraction_accuracy_pct > 98.0
        assert report.schema_validation_success_pct > 99.0
        assert report.hallucination_rate_pct < 1.0
        assert report.average_cost_per_document_usd > 0
        assert report.ai_runtime_status == "OPTIMAL"

    # ──────────────────────────────────────────────────────────────────────────
    # 11. FinOps Unit Economics Tests (Part 3R.12)
    # ──────────────────────────────────────────────────────────────────────────

    def test_calculate_unit_economics(self):
        finops = FinOpsMonitor()
        report = finops.calculate_unit_economics()
        assert report.budget_utilized_pct < 50.0
        assert report.current_month_spend_usd < report.monthly_budget_usd
        assert report.cost_efficiency_score > 90.0
        assert report.cost_per_document_usd > 0
        assert "WITHIN_FORECAST" in report.cost_trend

    # ──────────────────────────────────────────────────────────────────────────
    # 12. Operational Maturity Scorer Tests (Part 3R.13)
    # ──────────────────────────────────────────────────────────────────────────

    def test_score_maturity_enterprise_mature(self):
        scorer = OperationalMaturityScorer()
        slo = SLOManager().evaluate_slos()
        budget = SLOManager().calculate_error_budget()
        health = HealthIntelligenceEngine().assess_production_health()
        incidents = IncidentManager().get_incident_summary()
        alerts = AlertingEngine().evaluate_alert_rules()
        runbooks = RunbookEngine().validate_runbooks()
        self_healing = SelfHealingEngine().execute_self_healing_verification()
        changes = ChangeManager().audit_changes()
        audit = AuditTrailEngine().verify_audit_trail()
        finops = FinOpsMonitor().calculate_unit_economics()

        context = {
            "slo": slo,
            "error_budget": budget,
            "health": health,
            "incidents": incidents,
            "alerts": alerts,
            "runbooks": runbooks,
            "self_healing": self_healing,
            "changes": changes,
            "audit": audit,
            "finops": finops,
        }

        score = scorer.score_maturity(context)
        assert score.overall_maturity_score >= 95.0
        assert score.certification == MaturityCertification.ENTERPRISE_OPERATIONS_MATURE
        assert score.governance_passed is True

    # ──────────────────────────────────────────────────────────────────────────
    # 13. Exporter & SHA-256 Manifest Tests (Part 3R.14)
    # ──────────────────────────────────────────────────────────────────────────

    def test_exporter_artifact_tree_and_sha256(self, temp_export_dir):
        exporter = OperationsGovernanceExporter(base_dir=temp_export_dir)
        slo = SLOManager().evaluate_slos()
        budget = SLOManager().calculate_error_budget()
        health = HealthIntelligenceEngine().assess_production_health()
        incidents = IncidentManager().get_incident_summary()
        alerts = AlertingEngine().evaluate_alert_rules()
        runbooks = RunbookEngine().validate_runbooks()
        self_healing = SelfHealingEngine().execute_self_healing_verification()
        rca = RootCauseAnalyzer().analyze_incident()
        changes = ChangeManager().audit_changes()
        audit = AuditTrailEngine().verify_audit_trail()
        ai_ops = AIOpsMonitor().monitor_ai_operations()
        finops = FinOpsMonitor().calculate_unit_economics()
        maturity = OperationalMaturityScorer().score_maturity({
            "slo": slo, "error_budget": budget, "health": health,
            "incidents": incidents, "alerts": alerts, "runbooks": runbooks,
            "self_healing": self_healing, "changes": changes, "audit": audit,
            "finops": finops,
        })

        manifest = exporter.export_all(
            slo=slo,
            error_budget=budget,
            health=health,
            incidents=incidents,
            alerts=alerts,
            runbooks=runbooks,
            self_healing=self_healing,
            rca=rca,
            changes=changes,
            audit=audit,
            ai_ops=ai_ops,
            finops=finops,
            maturity=maturity,
            export_dir=temp_export_dir,
        )

        assert manifest.governance_approved is True
        assert len(manifest.files) >= 13

        # Verify physical files exist
        p = Path(temp_export_dir)
        assert (p / "slo_report.json").exists()
        assert (p / "error_budget_report.json").exists()
        assert (p / "health_report.json").exists()
        assert (p / "incident_report.json").exists()
        assert (p / "alert_report.json").exists()
        assert (p / "runbook_report.json").exists()
        assert (p / "self_healing_report.json").exists()
        assert (p / "root_cause_analysis.json").exists()
        assert (p / "change_history.json").exists()
        assert (p / "audit_report.json").exists()
        assert (p / "ai_ops_report.json").exists()
        assert (p / "finops_report.json").exists()
        assert (p / "maturity_score.json").exists()
        assert (p / "metadata.json").exists()
        assert (p / "manifest.json").exists()

    # ──────────────────────────────────────────────────────────────────────────
    # 14. Master Runtime Orchestrator Tests
    # ──────────────────────────────────────────────────────────────────────────

    def test_runtime_governance_cycle(self, temp_export_dir):
        runtime = OperationsGovernanceRuntime()
        result = runtime.run_governance_cycle(export_dir=temp_export_dir)
        assert result["passed"] is True
        assert result["maturity"].certification == MaturityCertification.ENTERPRISE_OPERATIONS_MATURE
        assert result["manifest"].overall_score >= 95.0

    @pytest.mark.asyncio
    async def test_runtime_async_run_all(self, temp_export_dir):
        runtime = OperationsGovernanceRuntime()
        manifest = await runtime.run_all(export_dir=temp_export_dir)
        assert manifest.governance_approved is True
        assert manifest.overall_score >= 95.0

    # ──────────────────────────────────────────────────────────────────────────
    # 15. FastAPI Endpoints Tests
    # ──────────────────────────────────────────────────────────────────────────

    def test_api_health(self, app_client):
        res = app_client.get("/api/v1/operations/health")
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "healthy"

    def test_api_domains(self, app_client):
        res = app_client.get("/api/v1/operations/domains")
        assert res.status_code == 200
        data = res.json()
        assert len(data) == 10

    def test_api_run_cycle(self, app_client):
        res = app_client.post("/api/v1/operations/run")
        assert res.status_code == 200
        data = res.json()
        assert data["governance_approved"] is True
        assert data["overall_score"] >= 95.0

    def test_api_get_slo(self, app_client):
        res = app_client.get("/api/v1/operations/slo")
        assert res.status_code == 200
        data = res.json()
        assert data["all_slos_met"] is True

    def test_api_get_status(self, app_client):
        res = app_client.get("/api/v1/operations/status")
        assert res.status_code == 200
        data = res.json()
        assert data["overall_status"] == "HEALTHY"

    def test_api_get_incidents(self, app_client):
        res = app_client.get("/api/v1/operations/incidents")
        assert res.status_code == 200
        data = res.json()
        assert data["active_incidents_count"] == 0

    def test_api_get_alerts(self, app_client):
        res = app_client.get("/api/v1/operations/alerts")
        assert res.status_code == 200
        data = res.json()
        assert data["active_firing_alerts"] == 0

    def test_api_get_maturity(self, app_client):
        res = app_client.get("/api/v1/operations/maturity")
        assert res.status_code == 200
        data = res.json()
        assert data["certification"] == "Enterprise Operations Mature"

    def test_api_get_manifest(self, app_client):
        res = app_client.get("/api/v1/operations/manifest")
        assert res.status_code == 200
        data = res.json()
        assert data["project"] == "DocuTask-Agent"
