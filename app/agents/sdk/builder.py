"""
Enterprise Multi-Agent Intelligence Platform (EMAIP) - Agent SDK.
Provides a fluent AgentBuilder API for declarative definition, configuration,
and instantiation of autonomous agents.
"""

from __future__ import annotations

from typing import Any, Dict, List
import uuid

from app.agents.domain.agent_entity import Agent, AgentLifecycleState, AgentType, TrustLevel


class AgentBuilder:
    """
    Fluent builder pattern for configuring and instantiating Agent platform entities.
    """

    def __init__(self, name: str = "CustomAgent"):
        self._name = name
        self._id = f"agent-{uuid.uuid4().hex[:12]}"
        self._type: AgentType | str = AgentType.EXECUTION
        self._version = "1.0.0"
        self._organization_id = "org-default"
        self._workspace_id = "ws-default"
        self._owner = "system"
        self._capabilities: List[str] = []
        self._skills: List[str] = []
        self._model = "gemini-2.5-flash"
        self._prompt_version = "1.0.0"
        self._memory_namespace = "default"
        self._policy_set = "enterprise_default"
        self._trust_level: TrustLevel | str = TrustLevel.STANDARD
        self._budget: Dict[str, Any] = {
            "max_tokens": 100000,
            "max_cost_usd": 1.0,
            "max_execution_time_seconds": 300,
            "max_tool_calls": 50,
        }
        self._metadata: Dict[str, Any] = {}

    def id(self, agent_id: str) -> AgentBuilder:
        self._id = agent_id
        return self

    def type(self, agent_type: AgentType | str) -> AgentBuilder:
        self._type = agent_type
        return self

    def version(self, version_str: str) -> AgentBuilder:
        self._version = version_str
        return self

    def organization(self, org_id: str) -> AgentBuilder:
        self._organization_id = org_id
        return self

    def workspace(self, ws_id: str) -> AgentBuilder:
        self._workspace_id = ws_id
        return self

    def owner(self, owner_name: str) -> AgentBuilder:
        self._owner = owner_name
        return self

    def skill(self, skill_name: str) -> AgentBuilder:
        if skill_name not in self._skills:
            self._skills.append(skill_name)
        return self

    def skills(self, skills_list: List[str]) -> AgentBuilder:
        for s in skills_list:
            self.skill(s)
        return self

    def capability(self, capability_name: str) -> AgentBuilder:
        if capability_name not in self._capabilities:
            self._capabilities.append(capability_name)
        return self

    def capabilities(self, capabilities_list: List[str]) -> AgentBuilder:
        for c in capabilities_list:
            self.capability(c)
        return self

    def model(self, model_name: str) -> AgentBuilder:
        self._model = model_name
        return self

    def prompt_version(self, prompt_ver: str) -> AgentBuilder:
        self._prompt_version = prompt_ver
        return self

    def memory_namespace(self, namespace: str) -> AgentBuilder:
        self._memory_namespace = namespace
        return self

    def policy_set(self, policy_set_name: str) -> AgentBuilder:
        self._policy_set = policy_set_name
        return self

    def trust_level(self, trust_level: TrustLevel | str) -> AgentBuilder:
        self._trust_level = trust_level
        return self

    def budget(self, **kwargs: Any) -> AgentBuilder:
        self._budget.update(kwargs)
        return self

    def metadata(self, **kwargs: Any) -> AgentBuilder:
        self._metadata.update(kwargs)
        return self

    def build(self) -> Agent:
        """Constructs and returns the configured Agent entity."""
        return Agent(
            id=self._id,
            name=self._name,
            type=self._type,
            version=self._version,
            organization_id=self._organization_id,
            workspace_id=self._workspace_id,
            owner=self._owner,
            capabilities=list(self._capabilities),
            skills=list(self._skills),
            model=self._model,
            prompt_version=self._prompt_version,
            memory_namespace=self._memory_namespace,
            policy_set=self._policy_set,
            trust_level=self._trust_level,
            budget=dict(self._budget),
            status=AgentLifecycleState.CREATED,
            metadata=dict(self._metadata),
        )
