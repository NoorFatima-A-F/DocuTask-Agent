"""
FastAPI Endpoints for Phase 13.22 Enterprise Cognitive Intelligence & Autonomous Organizational Learning Platform (ECIAOLP)
"""
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from app.platform_cognitive.runtime.cognitive_master_orchestrator import cognitive_orchestrator
from app.platform_cognitive.models.schemas import (
    ExperienceMemoryEntry, DiscoveredProcess,
    DecisionRecord, Hypothesis, SimulationScenario, OptimizationOpportunity,
    GoalAlignmentNode, StrategicRecommendation, ExecutiveInsightReport
)

router = APIRouter(tags=["Enterprise Cognitive Intelligence & Autonomous Learning"])

class RecordDecisionRequest(BaseModel):
    tenant_id: str = "default-tenant"
    topic: str
    chosen_action: str
    alternatives: List[str] = Field(default_factory=list)
    rationale: str
    confidence: float = 0.95
    expected_outcome: Dict[str, Any] = Field(default_factory=dict)

class ResolveDecisionRequest(BaseModel):
    actual_outcome: Dict[str, Any]
    matched: bool = True

class StoreExperienceRequest(BaseModel):
    tenant_id: str = "default-tenant"
    task_fingerprint: str
    agent_id: str
    input_pattern: str
    successful_trace: List[str] = Field(default_factory=list)
    metrics: Dict[str, float] = Field(default_factory=dict)
    reusable_knowledge: str

class SimulateScenarioRequest(BaseModel):
    tenant_id: str = "default-tenant"
    scenario_name: str
    parameter_overrides: Dict[str, Any] = Field(default_factory=dict)

class ProcessAnalysisRequest(BaseModel):
    tenant_id: str = "default-tenant"
    log_stream: List[Dict[str, Any]] = Field(default_factory=list)

# 1. Executive Insights & Health
@router.get("/executive-insights", response_model=ExecutiveInsightReport)
def get_executive_insights(tenant_id: str = Query("default-tenant")):
    return cognitive_orchestrator.get_executive_insight_report(tenant_id)

@router.get("/health")
def get_cognitive_health(tenant_id: str = Query("default-tenant")):
    report = cognitive_orchestrator.get_executive_insight_report(tenant_id)
    return {
        "tenant_id": tenant_id,
        "status": "OPERATIONAL",
        "cognitive_health_index": report.cognitive_health_index,
        "active_hypotheses": report.active_hypotheses_count,
        "reused_experiences": report.experience_memories_reused_count
    }

# 2. Strategic Recommendations
@router.get("/recommendations", response_model=List[StrategicRecommendation])
def get_strategic_recommendations(tenant_id: str = Query("default-tenant")):
    return cognitive_orchestrator.recommendations_engine.generate_recommendations(tenant_id)

# 3. Organizational Learning
@router.get("/learning/insights", response_model=List[Dict[str, Any]])
def get_learning_insights(tenant_id: str = Query("default-tenant")):
    # Trigger trace processing if empty
    insights = cognitive_orchestrator.learning_engine.list_insights(tenant_id)
    if not insights:
        cognitive_orchestrator.learning_engine.process_execution_traces(tenant_id, [])
        insights = cognitive_orchestrator.learning_engine.list_insights(tenant_id)
    return insights

# 4. Cross-Agent Experience Memory
@router.get("/experience-memory", response_model=List[ExperienceMemoryEntry])
def list_experience_memory(
    tenant_id: str = Query("default-tenant"),
    query: Optional[str] = None
):
    if query:
        return cognitive_orchestrator.experience_memory.query_experience(tenant_id, query)
    return cognitive_orchestrator.experience_memory.list_all_experiences(tenant_id)

@router.post("/experience-memory/store", response_model=ExperienceMemoryEntry)
def store_experience_memory(payload: StoreExperienceRequest):
    return cognitive_orchestrator.experience_memory.store_experience(
        tenant_id=payload.tenant_id,
        task_fingerprint=payload.task_fingerprint,
        agent_id=payload.agent_id,
        input_pattern=payload.input_pattern,
        successful_trace=payload.successful_trace,
        metrics=payload.metrics,
        reusable_knowledge=payload.reusable_knowledge
    )

