"""FastAPI Router for Health Root Cause Analysis & Operational Diagnosis (3H.4.2.11).

Exposes REST endpoints for real-time diagnosis, dependency graph topology,
multi-signal correlation, impact analysis, cascading failure isolation, and scorecards.
"""

from fastapi import APIRouter
from typing import Dict, Any
import json

from ..runtime.health_root_cause_runtime import HealthRootCauseRuntime
from ..exporter.rca_evidence_exporter import EnhancedJSONEncoder

router = APIRouter(prefix="/health", tags=["Health Diagnosis & Root Cause Analysis"])
_runtime = HealthRootCauseRuntime()


def _to_dict(obj: Any) -> Any:
    return json.loads(json.dumps(obj, cls=EnhancedJSONEncoder))


@router.get("/diagnosis", summary="Get Real-Time Health Diagnosis, Root Cause & Timeline (3H.4.2.11)")
def get_diagnosis() -> Dict[str, Any]:
    diagnosis = _runtime.diagnose_incident()
    return _to_dict(diagnosis)


@router.get("/rca/topology", summary="Get Runtime Dependency Graph Topology (3H.4.2.1)")
def get_topology() -> Dict[str, Any]:
    return _to_dict(_runtime.dep_graph.build_graph_report())


@router.get("/rca/correlation", summary="Get Multi-Signal Correlated Event Clusters (3H.4.2.2)")
def get_correlation() -> Dict[str, Any]:
    return _to_dict(_runtime.correlator.correlate_events())


@router.get("/rca/impact", summary="Get Blast Radius & Service Impact Assessment (3H.4.2.5)")
def get_impact() -> Dict[str, Any]:
    return _to_dict(_runtime.impact_analyzer.analyze_impact("postgresql"))


@router.get("/rca/cascade", summary="Get Cascading Failure Isolation Chains (3H.4.2.8)")
def get_cascade() -> Dict[str, Any]:
    return _to_dict(_runtime.cascade_detector.detect_cascade("INC-ACTIVE-001"))


@router.get("/rca/memory", summary="Get Historical Incident Signatures & Knowledge Base (3H.4.2.10)")
def get_memory() -> Dict[str, Any]:
    return _to_dict(_runtime.memory_engine.get_memory_report())


@router.get("/rca/scorecard", summary="Get Composite RCA Quality Scorecard (3H.4.2.14)")
def get_scorecard() -> Dict[str, Any]:
    res = _runtime.run_full_verification()
    return _to_dict(res["scorecard"])


@router.post("/rca/verify", summary="Run Full Root Cause Analysis Verification & Export Manifests")
def execute_full_verification() -> Dict[str, Any]:
    res = _runtime.run_full_verification()
    return _to_dict(res)
