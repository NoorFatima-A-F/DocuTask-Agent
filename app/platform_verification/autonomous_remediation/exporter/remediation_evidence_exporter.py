"""Evidence Exporter for Phase 3H.4.3 Autonomous Remediation (3H.4.3.13).

Exports structured JSON audit manifests to health_remediation_verification/:
1. remediation_policy_report.json
2. action_execution_report.json
3. recovery_validation_report.json
4. rollback_report.json
5. self_healing_test_report.json
6. security_report.json
7. certification_report.json
8. metadata.json
"""

import os
import json
from dataclasses import asdict, is_dataclass
from enum import Enum
from typing import Dict, Any
from ..domain.models import (
    RemediationPolicyReport,
    ActionExecutionReport,
    RecoveryValidationReport,
    RollbackReport,
    SelfHealingTestReport,
    RemediationMetricsReport,
    RemediationSecurityReport,
    AutonomousRemediationScorecard,
)
from ..domain.interfaces import IRemediationEvidenceExporter


class EnhancedJSONEncoder(json.JSONEncoder):
    """JSON Encoder that converts dataclasses and enums into serializable dicts."""

    def default(self, obj: Any) -> Any:
        if isinstance(obj, Enum):
            return obj.value
        if is_dataclass(obj):
            return asdict(obj)
        return super().default(obj)


class RemediationEvidenceExporter(IRemediationEvidenceExporter):
    """Exports structured self-healing audit evidence manifests."""

    def __init__(self, export_dir: str = "health_remediation_verification"):
        self.export_dir = export_dir

    def export_all(
        self,
        policy_rep: RemediationPolicyReport,
        exec_rep: ActionExecutionReport,
        val_rep: RecoveryValidationReport,
        roll_rep: RollbackReport,
        scen_rep: SelfHealingTestReport,
        metrics_rep: RemediationMetricsReport,
        sec_rep: RemediationSecurityReport,
        scorecard: AutonomousRemediationScorecard,
    ) -> Dict[str, str]:
        os.makedirs(self.export_dir, exist_ok=True)
        manifests: Dict[str, str] = {}

        # 1. remediation_policy_report.json
        p1 = os.path.join(self.export_dir, "remediation_policy_report.json")
        with open(p1, "w", encoding="utf-8") as f:
            json.dump(asdict(policy_rep), f, indent=2, cls=EnhancedJSONEncoder)
        manifests["remediation_policy_report.json"] = p1

        # 2. action_execution_report.json
        p2 = os.path.join(self.export_dir, "action_execution_report.json")
        with open(p2, "w", encoding="utf-8") as f:
            json.dump(asdict(exec_rep), f, indent=2, cls=EnhancedJSONEncoder)
        manifests["action_execution_report.json"] = p2

        # 3. recovery_validation_report.json
        p3 = os.path.join(self.export_dir, "recovery_validation_report.json")
        with open(p3, "w", encoding="utf-8") as f:
            json.dump(asdict(val_rep), f, indent=2, cls=EnhancedJSONEncoder)
        manifests["recovery_validation_report.json"] = p3

        # 4. rollback_report.json
        p4 = os.path.join(self.export_dir, "rollback_report.json")
        with open(p4, "w", encoding="utf-8") as f:
            json.dump(asdict(roll_rep), f, indent=2, cls=EnhancedJSONEncoder)
        manifests["rollback_report.json"] = p4

        # 5. self_healing_test_report.json
        p5 = os.path.join(self.export_dir, "self_healing_test_report.json")
        with open(p5, "w", encoding="utf-8") as f:
            json.dump(asdict(scen_rep), f, indent=2, cls=EnhancedJSONEncoder)
        manifests["self_healing_test_report.json"] = p5

        # 6. security_report.json
        p6 = os.path.join(self.export_dir, "security_report.json")
        with open(p6, "w", encoding="utf-8") as f:
            json.dump(asdict(sec_rep), f, indent=2, cls=EnhancedJSONEncoder)
        manifests["security_report.json"] = p6

        # 7. certification_report.json
        p7 = os.path.join(self.export_dir, "certification_report.json")
        with open(p7, "w", encoding="utf-8") as f:
            json.dump(asdict(scorecard), f, indent=2, cls=EnhancedJSONEncoder)
        manifests["certification_report.json"] = p7

        # 8. metadata.json
        metadata = {
            "project": "DocuTask-Agent",
            "phase": "3H.4.3",
            "component": "Autonomous Health Remediation Engine",
            "environment": "production-simulation",
            "timestamp": scorecard.timestamp,
            "metrics": asdict(metrics_rep),
            "scorecard": asdict(scorecard),
            "manifest_files": list(manifests.keys()),
            "status": "CERTIFIED" if scorecard.passed else "FAILED",
        }
        p8 = os.path.join(self.export_dir, "metadata.json")
        with open(p8, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, cls=EnhancedJSONEncoder)
        manifests["metadata.json"] = p8

        return manifests
