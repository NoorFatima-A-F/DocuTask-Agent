"""Task Graph Mutation Engine for Autonomous Agent OS.

Enables runtime graph re-structuring: dynamic node insertion, fallback branch
splicing, failure recovery replanning, and edge rerouting without restarting workflows.
"""

from __future__ import annotations

import copy
import logging
import uuid
from typing import Any, Dict, List, Optional

from app.agents.planning.execution_plan import PlannedTask, TaskStatus
from app.agents.workflow.task_graph.dynamic_task_graph import DynamicTaskGraph, NodeState

logger = logging.getLogger(__name__)


class TaskGraphMutationEngine:
    """Performs transactional, validated mutations on live DynamicTaskGraphs."""

    def __init__(self, graph: DynamicTaskGraph) -> None:
        self.graph = graph

    def insert_node_between(
        self,
        upstream_task_id: str,
        downstream_task_id: str,
        new_task: PlannedTask,
    ) -> PlannedTask:
        """Insert a new task between an upstream task and a downstream task.

        Updates dependencies so: upstream -> new_task -> downstream.
        """
        upstream = self.graph.get_task(upstream_task_id)
        downstream = self.graph.get_task(downstream_task_id)

        if not upstream or not downstream:
            raise KeyError(f"Both {upstream_task_id} and {downstream_task_id} must exist")

        if upstream_task_id not in downstream.dependencies:
            raise ValueError(f"{downstream_task_id} does not depend on {upstream_task_id}")

        # Set new_task dependencies to include upstream
        new_task.dependencies = [upstream_task_id]
        self.graph.add_task(new_task)

        # Reroute downstream dependency from upstream to new_task
        downstream.dependencies.remove(upstream_task_id)
        downstream.dependencies.append(new_task.task_id)

        # If upstream is already completed, promote new_task to READY
        if self.graph.get_state(upstream_task_id) == NodeState.COMPLETED:
            self.graph.set_state(new_task.task_id, NodeState.READY)

        self.graph.record_mutation(
            mutation_type="NODE_INSERTED",
            node_id=new_task.task_id,
            details={
                "upstream": upstream_task_id,
                "downstream": downstream_task_id,
                "inserted_action": new_task.action,
            },
        )
        logger.info(
            "Inserted node %s between %s and %s",
            new_task.task_id,
            upstream_task_id,
            downstream_task_id,
        )
        return new_task

    def replace_failed_node_with_fallback(
        self,
        failed_task_id: str,
        fallback_agent: str,
        fallback_tools: List[str],
        additional_params: Optional[Dict[str, Any]] = None,
    ) -> PlannedTask:
        """Handle failure by generating a replacement fallback node with alternative agent/tools."""
        failed_task = self.graph.get_task(failed_task_id)
        if not failed_task:
            raise KeyError(f"Task {failed_task_id} not found")

        self.graph.set_state(failed_task_id, NodeState.MUTATED)

        replacement_id = f"fallback_{failed_task.action}_{uuid.uuid4().hex[:6]}"
        replacement_task = PlannedTask(
            task_id=replacement_id,
            name=f"Fallback: {failed_task.name}",
            action=failed_task.action,
            assigned_agent=fallback_agent,
            required_tools=list(fallback_tools),
            dependencies=list(failed_task.dependencies),
            input_parameters={**failed_task.input_parameters, **(additional_params or {})},
            output_key=failed_task.output_key,
            is_critical=failed_task.is_critical,
            metadata={"original_task_id": failed_task_id, "is_fallback": True},
        )

        self.graph.add_task(replacement_task)

        # Reroute all downstream dependents of failed_task to depend on replacement_task
        downstream = self.graph.get_downstream_dependents(failed_task_id)
        for dep in downstream:
            dep.dependencies.remove(failed_task_id)
            dep.dependencies.append(replacement_id)

        # Evaluate readiness of replacement node
        self.graph.refresh_states()

        self.graph.record_mutation(
            mutation_type="NODE_REPLACED",
            node_id=replacement_id,
            details={
                "original_task_id": failed_task_id,
                "fallback_agent": fallback_agent,
                "fallback_tools": fallback_tools,
            },
        )
        logger.info(
            "Replaced failed task %s with fallback task %s (Agent: %s, Tools: %s)",
            failed_task_id,
            replacement_id,
            fallback_agent,
            fallback_tools,
        )
        return replacement_task

    def inject_correction_cycle(
        self,
        trigger_task_id: str,
        error_context: Dict[str, Any],
        correction_agent: str = "agent_correction_gemini",
        trigger: Optional[Any] = None,
        original_output: Optional[Any] = None,
    ) -> PlannedTask:
        """Dynamically injects a Reflection / Self-Correction node after a task that yielded low quality."""
        trigger_task = self.graph.get_task(trigger_task_id)
        if not trigger_task:
            raise KeyError(f"Trigger task {trigger_task_id} not found")

        correction_id = f"task_correction_{uuid.uuid4().hex[:6]}"
        correction_task = PlannedTask(
            task_id=correction_id,
            name=f"Self-Correction: {trigger_task.name}",
            action="reflection_repair",
            assigned_agent=correction_agent,
            required_tools=["tool_gemini_vision", "tool_json_validator"],
            dependencies=[trigger_task_id],
            input_parameters={
                "trigger_task_id": trigger_task_id,
                "error_context": error_context,
                "trigger": trigger,
                "original_output": original_output or self.graph.get_output(trigger_task_id),
            },
            output_key=f"corrected_{trigger_task.output_key}",
            is_critical=True,
        )

        self.graph.add_task(correction_task)

        # Downstream nodes waiting on trigger_task are rerouted to await correction
        downstream = self.graph.get_downstream_dependents(trigger_task_id)
        for dep in downstream:
            if dep.task_id != correction_id:
                dep.dependencies.remove(trigger_task_id)
                dep.dependencies.append(correction_id)

        self.graph.refresh_states()

        self.graph.record_mutation(
            mutation_type="CORRECTION_INJECTED",
            node_id=correction_id,
            details={"trigger_task": trigger_task_id, "error_context": error_context},
        )
        return correction_task

    def skip_task(self, task_id: str, reason: str = "Conditional bypass") -> None:
        """Safely skip a non-critical task and reroute its dependents."""
        task = self.graph.get_task(task_id)
        if not task:
            raise KeyError(f"Task {task_id} not found")

        self.graph.set_state(task_id, NodeState.SKIPPED)
        self.graph.record_mutation(
            mutation_type="NODE_SKIPPED",
            node_id=task_id,
            details={"reason": reason},
        )
        self.graph.refresh_states()
        logger.info("Task %s skipped. Reason: %s", task_id, reason)
