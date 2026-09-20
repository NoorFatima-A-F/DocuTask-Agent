"""
FastAPI REST API Router for Enterprise Infrastructure Quality Scoring & Certification (Phase 3O).
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, List
from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse

from ..domain.models import (
    CertificationDecision,
    MaturityAssessment,
    QualityRegressionReport,
    QualityScorecard,
    RiskAssessmentReport,
    VerificationManifest,
)
from ..runtime.infrastructure_certification_runtime import (
    InfrastructureCertificationRuntime,
)

router = APIRouter(prefix="/api/v1/certification", tags=["Enterprise Infrastructure Certification"])
_runtime = InfrastructureCertificationRuntime()


@router.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check for infrastructure certification service."""
    return {"status": "healthy", "service": "enterprise-infrastructure-certification"}


@router.get("/pillars")
async def list_pillars() -> List[Dict[str, Any]]:
    """List the 6 SRE infrastructure quality pillars and their evaluation weights."""
    return [
        {"name": "Reliability", "weight": 0.25, "description": "Chaos resilience, health liveness/readiness, worker resilience"},
        {"name": "Security", "weight": 0.20, "description": "Zero-trust container isolation, KMS secrets, IAM RBAC, mTLS, AI defense"},
        {"name": "Scalability", "weight": 0.20, "description": "Throughput capacity, latency SLAs, resource efficiency, horizontal scaling"},
        {"name": "Observability", "weight": 0.15, "description": "OpenTelemetry tracing, structured JSON logs, Prometheus metrics, alert precision"},
        {"name": "Deployment Quality", "weight": 0.10, "description": "IaC Terraform/Helm reproducibility, CI/CD blocking quality gates"},
        {"name": "Recovery Capability", "weight": 0.10, "description": "PITR restore consistency, RTO (<15m), RPO (<5m), multi-region DR"},
    ]


@router.post("/run", response_model=VerificationManifest)
@router.post("/verify/all", response_model=VerificationManifest)
async def run_certification_suite(export_dir: str = "infrastructure_certification") -> VerificationManifest:
    """Trigger full end-to-end infrastructure evidence collection, quality scoring, risk assessment, and certification export."""
    manifest = await _runtime.run_all(export_dir=export_dir)
    return manifest


@router.get("/scorecard", response_model=QualityScorecard)
async def get_scorecard() -> QualityScorecard:
    """Retrieve the latest 6-pillar quality scorecard."""
    scorecard = _runtime.get_latest_scorecard()
    if scorecard is None:
        res = _runtime.run_full_certification()
        scorecard = res["scorecard"]
    return scorecard


@router.get("/decision", response_model=CertificationDecision)
async def get_decision() -> CertificationDecision:
    """Retrieve the latest formal production certification and deployment gate decision."""
    decision = _runtime.get_latest_decision()
    if decision is None:
        res = _runtime.run_full_certification()
        decision = res["decision"]
    return decision


@router.get("/risks", response_model=RiskAssessmentReport)
async def get_risks() -> RiskAssessmentReport:
    """Retrieve the latest infrastructure risk and vulnerability assessment report."""
    risk_report = _runtime.get_latest_risk_report()
    if risk_report is None:
        res = _runtime.run_full_certification()
        risk_report = res["risk_report"]
    return risk_report


@router.get("/maturity", response_model=MaturityAssessment)
async def get_maturity() -> MaturityAssessment:
    """Retrieve the operational maturity model evaluation (Level 0 - Level 5)."""
    maturity = _runtime.get_latest_maturity()
    if maturity is None:
        res = _runtime.run_full_certification()
        maturity = res["maturity"]
    return maturity


@router.get("/manifest", response_model=VerificationManifest)
@router.get("/evidence/manifest", response_model=VerificationManifest)
async def get_manifest() -> VerificationManifest:
    """Retrieve the latest cryptographic SHA-256 verification manifest."""
    manifest = _runtime.get_latest_manifest()
    if manifest is not None:
        return manifest

    manifest_path = os.path.join("infrastructure_certification", "metadata.json")
    if os.path.exists(manifest_path):
        with open(manifest_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return VerificationManifest(**data)
    raise HTTPException(status_code=404, detail="Manifest not found. Run /run or /verify/all endpoint first.")


@router.get("/report/markdown", response_class=PlainTextResponse)
async def get_markdown_report() -> str:
    """Retrieve the human-readable Infrastructure_Readiness_Report.md content."""
    md_path = Path("infrastructure_certification") / "Infrastructure_Readiness_Report.md"
    if md_path.exists():
        return md_path.read_text(encoding="utf-8")
    res = _runtime.run_full_certification()
    return (Path("infrastructure_certification") / "Infrastructure_Readiness_Report.md").read_text(encoding="utf-8")
