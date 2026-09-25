"""
Phase 13.17: Master AI Operations Runtime Coordinator
Orchestrates the continuous enterprise loop:
Observe -> Evaluate -> Diagnose -> Optimize -> Propose -> Experiment -> Deploy -> Monitor
"""

from __future__ import annotations
from datetime import datetime, timezone
from typing import Dict, Optional, Any
from app.runtime.ai_operations.models.schemas import (
    SpanStatus,
)
from app.runtime.ai_operations.models.events import (
    AIOpsEvent,
    AIOpsEventType,
    AIOpsEventBus,
)
from app.runtime.ai_operations.telemetry.telemetry_engine import TelemetryEngine
from app.runtime.ai_operations.evaluation.evaluation_engine import EvaluationEngine
from app.runtime.ai_operations.debugging.debugging_engine import DebuggingEngine
from app.runtime.ai_operations.optimization.model_router import ModelRouter
from app.runtime.ai_operations.optimization.prompt_optimizer import PromptOptimizer, CostOptimizer
from app.runtime.ai_operations.prediction.failure_prediction_engine import FailurePredictionEngine
from app.runtime.ai_operations.improvement.experiment_engine import ExperimentEngine
from app.runtime.ai_operations.improvement.improvement_engine import ImprovementEngine
from app.runtime.ai_operations.governance.ai_governance_engine import AIGovernanceEngine


class AIOperationsRuntime:
    """Master Control Plane for Autonomous AI Operations."""

    def __init__(self):
        self.event_bus = AIOpsEventBus()
        self.telemetry = TelemetryEngine(event_bus=self.event_bus)
        self.evaluation = EvaluationEngine()
        self.debugging = DebuggingEngine()
        self.model_router = ModelRouter()
        self.prompt_optimizer = PromptOptimizer()
        self.cost_optimizer = CostOptimizer()
        self.prediction = FailurePredictionEngine()
        self.experiment = ExperimentEngine()
        self.improvement = ImprovementEngine(experiment_engine=self.experiment, event_bus=self.event_bus)
        self.governance = AIGovernanceEngine()

    async def execute_operations_cycle(self, target_agent_id: Optional[str] = None) -> Dict[str, Any]:
        """Runs an end-to-end automated AI Operations Control Plane cycle."""
        agent_id = target_agent_id or "agent_chief_architect"

        # 1. Observe: Collect latest telemetry
        fleet = self.telemetry.get_fleet_telemetry()
        target_telemetry = next((a for a in fleet if a.agent_id == agent_id), fleet[0])

        # 2. Evaluate: Run latest evaluation benchmark
        traces = self.telemetry.collector.list_traces(limit=5, agent_id=agent_id)
        eval_result = None
        if traces:
            eval_result = self.evaluation.evaluate_trace(traces[0])
        else:
            eval_result = self.evaluation.get_evaluation_history(limit=1, agent_id=agent_id)[0]

        # 3. Diagnose: Root-cause analysis on failing or degraded traces
        failure_analysis = None
        if traces and traces[0].status == SpanStatus.ERROR:
            failure_analysis = self.debugging.diagnose_trace(traces[0])

        # 4. Predict: Predict context or failure risks
        risk_prediction = self.prediction.analyze_agent_risk(target_telemetry)

        # 5. Optimize: Evaluate Pareto model routing and prompt refinements
        route_decision = self.model_router.route_task(
            task_id=f"task_{datetime.now().strftime('%H%M%S')}",
            estimated_prompt_tokens=1800,
            estimated_completion_tokens=600,
            weight_quality=0.55,
            weight_latency=0.25,
            weight_cost=0.20,
        )

        # 6. Propose & Experiment: Generate candidate improvement & run canary A/B test
        candidate_prompt = self.prompt_optimizer.propose_prompt_refinement(
            agent_id=agent_id,
            feedback_critique="Enforce low-latency reasoning and strict factual grounding.",
        )

        experiment_record = self.experiment.run_experiment(
            name=f"Automated Canary Evaluation ({candidate_prompt.version})",
            agent_id=agent_id,
            control_version="v1.0.0",
            candidate_version=candidate_prompt.version,
            sample_size=100,
        )

        proposal = self.improvement.create_proposal_from_analysis(
            agent_id=agent_id,
            title=f"Deploy Refined System Prompt {candidate_prompt.version}",
            description="Auto-generated prompt mutation based on continuous telemetry evaluation and A/B canary validation.",
            proposal_type="PROMPT_REFINEMENT",
            changes={"prompt_id": candidate_prompt.prompt_id, "version": candidate_prompt.version},
            diff_summary=f"+ Optimized system prompt for {agent_id}\n+ Integrated safety and grounding reinforcement",
            expected_quality_delta=round(experiment_record.candidate_success_rate - experiment_record.control_success_rate, 3),
        )
        proposal.experiment_id = experiment_record.experiment_id

        # 7. Audit & Log
        audit_rec = self.governance.log_event(
            event_type="OPERATIONS_CYCLE_COMPLETED",
            actor="ai_operations_runtime",
            agent_id=agent_id,
            action_summary=f"Completed autonomous operations cycle. Generated proposal {proposal.proposal_id}.",
            compliance_passed=True,
            policy_name="ENTERPRISE_CONTROLLED_SELF_IMPROVEMENT_V1",
        )

        await self.event_bus.publish(
            AIOpsEvent(
                event_type=AIOpsEventType.PROPOSAL_GENERATED,
                agent_id=agent_id,
                payload={"proposal_id": proposal.proposal_id, "experiment_id": experiment_record.experiment_id},
            )
        )

        return {
            "cycle_status": "COMPLETED",
            "agent_id": agent_id,
            "telemetry_observed": target_telemetry.model_dump(),
            "evaluation_result": eval_result.model_dump() if eval_result else None,
            "failure_analysis": failure_analysis.model_dump() if failure_analysis else None,
            "risk_prediction": risk_prediction,
            "model_route_decision": route_decision.model_dump(),
            "experiment_result": experiment_record.model_dump(),
            "improvement_proposal": proposal.model_dump(),
            "audit_record": audit_rec.model_dump(),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }


# Global singleton instance
ai_operations_runtime = AIOperationsRuntime()
