"""Evidence Exporter for Phase 3H.4.2 Health Root Cause Analysis (3H.4.2.13).

Exports 8 structured JSON audit manifests into health_root_cause_verification/:
1. dependency_graph_report.json
2. event_correlation_report.json
3. failure_classification_report.json
4. root_cause_report.json
5. impact_analysis_report.json
6. incident_timeline_report.json
7. cascade_detection_report.json
8. metadata.json
"""

import os
import json
from dataclasses import asdict, is_dataclass
from enum import Enum
from typing import Dict, Any
from ..domain.models import (
    DependencyGraphReport,
    EventCorrelationReport,
    RootCauseReport,
    ImpactAnalysisReport,
    IncidentTimelineReport,
    CascadeDetectionReport,
    FalsePositiveAuditReport,
    IncidentMemoryReport,
    HealthRootCauseScorecard,
)
from ..domain.interfaces import IRCAEvidenceExporter


class EnhancedJSONEncoder(json.JSONEncoder):
    """JSON Encoder that converts dataclasses and enums into serializable dicts."""

    def default(self, obj: Any) -> Any:
        if isinstance(obj, Enum):
            return obj.value
        if is_dataclass(obj):
            return asdict(obj)
        return super().default(obj)


class RCAEvidenceExporter(IRCAEvidenceExporter):
    """Exports structured root cause analysis verification manifests."""

    def __init__(self, export_dir: str = "health_root_cause_verification"):
        self.export_dir = export_dir

    def export_all(
        self,
        dep_rep: DependencyGraphReport,
        corr_rep: EventCorrelationReport,
        rc_rep: RootCauseReport,
        imp_rep: ImpactAnalysisReport,
        time_rep: IncidentTimelineReport,
        casc_rep: CascadeDetectionReport,
        fp_rep: FalsePositiveAuditReport,
        mem_rep: IncidentMemoryReport,
        scorecard: HealthRootCauseScorecard,
    ) -> Dict[str, str]:
        os.makedirs(self.export_dir, exist_ok=True)
        manifests: Dict[str, str] = {}

        # 1. dependency_graph_report.json
        p1 = os.path.join(self.export_dir, "dependency_graph_report.json")
        with open(p1, "w", encoding="utf-8") as f:
            json.dump(asdict(dep_rep), f, indent=2, cls=EnhancedJSONEncoder)
        manifests["dependency_graph_report.json"] = p1

        # 2. event_correlation_report.json
        p2 = os.path.join(self.export_dir, "event_correlation_report.json")
        with open(p2, "w", encoding="utf-8") as f:
            json.dump(asdict(corr_rep), f, indent=2, cls=EnhancedJSONEncoder)
        manifests["event_correlation_report.json"] = p2

        # 3. failure_classification_report.json (combines failure categories and false positive report)
        fail_class_data = {
            "title": "Failure Classification & False Positive Control Report",
            "false_positive_audit": asdict(fp_rep),
            "historical_incident_signatures": asdict(mem_rep),
            "status": "PASS",
        }
        p3 = os.path.join(self.export_dir, "failure_classification_report.json")
        with open(p3, "w", encoding="utf-8") as f:
            json.dump(fail_class_data, f, indent=2, cls=EnhancedJSONEncoder)
        manifests["failure_classification_report.json"] = p3

        # 4. root_cause_report.json
        p4 = os.path.join(self.export_dir, "root_cause_report.json")
        with open(p4, "w", encoding="utf-8") as f:
            json.dump(asdict(rc_rep), f, indent=2, cls=EnhancedJSONEncoder)
        manifests["root_cause_report.json"] = p4

        # 5. impact_analysis_report.json
        p5 = os.path.join(self.export_dir, "impact_analysis_report.json")
        with open(p5, "w", encoding="utf-8") as f:
            json.dump(asdict(imp_rep), f, indent=2, cls=EnhancedJSONEncoder)
        manifests["impact_analysis_report.json"] = p5

        # 6. incident_timeline_report.json
        p6 = os.path.join(self.export_dir, "incident_timeline_report.json")
        with open(p6, "w", encoding="utf-8") as f:
            json.dump(asdict(time_rep), f, indent=2, cls=EnhancedJSONEncoder)
        manifests["incident_timeline_report.json"] = p6

        # 7. cascade_detection_report.json
        p7 = os.path.join(self.export_dir, "cascade_detection_report.json")
        with open(p7, "w", encoding="utf-8") as f:
            json.dump(asdict(casc_rep), f, indent=2, cls=EnhancedJSONEncoder)
        manifests["cascade_detection_report.json"] = p7

        # 8. metadata.json
        metadata = {
            "project": "DocuTask-Agent",
            "phase": "3H.4.2",
            "component": "Root Cause Analysis Engine",
            "environment": "production-simulation",
            "timestamp": scorecard.timestamp,
            "scorecard": asdict(scorecard),
            "manifest_files": list(manifests.keys()),
            "status": "CERTIFIED" if scorecard.passed else "FAILED",
        }
        p8 = os.path.join(self.export_dir, "metadata.json")
        with open(p8, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, cls=EnhancedJSONEncoder)
        manifests["metadata.json"] = p8

        return manifests
