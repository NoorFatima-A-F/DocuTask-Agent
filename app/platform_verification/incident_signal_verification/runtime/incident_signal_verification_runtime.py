"""Incident Signal Verification Runtime.

Coordinates full end-to-end incident signal processing, context enrichment, and remediation verification.
"""

from typing import Dict, Any, Tuple
from ..domain.models import (
    IncidentArchitectureReport,
    AlertMappingReport,
    PayloadQualityReport,
    DependencyAnalysisReport,
    ImpactReport,
    PriorityReport,
    IncidentCorrelationReport,
    TimelineReport,
    RunbookReport,
    IncidentSecurityReport,
    IncidentAutomationReport,
    IncidentQualityScorecard,
)
from ..verifiers.incident_architecture_verifier import IncidentArchitectureVerifier
from ..verifiers.alert_incident_mapping_verifier import AlertIncidentMappingVerifier
from ..verifiers.incident_payload_verifier import IncidentPayloadVerifier
from ..verifiers.dependency_blast_radius_verifier import DependencyBlastRadiusVerifier
from ..verifiers.impact_assessment_verifier import ImpactAssessmentVerifier
from ..verifiers.priority_calculator_verifier import PriorityCalculatorVerifier
from ..verifiers.incident_correlation_verifier import IncidentCorrelationVerifier
from ..verifiers.incident_timeline_verifier import IncidentTimelineVerifier
from ..verifiers.runbook_integration_verifier import RunbookIntegrationVerifier
from ..verifiers.incident_security_verifier import IncidentSecurityVerifier
from ..verifiers.incident_automation_verifier import IncidentAutomationVerifier
from ..scoring.incident_quality_scorer import IncidentQualityScorer
from ..exporter.incident_evidence_exporter import IncidentEvidenceExporter


class IncidentSignalVerificationRuntime:
    """Runtime coordinator executing all incident signal validation sub-engines."""

    def __init__(self, output_dir: str = "incident_signal_verification"):
        self.arch_verifier = IncidentArchitectureVerifier()
        self.map_verifier = AlertIncidentMappingVerifier()
        self.payload_verifier = IncidentPayloadVerifier()
        self.dep_verifier = DependencyBlastRadiusVerifier()
        self.impact_verifier = ImpactAssessmentVerifier()
        self.prio_verifier = PriorityCalculatorVerifier()
        self.corr_verifier = IncidentCorrelationVerifier()
        self.timeline_verifier = IncidentTimelineVerifier()
        self.runbook_verifier = RunbookIntegrationVerifier()
        self.sec_verifier = IncidentSecurityVerifier()
        self.auto_verifier = IncidentAutomationVerifier()
        self.scorer = IncidentQualityScorer()
        self.exporter = IncidentEvidenceExporter(output_dir=output_dir)

    def execute_full_verification(self) -> Tuple[IncidentQualityScorecard, Dict[str, str]]:
        # 1. Architecture
        arch_rep = self.arch_verifier.verify_architecture()

        # 2. Alert Mapping
        map_rep = self.map_verifier.verify_alert_mapping()

        # 3. Payload Quality
        payload_rep = self.payload_verifier.verify_payload_quality()

        # 4. Dependency Blast Radius
        dep_rep = self.dep_verifier.verify_dependency_analysis()

        # 5. Impact Assessment
        impact_rep = self.impact_verifier.verify_impact_assessment()

        # 6. Priority Calculation
        prio_rep = self.prio_verifier.verify_priority_calculation()

        # 7. Correlation
        corr_rep = self.corr_verifier.verify_correlation()

        # 8. Timeline
        time_rep = self.timeline_verifier.verify_timeline()

        # 9. Runbook Integration
        runbook_rep = self.runbook_verifier.verify_runbooks()

        # 10. Security Audit
        sec_rep = self.sec_verifier.verify_security()

        # 11. Response Automation
        auto_rep = self.auto_verifier.verify_automation()

        # 12. Quality Scoring
        scorecard = self.scorer.score_incidents(
            arch_rep=arch_rep,
            map_rep=map_rep,
            payload_rep=payload_rep,
            dep_rep=dep_rep,
            impact_rep=impact_rep,
            prio_rep=prio_rep,
            corr_rep=corr_rep,
            time_rep=time_rep,
            runbook_rep=runbook_rep,
            sec_rep=sec_rep,
            auto_rep=auto_rep,
        )

        # 13. Evidence Export
        exported_manifests = self.exporter.export_all(
            arch_rep=arch_rep,
            map_rep=map_rep,
            payload_rep=payload_rep,
            dep_rep=dep_rep,
            impact_rep=impact_rep,
            prio_rep=prio_rep,
            corr_rep=corr_rep,
            time_rep=time_rep,
            runbook_rep=runbook_rep,
            sec_rep=sec_rep,
            auto_rep=auto_rep,
            scorecard=scorecard,
        )

        return scorecard, exported_manifests
