"""
Autonomous Runtime Engine for Autonomous Agent Operating System.
Top-level operating system facade orchestrating cognition, planning, execution, reflection,
learning, security governance, and human collaboration.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from app.agents.collaboration.agent_registry import AgentRegistry
from app.agents.collaboration.reputation.performance_tracker import PerformanceTracker
from app.agents.collaboration.reputation.reputation_engine import ReputationEngine
from app.agents.events.event_bus import EnterpriseEventBus
from app.agents.human.human_task_manager import HumanTaskManager
from app.agents.intelligence.goal.goal_manager import GoalManager
from app.agents.intelligence.reasoning.semantic_reasoner import SemanticReasoner
from app.agents.memory.consolidation.consolidation_agent import MemoryConsolidationAgent
from app.agents.memory.intelligence.episodic_memory import EpisodicMemory
from app.agents.memory.intelligence.semantic_memory import SemanticMemory
from app.agents.planning.autonomous_planner import AutonomousPlanner
from app.agents.planning.optimizer.plan_selector import PlanSelector
from app.agents.reflection.critics.consensus_evaluator import MultiCriticConsensusEvaluator
from app.agents.reflection.critics.historical_critic import HistoricalCritic
from app.agents.runtime.autonomous.decision_loop import DecisionCycleResult, DecisionLoop
from app.agents.runtime.autonomous.event_controller import EventController
from app.agents.runtime.autonomous.execution_controller import ExecutionController
from app.agents.runtime.autonomous.observation_manager import ObservationManager
from app.agents.runtime.autonomous.runtime_context import RuntimeContext
from app.agents.workflow.task_graph.dynamic_task_graph import DynamicTaskGraph
from app.agents.runtime.autonomous.state_machine import RuntimeStateMachine
from app.agents.security.security_guardian import SecurityGuardian
from app.agents.tools.policy.tool_decision_engine import ToolDecisionEngine
from app.agents.workflow.persistence.recovery_manager import RecoveryManager
from app.agents.workflow.persistence.task_graph_repository import (
    InMemoryTaskGraphRepository,
    TaskGraphRepository,
)
from app.agents.workflow.persistence.workflow_checkpoint import TaskGraphSnapshot

logger = logging.getLogger(__name__)


class AutonomousRuntime:
    """The central Autonomous Agent Operating System runtime instance."""

    def __init__(
        self,
        event_bus: Optional[EnterpriseEventBus] = None,
        task_repository: Optional[TaskGraphRepository] = None,
        agent_registry: Optional[AgentRegistry] = None,
    ) -> None:
        # 1. Core Event & Persistence Infrastructure
        self.event_bus = event_bus or EnterpriseEventBus()
        self.task_repo = task_repository or InMemoryTaskGraphRepository()
        self.recovery_mgr = RecoveryManager(self.task_repo)

        # 2. Security & Policy Subsystems
        self.security_guardian = SecurityGuardian()
        self.tool_engine = ToolDecisionEngine()

        # 3. Collaboration & Reputation Subsystems
        self.agent_registry = agent_registry or AgentRegistry()
        self.performance_tracker = PerformanceTracker()
        self.reputation_engine = ReputationEngine(
            performance_tracker=self.performance_tracker,
            registry=self.agent_registry,
        )

        # 4. Cognitive Memory Subsystems
        self.episodic_memory = EpisodicMemory()
        self.semantic_memory = SemanticMemory()
        self.consolidation_agent = MemoryConsolidationAgent(
            episodic_memory=self.episodic_memory,
            semantic_memory=self.semantic_memory,
        )

        # 5. Human-in-the-Loop Subsystem
        self.human_manager = HumanTaskManager(
            semantic_memory=self.semantic_memory,
            episodic_memory=self.episodic_memory,
        )

        # 6. Cognitive & Planning Engines
        self.semantic_reasoner = SemanticReasoner()
        self.goal_manager = GoalManager()
        self.planner = AutonomousPlanner()
        self.plan_optimizer = PlanSelector()
        self.historical_critic = HistoricalCritic(
            episodic_memory=self.episodic_memory,
            semantic_memory=self.semantic_memory,
        )
        self.reflection_evaluator = MultiCriticConsensusEvaluator(
            historical_critic=self.historical_critic,
        )

        # 7. Runtime Loop Components
        self.state_machine = RuntimeStateMachine()
        self.observation_manager = ObservationManager()
        self.event_controller = EventController(event_bus=self.event_bus)
        self.execution_controller = ExecutionController(
            security_guardian=self.security_guardian,
            tool_engine=self.tool_engine,
            performance_tracker=self.performance_tracker,
            agent_registry=self.agent_registry,
        )

        # 8. Unified Decision Loop
        self.decision_loop = DecisionLoop(
            state_machine=self.state_machine,
            observation_manager=self.observation_manager,
            semantic_reasoner=self.semantic_reasoner,
            goal_manager=self.goal_manager,
            planner=self.planner,
            plan_optimizer=self.plan_optimizer,
            execution_controller=self.execution_controller,
            reflection_evaluator=self.reflection_evaluator,
            consolidation_agent=self.consolidation_agent,
            human_manager=self.human_manager,
            event_controller=self.event_controller,
            repository=self.task_repo,
        )

    async def run_goal(
        self,
        goal_text: str,
        document_id: str = "",
        context_metadata: Optional[Dict[str, Any]] = None,
    ) -> DecisionCycleResult:
        """Executes an end-to-end autonomous goal cycle."""
        ctx = RuntimeContext(
            goal_text=goal_text,
            document_id=document_id,
            metadata=context_metadata or {},
        )
        return await self.decision_loop.run(goal_text=goal_text, context=ctx)

    def save_checkpoint(self, context: RuntimeContext) -> TaskGraphSnapshot:
        """Explicitly checkpoints active workflow graph state."""
        if not context.task_graph:
            raise ValueError("No active task graph to checkpoint in context")
        snapshot = TaskGraphSnapshot.create(
            context.task_graph,
            session_id=context.session_id,
            step_index=context.iteration_count,
        )
        self.task_repo.save(snapshot)
        logger.info("Saved runtime checkpoint %s for execution %s", snapshot.snapshot_id, context.execution_id)
        return snapshot

    def recover_and_resume(self, plan_id: str) -> Optional[DynamicTaskGraph]:
        """Recovers interrupted task graph from repository."""
        return self.recovery_mgr.recover_latest_plan(plan_id)
