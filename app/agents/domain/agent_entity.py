"""
Enterprise Multi-Agent Intelligence Platform (EMAIP) - Agent Domain Entities.
Defines Agent as a first-class platform resource, AgentType, AgentLifecycleState,
Goal models, and structured cognitive data structures.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
import uuid


class AgentType(str, Enum):
    """Classification of autonomous agents."""
    SUPERVISOR = "SupervisorAgent"
    COORDINATOR = "CoordinatorAgent"
    PLANNER = "PlannerAgent"
    EXECUTION = "ExecutionAgent"
    RESEARCH = "ResearchAgent"
    VALIDATION = "ValidationAgent"
    REFLECTION = "ReflectionAgent"
    CRITIC = "CriticAgent"
    RECOVERY = "RecoveryAgent"
    MEMORY = "MemoryAgent"
    KNOWLEDGE = "KnowledgeAgent"
    COMPLIANCE = "ComplianceAgent"
    SECURITY = "SecurityAgent"
    COMMUNICATION = "CommunicationAgent"
    HUMAN_LIAISON = "HumanLiaisonAgent"
    INVOICE = "InvoiceAgent"
    LEGAL = "LegalAgent"
    HEALTHCARE = "HealthcareAgent"
    FINANCE = "FinanceAgent"
    CUSTOM = "CustomAgent"


class AgentLifecycleState(str, Enum):
    """
    Formal lifecycle state machine for autonomous agents.
    Active states + Failure/Intervention states.
    """
    CREATED = "CREATED"
    REGISTERED = "REGISTERED"
    INITIALIZED = "INITIALIZED"
    PLANNING = "PLANNING"
    REASONING = "REASONING"
    EXECUTING = "EXECUTING"
    OBSERVING = "OBSERVING"
    REFLECTING = "REFLECTING"
    EVALUATING = "EVALUATING"
    CORRECTING = "CORRECTING"
    WAITING = "WAITING"
    RESUMING = "RESUMING"
    COMPLETED = "COMPLETED"
    ARCHIVED = "ARCHIVED"

    # Failure / Interrupted States
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    TIMED_OUT = "TIMED_OUT"
    BLOCKED = "BLOCKED"
    RECOVERING = "RECOVERING"
    SUSPENDED = "SUSPENDED"


class TrustLevel(str, Enum):
    """Trust and authorization classification for autonomous agents."""
    UNTRUSTED = "UNTRUSTED"
    LOW = "LOW"
    STANDARD = "STANDARD"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass
class Agent:
    """
    Agent is a first-class platform resource with governed identity,
    capabilities, permissions, memory boundaries, and execution parameters.
    """
    id: str = field(default_factory=lambda: f"agent-{uuid.uuid4().hex[:12]}")
    name: str = "EnterpriseAgent"
    type: AgentType | str = AgentType.EXECUTION
    version: str = "1.0.0"
    organization_id: str = "org-default"
    workspace_id: str = "ws-default"
    owner: str = "system"
    capabilities: List[str] = field(default_factory=list)
    skills: List[str] = field(default_factory=list)
    model: str = "gemini-2.5-flash"
    prompt_version: str = "1.0.0"
    memory_namespace: str = "default"
    policy_set: str = "enterprise_default"
    trust_level: TrustLevel | str = TrustLevel.STANDARD
    budget: Dict[str, Any] = field(default_factory=lambda: {
        "max_tokens": 100000,
        "max_cost_usd": 1.0,
        "max_execution_time_seconds": 300,
        "max_tool_calls": 50,
        "max_retries": 3,
    })
    status: AgentLifecycleState | str = AgentLifecycleState.CREATED
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type.value if isinstance(self.type, Enum) else str(self.type),
            "version": self.version,
            "organization_id": self.organization_id,
            "workspace_id": self.workspace_id,
            "owner": self.owner,
            "capabilities": list(self.capabilities),
            "skills": list(self.skills),
            "model": self.model,
            "prompt_version": self.prompt_version,
            "memory_namespace": self.memory_namespace,
            "policy_set": self.policy_set,
            "trust_level": self.trust_level.value if isinstance(self.trust_level, Enum) else str(self.trust_level),
            "budget": dict(self.budget),
            "status": self.status.value if isinstance(self.status, Enum) else str(self.status),
            "metadata": dict(self.metadata),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Agent:
        agent_type = data.get("type", AgentType.EXECUTION)
        if isinstance(agent_type, str):
            try:
                agent_type = AgentType(agent_type)
            except ValueError:
                agent_type = agent_type

        status = data.get("status", AgentLifecycleState.CREATED)
        if isinstance(status, str):
            try:
                status = AgentLifecycleState(status)
            except ValueError:
                status = status

        trust_level = data.get("trust_level", TrustLevel.STANDARD)
        if isinstance(trust_level, str):
            try:
                trust_level = TrustLevel(trust_level)
            except ValueError:
                trust_level = trust_level

        return cls(
            id=data.get("id", f"agent-{uuid.uuid4().hex[:12]}"),
            name=data.get("name", "EnterpriseAgent"),
            type=agent_type,
            version=data.get("version", "1.0.0"),
            organization_id=data.get("organization_id", "org-default"),
            workspace_id=data.get("workspace_id", "ws-default"),
            owner=data.get("owner", "system"),
            capabilities=data.get("capabilities", []),
            skills=data.get("skills", []),
            model=data.get("model", "gemini-2.5-flash"),
            prompt_version=data.get("prompt_version", "1.0.0"),
            memory_namespace=data.get("memory_namespace", "default"),
            policy_set=data.get("policy_set", "enterprise_default"),
            trust_level=trust_level,
            budget=data.get("budget", {}),
            status=status,
            metadata=data.get("metadata", {}),
        )


@dataclass
class GoalModel:
    """
    Goal Model representation for goal-driven autonomous agent execution.
    """
    id: str = field(default_factory=lambda: f"goal-{uuid.uuid4().hex[:12]}")
    description: str = ""
    priority: str = "HIGH"  # CRITICAL, HIGH, NORMAL, LOW
    deadline: Optional[datetime] = None
    constraints: List[str] = field(default_factory=list)
    budget: Dict[str, Any] = field(default_factory=dict)
    success_conditions: List[str] = field(default_factory=list)
    failure_conditions: List[str] = field(default_factory=list)
    subgoals: List[str] = field(default_factory=list)
    status: str = "PENDING"
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "description": self.description,
            "priority": self.priority,
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "constraints": self.constraints,
            "budget": self.budget,
            "success_conditions": self.success_conditions,
            "failure_conditions": self.failure_conditions,
            "subgoals": self.subgoals,
            "status": self.status,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class PlanStep:
    """A step within an agent-generated or decomposed execution plan."""
    id: str = field(default_factory=lambda: f"step-{uuid.uuid4().hex[:8]}")
    name: str = ""
    description: str = ""
    assigned_agent_type: str = ""
    required_skills: List[str] = field(default_factory=list)
    required_tools: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    timeout_seconds: int = 60
    estimated_cost_usd: float = 0.01
    requires_human_approval: bool = False
    compensation_action: Optional[str] = None
    status: str = "PENDING"
    result: Optional[Dict[str, Any]] = None


@dataclass
class AgentPlan:
    """Plan generated by the Planner Engine or Task Decomposer."""
    plan_id: str = field(default_factory=lambda: f"plan-{uuid.uuid4().hex[:12]}")
    goal_id: str = ""
    goal_description: str = ""
    steps: List[PlanStep] = field(default_factory=list)
    dependencies: Dict[str, List[str]] = field(default_factory=dict)
    assigned_agents: List[str] = field(default_factory=list)
    estimated_cost_usd: float = 0.0
    estimated_duration_seconds: float = 0.0
    risk_score: float = 0.0
    strategy: str = "HYBRID"  # DETERMINISTIC, AI, CONSTRAINT, HYBRID
    status: str = "CREATED"
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "plan_id": self.plan_id,
            "goal_id": self.goal_id,
            "goal_description": self.goal_description,
            "steps": [
                {
                    "id": s.id,
                    "name": s.name,
                    "description": s.description,
                    "assigned_agent_type": s.assigned_agent_type,
                    "required_skills": s.required_skills,
                    "required_tools": s.required_tools,
                    "dependencies": s.dependencies,
                    "timeout_seconds": s.timeout_seconds,
                    "estimated_cost_usd": s.estimated_cost_usd,
                    "requires_human_approval": s.requires_human_approval,
                    "compensation_action": s.compensation_action,
                    "status": s.status,
                }
                for s in self.steps
            ],
            "dependencies": self.dependencies,
            "assigned_agents": self.assigned_agents,
            "estimated_cost_usd": self.estimated_cost_usd,
            "estimated_duration_seconds": self.estimated_duration_seconds,
            "risk_score": self.risk_score,
            "strategy": self.strategy,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class ReasoningSummary:
    """
    Governed Reasoning Summary.
    Stores summary, decision, evidence, confidence, and validation results.
    Never persists raw private chain-of-thought.
    """
    id: str = field(default_factory=lambda: f"rsn-{uuid.uuid4().hex[:10]}")
    agent_id: str = ""
    task_id: str = ""
    summary: str = ""
    decision: str = ""
    evidence: List[Dict[str, Any]] = field(default_factory=list)
    confidence_score: float = 1.0
    validation_results: Dict[str, Any] = field(default_factory=dict)
    risk_assessment: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "agent_id": self.agent_id,
            "task_id": self.task_id,
            "summary": self.summary,
            "decision": self.decision,
            "evidence": self.evidence,
            "confidence_score": self.confidence_score,
            "validation_results": self.validation_results,
            "risk_assessment": self.risk_assessment,
            "timestamp": self.timestamp.isoformat(),
        }
