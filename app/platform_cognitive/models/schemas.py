"""
Phase 13.22 - Enterprise Cognitive Intelligence & Autonomous Organizational Learning Platform (ECIAOLP) Schemas
"""
from __future__ import annotations
from enum import Enum
from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from pydantic import BaseModel, Field
import uuid

class ReasoningNodeType(str, Enum):
    AGENT = "AGENT"
    PROJECT = "PROJECT"
    CUSTOMER = "CUSTOMER"
    BUSINESS_GOAL = "BUSINESS_GOAL"
    KPI = "KPI"
    INCIDENT = "INCIDENT"
    WORKFLOW = "WORKFLOW"
    POLICY = "POLICY"
    RISK = "RISK"
    DECISION = "DECISION"
    HYPOTHESIS = "HYPOTHESIS"

class ReasoningRelationType(str, Enum):
    CAUSED_BY = "caused_by"
    INFLUENCES = "influences"
    DEPENDS_ON = "depends_on"
    CONTRADICTS = "contradicts"
    RECOMMENDS = "recommends"
    IMPROVES = "improves"
    BLOCKED_BY = "blocked_by"
    VALIDATES = "validates"
    PREDICTS = "predicts"

class CognitiveNode(BaseModel):
    id: str = Field(default_factory=lambda: f"cnode-{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default-tenant"
    node_type: ReasoningNodeType
    name: str
    description: str = ""
    properties: Dict[str, Any] = Field(default_factory=dict)
    confidence: float = 1.0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class CognitiveEdge(BaseModel):
    id: str = Field(default_factory=lambda: f"cedge-{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default-tenant"
    source_node_id: str
    target_node_id: str
    relation: ReasoningRelationType
    weight: float = 1.0
    evidence: str = ""
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ExperienceMemoryEntry(BaseModel):
    id: str = Field(default_factory=lambda: f"exp-{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default-tenant"
    task_fingerprint: str
    agent_id: str
    input_pattern: str
    successful_execution_trace: List[str] = Field(default_factory=list)
    performance_metrics: Dict[str, float] = Field(default_factory=dict)  # latency_ms, cost_usd, quality_score
    reusable_knowledge: str
    reuse_count: int = 0
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class DiscoveredProcess(BaseModel):
    id: str = Field(default_factory=lambda: f"proc-{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default-tenant"
    process_name: str
    reconstructed_steps: List[str] = Field(default_factory=list)
    observed_executions_count: int = 0
    avg_cycle_time_seconds: float = 0.0
    bottlenecks: List[str] = Field(default_factory=list)
    automation_opportunity_score: float = 0.85
    discovered_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class DecisionRecord(BaseModel):
    id: str = Field(default_factory=lambda: f"dec-{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default-tenant"
    decision_topic: str
    chosen_action: str
    alternatives_considered: List[str] = Field(default_factory=list)
    reasoning_rationale: str
    risk_level: str = "LOW"
    confidence_score: float = 0.95
    expected_outcome: Dict[str, Any] = Field(default_factory=dict)
    actual_outcome: Optional[Dict[str, Any]] = None
    outcome_matched: Optional[bool] = None
    decided_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    resolved_at: Optional[datetime] = None

class Hypothesis(BaseModel):
    id: str = Field(default_factory=lambda: f"hyp-{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default-tenant"
    statement: str
    supporting_evidence: List[str] = Field(default_factory=list)
    confidence_score: float = 0.88
    suggested_action: str
    impact_area: str = "OPERATIONS"  # "COST", "LATENCY", "SUPPLY_CHAIN", "QUALITY"
    status: str = "PROPOSED"  # "PROPOSED", "VALIDATED", "DISPROVED", "EXECUTED"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class SimulationScenario(BaseModel):
    id: str = Field(default_factory=lambda: f"sim-{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default-tenant"
    scenario_name: str
    parameter_overrides: Dict[str, Any] = Field(default_factory=dict)
    projected_latency_change_pct: float = -25.0
    projected_cost_change_pct: float = -18.0
    projected_roi_factor: float = 2.4
    risk_assessment: str = "LOW"

class OptimizationOpportunity(BaseModel):
    id: str = Field(default_factory=lambda: f"opt-{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default-tenant"
    subsystem: str  # "PROMPT", "MODEL_ROUTING", "WORKER_FLEET", "CACHE"
    target_resource: str
    recommended_change: str
    projected_savings_monthly_usd: float = 1250.0
    status: str = "READY_TO_APPLY"

class GoalAlignmentNode(BaseModel):
    id: str = Field(default_factory=lambda: f"goal-{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default-tenant"
    corporate_kpi: str
    business_goal: str
    department_goal: str
    assigned_agents: List[str] = Field(default_factory=list)
    current_progress_pct: float = 82.5
    alignment_health: str = "HEALTHY"

class StrategicRecommendation(BaseModel):
    id: str = Field(default_factory=lambda: f"rec-{uuid.uuid4().hex[:8]}")
    tenant_id: str = "default-tenant"
    category: str  # "HIRING", "AUTOMATION", "RISK_PREVENTION", "BUDGET", "MODEL_UPGRADE"
    title: str
    description: str
    urgency: str = "HIGH"
    projected_business_impact: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ExecutiveInsightReport(BaseModel):
    tenant_id: str
    cognitive_health_index: float = 0.98
    active_hypotheses_count: int = 5
    discovered_processes_count: int = 8
    experience_memories_reused_count: int = 1420
    strategic_recommendations: List[StrategicRecommendation] = Field(default_factory=list)
    active_optimizations: List[OptimizationOpportunity] = Field(default_factory=list)
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
