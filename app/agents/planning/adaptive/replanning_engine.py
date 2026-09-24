"""
Adaptive Replanning Engine for Autonomous Agent Operating System.
Enables dynamic runtime DAG mutation in response to reflection critique scores,
tool failures, constraint violations, and human feedback.
"""

from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

from app.agents.planning.execution_plan import PlannedTask
from app.agents.reflection.critics.consensus_evaluator import ConsensusCritiqueResult
from app.agents.workflow.task_graph.dynamic_task_graph import DynamicTaskGraph, NodeState

logger = logging.getLogger(__name__)


class MutationActionType(str, Enum):
    REPLACE_TOOL = "REPLACE_TOOL"
    INSERT_VALIDATION_GATE = "INSERT_VALIDATION_GATE"
    INJECT_FALLBACK_BRANCH = "INJECT_FALLBACK_BRANCH"
    SPLIT_TASK = "SPLIT_TASK"
    SKIP_FAILED_OPTIONAL = "SKIP_FAILED_OPTIONAL"
    RETRY_WITH_HIGHER_BUDGET = "RETRY_WITH_HIGHER_BUDGET"


@dataclass
class DynamicMutationDirective:
    """Actionable instruction for modifying the active runtime task graph."""

    action_type: MutationActionType
    target_task_id: str
    reason: str
    new_tool: Optional[str] = None
    new_task: Optional[PlannedTask] = None
    parameters: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ReplanOutcome:
    """Result of an adaptive replanning operation."""

    success: bool
    mutations_applied: List[DynamicMutationDirective]
    nodes_added: int = 0
    nodes_modified: int = 0
    new_ready_count: int = 0
    replan_rationale: str = ""


