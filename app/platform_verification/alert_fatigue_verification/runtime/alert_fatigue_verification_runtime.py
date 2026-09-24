"""Alert Fatigue Verification Runtime.

Coordinates full end-to-end alert fatigue reduction, signal optimization, and noise suppression verification.
"""

from typing import Dict, Tuple
from ..domain.models import (
    AlertFatigueScorecard,
)
from ..verifiers.fatigue_architecture_verifier import FatigueArchitectureVerifier
from ..verifiers.alert_deduplication_verifier import AlertDeduplicationVerifier
from ..verifiers.alert_correlation_verifier import AlertCorrelationVerifier
from ..verifiers.severity_optimization_verifier import SeverityOptimizationVerifier
from ..verifiers.alert_routing_verifier import AlertRoutingVerifier
from ..verifiers.alert_suppression_verifier import AlertSuppressionVerifier
from ..verifiers.alert_grouping_verifier import AlertGroupingVerifier
from ..verifiers.noise_metrics_verifier import NoiseMetricsVerifier
from ..verifiers.alert_storm_simulator import AlertStormSimulator
from ..verifiers.machine_prioritization_verifier import MachinePrioritizationVerifier
from ..scoring.alert_fatigue_scorer import AlertFatigueScorer
from ..exporter.alert_fatigue_evidence_exporter import AlertFatigueEvidenceExporter


class AlertFatigueVerificationRuntime:
    """Runtime coordinator executing all alert fatigue reduction and signal optimization engines."""

    def __init__(self, output_dir: str = "alert_fatigue_verification"):
        self.arch_verifier = FatigueArchitectureVerifier()
        self.dedup_verifier = AlertDeduplicationVerifier()
        self.corr_verifier = AlertCorrelationVerifier()
        self.sev_verifier = SeverityOptimizationVerifier()
        self.route_verifier = AlertRoutingVerifier()
        self.supp_verifier = AlertSuppressionVerifier()
        self.group_verifier = AlertGroupingVerifier()
        self.noise_verifier = NoiseMetricsVerifier()
        self.storm_simulator = AlertStormSimulator()
        self.ml_verifier = MachinePrioritizationVerifier()
        self.scorer = AlertFatigueScorer()
        self.exporter = AlertFatigueEvidenceExporter(output_dir=output_dir)

    def execute_full_verification(self) -> Tuple[AlertFatigueScorecard, Dict[str, str]]:
        # 1. Architecture
        arch_rep = self.arch_verifier.verify_architecture()

        # 2. Deduplication
        dedup_rep = self.dedup_verifier.verify_deduplication()

        # 3. Correlation
        corr_rep = self.corr_verifier.verify_correlation()

        # 4. Severity
        sev_rep = self.sev_verifier.verify_severity_optimization()

        # 5. Routing
        route_rep = self.route_verifier.verify_routing()

        # 6. Suppression
        supp_rep = self.supp_verifier.verify_suppression()

        # 7. Grouping
        group_rep = self.group_verifier.verify_grouping()

        # 8. Noise Metrics
        noise_rep = self.noise_verifier.verify_noise_metrics()

        # 9. Alert Storm Simulation
        storm_rep = self.storm_simulator.simulate_alert_storm()

        # 10. Machine Prioritization
        ml_rep = self.ml_verifier.verify_machine_prioritization()

        # 11. Scoring
        scorecard = self.scorer.score_fatigue(
            arch_rep=arch_rep,
            dedup_rep=dedup_rep,
            corr_rep=corr_rep,
            sev_rep=sev_rep,
            route_rep=route_rep,
            supp_rep=supp_rep,
            group_rep=group_rep,
            noise_rep=noise_rep,
            storm_rep=storm_rep,
            ml_rep=ml_rep,
        )

        # 12. Evidence Export
        exported_manifests = self.exporter.export_all(
            arch_rep=arch_rep,
            dedup_rep=dedup_rep,
            corr_rep=corr_rep,
            sev_rep=sev_rep,
            route_rep=route_rep,
            supp_rep=supp_rep,
            group_rep=group_rep,
            noise_rep=noise_rep,
            storm_rep=storm_rep,
            ml_rep=ml_rep,
            scorecard=scorecard,
        )

        return scorecard, exported_manifests
