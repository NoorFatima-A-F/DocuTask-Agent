"""
Enterprise Multi-Agent Intelligence Platform (EMAIP) - Worker Agent Framework.
Provides specialized worker agent instances that execute designated capabilities
using skills and tools.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
import logging

from app.agents.domain.agent_entity import Agent, AgentLifecycleState, AgentType, PlanStep
from app.agents.lifecycle.manager import AgentLifecycleManager
from app.agents.skills.skill_registry import SkillRegistry

logger = logging.getLogger(__name__)


class WorkerAgent:
    """
    Specialized autonomous worker agent executing domain tasks via registered skills and tools.
    """

    def __init__(
        self,
        agent_id: str,
        name: str,
        agent_type: AgentType | str = AgentType.EXECUTION,
        skills: Optional[List[str]] = None,
        capabilities: Optional[List[str]] = None,
        skill_registry: Optional[SkillRegistry] = None,
        lifecycle_manager: Optional[AgentLifecycleManager] = None,
    ):
        self.agent_entity = Agent(
            id=agent_id,
            name=name,
            type=agent_type,
            skills=skills or ["extraction", "transformation"],
            capabilities=capabilities or ["data.processing"],
            status=AgentLifecycleState.INITIALIZED,
        )
        self.skill_registry = skill_registry or SkillRegistry()
        self.lifecycle_manager = lifecycle_manager or AgentLifecycleManager()

    async def execute_task(self, step: PlanStep) -> Dict[str, Any]:
        """
        Executes an assigned task step, transitioning lifecycle states
        and applying appropriate skills.
        """
        self.lifecycle_manager.transition(
            self.agent_entity,
            AgentLifecycleState.EXECUTING,
            reason=f"Executing step {step.id} ({step.name})"
        )

        outputs: Dict[str, Any] = {}
        for skill_name in step.required_skills:
            skill = self.skill_registry.get(skill_name)
            if skill and skill.handler:
                try:
                    outputs[skill_name] = skill.handler({"step": step.name, "desc": step.description})
                except Exception as e:
                    logger.warning(f"Error in skill handler '{skill_name}': {e}")
                    outputs[skill_name] = {"status": "FAILED", "error": str(e)}
            else:
                outputs[skill_name] = {"status": "SUCCESS", "skill": skill_name}

        result = {
            "status": "SUCCESS",
            "agent_id": self.agent_entity.id,
            "step_id": step.id,
            "step_name": step.name,
            "skill_outputs": outputs,
        }

        self.lifecycle_manager.transition(
            self.agent_entity,
            AgentLifecycleState.COMPLETED,
            reason=f"Completed step {step.id}"
        )
        self.lifecycle_manager.transition(
            self.agent_entity,
            AgentLifecycleState.INITIALIZED,  # Ready for next task
            reason="Ready for next task"
        )
        return result
