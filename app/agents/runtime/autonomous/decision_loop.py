"""
Decision Loop for Autonomous Runtime Brain.
Coordinates the continuous cognitive decision cycle:
Observe -> Reason -> Select Action -> Execute -> Reflect -> Learn.
"""

from __future__ import annotations

import asyncio
import logging
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional

from app.agents.human.human_task_manager import HumanTaskManager
from app.agents.intelligence.goal.goal_manager import GoalManager
from app.agents.intelligence.reasoning.semantic_reasoner import SemanticReasoner
from app.agents.memory.consolidation.consolidation_agent import MemoryConsolidationAgent
from app.agents.planning.autonomous_planner import AutonomousPlanner
from app.agents.planning.optimizer.plan_selector import PlanSelector
from app.agents.reflection.critics.consensus_evaluator import (
    ConsensusCritiqueResult,
    MultiCriticConsensusEvaluator,
)
from app.agents.runtime.autonomous.event_controller import EventController
from app.agents.runtime.autonomous.execution_controller import ExecutionController
from app.agents.runtime.autonomous.observation_manager import ObservationManager
from app.agents.runtime.autonomous.runtime_context import RuntimeContext
from app.agents.runtime.autonomous.state_machine import AutonomousState, RuntimeStateMachine
from app.agents.workflow.persistence.task_graph_repository import TaskGraphRepository
from app.agents.workflow.persistence.workflow_checkpoint import TaskGraphSnapshot
from app.agents.workflow.task_graph.dynamic_task_graph import DynamicTaskGraph, NodeState

logger = logging.getLogger(__name__)


@dataclass
class DecisionCycleResult:
    """Outcome deliverable of a complete cognitive execution cycle."""

    execution_id: str
    final_state: AutonomousState
    success: bool
    iterations_run: int
    extracted_data: Dict[str, Any]
    reflection_result: Optional[ConsensusCritiqueResult] = None
    audit_summary: str = ""


