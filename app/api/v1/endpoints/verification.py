"""
FastAPI REST & SSE Gateway for the Enterprise Verification Platform.
Exposes the 15 Core Components and lifecycle actions.
"""
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from app.platform_verification.runtime.enterprise_verification_runtime import EnterpriseVerificationRuntime
from app.platform_verification.domain.models import (
    VerificationDefinition,
    VerificationRun,
    DatasetRecord,
    EnvironmentReadiness,
    EvidenceItem,
    AuditEntry,
    TraceabilityNode,
    PluginDescriptor,
    ComponentHealth,
)

router = APIRouter(tags=["Enterprise Verification Platform"])

def get_runtime() -> EnterpriseVerificationRuntime:
    return EnterpriseVerificationRuntime.get_instance()

# 1. Overview & Components Health
@router.get("/overview", response_model=Dict[str, Any])
def get_verification_overview(runtime: EnterpriseVerificationRuntime = Depends(get_runtime)):
    return runtime.get_overview()

@router.get("/components/health", response_model=List[ComponentHealth])
def get_components_health(runtime: EnterpriseVerificationRuntime = Depends(get_runtime)):
    return runtime.get_components_health()

# 2. Orchestrator & Runs
@router.get("/runs", response_model=List[VerificationRun])
def list_verification_runs(runtime: EnterpriseVerificationRuntime = Depends(get_runtime)):
    return runtime.orchestrator.list_runs()

@router.get("/runs/{run_id}", response_model=VerificationRun)
def get_verification_run(run_id: str, runtime: EnterpriseVerificationRuntime = Depends(get_runtime)):
    run = runtime.orchestrator.get_run_status(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return run

@router.post("/runs/execute/{definition_id}", response_model=VerificationRun)
def trigger_verification_run(definition_id: str, environment_id: str = "env_integration", runtime: EnterpriseVerificationRuntime = Depends(get_runtime)):
    try:
        return runtime.orchestrator.orchestrate_verification(definition_id, environment_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/runs/{run_id}/cancel")
def cancel_verification_run(run_id: str, runtime: EnterpriseVerificationRuntime = Depends(get_runtime)):
    success = runtime.orchestrator.cancel_execution(run_id)
    if not success:
        raise HTTPException(status_code=404, detail="Run not found or cannot be cancelled")
    return {"status": "CANCELLED", "run_id": run_id}

# 3. Definitions Manager
@router.get("/definitions", response_model=List[VerificationDefinition])
def list_definitions(runtime: EnterpriseVerificationRuntime = Depends(get_runtime)):
    return runtime.definition_mgr.list_definitions()

@router.post("/definitions", response_model=VerificationDefinition)
def create_definition(definition: VerificationDefinition, runtime: EnterpriseVerificationRuntime = Depends(get_runtime)):
    return runtime.definition_mgr.create_definition(definition)

# 4. Registry & Plugins
@router.get("/plugins", response_model=List[PluginDescriptor])
def list_plugins(domain: Optional[str] = None, runtime: EnterpriseVerificationRuntime = Depends(get_runtime)):
    return runtime.registry.list_plugins(domain)

# 5. Datasets Manager (11 Classes)
@router.get("/datasets", response_model=List[DatasetRecord])
def list_datasets(runtime: EnterpriseVerificationRuntime = Depends(get_runtime)):
    return runtime.dataset_mgr.list_datasets()

@router.post("/datasets", response_model=DatasetRecord)
def register_dataset(dataset: DatasetRecord, runtime: EnterpriseVerificationRuntime = Depends(get_runtime)):
    return runtime.dataset_mgr.register_dataset(dataset)

# 6. Environments Manager
@router.get("/environments", response_model=List[EnvironmentReadiness])
def list_environments(runtime: EnterpriseVerificationRuntime = Depends(get_runtime)):
    return runtime.env_mgr.list_environments()

# 7. Evidence Manager
@router.get("/evidence", response_model=List[EvidenceItem])
def list_evidence(run_id: Optional[str] = None, runtime: EnterpriseVerificationRuntime = Depends(get_runtime)):
    return runtime.evidence_mgr.list_evidence(run_id)

class EvidenceVerificationRequest(BaseModel):
    evidence_id: str
    raw_payload: Optional[Any] = None

@router.post("/evidence/verify")
def verify_evidence(request: EvidenceVerificationRequest, runtime: EnterpriseVerificationRuntime = Depends(get_runtime)):
    is_valid = runtime.evidence_mgr.verify_evidence_integrity(request.evidence_id, request.raw_payload)
    return {"evidence_id": request.evidence_id, "is_valid": is_valid, "tamper_detected": not is_valid}

# 8. Audit Ledger & Chain Integrity
@router.get("/audit", response_model=List[AuditEntry])
def get_audit_trail(entity_id: Optional[str] = None, runtime: EnterpriseVerificationRuntime = Depends(get_runtime)):
    return runtime.audit_mgr.get_audit_trail(entity_id)

@router.get("/audit/verify-chain")
def verify_audit_chain(runtime: EnterpriseVerificationRuntime = Depends(get_runtime)):
    is_valid = runtime.audit_mgr.verify_chain_integrity()
    return {"chain_integrity_valid": is_valid, "total_entries": len(runtime.audit_mgr.get_audit_trail())}

# 9. Traceability Graph Lineage
@router.get("/traceability/{root_id}", response_model=List[TraceabilityNode])
def get_lineage(root_id: str, runtime: EnterpriseVerificationRuntime = Depends(get_runtime)):
    return runtime.traceability_mgr.get_lineage(root_id)