class AdaptiveReplanningEngine:
    """
    Production-grade dynamic replanning engine.
    Inspects live execution failures and multi-critic reflection critiques,
    derives optimal graph mutations, and modifies the DynamicTaskGraph in-place
    without losing completed node states or intermediate artifacts.
    """

    def __init__(self, max_mutations_per_cycle: int = 5) -> None:
        self.max_mutations_per_cycle = max_mutations_per_cycle
        self.mutation_history: List[ReplanOutcome] = []

    def evaluate_and_mutate(
        self,
        graph: DynamicTaskGraph,
        critique: Optional[ConsensusCritiqueResult] = None,
        failed_task_ids: Optional[List[str]] = None,
        human_instruction: Optional[str] = None,
    ) -> ReplanOutcome:
        """Evaluates anomalies and dynamically mutates the task graph to recover."""
        directives = self._derive_mutation_directives(graph, critique, failed_task_ids, human_instruction)
        applied: List[DynamicMutationDirective] = []
        nodes_added = 0
        nodes_modified = 0

        for directive in directives[: self.max_mutations_per_cycle]:
            if directive.action_type == MutationActionType.REPLACE_TOOL:
                if directive.target_task_id in graph._nodes:
                    task = graph._nodes[directive.target_task_id]
                    old_tool = task.required_tools[0] if task.required_tools else ""
                    new_tool_name = directive.new_tool or "robust_fallback_extractor"
                    task.required_tools = [new_tool_name]
                    graph._states[directive.target_task_id] = NodeState.READY
                    graph.mutate(
                        mutation_type="NODE_REPLACED",
                        node_id=directive.target_task_id,
                        details={"old_tool": old_tool, "new_tool": new_tool_name, "reason": directive.reason},
                    )
                    applied.append(directive)
                    nodes_modified += 1

            elif directive.action_type == MutationActionType.INSERT_VALIDATION_GATE:
                gate_id = f"gate_val_{directive.target_task_id}_{uuid.uuid4().hex[:6]}"
                val_task = PlannedTask(
                    task_id=gate_id,
                    name=f"Automated Validation for {directive.target_task_id}",
                    action="validate",
                    required_tools=["semantic_cross_validator"],
                    input_parameters={"source_task": directive.target_task_id},
                    dependencies=[directive.target_task_id],
                )
                graph.add_task(val_task)
                # Rewire downstream dependencies
                for tid, task in graph._nodes.items():
                    if directive.target_task_id in task.dependencies and tid != gate_id:
                        task.dependencies.remove(directive.target_task_id)
                        task.dependencies.append(gate_id)
                graph.mutate(
                    mutation_type="NODE_INSERTED",
                    node_id=gate_id,
                    details={"gate_for": directive.target_task_id, "reason": directive.reason},
                )
                applied.append(directive)
                nodes_added += 1

            elif directive.action_type == MutationActionType.SKIP_FAILED_OPTIONAL:
                if directive.target_task_id in graph._nodes:
                    graph._states[directive.target_task_id] = NodeState.SKIPPED
                    graph.mutate(
                        mutation_type="NODE_SKIPPED",
                        node_id=directive.target_task_id,
                        details={"reason": directive.reason},
                    )
                    applied.append(directive)
                    nodes_modified += 1

            elif directive.action_type == MutationActionType.RETRY_WITH_HIGHER_BUDGET:
                if directive.target_task_id in graph._nodes:
                    task = graph._nodes[directive.target_task_id]
                    task.input_parameters["retry_count"] = task.input_parameters.get("retry_count", 0) + 1
                    task.input_parameters["high_precision_mode"] = True
                    graph._states[directive.target_task_id] = NodeState.READY
                    graph.mutate(
                        mutation_type="NODE_RETRY_CONFIGURED",
                        node_id=directive.target_task_id,
                        details={"retry": task.input_parameters["retry_count"]},
                    )
                    applied.append(directive)
                    nodes_modified += 1

        graph.refresh_states()
        ready_count = len(graph.get_ready_tasks())

        outcome = ReplanOutcome(
            success=len(applied) > 0,
            mutations_applied=applied,
            nodes_added=nodes_added,
            nodes_modified=nodes_modified,
            new_ready_count=ready_count,
            replan_rationale=f"Applied {len(applied)} dynamic DAG mutations to resolve runtime issues.",
        )
        self.mutation_history.append(outcome)
        return outcome

    def _derive_mutation_directives(
        self,
        graph: DynamicTaskGraph,
        critique: Optional[ConsensusCritiqueResult],
        failed_tasks: Optional[List[str]],
        human_instruction: Optional[str],
    ) -> List[DynamicMutationDirective]:
        """Derives specific mutation directives based on inputs."""
        directives: List[DynamicMutationDirective] = []

        # 1. Handle explicit failed tasks
        if failed_tasks:
            for ftid in failed_tasks:
                if ftid in graph._nodes:
                    task = graph._nodes[ftid]
                    has_ocr = any("ocr" in t.lower() for t in task.required_tools) or "ocr" in task.action.lower()
                    if has_ocr:
                        directives.append(
                            DynamicMutationDirective(
                                action_type=MutationActionType.REPLACE_TOOL,
                                target_task_id=ftid,
                                reason="OCR tool failed on poor quality input; replacing with advanced vision OCR",
                                new_tool="advanced_vision_ocr",
                            )
                        )
                    else:
                        directives.append(
                            DynamicMutationDirective(
                                action_type=MutationActionType.RETRY_WITH_HIGHER_BUDGET,
                                target_task_id=ftid,
                                reason=f"Task {ftid} failed; retrying with high-precision mode",
                            )
                        )

        # 2. Handle reflection critique recommendations
        if critique and not critique.passed:
            for issue in critique.all_issues:
                # If arithmetic or cross-field validation issue
                if any(k in issue.lower() for k in ["total", "sum", "math", "arithmetic", "mismatch"]):
                    # Find extraction task to insert validation gate after
                    for tid, node in graph._nodes.items():
                        has_extract = any("extract" in t.lower() for t in node.required_tools) or "extract" in tid.lower() or "extract" in node.action.lower()
                        if has_extract:
                            directives.append(
                                DynamicMutationDirective(
                                    action_type=MutationActionType.INSERT_VALIDATION_GATE,
                                    target_task_id=tid,
                                    reason=f"Reflection detected calculation discrepancies: {issue}",
                                )
                            )
                            break

        # 3. Handle human instruction overrides
        if human_instruction:
            directives.append(
                DynamicMutationDirective(
                    action_type=MutationActionType.RETRY_WITH_HIGHER_BUDGET,
                    target_task_id=list(graph._nodes.keys())[0] if graph._nodes else "task_root",
                    reason=f"Human operator instruction: {human_instruction}",
                )
            )

        return directives