class DecisionLoop:
    """Coordinates the full autonomous cognitive cycle until goal achievement or escalation."""

    def __init__(
        self,
        state_machine: Optional[RuntimeStateMachine] = None,
        observation_manager: Optional[ObservationManager] = None,
        semantic_reasoner: Optional[SemanticReasoner] = None,
        goal_manager: Optional[GoalManager] = None,
        planner: Optional[AutonomousPlanner] = None,
        plan_optimizer: Optional[PlanSelector] = None,
        execution_controller: Optional[ExecutionController] = None,
        reflection_evaluator: Optional[MultiCriticConsensusEvaluator] = None,
        consolidation_agent: Optional[MemoryConsolidationAgent] = None,
        human_manager: Optional[HumanTaskManager] = None,
        event_controller: Optional[EventController] = None,
        repository: Optional[TaskGraphRepository] = None,
    ) -> None:
        self.state_machine = state_machine or RuntimeStateMachine()
        self.obs_mgr = observation_manager or ObservationManager()
        self.reasoner = semantic_reasoner or SemanticReasoner()
        self.goal_mgr = goal_manager or GoalManager()
        self.planner = planner or AutonomousPlanner()
        self.optimizer = plan_optimizer or PlanSelector()
        self.exec_ctrl = execution_controller or ExecutionController()
        self.reflection = reflection_evaluator or MultiCriticConsensusEvaluator()
        self.consolidation = consolidation_agent
        self.human_mgr = human_manager
        self.events = event_controller or EventController()
        self.repo = repository

    async def run(self, goal_text: str, context: Optional[RuntimeContext] = None) -> DecisionCycleResult:
        """Executes the full autonomous lifecycle for the given goal."""
        ctx = context or RuntimeContext(goal_text=goal_text)

        # 1. State: CREATED -> INITIALIZING
        self._transition(AutonomousState.INITIALIZING, ctx)
        await self.events.emit_goal_received(goal_text, ctx)

        # 2. State: INITIALIZING -> OBSERVING
        self._transition(AutonomousState.OBSERVING, ctx)
        self.obs_mgr.observe(ctx)

        # 3. State: OBSERVING -> REASONING
        self._transition(AutonomousState.REASONING, ctx)
        semantic_res = await self.reasoner.reason_about_goal(goal_text=goal_text)
        ctx.metadata["semantic_intent"] = semantic_res.primary_intent

        # 4. State: REASONING -> PLANNING
        self._transition(AutonomousState.PLANNING, ctx)
        goal_spec = self.goal_mgr.submit_goal(objective=goal_text)
        ctx.goal_spec = goal_spec
        base_plan = self.planner.generate_plan(goal_spec)

        # 5. State: PLANNING -> OPTIMIZING
        self._transition(AutonomousState.OPTIMIZING, ctx)
        opt_res = self.optimizer.optimize_and_select(base_plan)
        ctx.active_plan = opt_res.selected_plan
        await self.events.emit_plan_optimized(opt_res.winning_strategy, opt_res.winning_metrics.composite_score, ctx)

        # 6. Initialize live DynamicTaskGraph
        ctx.task_graph = DynamicTaskGraph.from_execution_plan(ctx.active_plan)

        # 7. Cognitive Execution Loop
        critique_result: Optional[ConsensusCritiqueResult] = None

        while ctx.iteration_count < ctx.max_iterations:
            ctx.iteration_count += 1
            logger.info("Starting Cognitive Iteration %d for execution %s", ctx.iteration_count, ctx.execution_id)

            # State: EXECUTING
            self._transition(AutonomousState.EXECUTING, ctx)

            # Checkpoint graph state prior to execution wave
            if self.repo:
                snapshot = TaskGraphSnapshot.create(ctx.task_graph, session_id=ctx.session_id, step_index=ctx.iteration_count)
                self.repo.save(snapshot)

            # Execute topological waves until DAG completes or blocks
            while not ctx.task_graph.is_completed() and not ctx.task_graph.has_failures():
                ready_tasks = ctx.task_graph.get_ready_tasks()
                if not ready_tasks:
                    break
                await self.exec_ctrl.execute_wave(ctx.task_graph, ctx)

            # State: REFLECTING
            self._transition(AutonomousState.REFLECTING, ctx)
            critique_result = await self.reflection.evaluate_extraction(
                extracted_data=ctx.extracted_data,
                goal_description=goal_text,
            )
            await self.events.emit_reflection_completed(critique_result.overall_score, critique_result.passed, ctx)

            # Check if reflection passed
            if critique_result.passed:
                logger.info("Multi-critic reflection passed with score %.3f", critique_result.overall_score)
                break

            # Handle Human Escalation if confidence is critically low
            if critique_result.needs_human_escalation and self.human_mgr:
                self._transition(AutonomousState.PAUSED_FOR_HUMAN, ctx)
                ctx.is_paused = True
                ticket = self.human_mgr.escalate(
                    execution_id=ctx.execution_id,
                    task_id="extraction_validation",
                    reason=f"Multi-critic score ({critique_result.overall_score:.2f}) below threshold",
                    extracted_data=ctx.extracted_data,
                )
                logger.warning("Execution paused for human review: ticket %s", ticket.ticket_id)
                # For automated demo/test workflows, proceed with current data
                ctx.is_paused = False
                break

            # Self-correction loop: Replan and retry
            if critique_result.needs_replanning and ctx.iteration_count < ctx.max_iterations:
                logger.warning("Self-correction triggered (attempt %d). Replanning...", ctx.iteration_count)
                self._transition(AutonomousState.PLANNING, ctx)
                # Reset graph for retry
                for tid in ctx.task_graph._nodes:
                    ctx.task_graph._states[tid] = NodeState.PENDING
                ctx.task_graph.refresh_states()
                continue
            else:
                break

        # 8. State: LEARNING
        self._transition(AutonomousState.LEARNING, ctx)
        if self.consolidation:
            self.consolidation.run_consolidation(cycle_id=f"auto_{ctx.execution_id[:8]}")

        # 9. Final Completion
        ctx.completed_at = time.time()
        success = critique_result.passed if critique_result else True
        if success:
            self._transition(AutonomousState.COMPLETED, ctx)
            await self.events.emit_completion(ctx)
        else:
            self._transition(AutonomousState.FAILED, ctx)
            await self.events.emit_failure(f"Reflection failed: {critique_result.all_issues if critique_result else 'Unknown'}", ctx)

        summary = (
            f"Execution {ctx.execution_id} concluded in state {self.state_machine.current_state.value} "
            f"({ctx.elapsed_time_seconds():.2f}s, {ctx.iteration_count} iterations, "
            f"score={critique_result.overall_score if critique_result else 1.0:.2f})"
        )

        return DecisionCycleResult(
            execution_id=ctx.execution_id,
            final_state=self.state_machine.current_state,
            success=success,
            iterations_run=ctx.iteration_count,
            extracted_data=ctx.extracted_data,
            reflection_result=critique_result,
            audit_summary=summary,
        )

    def _transition(self, target_state: AutonomousState, context: RuntimeContext) -> None:
        """Helper to transition state and log."""
        from_state = self.state_machine.current_state
        if self.state_machine.can_transition_to(target_state):
            self.state_machine.transition_to(target_state)
            asyncio.create_task(self.events.emit_state_transition(from_state, target_state, context))
