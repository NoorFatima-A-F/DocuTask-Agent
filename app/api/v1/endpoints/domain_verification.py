"""
FastAPI REST Gateway for Enterprise Verification Domain Model & Data Architecture.
Part 1.2 of the Enterprise Verification Platform.
"""
from typing import List
from fastapi import APIRouter, HTTPException, Depends

from app.platform_verification.domain_model.domain.verification_management import (
    VerificationDefinition
)
from app.platform_verification.domain_model.domain.verification_plan import VerificationPlan
from app.platform_verification.domain_model.domain.dataset_management import Dataset
from app.platform_verification.domain_model.domain.execution_management import VerificationExecution
from app.platform_verification.domain_model.domain.evidence_management import EvidenceArtifact
from app.platform_verification.domain_model.domain.metrics_management import MetricResult
from app.platform_verification.domain_model.domain.certification_management import Certification
from app.platform_verification.domain_model.domain.audit_management import AuditRecord
from app.platform_verification.domain_model.runtime.verification_domain_runtime import (
    VerificationDomainRuntime, verification_domain_runtime
)

router = APIRouter(tags=["Enterprise Verification Domain Model & Data Architecture"])

def get_domain_runtime() -> VerificationDomainRuntime:
    return verification_domain_runtime


# 1. Definitions
@router.get("/definitions", response_model=List[VerificationDefinition])
def list_definitions(runtime: VerificationDomainRuntime = Depends(get_domain_runtime)):
    return runtime.repo.list_definitions()


@router.post("/definitions", response_model=VerificationDefinition)
def create_definition(
    definition: VerificationDefinition,
    runtime: VerificationDomainRuntime = Depends(get_domain_runtime)
):
    saved = runtime.repo.save_definition(definition)
    runtime.repo.append_audit_record(
        entity_type="VerificationDefinition",
        entity_id=saved.definition_id,
        action="CREATE",
        new_state=saved.model_dump()
    )
    return saved


# 2. Plans
@router.get("/plans", response_model=List[VerificationPlan])
def list_plans(runtime: VerificationDomainRuntime = Depends(get_domain_runtime)):
    return list(runtime.repo.plans.values())


@router.post("/plans", response_model=VerificationPlan)
def create_plan(
    plan: VerificationPlan,
    runtime: VerificationDomainRuntime = Depends(get_domain_runtime)
):
    saved = runtime.repo.save_plan(plan)
    runtime.repo.append_audit_record(
        entity_type="VerificationPlan",
        entity_id=saved.plan_id,
        action="CREATE",
        new_state=saved.model_dump()
    )
    return saved


# 3. Datasets
@router.get("/datasets", response_model=List[Dataset])
def list_datasets(runtime: VerificationDomainRuntime = Depends(get_domain_runtime)):
    return list(runtime.repo.datasets.values())


# 4. Executions
@router.get("/executions", response_model=List[VerificationExecution])
def list_executions(runtime: VerificationDomainRuntime = Depends(get_domain_runtime)):
    return runtime.repo.list_executions()


@router.get("/executions/{execution_id}", response_model=VerificationExecution)
def get_execution(
    execution_id: str,
    runtime: VerificationDomainRuntime = Depends(get_domain_runtime)
):
    ex = runtime.repo.get_execution(execution_id)
    if not ex:
        raise HTTPException(status_code=404, detail=f"Execution '{execution_id}' not found.")
    return ex


# 5. Evidence
@router.get("/evidence/{execution_id}", response_model=List[EvidenceArtifact])
def get_evidence_for_execution(
    execution_id: str,
    runtime: VerificationDomainRuntime = Depends(get_domain_runtime)
):
    return runtime.repo.get_evidence_for_execution(execution_id)


# 6. Metrics
@router.get("/metrics/{execution_id}", response_model=List[MetricResult])
def get_metrics_for_execution(
    execution_id: str,
    runtime: VerificationDomainRuntime = Depends(get_domain_runtime)
):
    return runtime.repo.get_metrics_for_execution(execution_id)


# 7. Certifications
@router.get("/certifications", response_model=List[Certification])
def list_certifications(runtime: VerificationDomainRuntime = Depends(get_domain_runtime)):
    return list(runtime.repo.certifications.values())


# 8. Provenance & Evidence Graph Lineage
@router.get("/lineage/provenance/{certification_id}")
def get_provenance_chain(
    certification_id: str,
    runtime: VerificationDomainRuntime = Depends(get_domain_runtime)
):
    try:
        return runtime.lineage.build_provenance_chain(certification_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# 9. Audit Trail
@router.get("/audit", response_model=List[AuditRecord])
def get_audit_trail(runtime: VerificationDomainRuntime = Depends(get_domain_runtime)):
    return runtime.repo.list_audit_trail()
