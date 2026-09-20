"""
Phase 3I.9: Observability Intelligence & Predictive Reliability REST API Router
Provides endpoints for triggering predictive verification, querying failure predictions, capacity forecasts, and AI reliability telemetry.
"""
from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any

from ..runtime.observability_intelligence_runtime import ObservabilityIntelligenceRuntime

router = APIRouter(
    prefix="/api/v1/observability-intelligence",
    tags=["Observability Intelligence, Predictive Reliability & AIOps Maturity"],
)

_runtime = ObservabilityIntelligenceRuntime()


@router.post("/run-verification", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
def trigger_observability_intelligence_verification() -> Dict[str, Any]:
    """Execute complete Phase 3I.9 Observability Intelligence & Predictive Reliability verification suite."""
    try:
        results = _runtime.run_full_verification()
        return results
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Observability intelligence verification failed: {str(exc)}",
        )


@router.get("/status", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
def get_predictive_certification_status() -> Dict[str, Any]:
    """Retrieve current predictive reliability certification status and 6-pillar score."""
    arch = _runtime.arch_verifier.verify_aiops_architecture()
    data = _runtime.data_verifier.verify_data_quality()
    pred = _runtime.pred_verifier.verify_failure_prediction()
    capacity = _runtime.capacity_verifier.verify_capacity_forecasting()
    baseline = _runtime.baseline_verifier.verify_behavior_baselines()
    anomaly = _runtime.anomaly_verifier.verify_predictive_anomalies()
    score = _runtime.score_verifier.verify_reliability_score()
    prevention = _runtime.prevention_verifier.verify_incident_prevention()
    deploy = _runtime.deploy_verifier.verify_deployment_intelligence()
    ai = _runtime.ai_verifier.verify_ai_reliability()
    opt = _runtime.opt_verifier.verify_continuous_optimization()
    explain = _runtime.explain_verifier.verify_aiops_explainability()
    val = _runtime.val_verifier.verify_aiops_validation()

    cert = _runtime.scorer.calculate_certification_score(
        arch_report=arch,
        data_report=data,
        pred_report=pred,
        capacity_report=capacity,
        baseline_report=baseline,
        anomaly_report=anomaly,
        score_report=score,
        prevention_report=prevention,
        deploy_report=deploy,
        ai_report=ai,
        opt_report=opt,
        explain_report=explain,
        val_report=val,
    )

    return {
        "certification_tier": cert.certification_tier.value,
        "overall_score_pct": cert.overall_score_pct,
        "certification_granted": cert.certification_granted,
        "evaluated_at": cert.evaluated_at,
        "pillar_scores": [p.model_dump(mode="json") for p in cert.pillar_scores],
    }


@router.get("/predictions", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
def get_failure_predictions() -> Dict[str, Any]:
    """Retrieve proactive failure predictions, lead times, and explainable decision citations."""
    pred = _runtime.pred_verifier.verify_failure_prediction()
    anomaly = _runtime.anomaly_verifier.verify_predictive_anomalies()
    explain = _runtime.explain_verifier.verify_aiops_explainability()

    return {
        "failure_predictions": pred.model_dump(mode="json"),
        "predictive_anomalies": anomaly.model_dump(mode="json"),
        "explainable_decisions": explain.model_dump(mode="json"),
    }


@router.get("/capacity-forecast", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
def get_capacity_forecasts() -> Dict[str, Any]:
    """Retrieve 30-day and 90-day multi-horizon capacity forecasts and dynamic baselines."""
    capacity = _runtime.capacity_verifier.verify_capacity_forecasting()
    baseline = _runtime.baseline_verifier.verify_behavior_baselines()

    return {
        "capacity_forecasts": capacity.model_dump(mode="json"),
        "behavioral_baselines": baseline.model_dump(mode="json"),
    }


@router.get("/ai-reliability", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
def get_ai_reliability_status() -> Dict[str, Any]:
    """Retrieve AI model reliability telemetry, hallucination indicators, and continuous optimizations."""
    ai = _runtime.ai_verifier.verify_ai_reliability()
    opt = _runtime.opt_verifier.verify_continuous_optimization()
    deploy = _runtime.deploy_verifier.verify_deployment_intelligence()

    return {
        "ai_model_reliability": ai.model_dump(mode="json"),
        "continuous_optimizations": opt.model_dump(mode="json"),
        "deployment_impact": deploy.model_dump(mode="json"),
    }
