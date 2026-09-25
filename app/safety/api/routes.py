"""FastAPI REST API Routes for Safety Gateway & Incident Management."""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from ..gateway.context import SafetyContext, ModelContext, PromptContext
from ..gateway.runtime import SafetyGateway
from ..incidents.lifecycle import IncidentLifecycleState, SafetyIncident
from ..gateway.decision import ViolationSeverity
from .schemas import (
    GuardInputRequest,
    GuardInputResponse,
    GuardOutputRequest,
    GuardOutputResponse,
    ValidateToolRequest,
    ValidateToolResponse,
    VerifyGroundingRequest,
    VerifyGroundingResponse,
    IncidentCreateRequest,
    IncidentTransitionRequest,
)

router = APIRouter(prefix="/api/v1/safety", tags=["AI Safety & Runtime Guardrails"])

# Global gateway singleton
safety_gateway = SafetyGateway()


@router.post("/guard/input", response_model=GuardInputResponse)
def guard_input(request: GuardInputRequest):
    context = SafetyContext(
        tenant_id=request.tenant_id,
        user_id=request.user_id,
        agent_id=request.agent_id,
        raw_input=request.raw_input,
        source_trust=request.source_trust,
        model_context=ModelContext(model_id=request.model_id) if request.model_id else None,
        knowledge_chunks=request.knowledge_chunks,
    )
    decision = safety_gateway.inspect_input(context)
    return GuardInputResponse(
        decision_id=decision.decision_id,
        is_allowed=decision.is_allowed,
        status=decision.status,
        sanitized_input=decision.sanitized_content,
        composite_risk_score=decision.composite_risk_score,
        violations=decision.violations,
        explanation=decision.explanation,
    )


@router.post("/guard/output", response_model=GuardOutputResponse)
def guard_output(request: GuardOutputRequest):
    context = SafetyContext(
        tenant_id=request.tenant_id,
        generated_output=request.generated_output,
        prompt_context=PromptContext(system_prompt=request.system_prompt) if request.system_prompt else None,
        knowledge_chunks=request.knowledge_chunks,
    )
    decision = safety_gateway.inspect_output(context)
    return GuardOutputResponse(
        decision_id=decision.decision_id,
        is_allowed=decision.is_allowed,
        status=decision.status,
        sanitized_output=decision.sanitized_content,
        composite_risk_score=decision.composite_risk_score,
        violations=decision.violations,
        explanation=decision.explanation,
    )


@router.post("/tools/validate", response_model=ValidateToolResponse)
def validate_tool(request: ValidateToolRequest):
    context = SafetyContext(tenant_id=request.tenant_id)
    decision = safety_gateway.inspect_tool(
        context=context,
        tool_name=request.tool_name,
        parameters=request.parameters,
        user_role=request.user_role,
        is_dry_run=request.is_dry_run,
    )
    return ValidateToolResponse(
        is_allowed=decision.is_allowed,
        status=decision.status,
        violations=decision.violations,
        explanation=decision.explanation,
    )


@router.post("/grounding/verify", response_model=VerifyGroundingResponse)
def verify_grounding(request: VerifyGroundingRequest):
    report = safety_gateway.pipeline.hallucination_detector.grounding_verifier.verify_grounding(
        output_text=request.output_text,
        knowledge_chunks=request.knowledge_chunks,
    )
    return VerifyGroundingResponse(
        is_grounded=report.is_grounded,
        grounding_score=report.grounding_score,
        total_claims=report.total_claims,
        grounded_claims=report.grounded_claims,
        citations_mapped=report.citations_mapped,
    )


@router.post("/incidents", response_model=SafetyIncident)
def create_incident(request: IncidentCreateRequest):
    return safety_gateway.incident_manager.create_incident(
        tenant_id=request.tenant_id,
        title=request.title,
        description=request.description,
        category=request.category,
        severity=request.severity,
        context_id=request.context_id,
        user_id=request.user_id,
        agent_id=request.agent_id,
    )


@router.get("/incidents", response_model=List[SafetyIncident])
def list_incidents(
    tenant_id: str = Query(...),
    state: Optional[IncidentLifecycleState] = None,
    severity: Optional[ViolationSeverity] = None,
):
    return safety_gateway.incident_manager.list_incidents(
        tenant_id=tenant_id,
        state=state,
        severity=severity,
    )


@router.get("/incidents/{incident_id}", response_model=SafetyIncident)
def get_incident(incident_id: str, tenant_id: Optional[str] = None):
    incident = safety_gateway.incident_manager.get_incident(incident_id, tenant_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident


@router.post("/incidents/{incident_id}/transition", response_model=SafetyIncident)
def transition_incident(incident_id: str, request: IncidentTransitionRequest, tenant_id: Optional[str] = None):
    try:
        return safety_gateway.incident_manager.transition_state(
            incident_id=incident_id,
            new_state=request.new_state,
            actor=request.actor,
            notes=request.notes,
            tenant_id=tenant_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
