"""
Phase 13.17: AI Operations REST API Endpoints
Enterprise Agent Observability, Evaluation, Optimization & Controlled Self-Improvement.
"""

from __future__ import annotations
from typing import Dict, List, Optional, Any
from fastapi import APIRouter, HTTPException, Query, Body
from pydantic import BaseModel, Field

from app.runtime.ai_operations.runtime.ai_operations_runtime import ai_operations_runtime
from app.runtime.ai_operations.models.schemas import (
    Span,
    ExecutionTrace,
    AgentTelemetry,
    EvaluationResult,
    FailureAnalysisResult,
    ModelRouteDecision,
    PromptVersion,
    ImprovementProposal,
    ExperimentRecord,
    GovernanceAuditRecord,
    ProposalStatus,
)

router = APIRouter()


class RouteTaskRequest(BaseModel):
    task_id: str = "task_001"
    estimated_prompt_tokens: int = 1500
    estimated_completion_tokens: int = 500
    weight_quality: float = 0.50
    weight_latency: float = 0.30
    weight_cost: float = 0.20
    max_latency_sla_ms: Optional[float] = None
    max_cost_budget_usd: Optional[float] = None


class RunExperimentRequest(BaseModel):
    name: str = "A/B Canary Test"
    agent_id: str
    control_version: str = "v1.0.0"
    candidate_version: str = "v1.1.0"
    sample_size: int = 100


class ProposalDecisionRequest(BaseModel):
    actor: str = "Enterprise Administrator"
    reason: Optional[str] = None


class CycleRunRequest(BaseModel):
    agent_id: Optional[str] = "agent_chief_architect"


@router.get("/overview", summary="High-level AI operations metrics and fleet health")
async def get_operations_overview() -> Dict[str, Any]:
    return ai_operations_runtime.telemetry.get_overview_metrics()


@router.get("/telemetry/agents", summary="Fleet agent telemetry and performance", response_model=List[AgentTelemetry])
async def get_agent_telemetry() -> List[AgentTelemetry]:
    return ai_operations_runtime.telemetry.get_fleet_telemetry()


@router.get("/telemetry/traces", summary="List execution traces", response_model=List[ExecutionTrace])
async def get_execution_traces(
    limit: int = Query(50, ge=1, le=500),
    agent_id: Optional[str] = Query(None),
) -> List[ExecutionTrace]:
    return ai_operations_runtime.telemetry.collector.list_traces(limit=limit, agent_id=agent_id)


@router.get("/telemetry/traces/{trace_id}", summary="Get detailed trace by ID", response_model=ExecutionTrace)
async def get_trace_by_id(trace_id: str) -> ExecutionTrace:
    trace = ai_operations_runtime.telemetry.collector.get_trace(trace_id)
    if not trace:
        raise HTTPException(status_code=404, detail=f"Trace {trace_id} not found")
    return trace


@router.get("/evaluation/results", summary="Get continuous evaluation benchmark history", response_model=List[EvaluationResult])
async def get_evaluation_results(
    limit: int = Query(50, ge=1, le=500),
    agent_id: Optional[str] = Query(None),
) -> List[EvaluationResult]:
    return ai_operations_runtime.evaluation.get_evaluation_history(limit=limit, agent_id=agent_id)


@router.post("/optimization/model-route", summary="Evaluate Pareto optimal model selection", response_model=ModelRouteDecision)
async def route_model(request: RouteTaskRequest) -> ModelRouteDecision:
    return ai_operations_runtime.model_router.route_task(
        task_id=request.task_id,
        estimated_prompt_tokens=request.estimated_prompt_tokens,
        estimated_completion_tokens=request.estimated_completion_tokens,
        weight_quality=request.weight_quality,
        weight_latency=request.weight_latency,
        weight_cost=request.weight_cost,
        max_latency_sla_ms=request.max_latency_sla_ms,
        max_cost_budget_usd=request.max_cost_budget_usd,
    )


@router.get("/optimization/prompts", summary="List prompt laboratory versions", response_model=List[PromptVersion])
async def get_prompts(agent_id: Optional[str] = Query(None)) -> List[PromptVersion]:
    if agent_id:
        return ai_operations_runtime.prompt_optimizer.get_prompt_versions(agent_id)
    return ai_operations_runtime.prompt_optimizer.get_all_prompts()


