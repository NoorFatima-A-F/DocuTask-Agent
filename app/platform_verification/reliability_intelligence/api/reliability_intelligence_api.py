"""Reliability Intelligence API Endpoints.

FastAPI router exposing SRE intelligence, SLO metrics, and reliability scorecards.
"""

from fastapi import APIRouter
from typing import Dict, Any

from app.platform_verification.reliability_intelligence.runtime.reliability_intelligence_runtime import ReliabilityIntelligenceRuntime
from app.platform_verification.reliability_intelligence.exporter.reliability_evidence_exporter import EnhancedJSONEncoder
import json

router = APIRouter(prefix="/health/reliability", tags=["Reliability Intelligence"])
_runtime = ReliabilityIntelligenceRuntime()


def _to_dict(obj: Any) -> Any:
    return json.loads(json.dumps(obj, cls=EnhancedJSONEncoder))


@router.get("/model", summary="Get Reliability Model & SLI Definitions")
def get_reliability_model() -> Dict[str, Any]:
    report = _runtime.model_verifier.verify_reliability_model()
    return _to_dict(report)


@router.get("/slos", summary="Get SLO Attainment & Compliance")
def get_slos() -> Dict[str, Any]:
    report = _runtime.slo_verifier.verify_slos()
    return _to_dict(report)


@router.get("/error-budgets", summary="Get Error Budgets & Burn Rates")
def get_error_budgets() -> Dict[str, Any]:
    report = _runtime.error_budget_mgr.evaluate_error_budgets()
    return _to_dict(report)


@router.get("/failure-patterns", summary="Get 30-Day Failure Pattern Analysis")
def get_failure_patterns() -> Dict[str, Any]:
    report = _runtime.pattern_analyzer.analyze_rolling_patterns()
    return _to_dict(report)


@router.get("/root-causes", summary="Get Multi-Signal Root Cause Intelligence")
def get_root_causes() -> Dict[str, Any]:
    report = _runtime.root_cause_engine.analyze_root_causes()
    return _to_dict(report)


@router.get("/risk-scores", summary="Get Service Reliability Risk Scores")
def get_risk_scores() -> Dict[str, Any]:
    report = _runtime.risk_scorer.compute_risk_scores()
    return _to_dict(report)


@router.get("/capacity", summary="Get Capacity Forecasts & Exhaustion Predictions")
def get_capacity_forecasts() -> Dict[str, Any]:
    report = _runtime.capacity_engine.forecast_capacity()
    return _to_dict(report)


@router.get("/change-impact", summary="Get Release Change Regressions")
def get_change_impact() -> Dict[str, Any]:
    report = _runtime.change_analyzer.analyze_releases()
    return _to_dict(report)


@router.get("/chaos-learning", summary="Get Chaos Experiment MTTR Gains")
def get_chaos_learning() -> Dict[str, Any]:
    report = _runtime.chaos_tracker.track_experiment_gains()
    return _to_dict(report)


@router.get("/recommendations", summary="Get Prioritized SRE Action Recommendations")
def get_recommendations() -> Dict[str, Any]:
    report = _runtime.recommender.generate_recommendations()
    return _to_dict(report)


@router.get("/improvement", summary="Get Continuous Improvement Review Cycles")
def get_improvement_cycles() -> Dict[str, Any]:
    report = _runtime.improvement_loop.evaluate_improvement_velocity()
    return _to_dict(report)


@router.get("/security", summary="Get SRE Security & PII Redaction Audit")
def get_security_audit() -> Dict[str, Any]:
    report = _runtime.security_auditor.audit_security_controls()
    return _to_dict(report)


@router.get("/scorecard", summary="Get Platform Reliability Maturity Scorecard")
def get_maturity_scorecard() -> Dict[str, Any]:
    res = _runtime.run_full_verification()
    return _to_dict(res["scorecard"])


@router.post("/verify", summary="Execute Full Verification & Export Artifacts")
def execute_full_verification() -> Dict[str, Any]:
    res = _runtime.run_full_verification()
    return _to_dict(res)
