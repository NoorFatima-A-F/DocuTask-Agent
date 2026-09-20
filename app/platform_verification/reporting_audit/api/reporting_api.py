"""
REST API Router for Enterprise Reporting & Audit Intelligence (PART 8).
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from app.platform_verification.reporting_audit.domain.models import (
    ReportFormat,
    ReportType,
    UserRole,
)
from app.platform_verification.reporting_audit.runtime.reporting_platform_runtime import (
    EnterpriseReportingPlatformRuntime,
)

router = APIRouter(prefix="/reports", tags=["Enterprise Verification Reporting & Audit"])
_runtime = EnterpriseReportingPlatformRuntime()


class GenerateReportRequest(BaseModel):
    report_type: ReportType
    title: str
    scope: str
    data: Dict[str, Any]
    evidence_references: List[str]
    generated_by: str
    format: ReportFormat = ReportFormat.JSON


class AuditExportRequest(BaseModel):
    system_version: str
    include_reports: List[str]
    evidence_manifest: List[str]


@router.post("/generate", response_model=Dict[str, Any])
def generate_audit_report(req: GenerateReportRequest):
    """Generates and cryptographically seals an audit report."""
    record = _runtime.report_generator.generate_report(
        report_type=req.report_type,
        title=req.title,
        scope=req.scope,
        data=req.data,
        evidence_refs=req.evidence_references,
        generated_by=req.generated_by,
        report_format=req.format,
    )
    return {
        "report_id": record.report_id,
        "title": record.title,
        "report_type": record.report_type.value,
        "generated_at": record.generated_at,
        "sha256_digest": record.sha256_digest,
        "verified": record.verify_integrity(),
    }


@router.get("/{report_id}", response_model=Dict[str, Any])
def get_audit_report(report_id: str):
    """Retrieves an audit report and validates cryptographic integrity."""
    record = _runtime.report_generator.get_report(report_id)
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Report '{report_id}' not found.",
        )
    return {
        "report_id": record.report_id,
        "title": record.title,
        "scope": record.scope,
        "generated_at": record.generated_at,
        "content": record.content,
        "sha256_digest": record.sha256_digest,
        "is_valid": record.verify_integrity(),
    }


@router.get("/search", response_model=List[Dict[str, Any]])
def search_reports(q: str):
    """Searches reports by query term."""
    records = getattr(_runtime.report_generator, "search_reports", lambda q: [])(q)
    return [
        {
            "report_id": r.report_id,
            "title": r.title,
            "report_type": r.report_type.value,
            "generated_at": r.generated_at,
        }
        for r in records
    ]


@router.post("/audit/export", response_model=Dict[str, Any])
def export_audit_package(req: AuditExportRequest):
    """Exports a self-contained, auditable package with verified evidence."""
    pkg = _runtime.export_manager.export_audit_package(
        system_version=req.system_version,
        include_reports=req.include_reports,
        evidence_manifest=req.evidence_manifest,
    )
    return {
        "package_id": pkg.package_id,
        "system_version": pkg.system_version,
        "reports_count": len(pkg.reports),
        "package_checksum": pkg.package_checksum,
        "generated_at": pkg.generated_at,
    }


@router.get("/dashboards/{role}", response_model=Dict[str, Any])
def get_dashboard_by_role(role: UserRole):
    """Retrieves role-tailored governance dashboard."""
    if role == UserRole.EXECUTIVE:
        view = _runtime.dashboard_engine.build_executive_dashboard()
        return {
            "role": role.value,
            "readiness_pct": view.production_readiness_pct,
            "certification_level": view.current_certification_level,
            "overall_score": view.overall_quality_score,
            "risk_summary": view.risk_summary,
        }
    elif role == UserRole.ENGINEER:
        view = _runtime.dashboard_engine.build_engineering_dashboard()
        return {
            "role": role.value,
            "coverage_pct": view.code_coverage_pct,
            "ai_metrics": view.ai_quality_metrics,
        }
    elif role == UserRole.SECURITY_OFFICER:
        view = _runtime.dashboard_engine.build_security_dashboard()
        return {
            "role": role.value,
            "vulnerabilities": view.vulnerability_counts,
            "prompt_injection_resistance": view.prompt_injection_resistance_pct,
        }
    else:
        view = _runtime.dashboard_engine.build_ai_governance_dashboard()
        return {
            "role": role.value,
            "model_version": view.active_model_version,
            "hallucination_rate": view.hallucination_rate,
            "grounding_score": view.grounding_score,
        }
