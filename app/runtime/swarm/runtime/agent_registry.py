"""
AMCN-SIP Phase 13.8 - Agent Registry
Dynamic registry maintaining identities, roles, capabilities, tools, permissions, reputation, and health for all agents in the society.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional, Set, Union
import uuid
from app.runtime.swarm.events.swarm_events import AgentRoleType, AgentLifecycleState, AgentRole, AgentState


@dataclass
class SwarmAgentProfile:
    agent_id: str
    name: str
    role: AgentRoleType
    state: AgentLifecycleState = AgentLifecycleState.REGISTERED
    capabilities: List[str] = field(default_factory=list)
    tools: List[str] = field(default_factory=list)
    permissions: List[str] = field(default_factory=list)
    max_concurrency: int = 4
    compute_cost_per_sec: float = 0.05
    reputation_score: float = 0.95  # 0.0 - 1.0
    availability_pct: float = 100.0
    cost_per_token_usd: float = 0.000002
    avg_latency_ms: float = 240.0
    health_status: str = "HEALTHY"
    assigned_tasks_count: int = 0
    completed_tasks_count: int = 0
    version: str = "1.0.0"
    description: str = ""
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    last_active_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class AgentRegistry:
    """
    Central agent directory providing dynamic registration, query, and capability indexing.
    """

    def __init__(self):
        self._agents: Dict[str, SwarmAgentProfile] = {}
        self._capability_index: Dict[str, Set[str]] = {}
        self._role_index: Dict[AgentRoleType, Set[str]] = {}
        self._seed_default_society()

    def register_agent(
        self,
        profile_or_name: Union[SwarmAgentProfile, str],
        role: Optional[AgentRoleType] = None,
        capabilities: Optional[List[str]] = None,
        tools: Optional[List[str]] = None,
        permissions: Optional[List[str]] = None,
        cost_per_token: float = 0.000002,
        avg_latency: float = 250.0,
        **kwargs,
    ) -> SwarmAgentProfile:
        if isinstance(profile_or_name, SwarmAgentProfile):
            profile = profile_or_name
        else:
            agent_id = kwargs.get("agent_id") or f"agt-{role.value.lower()[:3] if role else 'gen'}-{uuid.uuid4().hex[:6]}"
            profile = SwarmAgentProfile(
                agent_id=agent_id,
                name=profile_or_name,
                role=role or AgentRole.SPECIALIST,
                state=AgentState.REGISTERED,
                capabilities=capabilities or [],
                tools=tools or [],
                permissions=permissions or [],
                cost_per_token_usd=cost_per_token,
                avg_latency_ms=avg_latency,
                description=kwargs.get("description", ""),
            )

        self._agents[profile.agent_id] = profile

        # Index capabilities
        for cap in profile.capabilities:
            if cap not in self._capability_index:
                self._capability_index[cap] = set()
            self._capability_index[cap].add(profile.agent_id)

        # Index roles
        if profile.role not in self._role_index:
            self._role_index[profile.role] = set()
        self._role_index[profile.role].add(profile.agent_id)

        return profile

    def get_agent(self, agent_id: str) -> Optional[SwarmAgentProfile]:
        return self._agents.get(agent_id)

    def get_by_role(self, role: AgentRoleType) -> List[SwarmAgentProfile]:
        return [self._agents[aid] for aid in self._role_index.get(role, set()) if aid in self._agents]

    def list_agents(
        self,
        role: Optional[AgentRoleType] = None,
        capability: Optional[str] = None,
        state: Optional[AgentLifecycleState] = None,
    ) -> List[SwarmAgentProfile]:
        res = list(self._agents.values())
        if role:
            res = [a for a in res if a.role == role]
        if capability:
            res = [a for a in res if capability in a.capabilities or capability.lower() in [c.lower() for c in a.capabilities]]
        if state:
            res = [a for a in res if a.state == state]
        return res

    def _seed_default_society(self):
        default_profiles = [
            SwarmAgentProfile(
                agent_id="agent-exec-01",
                name="Executive Director",
                role=AgentRole.EXECUTIVE,
                state=AgentState.AVAILABLE,
                capabilities=["mission_orchestration", "goal_alignment", "strategic_planning"],
                tools=["mission_decomposer", "resource_allocator"],
                reputation_score=0.99,
                avg_latency_ms=120.0,
            ),
            SwarmAgentProfile(
                agent_id="agent-plan-01",
                name="Lead Planner",
                role=AgentRole.PLANNER,
                state=AgentState.AVAILABLE,
                capabilities=["dag_scheduling", "critical_path_analysis", "dependency_resolution"],
                tools=["dag_mutator", "scheduler_engine"],
                reputation_score=0.98,
                avg_latency_ms=180.0,
            ),
            SwarmAgentProfile(
                agent_id="agent-coord-01",
                name="Swarm Coordinator",
                role=AgentRole.COORDINATOR,
                state=AgentState.AVAILABLE,
                capabilities=["task_routing", "agent_synchronization", "market_auctioning"],
                tools=["task_broker", "auction_manager"],
                reputation_score=0.97,
                avg_latency_ms=150.0,
            ),
            SwarmAgentProfile(
                agent_id="agent-spec-ocr",
                name="OCR Specialist",
                role=AgentRole.SPECIALIST,
                state=AgentState.AVAILABLE,
                capabilities=["ocr_extraction", "table_parsing", "layout_detection", "tokenization"],
                tools=["tesseract_engine", "vision_transformer"],
                reputation_score=0.98,
                avg_latency_ms=310.0,
            ),
            SwarmAgentProfile(
                agent_id="agent-val-sec",
                name="Security Validator",
                role=AgentRole.VALIDATOR,
                state=AgentState.AVAILABLE,
                capabilities=["security_verification", "cryptographic_audit", "schema_validation", "governance_assurance"],
                tools=["sha256_verifier", "policy_evaluator"],
                reputation_score=0.99,
                avg_latency_ms=90.0,
            ),
            SwarmAgentProfile(
                agent_id="agent-res-opt",
                name="Resource Governor",
                role=AgentRole.RESOURCE,
                state=AgentState.AVAILABLE,
                capabilities=["budget_management", "token_quota_control", "rate_limiting"],
                tools=["cost_calculator", "load_balancer"],
                reputation_score=0.96,
                avg_latency_ms=80.0,
            ),
        ]
        for p in default_profiles:
            self.register_agent(p)
