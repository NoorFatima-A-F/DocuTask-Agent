"""
Phase 3I.7: Observability Security, Privacy & Compliance REST API Router
Provides endpoints for executing security verification, querying privacy audits, and retrieving compliance certificates.
"""
from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any

from ..runtime.observability_security_runtime import ObservabilitySecurityRuntime

router = APIRouter(
    prefix="/api/v1/observability-security",
    tags=["Observability Security, Privacy & Compliance"],
)

_runtime = ObservabilitySecurityRuntime()


@router.post("/run-verification", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
def trigger_observability_security_verification() -> Dict[str, Any]:
    """Execute complete Phase 3I.7 Observability Security & Privacy Verification suite."""
    try:
        results = _runtime.run_full_verification()
        return results
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Observability security verification failed: {str(exc)}",
        )


@router.get("/status", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
def get_security_certification_status() -> Dict[str, Any]:
    """Retrieve current observability security certification status and 6-pillar score."""
    threat = _runtime.threat_verifier.verify_threat_model()
    data = _runtime.data_verifier.verify_sensitive_data_protection()
    redact = _runtime.redact_verifier.verify_log_redaction()
    ai = _runtime.ai_verifier.verify_ai_telemetry_privacy()
    access = _runtime.access_verifier.verify_access_control()
    encrypt = _runtime.encrypt_verifier.verify_telemetry_encryption()
    retention = _runtime.retention_verifier.verify_data_retention()
    audit = _runtime.audit_verifier.verify_audit_trail()
    compliance = _runtime.compliance_verifier.verify_compliance_mapping()
    attack = _runtime.attack_verifier.verify_attack_simulations()
    incident = _runtime.incident_verifier.verify_incident_response()
    continuous = _runtime.continuous_verifier.verify_continuous_security()

    cert = _runtime.scorer.calculate_certification_score(
        threat_report=threat,
        data_report=data,
        redact_report=redact,
        ai_report=ai,
        access_report=access,
        encrypt_report=encrypt,
        retention_report=retention,
        audit_report=audit,
        compliance_report=compliance,
        attack_report=attack,
        incident_report=incident,
        continuous_report=continuous,
    )

    return {
        "certification_tier": cert.certification_tier.value,
        "overall_score_pct": cert.overall_score_pct,
        "certification_granted": cert.certification_granted,
        "evaluated_at": cert.evaluated_at,
        "pillar_scores": [p.model_dump(mode="json") for p in cert.pillar_scores],
    }


@router.get("/privacy-audit", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
def get_privacy_and_redaction_audit() -> Dict[str, Any]:
    """Retrieve sensitive data scan results, automated redaction rules, and AI telemetry privacy status."""
    data = _runtime.data_verifier.verify_sensitive_data_protection()
    redact = _runtime.redact_verifier.verify_log_redaction()
    ai = _runtime.ai_verifier.verify_ai_telemetry_privacy()

    return {
        "sensitive_data_scan": data.model_dump(mode="json"),
        "redaction_rules": redact.model_dump(mode="json"),
        "ai_telemetry_privacy": ai.model_dump(mode="json"),
    }


@router.get("/threat-model", response_model=Dict[str, Any], status_code=status.HTTP_200_OK)
def get_observability_threat_model() -> Dict[str, Any]:
    """Retrieve observability threat model and attack simulation defenses."""
    threat = _runtime.threat_verifier.verify_threat_model()
    attack = _runtime.attack_verifier.verify_attack_simulations()

    return {
        "threat_model": threat.model_dump(mode="json"),
        "attack_simulations": attack.model_dump(mode="json"),
    }
