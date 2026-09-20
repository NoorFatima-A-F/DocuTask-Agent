"""Master Runtime Coordinator for Phase 3H.4 Enterprise Health Monitoring & Alerting Framework."""

from typing import Dict, Any
from ..signals.health_signal_architecture_verifier import HealthSignalArchitectureVerifier
from ..metrics.operational_metrics_verifier import OperationalMetricsVerifier
from ..prometheus.prometheus_scraping_verifier import PrometheusScrapingVerifier
from ..grafana.grafana_dashboard_verifier import GrafanaDashboardVerifier
from ..alerting.alert_rule_verifier import AlertRuleVerifier
from ..accuracy.alert_accuracy_verifier import AlertAccuracyVerifier
from ..incident.incident_signal_verifier import IncidentSignalVerifier
from ..fatigue.alert_fatigue_prevention_verifier import AlertFatiguePreventionVerifier
from ..simulation.monitoring_failure_simulator import MonitoringFailureSimulator
from ..security.observability_security_auditor import ObservabilitySecurityAuditor
from ..scoring.health_monitoring_scorer import HealthMonitoringScorer
from ..exporter.health_monitoring_evidence_exporter import HealthMonitoringEvidenceExporter


class HealthMonitoringAlertingRuntime:
    """Master orchestrator executing the 12-part health monitoring, alerting, and incident signal framework."""

    def __init__(self, export_dir: str = "health_monitoring_verification"):
        self.signal_verifier = HealthSignalArchitectureVerifier()
        self.metrics_verifier = OperationalMetricsVerifier()
        self.prometheus_verifier = PrometheusScrapingVerifier()
        self.dashboard_verifier = GrafanaDashboardVerifier()
        self.alert_verifier = AlertRuleVerifier()
        self.accuracy_verifier = AlertAccuracyVerifier()
        self.incident_verifier = IncidentSignalVerifier()
        self.fatigue_verifier = AlertFatiguePreventionVerifier()
        self.simulation_verifier = MonitoringFailureSimulator()
        self.security_auditor = ObservabilitySecurityAuditor()
        self.scorer = HealthMonitoringScorer()
        self.exporter = HealthMonitoringEvidenceExporter(export_dir=export_dir)

    def run_full_verification(self) -> Dict[str, Any]:
        """Runs the complete end-to-end monitoring, alerting, and incident verification pipeline."""
        # 1. Signals & Metrics
        signal_rep = self.signal_verifier.verify_signal_architecture()
        metrics_rep = self.metrics_verifier.verify_metrics_collection()

        # 2. Prometheus & Dashboards
        prom_rep = self.prometheus_verifier.verify_prometheus_scraping()
        dash_rep = self.dashboard_verifier.verify_dashboards()

        # 3. Alerting, Accuracy, Incidents & Fatigue
        alert_rep = self.alert_verifier.verify_alert_rules()
        acc_rep = self.accuracy_verifier.verify_alert_accuracy()
        inc_rep = self.incident_verifier.verify_incident_signals()
        fatigue_rep = self.fatigue_verifier.verify_fatigue_prevention()

        # 4. Failure Chaos & Security
        sim_rep = self.simulation_verifier.run_monitoring_failure_tests()
        sec_rep = self.security_auditor.audit_security()

        # 5. Quality Scorecard
        scorecard = self.scorer.score_observability(
            signal_rep=signal_rep,
            metrics_rep=metrics_rep,
            prom_rep=prom_rep,
            dash_rep=dash_rep,
            alert_rep=alert_rep,
            acc_rep=acc_rep,
            inc_rep=inc_rep,
            fatigue_rep=fatigue_rep,
            sim_rep=sim_rep,
            sec_rep=sec_rep,
        )

        # 6. Export 10 Manifests
        manifests = self.exporter.export_all(
            signal_rep=signal_rep,
            metrics_rep=metrics_rep,
            prom_rep=prom_rep,
            dash_rep=dash_rep,
            alert_rep=alert_rep,
            acc_rep=acc_rep,
            inc_rep=inc_rep,
            fatigue_rep=fatigue_rep,
            sim_rep=sim_rep,
            sec_rep=sec_rep,
            scorecard=scorecard,
        )

        return {
            "signal_report": signal_rep,
            "metrics_report": metrics_rep,
            "prometheus_report": prom_rep,
            "dashboard_report": dash_rep,
            "alert_report": alert_rep,
            "accuracy_report": acc_rep,
            "incident_report": inc_rep,
            "fatigue_report": fatigue_rep,
            "failure_test_report": sim_rep,
            "security_report": sec_rep,
            "scorecard": scorecard,
            "exported_manifests": manifests,
        }
