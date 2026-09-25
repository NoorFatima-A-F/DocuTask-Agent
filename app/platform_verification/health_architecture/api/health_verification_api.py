"""
FastAPI Endpoints for Health Check Architecture Verification (Part 3H.1).
"""
from fastapi import APIRouter, Header
from typing import Dict, Any, Optional
from dataclasses import asdict

from app.platform_verification.health_architecture.runtime.health_runtime import (
    HealthVerificationRuntime,
)
from app.platform_verification.health_architecture.contracts.health_contract_manager import (
    HealthContractManager,
)
from app.platform_verification.health_architecture.dependency_graph.dependency_graph_manager import (
    DependencyGraphManager,
)
from app.platform_verification.health_architecture.policies_and_security.health_failure_policy import (
    HealthFailurePolicyManager,
)
from app.platform_verification.health_architecture.policies_and_security.health_security_auditor import (
    HealthSecurityAuditor,
)
from app.platform_verification.health_architecture.automation.orchestration_automation_verifier import (
    OrchestrationAutomationVerifier,
)

router = APIRouter(prefix="/api/v1/health-architecture", tags=["Health Architecture Verification"])


@router.get("/verify")
def run_full_health_architecture_verification() -> Dict[str, Any]:
    """Execute complete 6-dimensional health check architecture verification."""
    runtime = HealthVerificationRuntime()
    result = runtime.run_full_verification(export=True)
    return {
        "scorecard": asdict(result["scorecard"]),
        "exported_files": result["exported_files"],
        "success": result["success"],
    }


@router.get("/contracts")
def get_health_contracts() -> Dict[str, Any]:
    """Validate and return contract enforcement for /live, /ready, and /health."""
    manager = HealthContractManager()
    report = manager.validate_contracts()
    return asdict(report)


@router.get("/dependency-graph")
def get_dependency_graph() -> Dict[str, Any]:
    """Return mapped dependency graph, priority tiers, and recovery strategies."""
    manager = DependencyGraphManager()
    report = manager.generate_dependency_graph()
    return asdict(report)


@router.get("/failure-policies")
def get_failure_policies() -> Dict[str, Any]:
    """Return failure response workflows and automated remediation rules."""
    manager = HealthFailurePolicyManager()
    report = manager.verify_failure_policies()
    return asdict(report)


@router.get("/security-audit")
def get_security_audit() -> Dict[str, Any]:
    """Return security and credential leak audit for all health visibility tiers."""
    auditor = HealthSecurityAuditor()
    report = auditor.audit_security()
    return asdict(report)


@router.get("/automation")
def get_automation_compatibility() -> Dict[str, Any]:
    """Return Docker HEALTHCHECK, Kubernetes probes, and CI/CD gating spec."""
    verifier = OrchestrationAutomationVerifier()
    report = verifier.verify_automation_integration()
    return asdict(report)


@router.get("/live")
def get_liveness():
    """Liveness probe: Evaluates process integrity only without touching external deps."""
    manager = HealthContractManager()
    return manager.execute_liveness()


@router.get("/ready")
def get_readiness():
    """Readiness probe: Evaluates traffic readiness against critical dependencies."""
    manager = HealthContractManager()
    return manager.execute_readiness()


@router.get("/health")
def get_full_health(authorization: Optional[str] = Header(None)):
    """Full health endpoint: Returns detailed subsystem telemetry."""
    manager = HealthContractManager()
    return manager.execute_full_health(authorization=authorization)
