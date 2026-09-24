"""FastAPI Router for Phase 6: AI System Evaluation & Portfolio Certification."""

from typing import Any, Dict, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel

from ..domain.models import (
    PlatformCertificationScore,
    PortfolioShowcaseReport,
)
from ..runtime.evaluation_runtime import EvaluationRuntime


router = APIRouter(prefix="/api/v1/evaluation", tags=["AI System Evaluation & Certification"])
_runtime = EvaluationRuntime()


class HealthResponse(BaseModel):
    status: str
    phase: str
    evaluators_count: int
    evaluators: list[str]


@router.get("/health", response_model=HealthResponse)
def get_evaluation_health() -> HealthResponse:
    """Return health status of evaluation framework and registered evaluation dimensions."""
    return HealthResponse(
        status="healthy",
        phase="Phase 6 - AI System Evaluation, Benchmarking & Portfolio Certification",
        evaluators_count=len(_runtime.evaluators),
        evaluators=list(_runtime.evaluators.keys()),
    )


@router.post("/run", response_model=PortfolioShowcaseReport)
def run_full_evaluation() -> PortfolioShowcaseReport:
    """Execute all 10 evaluation modules, compute 6-pillar score, and export portfolio evidence."""
    try:
        report = _runtime.execute_all()
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Evaluation run failed: {str(e)}")


@router.get("/score", response_model=PlatformCertificationScore)
def get_certification_score() -> PlatformCertificationScore:
    """Execute all evaluators and return the 6-pillar weighted certification score."""
    try:
        showcase = _runtime.execute_all()
        return showcase.score
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to calculate score: {str(e)}")


@router.get("/report", response_model=PortfolioShowcaseReport)
def get_latest_report() -> PortfolioShowcaseReport:
    """Generate and return complete showcase report."""
    try:
        return _runtime.execute_all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch report: {str(e)}")


@router.get("/evaluator/{evaluator_key}")
def get_single_evaluator_report(evaluator_key: str) -> Dict[str, Any]:
    """Execute a single evaluator dimension (e.g. ai_capability, rag_evaluation, cost_business)."""
    if evaluator_key not in _runtime.evaluators:
        raise HTTPException(
            status_code=404,
            detail=f"Evaluator '{evaluator_key}' not found. Valid evaluators: {list(_runtime.evaluators.keys())}",
        )
    evaluator = _runtime.evaluators[evaluator_key]
    report = evaluator.evaluate()
    return report.model_dump() if hasattr(report, "model_dump") else report
