"""
AOIS-HROP Phase 13.7 - Diagnosis Engine
Master coordinator for autonomous root-cause analysis, causal graphs, and explainable incident diagnostics.
"""

from typing import Any, Dict, List, Optional
from app.runtime.operations.diagnostics.root_cause_engine import RootCauseEngine, RootCauseDiagnosis


class DiagnosisEngine:
    """
    Master coordinator for platform incident diagnosis and explainable root-cause resolution.
    """

    def __init__(self):
        self.root_cause_engine = RootCauseEngine()
        self._diagnoses: Dict[str, RootCauseDiagnosis] = {}

    def diagnose_incident(
        self,
        incident_id: str,
        affected_subsystems: List[str],
        error_type: str = "LATENCY_SPIKE",
    ) -> Dict[str, Any]:
        diagnosis = self.root_cause_engine.infer_root_cause(
            incident_id=incident_id,
            anomalous_subsystems=affected_subsystems,
            error_type=error_type,
        )
        self._diagnoses[incident_id] = diagnosis

        return {
            "diagnosis_id": diagnosis.diagnosis_id,
            "incident_id": diagnosis.incident_id,
            "primary_culprit": diagnosis.primary_culprit_subsystem,
            "error_pattern": diagnosis.error_pattern,
            "confidence": diagnosis.confidence,
            "recommended_action": diagnosis.recommended_healing_action.value,
            "causal_chain": diagnosis.explanation.causal_steps,
            "summary": diagnosis.explanation.root_cause_summary,
            "evidence_sources": diagnosis.explanation.evidence_sources,
            "created_at": diagnosis.created_at,
        }

    def get_diagnosis(self, incident_id: str) -> Optional[Dict[str, Any]]:
        diag = self._diagnoses.get(incident_id)
        if not diag:
            return None
        return {
            "diagnosis_id": diag.diagnosis_id,
            "incident_id": diag.incident_id,
            "primary_culprit": diag.primary_culprit_subsystem,
            "error_pattern": diag.error_pattern,
            "confidence": diag.confidence,
            "recommended_action": diag.recommended_healing_action.value,
            "causal_chain": diag.explanation.causal_steps,
            "summary": diag.explanation.root_cause_summary,
        }

    def get_all_diagnoses(self) -> List[Dict[str, Any]]:
        return [
            {
                "diagnosis_id": d.diagnosis_id,
                "incident_id": d.incident_id,
                "primary_culprit": d.primary_culprit_subsystem,
                "error_pattern": d.error_pattern,
                "confidence": d.confidence,
                "recommended_action": d.recommended_healing_action.value,
            }
            for d in self._diagnoses.values()
        ]


_GLOBAL_DIAGNOSIS_ENGINE: Optional[DiagnosisEngine] = None


def get_diagnosis_engine() -> DiagnosisEngine:
    global _GLOBAL_DIAGNOSIS_ENGINE
    if _GLOBAL_DIAGNOSIS_ENGINE is None:
        _GLOBAL_DIAGNOSIS_ENGINE = DiagnosisEngine()
    return _GLOBAL_DIAGNOSIS_ENGINE
