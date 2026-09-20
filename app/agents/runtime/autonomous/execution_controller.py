"""
Execution Controller for Autonomous Runtime Brain.
Dispatches DAG tasks in concurrent topological waves, enforces security/tool policies,
handles task mutations, and captures execution metrics.
"""

from __future__ import annotations

import asyncio
import logging
import time
from typing import Any, Dict, List, Optional

from app.agents.collaboration.agent_registry import AgentRegistry
from app.agents.collaboration.reputation.performance_tracker import PerformanceTracker
from app.agents.planning.execution_plan import PlannedTask
from app.agents.runtime.autonomous.runtime_context import RuntimeContext
from app.agents.security.agent_permission import AgentPermission, AgentRole
from app.agents.security.security_guardian import SecurityGuardian
from app.agents.tools.policy.tool_decision_engine import PolicyDecision, ToolDecisionEngine
from app.agents.workflow.task_graph.dynamic_task_graph import DynamicTaskGraph, NodeState

logger = logging.getLogger(__name__)


class ExecutionController:
    """Orchestrates safe, authorized parallel task execution across DAG waves."""

    def __init__(
        self,
        security_guardian: Optional[SecurityGuardian] = None,
        tool_engine: Optional[ToolDecisionEngine] = None,
        performance_tracker: Optional[PerformanceTracker] = None,
        agent_registry: Optional[AgentRegistry] = None,
    ) -> None:
        self.security = security_guardian or SecurityGuardian()
        self.tool_engine = tool_engine or ToolDecisionEngine()
        self.tracker = performance_tracker or PerformanceTracker()
        self.registry = agent_registry

    async def execute_wave(self, graph: DynamicTaskGraph, context: RuntimeContext) -> List[str]:
        """
        Retrieves all currently READY tasks and executes them concurrently.
        Returns list of executed task IDs.
        """
        ready_tasks = graph.get_ready_tasks()
        if not ready_tasks:
            return []

        executed_ids = [t.task_id for t in ready_tasks]
        tasks = [self._execute_single_task(task, graph, context) for task in ready_tasks]
        await asyncio.gather(*tasks, return_exceptions=True)
        return executed_ids

    async def _execute_single_task(
        self,
        task: PlannedTask,
        graph: DynamicTaskGraph,
        context: RuntimeContext,
    ) -> None:
        """Executes a single task node with security, tool policy, and error handling."""
        graph.set_state(task.task_id, NodeState.RUNNING)
        start_time = time.perf_counter()
        agent_id = task.assigned_agent or "DefaultExtractorAgent"
        role = AgentRole.EXTRACTOR if any(k in task.action.lower() for k in ["extract", "ocr", "ingest", "read"]) else AgentRole.VALIDATOR

        # 1. Security Authorization Check
        auth = self.security.verify_action(
            agent_id=agent_id,
            role=role,
            permission=AgentPermission.EXECUTE_OCR if "ocr" in task.action.lower() else AgentPermission.EXECUTE_LLM,
            target_resource=task.name,
        )
        if not auth.allowed:
            err = f"Security check failed for task {task.task_id}: {auth.reason}"
            graph.set_state(task.task_id, NodeState.FAILED)
            context.record_error(err)
            return

        # 2. Tool Authorization & Privacy Masking Check
        tools_to_run = task.required_tools or ["standard_extractor"]
        effective_payload = dict(task.input_parameters)

        for tool in tools_to_run:
            tool_auth = self.tool_engine.evaluate_tool_call(
                tool_name=tool,
                payload=effective_payload,
                document_domain=context.metadata.get("domain", "FINANCIAL"),
                agent_role=role.value,
            )
            if tool_auth.decision == PolicyDecision.DENIED:
                err = f"Tool policy denied execution of tool '{tool}': {'; '.join(tool_auth.violations)}"
                graph.set_state(task.task_id, NodeState.FAILED)
                context.record_error(err)
                return
            effective_payload = tool_auth.effective_payload

        # 3. Simulate / Run Task Logic
        try:
            # Task simulation with realistic output generation based on action
            output = await self._run_task_payload(task, effective_payload, context)
            latency_ms = (time.perf_counter() - start_time) * 1000.0

            graph.record_output(task.task_id, output)
            context.set_output(task.output_key, output)

            # Record success telemetry
            self.tracker.record_outcome(
                agent_id=agent_id,
                task_id=task.task_id,
                success=True,
                latency_ms=latency_ms,
                accuracy_score=0.98,
            )
            logger.info("Task %s completed successfully in %.1f ms", task.task_id, latency_ms)

        except Exception as ex:
            latency_ms = (time.perf_counter() - start_time) * 1000.0
            logger.exception("Task %s failed: %s", task.task_id, ex)
            graph.set_state(task.task_id, NodeState.FAILED)
            context.record_error(str(ex))

            # Record failure telemetry
            self.tracker.record_outcome(
                agent_id=agent_id,
                task_id=task.task_id,
                success=False,
                latency_ms=latency_ms,
                accuracy_score=0.0,
            )

    async def _run_task_payload(
        self,
        task: PlannedTask,
        payload: Dict[str, Any],
        context: RuntimeContext,
    ) -> Dict[str, Any]:
        """Generates domain data based on task action."""
        await asyncio.sleep(0.01)  # Async yield

        action = task.action.lower()
        if "ocr" in action or "ingest" in action:
            return {
                "raw_text": "ACME Corporation Invoice #INV-2026-991 Subtotal: $1,000.00 Tax: $100.00 Total: $1,100.00",
                "vendor_name": "ACME Corporation",
                "invoice_number": "INV-2026-991",
            }
        elif "extract" in action:
            return {
                "vendor_name": "ACME Corporation",
                "invoice_number": "INV-2026-991",
                "subtotal": 1000.00,
                "tax_amount": 100.00,
                "total_amount": 1100.00,
                "currency": "USD",
                "line_items": [{"description": "Cloud Agent Runtime", "amount": 1000.00}],
            }
        elif "val" in action or "audit" in action:
            return {
                "validation_passed": True,
                "math_consistent": True,
                "risk_rating": "LOW",
            }
        return {"status": "SUCCESS", "task_id": task.task_id}
