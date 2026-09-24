"""
FastAPI REST API Router for Enterprise Verification Evidence Intelligence System (Phase 3P).
"""

import json
import os
from pathlib import Path
from typing import Dict, List
from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse

from ..domain.models import (
    ComplianceReport,
    EngineeringAuditReport,
    EvidenceProvenance,
    ExecutiveCertificationReport,
    FailureEvidenceReport,
    PortfolioEvidenceBundle,
    StandardizedEvidenceItem,
    VerificationManifest,
)
from ..runtime.evidence_intelligence_runtime import (
    EvidenceIntelligenceRuntime,
)

router = APIRouter(prefix="/api/v1/evidence", tags=["Enterprise Evidence Intelligence"])
_runtime = EvidenceIntelligenceRuntime()


@router.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check for enterprise evidence intelligence service."""
    return {"status": "healthy", "service": "enterprise-evidence-intelligence"}


@router.get("/provenance", response_model=EvidenceProvenance)
async def get_provenance() -> EvidenceProvenance:
    """Retrieve the cryptographic provenance record of current verification build."""
    res = _runtime.run_full_pipeline()
    return res["provenance"]


@router.get("/items", response_model=List[StandardizedEvidenceItem])
async def list_evidence_items() -> List[StandardizedEvidenceItem]:
    """Retrieve all standardized evidence items collected across infrastructure domains."""
    items = _runtime.get_latest_items()
    if not items:
        res = _runtime.run_full_pipeline()
        items = res["evidence_items"]
    return items


@router.get("/compliance", response_model=ComplianceReport)
async def get_compliance_report() -> ComplianceReport:
    """Retrieve the compliance mapping report (SOC 2, ISO 27001, NIST CSF)."""
    comp = _runtime.get_latest_compliance()
    if comp is None:
        res = _runtime.run_full_pipeline()
        comp = res["compliance"]
    return comp


@router.get("/failures", response_model=FailureEvidenceReport)
async def get_failures_report() -> FailureEvidenceReport:
    """Retrieve the failure evidence and root cause intelligence report."""
    fails = _runtime.get_latest_failures()
    if fails is None:
        res = _runtime.run_full_pipeline()
        fails = res["failures"]
    return fails


@router.get("/executive", response_model=ExecutiveCertificationReport)
async def get_executive_report() -> ExecutiveCertificationReport:
    """Retrieve the executive certification report."""
    exec_rep = _runtime.get_latest_executive()
    if exec_rep is None:
        res = _runtime.run_full_pipeline()
        exec_rep = res["executive_report"]
    return exec_rep


@router.get("/audit", response_model=EngineeringAuditReport)
async def get_audit_report() -> EngineeringAuditReport:
    """Retrieve the deep-dive engineering audit report."""
    audit = _runtime.get_latest_audit()
    if audit is None:
        res = _runtime.run_full_pipeline()
        audit = res["audit_report"]
    return audit


@router.get("/portfolio", response_model=PortfolioEvidenceBundle)
async def get_portfolio_bundle() -> PortfolioEvidenceBundle:
    """Retrieve the public-safe portfolio presentation bundle and deployment badge."""
    port = _runtime.get_latest_portfolio()
    if port is None:
        res = _runtime.run_full_pipeline()
        port = res["portfolio"]
    return port


@router.post("/run", response_model=VerificationManifest)
@router.post("/verify/all", response_model=VerificationManifest)
async def run_evidence_pipeline(export_dir: str = "infrastructure_verification") -> VerificationManifest:
    """Trigger the complete automated evidence intelligence pipeline and export artifacts."""
    manifest = await _runtime.run_all(export_dir=export_dir)
    return manifest


@router.get("/manifest", response_model=VerificationManifest)
@router.get("/evidence/manifest", response_model=VerificationManifest)
async def get_manifest() -> VerificationManifest:
    """Retrieve the latest cryptographic SHA-256 verification manifest."""
    manifest = _runtime.get_latest_manifest()
    if manifest is not None:
        return manifest

    manifest_path = os.path.join("infrastructure_verification", "metadata.json")
    if os.path.exists(manifest_path):
        with open(manifest_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return VerificationManifest(**data)
    raise HTTPException(status_code=404, detail="Manifest not found. Run /run endpoint first.")


@router.get("/reports/executive/markdown", response_class=PlainTextResponse)
async def get_executive_markdown() -> str:
    """Retrieve the human-readable executive certification report markdown."""
    md_path = Path("infrastructure_verification") / "reports" / "executive_certification_report.md"
    if md_path.exists():
        return md_path.read_text(encoding="utf-8")
    _runtime.run_full_pipeline()
    return (Path("infrastructure_verification") / "reports" / "executive_certification_report.md").read_text(encoding="utf-8")


@router.get("/reports/audit/markdown", response_class=PlainTextResponse)
async def get_audit_markdown() -> str:
    """Retrieve the technical engineering audit report markdown."""
    md_path = Path("infrastructure_verification") / "reports" / "engineering_audit_report.md"
    if md_path.exists():
        return md_path.read_text(encoding="utf-8")
    _runtime.run_full_pipeline()
    return (Path("infrastructure_verification") / "reports" / "engineering_audit_report.md").read_text(encoding="utf-8")
