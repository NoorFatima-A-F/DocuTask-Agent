"""FastAPI Router for Enterprise Prompt Governance (Phase 8D)."""

from __future__ import annotations

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, status
from app.prompts.registry.models import Prompt, PromptCategory, PromptLifecycleState, PromptVersion
from app.prompts.registry.repository import PromptRegistryRepository
from app.prompts.registry.service import PromptRegistryService
from app.prompts.lifecycle.manager import PromptLifecycleManager
from app.prompts.approvals.workflow import PromptApprovalWorkflowEngine
from app.prompts.deployment.publisher import PromptPublisher
from app.prompts.templates.engine import PromptTemplateEngine
from app.prompts.security.validation import PromptSecurityValidator
from app.prompts.api.schemas import (
    PromptApprovalReviewRequestDTO,
    PromptCreateRequestDTO,
    PromptDeployRequestDTO,
    PromptLifecycleTransitionRequestDTO,
    PromptRenderRequestDTO,
    PromptVersionCreateRequestDTO,
)


router = APIRouter(prefix="/api/v1/governance/prompts", tags=["Prompt Governance"])

# Shared service instances
_repo = PromptRegistryRepository()
_registry_service = PromptRegistryService(_repo)
_lifecycle_manager = PromptLifecycleManager(_repo)
_approval_engine = PromptApprovalWorkflowEngine(_repo, _lifecycle_manager)
_publisher = PromptPublisher(_repo)
_template_engine = PromptTemplateEngine()
_security_validator = PromptSecurityValidator()


@router.post("", response_model=Prompt, status_code=status.HTTP_201_CREATED)
def create_prompt(payload: PromptCreateRequestDTO, organization_id: str = Query("org_default")):
    is_safe, violations = _security_validator.validate_security(payload.initial_template)
    if not is_safe:
        raise HTTPException(status_code=400, detail=f"Security scan failed: {violations}")

    prompt, _ = _registry_service.create_prompt(
        prompt_id=payload.prompt_id,
        name=payload.name,
        organization_id=organization_id,
        owner=payload.owner,
        category=payload.category,
        description=payload.description,
        purpose=payload.purpose,
        initial_template=payload.initial_template,
        variables=payload.variables,
        risk_level=payload.risk_level,
        tags=payload.tags,
    )
    return prompt


@router.get("", response_model=List[Prompt])
def list_prompts(
    organization_id: str = Query("org_default"),
    category: Optional[PromptCategory] = None,
    state: Optional[PromptLifecycleState] = None,
):
    return _registry_service.list_prompts(organization_id=organization_id, category=category, state=state)


@router.get("/{prompt_id}", response_model=Prompt)
def get_prompt(prompt_id: str, organization_id: str = Query("org_default")):
    prompt = _registry_service.get_prompt(prompt_id, organization_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt


@router.post("/{prompt_id}/versions", response_model=PromptVersion, status_code=status.HTTP_201_CREATED)
def create_version(
    prompt_id: str,
    payload: PromptVersionCreateRequestDTO,
    organization_id: str = Query("org_default"),
):
    is_safe, violations = _security_validator.validate_security(payload.template_text)
    if not is_safe:
        raise HTTPException(status_code=400, detail=f"Security scan failed: {violations}")

    try:
        return _registry_service.create_version(
            prompt_id=prompt_id,
            organization_id=organization_id,
            prompt_template=payload.template_text,
            version_number=payload.version_number,
            created_by=payload.author,
            change_reason=payload.change_reason,
            variables=payload.variables,
            expected_output_schema=payload.expected_output_schema,
        )
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{prompt_id}/lifecycle/transition")
def transition_lifecycle(
    prompt_id: str,
    payload: PromptLifecycleTransitionRequestDTO,
    organization_id: str = Query("org_default"),
):
    try:
        return _lifecycle_manager.transition(
            prompt_id=prompt_id,
            target_state=payload.target_state,
            actor=payload.actor,
            reason=payload.reason,
            organization_id=organization_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except KeyError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{prompt_id}/approvals/{version_id}/review")
def review_approval(
    prompt_id: str,
    version_id: str,
    payload: PromptApprovalReviewRequestDTO,
    organization_id: str = Query("org_default"),
):
    return _approval_engine.review_stage(
        prompt_id=prompt_id,
        version_id=version_id,
        organization_id=organization_id,
        stage_name=payload.stage_name,
        reviewer=payload.reviewer,
        decision=payload.decision,
        comments=payload.comments,
    )


@router.post("/{prompt_id}/deploy")
def deploy_prompt(
    prompt_id: str,
    payload: PromptDeployRequestDTO,
    organization_id: str = Query("org_default"),
):
    try:
        return _publisher.deploy_version(
            prompt_id=prompt_id,
            version_id=payload.version_id,
            organization_id=organization_id,
            environment=payload.environment,
            deployed_by=payload.deployed_by,
            traffic_percentage=payload.traffic_percentage,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{prompt_id}/render")
def render_prompt(
    prompt_id: str,
    payload: PromptRenderRequestDTO,
    organization_id: str = Query("org_default"),
):
    prompt = _registry_service.get_prompt(prompt_id, organization_id)
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")

    target_vid = payload.version_id or prompt.active_version_id
    if not target_vid:
        raise HTTPException(status_code=400, detail="No active version deployed for prompt")

    version = _registry_service.get_version(prompt_id, target_vid, organization_id)
    if not version:
        raise HTTPException(status_code=404, detail="Version not found")

    rendered = _template_engine.render(
        template=version.prompt_template,
        variables=payload.variables,
    )
    return {"prompt_id": prompt_id, "version_id": target_vid, "rendered_text": rendered}
