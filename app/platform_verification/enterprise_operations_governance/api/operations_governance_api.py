"""
FastAPI REST API Router for Enterprise Production Operations & Governance (Phase 3R).
"""

import json
import os
from typing import Dict, List
from fastapi import APIRouter, HTTPException

from ..domain.models import (
    AlertReport,
    IncidentReport,
    OperationalMaturityScore,
    OperationsManifest,
    ProductionHealthReport,
    SLODefinitionReport,
)
from ..runtime.operations_governance_runtime import OperationsGovernanceRuntime

router = APIRouter(prefix="/api/v1/operations", tags=["Enterprise Operations Governance"])
_runtime = OperationsGovernanceRuntime()


@router.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check for enterprise operations governance service."""
    return {"status": "healthy", "service": "enterprise-operations-governance"}


@router.get("/domains")
async def list_governance_domains() -> List[Dict[str, str]]:
    """List the core operational governance domains."""
    return [
        {"domain": "1. SLO & Error Budget Management", "metric": "99.5% Uptime, Error Budget: 216 mins/mo"},
        {"domain": "2. Production Health Intelligence", "metric": "Centralized Application, Workers, DB, Queue, Infra"},
        {"domain": "3. Incident Management & Lifecycle", "metric": "SEV1/SEV2/SEV3 Workflows, MTTR Tracking"},
        {"domain": "4. Automated Multi-Channel Alerting", "metric": "Silent Failure Prevention, PagerDuty / Slack / SIEM"},
        {"domain": "5. Runbook Automation & Procedures", "metric": "6 Validated Production Runbooks"},
        {"domain": "6. Self-Healing Automated Remediation", "metric": "Worker Restart, Queue Scale, DB Pool Reconnect"},
        {"domain": "7. Root Cause Analysis (RCA) Engine", "metric": "Telemetry Timeline & Ranked Hypotheses"},
        {"domain": "8. Change Management & Audit Trail", "metric": "Immutable Operational Accountability"},
        {"domain": "9. AIOps & FinOps Unit Economics", "metric": "Model Accuracy, Hallucination, Cost/Document"},
        {"domain": "10. Operational Maturity Scoring", "metric": "6-Dimensional Maturity Index & Certification"},
    ]


@router.post("/run", response_model=OperationsManifest)
@router.post("/verify/all", response_model=OperationsManifest)
async def run_governance_cycle() -> OperationsManifest:
    """Execute complete operational governance evaluation cycle."""
    manifest = await _runtime.run_all()
    return manifest


@router.get("/slo", response_model=SLODefinitionReport)
async def get_slos() -> SLODefinitionReport:
    """Retrieve production SLO definitions and compliance status."""
    slo = _runtime.get_latest_slo()
    if slo is None:
        res = _runtime.run_governance_cycle()
        slo = res["slo"]
    return slo


@router.get("/status", response_model=ProductionHealthReport)
async def get_production_health() -> ProductionHealthReport:
    """Retrieve centralized production health status."""
    health = _runtime.get_latest_health()
    if health is None:
        res = _runtime.run_governance_cycle()
        health = res["health"]
    return health


@router.get("/incidents", response_model=IncidentReport)
async def get_incidents() -> IncidentReport:
    """Retrieve incident management summary and MTTR metrics."""
    inc = _runtime.get_latest_incidents()
    if inc is None:
        res = _runtime.run_governance_cycle()
        inc = res["incidents"]
    return inc


@router.get("/alerts", response_model=AlertReport)
async def get_alerts() -> AlertReport:
    """Retrieve multi-channel alerting rules and firing status."""
    alerts = _runtime.get_latest_alerts()
    if alerts is None:
        res = _runtime.run_governance_cycle()
        alerts = res["alerts"]
    return alerts


@router.get("/maturity", response_model=OperationalMaturityScore)
async def get_maturity_score() -> OperationalMaturityScore:
    """Retrieve 6-dimensional operational maturity score and certification."""
    mat = _runtime.get_latest_maturity()
    if mat is None:
        res = _runtime.run_governance_cycle()
        mat = res["maturity"]
    return mat


@router.get("/manifest", response_model=OperationsManifest)
@router.get("/evidence/manifest", response_model=OperationsManifest)
async def get_manifest() -> OperationsManifest:
    """Retrieve the latest cryptographic SHA-256 operations verification manifest."""
    manifest = _runtime.get_latest_manifest()
    if manifest is not None:
        return manifest

    manifest_path = os.path.join("operations_verification", "metadata.json")
    if os.path.exists(manifest_path):
        with open(manifest_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return OperationsManifest(**data)
    raise HTTPException(status_code=404, detail="Operations manifest not found. Run /run endpoint first.")
