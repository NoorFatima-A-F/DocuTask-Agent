"""Master Runtime Coordinator for Phase 3H.4.2 Health Root Cause Analysis Framework."""

from typing import Dict, Any, Optional
from ..topology.dependency_graph import DependencyGraphEngine
from ..correlation.health_event_correlator import HealthEventCorrelator
from ..classifier.failure_classifier import FailureClassifier
from ..scoring.root_cause_scorer import RootCauseScorer
from ..impact.impact_analyzer import ImpactAnalyzer
from ..timeline.incident_timeline_reconstructor import IncidentTimelineReconstructor
from ..cascade.cascade_detector import CascadeDetector
from ..filters.false_positive_filter import FalsePositiveFilter
from ..memory.incident_memory import IncidentMemoryEngine
from ..scenarios.rca_scenarios_verifier import RCAScenariosVerifier
from ..scoring.rca_quality_scorer import HealthRootCauseScorer
from ..exporter.rca_evidence_exporter import RCAEvidenceExporter
from ..domain.models import HealthDiagnosisResponse


class HealthRootCauseRuntime:
    """Master orchestrator executing the 14-part health root cause analysis and diagnosis framework."""

    def __init__(self, export_dir: str = "health_root_cause_verification"):
        self.dep_graph = DependencyGraphEngine()
        self.correlator = HealthEventCorrelator()
        self.classifier = FailureClassifier()
        self.rc_scorer = RootCauseScorer()
        self.impact_analyzer = ImpactAnalyzer(dep_graph=self.dep_graph)
        self.timeline_reconstructor = IncidentTimelineReconstructor()
        self.cascade_detector = CascadeDetector()
        self.fp_filter = FalsePositiveFilter()
        self.memory_engine = IncidentMemoryEngine()
        self.scenarios_verifier = RCAScenariosVerifier()
        self.scorer = HealthRootCauseScorer()
        self.exporter = RCAEvidenceExporter(export_dir=export_dir)

    def diagnose_incident(self, incident_id: str = "INC-ACTIVE-001") -> HealthDiagnosisResponse:
        """Generates real-time full diagnosis for an operational incident."""
        rc_rep = self.rc_scorer.diagnose_root_cause(incident_id)
        imp_rep = self.impact_analyzer.analyze_impact(rc_rep.primary_root_cause.component)
        time_rep = self.timeline_reconstructor.reconstruct_timeline(incident_id)
        casc_rep = self.cascade_detector.detect_cascade(incident_id)

        sev = self.classifier.classify_severity(
            component=rc_rep.primary_root_cause.component,
            category=rc_rep.primary_root_cause.category,
        )

        return HealthDiagnosisResponse(
            state="UNHEALTHY",
            severity=sev,
            root_cause=rc_rep.primary_root_cause,
            impact=imp_rep.assessments[0] if imp_rep.assessments else None,
            timeline=time_rep,
            cascade=casc_rep,
        )

    def run_full_verification(self) -> Dict[str, Any]:
        """Executes full RCA verification pipeline across all 14 dimensions and exports manifests."""
        dep_rep = self.dep_graph.build_graph_report()
        corr_rep = self.correlator.correlate_events()
        rc_rep = self.rc_scorer.diagnose_root_cause("INC-VERIFY-POSTGRES")
        imp_rep = self.impact_analyzer.analyze_impact("postgresql")
        time_rep = self.timeline_reconstructor.reconstruct_timeline("INC-VERIFY-POSTGRES")
        casc_rep = self.cascade_detector.detect_cascade("INC-VERIFY-CASCADE")
        fp_rep = self.fp_filter.audit_false_positive_control()
        mem_rep = self.memory_engine.get_memory_report()
        scen_rep = self.scenarios_verifier.verify_scenarios()

        scorecard = self.scorer.score_rca(
            dep_rep=dep_rep,
            corr_rep=corr_rep,
            rc_rep=rc_rep,
            imp_rep=imp_rep,
            time_rep=time_rep,
            casc_rep=casc_rep,
            fp_rep=fp_rep,
            mem_rep=mem_rep,
        )

        manifests = self.exporter.export_all(
            dep_rep=dep_rep,
            corr_rep=corr_rep,
            rc_rep=rc_rep,
            imp_rep=imp_rep,
            time_rep=time_rep,
            casc_rep=casc_rep,
            fp_rep=fp_rep,
            mem_rep=mem_rep,
            scorecard=scorecard,
        )

        return {
            "dependency_report": dep_rep,
            "correlation_report": corr_rep,
            "root_cause_report": rc_rep,
            "impact_report": imp_rep,
            "timeline_report": time_rep,
            "cascade_report": casc_rep,
            "false_positive_report": fp_rep,
            "memory_report": mem_rep,
            "scenarios_report": scen_rep,
            "scorecard": scorecard,
            "exported_manifests": manifests,
        }