@router.get("/cost/analytics", summary="Get token and cost analytics with projections")
async def get_cost_analytics() -> Dict[str, Any]:
    fleet = ai_operations_runtime.telemetry.get_fleet_telemetry()
    return ai_operations_runtime.cost_optimizer.calculate_cost_analytics(fleet)


@router.get("/debugging/failures", summary="List failure classifications and root-cause diagnoses", response_model=List[FailureAnalysisResult])
async def get_failure_diagnoses(
    limit: int = Query(50, ge=1, le=500),
    agent_id: Optional[str] = Query(None),
) -> List[FailureAnalysisResult]:
    return ai_operations_runtime.debugging.get_failure_logs(limit=limit, agent_id=agent_id)


@router.get("/prediction/risks", summary="Get predictive failure & risk alerts")
async def get_predictive_risks(limit: int = Query(20, ge=1, le=100)) -> List[Dict[str, Any]]:
    return ai_operations_runtime.prediction.get_active_predictions(limit=limit)


@router.get("/improvement/proposals", summary="List self-improvement proposals", response_model=List[ImprovementProposal])
async def get_proposals(agent_id: Optional[str] = Query(None)) -> List[ImprovementProposal]:
    return ai_operations_runtime.improvement.list_proposals(agent_id=agent_id)


@router.post("/improvement/proposals/{proposal_id}/approve", summary="HITL Approval for proposal deployment", response_model=ImprovementProposal)
async def approve_proposal(proposal_id: str, request: ProposalDecisionRequest) -> ImprovementProposal:
    prop = ai_operations_runtime.improvement.approve_proposal(proposal_id, approved_by=request.actor)
    if not prop:
        raise HTTPException(status_code=404, detail=f"Proposal {proposal_id} not found")
    ai_operations_runtime.governance.log_event(
        event_type="PROPOSAL_APPROVED",
        actor=request.actor,
        action_summary=f"Approved proposal {proposal_id} for deployment.",
        agent_id=prop.target_agent_id,
        compliance_passed=True,
        policy_name="HITL_CHANGE_MANAGEMENT",
    )
    return prop


@router.post("/improvement/proposals/{proposal_id}/reject", summary="Reject improvement proposal", response_model=ImprovementProposal)
async def reject_proposal(proposal_id: str, request: ProposalDecisionRequest) -> ImprovementProposal:
    prop = ai_operations_runtime.improvement.reject_proposal(proposal_id, reason=request.reason or "Rejected by user")
    if not prop:
        raise HTTPException(status_code=404, detail=f"Proposal {proposal_id} not found")
    ai_operations_runtime.governance.log_event(
        event_type="PROPOSAL_REJECTED",
        actor=request.actor,
        action_summary=f"Rejected proposal {proposal_id}. Reason: {request.reason}",
        agent_id=prop.target_agent_id,
        compliance_passed=True,
    )
    return prop


@router.get("/experiments", summary="List A/B canary experiment results", response_model=List[ExperimentRecord])
async def list_experiments() -> List[ExperimentRecord]:
    return ai_operations_runtime.experiment.list_experiments()


@router.post("/experiments/run", summary="Run A/B canary experiment", response_model=ExperimentRecord)
async def run_experiment(request: RunExperimentRequest) -> ExperimentRecord:
    return ai_operations_runtime.experiment.run_experiment(
        name=request.name,
        agent_id=request.agent_id,
        control_version=request.control_version,
        candidate_version=request.candidate_version,
        sample_size=request.sample_size,
    )


@router.get("/governance/audit-logs", summary="List governance & compliance audit logs", response_model=List[GovernanceAuditRecord])
async def get_governance_audit_logs(
    limit: int = Query(50, ge=1, le=500),
    agent_id: Optional[str] = Query(None),
) -> List[GovernanceAuditRecord]:
    return ai_operations_runtime.governance.get_audit_logs(limit=limit, agent_id=agent_id)


@router.post("/runtime/cycle", summary="Execute autonomous AI operations control plane cycle")
async def execute_operations_cycle(request: CycleRunRequest) -> Dict[str, Any]:
    return await ai_operations_runtime.execute_operations_cycle(target_agent_id=request.agent_id)
