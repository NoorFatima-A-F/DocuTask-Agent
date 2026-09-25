"""
Phase 3R: Master Runtime Orchestrator for Enterprise Operations Governance.
"""

from typing import Any, Dict, Optional

from ..core import (
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
from ..domain.models import (
    AIOpsReport,
    AlertReport,
    AuditTrailReport,
    ChangeManagementReport,
    ErrorBudgetReport,
    FinOpsReport,
    IncidentReport,
    OperationalMaturityScore,
    OperationsManifest,
    ProductionHealthReport,
    RootCauseAnalysisReport,
    RunbookReport,
    SelfHealingReport,
    SLODefinitionReport,
)
from ..exporter.operations_governance_exporter import OperationsGovernanceExporter


class OperationsGovernanceRuntime:
    """
    Master Runtime Orchestrator for Phase 3R:
    Coordinates SLO measurement, error budget evaluation, health intelligence,
    incident lifecycle management, alerting, runbooks, self-healing remediation,
    root cause analysis, change auditing, AIOps, FinOps, and operational maturity certification.
    """

    def __init__(
        self,
        slo_manager: Optional[SLOManager] = None,
        health_engine: Optional[HealthIntelligenceEngine] = None,
        incident_manager: Optional[IncidentManager] = None,
        alerting_engine: Optional[AlertingEngine] = None,
        runbook_engine: Optional[RunbookEngine] = None,
        self_healing_engine: Optional[SelfHealingEngine] = None,
        rca_engine: Optional[RootCauseAnalyzer] = None,
        change_manager: Optional[ChangeManager] = None,
        audit_engine: Optional[AuditTrailEngine] = None,
        ai_ops_monitor: Optional[AIOpsMonitor] = None,
        finops_monitor: Optional[FinOpsMonitor] = None,
        maturity_scorer: Optional[OperationalMaturityScorer] = None,
        exporter: Optional[OperationsGovernanceExporter] = None,
    ):
        self.slo_manager = slo_manager or SLOManager()
        self.health_engine = health_engine or HealthIntelligenceEngine()
        self.incident_manager = incident_manager or IncidentManager()
        self.alerting_engine = alerting_engine or AlertingEngine()
        self.runbook_engine = runbook_engine or RunbookEngine()
        self.self_healing_engine = self_healing_engine or SelfHealingEngine()
        self.rca_engine = rca_engine or RootCauseAnalyzer()
        self.change_manager = change_manager or ChangeManager()
        self.audit_engine = audit_engine or AuditTrailEngine()
        self.ai_ops_monitor = ai_ops_monitor or AIOpsMonitor()
        self.finops_monitor = finops_monitor or FinOpsMonitor()
        self.maturity_scorer = maturity_scorer or OperationalMaturityScorer()
        self.exporter = exporter or OperationsGovernanceExporter()

        self._latest_slo: Optional[SLODefinitionReport] = None
        self._latest_error_budget: Optional[ErrorBudgetReport] = None
        self._latest_health: Optional[ProductionHealthReport] = None
        self._latest_incidents: Optional[IncidentReport] = None
        self._latest_alerts: Optional[AlertReport] = None
        self._latest_runbooks: Optional[RunbookReport] = None
        self._latest_self_healing: Optional[SelfHealingReport] = None
        self._latest_rca: Optional[RootCauseAnalysisReport] = None
        self._latest_changes: Optional[ChangeManagementReport] = None
        self._latest_audit: Optional[AuditTrailReport] = None
        self._latest_ai_ops: Optional[AIOpsReport] = None
        self._latest_finops: Optional[FinOpsReport] = None
        self._latest_maturity: Optional[OperationalMaturityScore] = None
        self._latest_manifest: Optional[OperationsManifest] = None

    def run_governance_cycle(self, export_dir: str = "operations_verification") -> Dict[str, Any]:
        # 1. SLOs & Error Budget
        slo = self.slo_manager.evaluate_slos()
        error_budget = self.slo_manager.calculate_error_budget()
        self._latest_slo = slo
        self._latest_error_budget = error_budget

        # 2. Production Health Intelligence
        health = self.health_engine.assess_production_health()
        self._latest_health = health

        # 3. Incident Management & Alerting
        incidents = self.incident_manager.get_incident_summary()
        alerts = self.alerting_engine.evaluate_alert_rules()
        self._latest_incidents = incidents
        self._latest_alerts = alerts

        # 4. Runbooks & Self-Healing
        runbooks = self.runbook_engine.validate_runbooks()
        self_healing = self.self_healing_engine.execute_self_healing_verification()
        self._latest_runbooks = runbooks
        self._latest_self_healing = self_healing

        # 5. Root Cause Analysis
        rca = self.rca_engine.analyze_incident()
        self._latest_rca = rca

        # 6. Change Management & Audit Trail
        changes = self.change_manager.audit_changes()
        audit = self.audit_engine.verify_audit_trail()
        self._latest_changes = changes
        self._latest_audit = audit

        # 7. AIOps & FinOps
        ai_ops = self.ai_ops_monitor.monitor_ai_operations()
        finops = self.finops_monitor.calculate_unit_economics()
        self._latest_ai_ops = ai_ops
        self._latest_finops = finops

        # 8. Operational Maturity Scoring
        reports_context = {
            "slo": slo,
            "error_budget": error_budget,
            "health": health,
            "incidents": incidents,
            "alerts": alerts,
            "runbooks": runbooks,
            "self_healing": self_healing,
            "changes": changes,
            "audit": audit,
            "ai_ops": ai_ops,
            "finops": finops,
        }
        maturity = self.maturity_scorer.score_maturity(reports_context)
        self._latest_maturity = maturity

        # 9. Cryptographic Export
        manifest = self.exporter.export_all(
            slo=slo,
            error_budget=error_budget,
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
            export_dir=export_dir,
        )
        self._latest_manifest = manifest

        return {
            "slo": slo,
            "error_budget": error_budget,
            "health": health,
            "incidents": incidents,
            "alerts": alerts,
            "runbooks": runbooks,
            "self_healing": self_healing,
            "rca": rca,
            "changes": changes,
            "audit": audit,
            "ai_ops": ai_ops,
            "finops": finops,
            "maturity": maturity,
            "manifest": manifest,
            "passed": maturity.governance_passed,
        }

    def get_latest_slo(self) -> Optional[SLODefinitionReport]:
        return self._latest_slo

    def get_latest_health(self) -> Optional[ProductionHealthReport]:
        return self._latest_health

    def get_latest_incidents(self) -> Optional[IncidentReport]:
        return self._latest_incidents

    def get_latest_alerts(self) -> Optional[AlertReport]:
        return self._latest_alerts

    def get_latest_maturity(self) -> Optional[OperationalMaturityScore]:
        return self._latest_maturity

    def get_latest_manifest(self) -> Optional[OperationsManifest]:
        return self._latest_manifest

    async def run_all(self, export_dir: str = "operations_verification") -> OperationsManifest:
        res = self.run_governance_cycle(export_dir=export_dir)
        return res["manifest"]
