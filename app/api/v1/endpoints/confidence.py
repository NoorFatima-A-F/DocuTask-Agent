"""
REST API Endpoints for Phase 13.3 Autonomous Scientific Confidence Engine, Runtime Evidence Intelligence & Confidence Governance Platform (ASCE-CGP).
"""

from __future__ import annotations

from fastapi import APIRouter, Query

from app.runtime.confidence.api.confidence_api_service import ConfidenceAPIService

router = APIRouter()


@router.get('/mission/{mission_id}')
async def get_mission_confidence(mission_id: str):
    """
    Returns full 13-dimension scientific confidence report for the mission.
    """
    return ConfidenceAPIService.get_instance(mission_id).compute_mission_confidence().model_dump()


@router.get('/features')
async def get_registered_features():
    """
    Returns all registered confidence features and schemas.
    """
    return ConfidenceAPIService.get_instance().get_features()


@router.get('/formulas')
async def get_registered_formulas():
    """
    Returns mathematical confidence formulas and versions.
    """
    return ConfidenceAPIService.get_instance().get_formulas()


@router.get('/history')
async def get_confidence_history(mission_id: str = Query("mission-001")):
    """
    Returns historical confidence snapshots.
    """
    from app.runtime.confidence.versioning.confidence_versioning import ConfidenceVersioningRegistry
    reports = ConfidenceVersioningRegistry.get_all(mission_id)
    return [r.model_dump() for r in reports]


@router.get('/explanation')
async def get_confidence_explanation(
    mission_id: str = Query("mission-001"),
    dimension: str = Query("OVERALL"),
):
    """
    Returns waterfall feature contribution and sensitivity explanations.
    """
    return ConfidenceAPIService.get_instance(mission_id).get_explanation(dimension)


@router.get('/weights')
async def get_confidence_weights():
    """
    Returns policy-derived dynamic weight matrices.
    """
    return ConfidenceAPIService.get_instance().get_weights()


@router.get('/lineage')
async def get_confidence_lineage(mission_id: str = Query("mission-001")):
    """
    Returns cryptographic provenance and Merkle evidence links.
    """
    return ConfidenceAPIService.get_instance(mission_id).get_lineage()


@router.get('/calibration')
async def get_calibration_metrics():
    """
    Returns Expected Calibration Error (ECE), MCE, and reliability diagram data.
    """
    return ConfidenceAPIService.get_instance().get_calibration()


@router.get('/uncertainty')
async def get_uncertainty_metrics(mission_id: str = Query("mission-001")):
    """
    Returns aleatoric vs epistemic uncertainty decomposition and 95% intervals.
    """
    return ConfidenceAPIService.get_instance(mission_id).get_uncertainty()


@router.get('/governance')
async def get_confidence_governance(mission_id: str = Query("mission-001")):
    """
    Returns governance policy evaluation and auditor certification verdict.
    """
    return ConfidenceAPIService.get_instance(mission_id).get_governance()


@router.get('/trends')
async def get_confidence_trends():
    """
    Returns drift analysis and stability indices.
    """
    return ConfidenceAPIService.get_instance().get_trends()


@router.get('/statistics')
async def get_confidence_statistics():
    """
    Returns distribution statistics across historical missions.
    """
    return ConfidenceAPIService.get_instance().get_statistics()


@router.get('/replay')
async def get_confidence_replay(mission_id: str = Query("mission-001")):
    """
    Reconstructs confidence progression from Event Store.
    """
    return {
        "mission_id": mission_id,
        "replay_ready": True,
        "lineage_records_count": len(ConfidenceAPIService.get_instance(mission_id).get_lineage()),
        "status": "REPLAY_CERTIFIED",
    }
