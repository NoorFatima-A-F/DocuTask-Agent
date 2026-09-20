"""AI Provider Health API Endpoints.

FastAPI router exposing AI provider health metrics, failover states, and LLMOps reliability scorecards.
"""

from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any
import json

from app.platform_verification.ai_provider_health.runtime.ai_provider_health_runtime import AIProviderHealthRuntime
from app.platform_verification.ai_provider_health.exporter.ai_evidence_exporter import EnhancedJSONEncoder

router = APIRouter(prefix="/health/ai", tags=["AI Provider Health"])
_runtime = AIProviderHealthRuntime()


def _to_dict(obj: Any) -> Any:
    return json.loads(json.dumps(obj, cls=EnhancedJSONEncoder))


@router.get("/status", summary="Get AI Provider Health Status & Contract")
def get_provider_health() -> Dict[str, Any]:
    report = _runtime.contract_verifier.verify_provider_health()
    return _to_dict(report)


@router.get("/auth", summary="Get AI Authentication Health")
def get_auth_health() -> Dict[str, Any]:
    report = _runtime.auth_verifier.verify_authentication()
    return _to_dict(report)


@router.get("/connectivity", summary="Get Network Connectivity & TLS Health")
def get_connectivity_health() -> Dict[str, Any]:
    report = _runtime.connectivity_verifier.verify_connectivity()
    return _to_dict(report)


@router.get("/latency", summary="Get AI Latency Distributions (P50, P95, P99)")
def get_latency_health() -> Dict[str, Any]:
    report = _runtime.latency_verifier.verify_latency()
    return _to_dict(report)


@router.get("/quota", summary="Get AI Quota & Rate Limit Utilization")
def get_quota_health() -> Dict[str, Any]:
    report = _runtime.quota_verifier.verify_quota()
    return _to_dict(report)


@router.get("/integrity", summary="Get AI Schema Integrity & Extraction Quality")
def get_response_integrity() -> Dict[str, Any]:
    report = _runtime.integrity_verifier.verify_response_integrity()
    return _to_dict(report)


@router.get("/failover", summary="Get Multi-Provider Failover Status")
def get_failover_status() -> Dict[str, Any]:
    report = _runtime.failover_verifier.verify_failover()
    return _to_dict(report)


@router.get("/simulations", summary="Get AI Chaos Failure Simulation Results")
def get_simulations_results() -> Dict[str, Any]:
    report = _runtime.failure_simulator.run_simulations()
    return _to_dict(report)


@router.get("/scorecard", summary="Get Platform AI Reliability Quality Scorecard")
def get_scorecard() -> Dict[str, Any]:
    res = _runtime.run_full_verification()
    return _to_dict(res["scorecard"])


@router.post("/verify", summary="Execute Full AI Provider Verification & Export Manifests")
def execute_full_verification() -> Dict[str, Any]:
    res = _runtime.run_full_verification()
    return _to_dict(res)