# 5. Process Discovery & Mining
@router.post("/process-discovery/analyze", response_model=DiscoveredProcess)
def analyze_process_discovery(payload: ProcessAnalysisRequest):
    return cognitive_orchestrator.process_discovery.discover_from_logs(
        tenant_id=payload.tenant_id,
        log_stream=payload.log_stream
    )

@router.get("/process-discovery/list", response_model=List[DiscoveredProcess])
def list_discovered_processes(tenant_id: str = Query("default-tenant")):
    procs = cognitive_orchestrator.process_discovery.list_discovered_processes(tenant_id)
    if not procs:
        cognitive_orchestrator.process_discovery.discover_from_logs(tenant_id, [])
        procs = cognitive_orchestrator.process_discovery.list_discovered_processes(tenant_id)
    return procs

# 6. Enterprise Decision Intelligence
@router.post("/decision/record", response_model=DecisionRecord)
def record_decision(payload: RecordDecisionRequest):
    return cognitive_orchestrator.decision_intelligence.record_decision(
        tenant_id=payload.tenant_id,
        topic=payload.topic,
        chosen_action=payload.chosen_action,
        alternatives=payload.alternatives,
        rationale=payload.rationale,
        confidence=payload.confidence,
        expected_outcome=payload.expected_outcome
    )

@router.get("/decision-history", response_model=List[DecisionRecord])
def list_decision_history(tenant_id: str = Query("default-tenant")):
    return cognitive_orchestrator.decision_intelligence.list_decisions(tenant_id)

@router.post("/decision/{decision_id}/resolve", response_model=DecisionRecord)
def resolve_decision_outcome(
    decision_id: str,
    payload: ResolveDecisionRequest,
    tenant_id: str = Query("default-tenant")
):
    resolved = cognitive_orchestrator.decision_intelligence.resolve_actual_outcome(
        decision_id=decision_id,
        tenant_id=tenant_id,
        actual_outcome=payload.actual_outcome,
        matched=payload.matched
    )
    if not resolved:
        raise HTTPException(status_code=404, detail="Decision record not found")
    return resolved

# 7. Hypothesis Generation
@router.post("/hypothesis/generate", response_model=List[Hypothesis])
def generate_hypotheses(tenant_id: str = Query("default-tenant")):
    return cognitive_orchestrator.hypothesis_engine.generate_hypotheses(tenant_id)

@router.get("/hypothesis/list", response_model=List[Hypothesis])
def list_hypotheses(tenant_id: str = Query("default-tenant")):
    hyps = cognitive_orchestrator.hypothesis_engine.list_hypotheses(tenant_id)
    if not hyps:
        hyps = cognitive_orchestrator.hypothesis_engine.generate_hypotheses(tenant_id)
    return hyps

# 8. Business Simulation
@router.post("/simulate", response_model=SimulationScenario)
def simulate_scenario(payload: SimulateScenarioRequest):
    return cognitive_orchestrator.simulation_engine.simulate_scenario(
        tenant_id=payload.tenant_id,
        scenario_name=payload.scenario_name,
        overrides=payload.parameter_overrides
    )

# 9. Autonomous Optimization
@router.get("/optimization/opportunities", response_model=List[OptimizationOpportunity])
def list_optimization_opportunities(tenant_id: str = Query("default-tenant")):
    return cognitive_orchestrator.optimization_engine.discover_opportunities(tenant_id)

@router.post("/optimize/execute")
def execute_optimization(
    opportunity_id: str = Query(...),
    tenant_id: str = Query("default-tenant")
):
    return cognitive_orchestrator.optimization_engine.apply_optimization(opportunity_id, tenant_id)

# 10. Goal Alignment
@router.get("/goal-alignment", response_model=List[GoalAlignmentNode])
def get_goal_alignment(tenant_id: str = Query("default-tenant")):
    return cognitive_orchestrator.goal_alignment.get_alignments(tenant_id)

# 11. Cognitive Reasoning Graph
@router.get("/cognitive-graph")
def get_cognitive_graph(tenant_id: str = Query("default-tenant")):
    return cognitive_orchestrator.graph_engine.get_overview(tenant_id)
