"""
Evidence Exporter Subsystem for Operational Resilience Framework (Part 3G.5J).
Assembles and exports all evidence manifests, metrics, dashboards, and certificates to:
resilience_verification/
"""
import json
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime, timezone

from app.platform_verification.operational_resilience.domain.models import (
    FailureExperimentResult,
    SelfHealingReport,
    IncidentAutomationReport,
    RunbookValidationReport,
    DependencyResilienceReport,
    StateConsistencyReport,
    DrillResult,
    OperationalResilienceScorecard,
)
from app.platform_verification.operational_resilience.runbooks.runbook_engine import (
    RunbookEngine,
)


class EvidenceExporter:
    """
    Exports comprehensive operational resilience evidence artifacts.
    """

    def __init__(self, base_dir: str = ".", output_dir_name: str = "resilience_verification"):
        self.base_dir = Path(base_dir)
        self.output_dir = self.base_dir / output_dir_name

    def export_all_evidence(
        self,
        experiments: List[FailureExperimentResult],
        self_healing: SelfHealingReport,
        orchestrator_report: Dict[str, Any],
        incidents: IncidentAutomationReport,
        runbooks: RunbookValidationReport,
        dependencies: DependencyResilienceReport,
        consistency: StateConsistencyReport,
        drill: DrillResult,
        scorecard: OperationalResilienceScorecard,
    ) -> Dict[str, Any]:
        """
        Builds all folders and files inside resilience_verification/
        """
        # 1. Create subdirectories
        recovery_dir = self.output_dir / "recovery_reports"
        experiments_dir = self.output_dir / "failure_experiments"
        incidents_dir = self.output_dir / "incident_reports"
        runbooks_dir = self.output_dir / "runbook_validation"
        metrics_dir = self.output_dir / "metrics"
        dashboards_dir = self.output_dir / "dashboards"

        for d in [recovery_dir, experiments_dir, incidents_dir, runbooks_dir, metrics_dir, dashboards_dir]:
            d.mkdir(parents=True, exist_ok=True)

        files_written = []
        now_str = datetime.now(timezone.utc).isoformat()

        # 2. Recovery Reports
        rec_file = recovery_dir / "recovery_automation_report.json"
        rec_file.write_text(json.dumps(orchestrator_report, indent=2), encoding="utf-8")
        files_written.append(str(rec_file))

        drill_file = recovery_dir / "drill_report.json"
        drill_data = {
            "experiment": drill.injected_failure,
            "detected": drill.detected,
            "recovered": drill.recovered,
            "rto": drill.rto_seconds,
            "data_loss": drill.data_loss_bytes,
            "score": drill.drill_score,
            "drill_id": drill.drill_id,
            "drill_name": drill.drill_name,
            "details": drill.details,
        }
        drill_file.write_text(json.dumps(drill_data, indent=2), encoding="utf-8")
        files_written.append(str(drill_file))

        healing_file = recovery_dir / "self_healing_report.json"
        healing_data = {
            "container_healing_passed": self_healing.container_healing_passed,
            "container_restart_time_sec": self_healing.container_restart_time_sec,
            "queue_healing_passed": self_healing.queue_healing_passed,
            "queue_messages_preserved_pct": self_healing.queue_messages_preserved_pct,
            "db_connection_recovery_passed": self_healing.db_connection_recovery_passed,
            "db_reconnect_time_sec": self_healing.db_reconnect_time_sec,
            "mttd_seconds": self_healing.mttd_seconds,
            "mttr_seconds": self_healing.mttr_seconds,
            "recovery_success_rate_pct": self_healing.recovery_success_rate_pct,
            "passed": self_healing.passed,
            "details": self_healing.details,
        }
        healing_file.write_text(json.dumps(healing_data, indent=2), encoding="utf-8")
        files_written.append(str(healing_file))

        # 3. Failure Experiments
        exp_file = experiments_dir / "experiments_summary.json"
        exp_data = {
            "total_experiments": len(experiments),
            "passed_count": sum(1 for e in experiments if e.status == "PASS"),
            "experiments": [
                {
                    "experiment_id": e.experiment_id,
                    "category": e.category.value,
                    "target_component": e.target_component,
                    "failure_description": e.failure_description,
                    "detection_time_seconds": e.detection_time_seconds,
                    "recovery_action": e.recovery_action,
                    "recovery_duration_seconds": e.recovery_duration_seconds,
                    "data_loss": e.data_loss,
                    "status": e.status,
                }
                for e in experiments
            ],
        }
        exp_file.write_text(json.dumps(exp_data, indent=2), encoding="utf-8")
        files_written.append(str(exp_file))

        # 4. Incident Reports
        inc_file = incidents_dir / "incident_automation_report.json"
        inc_data = {
            "total_incidents_simulated": incidents.total_incidents_simulated,
            "alerts_fired_count": incidents.alerts_fired_count,
            "tickets_auto_created": incidents.tickets_auto_created,
            "paged_oncall_verified": incidents.paged_oncall_verified,
            "average_mttd_seconds": incidents.average_mttd_seconds,
            "average_mttr_seconds": incidents.average_mttr_seconds,
            "passed": incidents.passed,
            "details": incidents.details,
            "incidents": [
                {
                    "incident_id": t.incident_id,
                    "severity": t.severity.value,
                    "title": t.title,
                    "component": t.component,
                    "assigned_owner": t.assigned_owner,
                    "mttd_seconds": t.mttd_seconds,
                    "mttr_seconds": t.mttr_seconds,
                    "status": t.status,
                }
                for t in incidents.incidents
            ],
        }
        inc_file.write_text(json.dumps(inc_data, indent=2), encoding="utf-8")
        files_written.append(str(inc_file))

        # 5. Runbook Validation & Markdown Files
        runbook_engine = RunbookEngine()
        runbooks_md = runbook_engine.generate_runbook_markdown()
        # Export runbooks to root runbooks/ directory as well as inside evidence
        root_rb_dir = self.base_dir / "runbooks"
        root_rb_dir.mkdir(parents=True, exist_ok=True)
        for rb_name, rb_text in runbooks_md.items():
            (root_rb_dir / rb_name).write_text(rb_text, encoding="utf-8")
            (runbooks_dir / rb_name).write_text(rb_text, encoding="utf-8")
            files_written.append(str(root_rb_dir / rb_name))

        rb_summary_file = runbooks_dir / "runbook_audit_summary.json"
        rb_summary_data = {
            "total_runbooks": runbooks.total_runbooks,
            "automated_runbooks_count": runbooks.automated_runbooks_count,
            "passed": runbooks.passed,
            "details": runbooks.details,
            "runbooks": [
                {
                    "id": r.runbook_id,
                    "title": r.title,
                    "file_path": r.file_path,
                    "automated_cli_supported": r.automated_cli_supported,
                }
                for r in runbooks.runbooks
            ],
        }
        rb_summary_file.write_text(json.dumps(rb_summary_data, indent=2), encoding="utf-8")
        files_written.append(str(rb_summary_file))

        # 6. Metrics & Prometheus Exposition
        metrics_json_file = metrics_dir / "resilience_metrics.json"
        metrics_data = {
            "mttd_average_seconds": self_healing.mttd_seconds,
            "mttr_average_seconds": self_healing.mttr_seconds,
            "recovery_success_rate_pct": self_healing.recovery_success_rate_pct,
            "queue_preservation_pct": dependencies.queue_preservation_pct,
            "scorecard": {
                "overall_resilience_score": scorecard.overall_resilience_score,
                "tier": scorecard.resilience_tier.value,
                "detection_score": scorecard.detection_score,
                "recovery_automation_score": scorecard.recovery_automation_score,
                "data_integrity_score": scorecard.data_integrity_score,
                "failure_containment_score": scorecard.failure_containment_score,
                "operational_visibility_score": scorecard.operational_visibility_score,
                "documentation_score": scorecard.documentation_score,
            },
        }
        metrics_json_file.write_text(json.dumps(metrics_data, indent=2), encoding="utf-8")
        files_written.append(str(metrics_json_file))

        prom_lines = [
            "# HELP docutask_resilience_mttd_seconds Mean Time To Detect in seconds",
            "# TYPE docutask_resilience_mttd_seconds gauge",
            f"docutask_resilience_mttd_seconds {self_healing.mttd_seconds}",
            "# HELP docutask_resilience_mttr_seconds Mean Time To Recovery in seconds",
            "# TYPE docutask_resilience_mttr_seconds gauge",
            f"docutask_resilience_mttr_seconds {self_healing.mttr_seconds}",
            "# HELP docutask_resilience_score Overall operational resilience composite score",
            "# TYPE docutask_resilience_score gauge",
            f"docutask_resilience_score {scorecard.overall_resilience_score}",
            "# HELP docutask_resilience_success_rate_pct Percentage of automated recovery successes",
            "# TYPE docutask_resilience_success_rate_pct gauge",
            f"docutask_resilience_success_rate_pct {self_healing.recovery_success_rate_pct}",
        ]
        prom_file = metrics_dir / "resilience_metrics.prom"
        prom_file.write_text("\n".join(prom_lines) + "\n", encoding="utf-8")
        files_written.append(str(prom_file))

        # 7. Grafana Dashboard JSON
        dash_file = dashboards_dir / "grafana_resilience_dashboard.json"
        dash_data = {
            "title": "DocuTask Agent - Operational Resilience & Recovery Dashboard",
            "schemaVersion": 38,
            "panels": [
                {"title": "Resilience Score", "type": "stat", "targets": [{"expr": "docutask_resilience_score"}]},
                {"title": "MTTD (Seconds)", "type": "gauge", "targets": [{"expr": "docutask_resilience_mttd_seconds"}]},
                {"title": "MTTR (Seconds)", "type": "gauge", "targets": [{"expr": "docutask_resilience_mttr_seconds"}]},
                {"title": "Recovery Success Rate (%)", "type": "stat", "targets": [{"expr": "docutask_resilience_success_rate_pct"}]},
            ],
        }
        dash_file.write_text(json.dumps(dash_data, indent=2), encoding="utf-8")
        files_written.append(str(dash_file))

        # 8. Certification JSON
        cert_file = self.output_dir / "certification.json"
        cert_data = {
            "certification_id": "CERT-3G5-OPERATIONAL-RESILIENCE-001",
            "platform": "DocuTask Agent Enterprise Platform",
            "phase": "3G.5",
            "overall_resilience_score": scorecard.overall_resilience_score,
            "resilience_tier": scorecard.resilience_tier.value,
            "certification_verdict": scorecard.certification_verdict,
            "ci_cd_deployment_approved": scorecard.ci_cd_deployment_approved,
            "issued_at_utc": now_str,
            "valid_until_utc": "2027-09-15T12:00:00Z",
            "evaluated_capabilities": [
                "Automated Recovery Orchestration (Part 3G.5A)",
                "Self-Healing Containers, Queues & DB Connections (Part 3G.5B)",
                "Failure Injection in 6 Domains (Part 3G.5C)",
                "Incident Lifecycle & Auto-Ticketing (Part 3G.5D)",
                "Executable Runbooks with Automated CLI (Part 3G.5E)",
                "Dependency Graceful Degradation & AI Fallback (Part 3G.5F)",
                "State Invariants & Idempotency Verification (Part 3G.5G)",
                "Automated Continuous DR Drills (Part 3G.5H)",
            ],
        }
        cert_file.write_text(json.dumps(cert_data, indent=2), encoding="utf-8")
        files_written.append(str(cert_file))

        # 9. Metadata JSON (matches Part 3G.5J)
        meta_file = self.output_dir / "metadata.json"
        meta_data = {
            "system": "DocuTask Agent",
            "phase": "3G.5",
            "timestamp": now_str,
            "commit": "git-head-3g5-resilience-certified",
            "environment": "enterprise-production-resilience",
        }
        meta_file.write_text(json.dumps(meta_data, indent=2), encoding="utf-8")
        files_written.append(str(meta_file))

        return {
            "total_files_exported": len(files_written),
            "output_directory": str(self.output_dir),
            "files": files_written,
        }
