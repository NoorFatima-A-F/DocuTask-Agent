"""Alert Rule Verification Runtime.

Coordinates full end-to-end alert intelligence and rule validation across all 14 sub-phases.
"""

from typing import Dict, Tuple
from ..domain.models import (
    AlertQualityScorecard,
)
from ..verifiers.alert_architecture_verifier import AlertArchitectureVerifier
from ..verifiers.alert_taxonomy_verifier import AlertTaxonomyVerifier
from ..verifiers.critical_alert_verifier import CriticalAlertVerifier
from ..verifiers.warning_alert_verifier import WarningAlertVerifier
from ..verifiers.alert_condition_verifier import AlertConditionVerifier
from ..verifiers.alert_severity_verifier import AlertSeverityVerifier
from ..verifiers.alert_message_verifier import AlertMessageVerifier
from ..verifiers.alert_routing_verifier import AlertRoutingVerifier
from ..verifiers.alert_fatigue_verifier import AlertFatigueVerifier
from ..verifiers.failure_injection_verifier import FailureInjectionVerifier
from ..verifiers.alert_performance_verifier import AlertPerformanceVerifier
from ..scoring.alert_quality_scorer import AlertQualityScorer
from ..exporter.alert_evidence_exporter import AlertEvidenceExporter


class AlertRuleVerificationRuntime:
    """Runtime coordinator executing all alert verification sub-engines."""

    def __init__(self, output_dir: str = "alert_verification"):
        self.arch_verifier = AlertArchitectureVerifier()
        self.tax_verifier = AlertTaxonomyVerifier()
        self.crit_verifier = CriticalAlertVerifier()
        self.warn_verifier = WarningAlertVerifier()
        self.cond_verifier = AlertConditionVerifier()
        self.sev_verifier = AlertSeverityVerifier()
        self.msg_verifier = AlertMessageVerifier()
        self.route_verifier = AlertRoutingVerifier()
        self.fatigue_verifier = AlertFatigueVerifier()
        self.fail_verifier = FailureInjectionVerifier()
        self.perf_verifier = AlertPerformanceVerifier()
        self.scorer = AlertQualityScorer()
        self.exporter = AlertEvidenceExporter(output_dir=output_dir)

    def execute_full_verification(self) -> Tuple[AlertQualityScorecard, Dict[str, str]]:
        # 1. Architecture
        arch_rep = self.arch_verifier.verify_architecture()

        # 2. Taxonomy
        tax_rep = self.tax_verifier.verify_taxonomy()

        # 3. Critical Alerts
        crit_rep = self.crit_verifier.verify_critical_alerts()

        # 4. Warning Alerts
        warn_rep = self.warn_verifier.verify_warning_alerts()

        # 5. Conditions Simulation
        cond_rep = self.cond_verifier.verify_conditions()

        # 6. Severity Verification
        sev_rep = self.sev_verifier.verify_severity()

        # 7. Message Quality
        msg_rep = self.msg_verifier.verify_messages()

        # 8. Routing Verification
        route_rep = self.route_verifier.verify_routing()

        # 9. Fatigue & Noise Prevention
        fatigue_rep = self.fatigue_verifier.verify_fatigue_prevention()

        # 10. Failure Injection
        fail_rep = self.fail_verifier.verify_failure_injection()

        # 11. Performance Metrics
        perf_rep = self.perf_verifier.verify_performance()

        # 12. Scoring
        scorecard = self.scorer.score_alerts(
            arch_rep=arch_rep,
            tax_rep=tax_rep,
            crit_rep=crit_rep,
            warn_rep=warn_rep,
            cond_rep=cond_rep,
            sev_rep=sev_rep,
            msg_rep=msg_rep,
            route_rep=route_rep,
            fatigue_rep=fatigue_rep,
            fail_rep=fail_rep,
            perf_rep=perf_rep,
        )

        # 13. Evidence Export
        exported_manifests = self.exporter.export_all(
            arch_rep=arch_rep,
            tax_rep=tax_rep,
            crit_rep=crit_rep,
            warn_rep=warn_rep,
            cond_rep=cond_rep,
            sev_rep=sev_rep,
            msg_rep=msg_rep,
            route_rep=route_rep,
            fatigue_rep=fatigue_rep,
            fail_rep=fail_rep,
            perf_rep=perf_rep,
            scorecard=scorecard,
        )

        return scorecard, exported_manifests
