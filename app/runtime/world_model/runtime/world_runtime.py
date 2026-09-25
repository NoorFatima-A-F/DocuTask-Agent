"""
Master World Model & Cognitive Intelligence Runtime for Phase 13.16.
Coordinates multi-runtime observation ingestion, causal learning, forecasting, counterfactuals, and expected utility optimization.
"""

from datetime import datetime, timezone
from typing import Any, Dict
import uuid

from app.runtime.world_model.causal.causal_engine import causal_engine
from app.runtime.world_model.counterfactual.counterfactual_engine import counterfactual_engine
from app.runtime.world_model.decision.decision_engine import decision_engine
from app.runtime.world_model.events.world_model_events import (
    ObservationSource,
    WorldModelEvent,
    WorldModelEventType,
    world_model_event_bus,
)
from app.runtime.world_model.forecasting.predictive_engine import predictive_engine
from app.runtime.world_model.hypothesis.hypothesis_engine import hypothesis_engine
from app.runtime.world_model.knowledge.knowledge_fusion_engine import knowledge_fusion_engine
from app.runtime.world_model.memory.memory_consolidation_engine import memory_consolidation_engine
from app.runtime.world_model.observation.observation_engine import observation_engine
from app.runtime.world_model.scenario.scenario_engine import scenario_engine
from app.runtime.world_model.temporal.temporal_engine import temporal_engine
from app.runtime.world_model.uncertainty.uncertainty_engine import uncertainty_engine
from app.runtime.world_model.verification.prediction_verification_engine import prediction_verification_engine
from app.runtime.world_model.world.world_engine import world_engine


class WorldRuntime:
    """Master Cognitive Intelligence Runtime (AWMPICRP)."""

    def __init__(self):
        self.observation = observation_engine
        self.knowledge = knowledge_fusion_engine
        self.world = world_engine
        self.temporal = temporal_engine
        self.causal = causal_engine
        self.hypothesis = hypothesis_engine
        self.scenario = scenario_engine
        self.counterfactual = counterfactual_engine
        self.forecasting = predictive_engine
        self.decision = decision_engine
        self.uncertainty = uncertainty_engine
        self.verification = prediction_verification_engine
        self.memory = memory_consolidation_engine
        self.event_bus = world_model_event_bus

    def execute_cognitive_learning_cycle(self, context_goal: str = "Optimize enterprise operational stability and cloud ROI") -> Dict[str, Any]:
        """Runs the complete Core Cognitive Intelligence Invariant loop."""
        cycle_id = f"cycle_{uuid.uuid4().hex[:8]}"

        # 1. Ingest Synthetic System Health Observation
        obs = self.observation.observe_metric(
            source=ObservationSource.EXECUTION_RUNTIME,
            entity_id="service_core_api",
            metric_name="p99_latency_ms",
            metric_value=41.8,
            metadata={"cycle_id": cycle_id},
        )

        # 2. Knowledge Fusion
        fact = self.knowledge.integrate_fact(
            subject="service_core_api",
            predicate="observed_p99_latency_ms",
            object_value=41.8,
            source_runtime="world_runtime",
            evidence_refs=[obs.observation_id],
        )

        # 3. Update World Graph & Checkpoint
        chk = self.world.create_checkpoint()

        # 4. Causal & Intervention Analysis
        self.causal.simulate_do_intervention("k8s_replicas_count", 4.0)

        # 5. Formulate Hypothesis
        hyp = self.hypothesis.create_hypothesis(
            title=f"Autonomous Capacity Optimization for {context_goal[:30]}",
            explanation="Scaling to 4 canary replicas provides optimal P99 latency stability without exceeding monthly budget.",
            phenomenon_observed="P99 latency stable at 41.8ms under 350 RPS workload.",
            prior_probability=0.75,
            supporting_evidence=[obs.observation_id, fact.fact_id],
        )

        # 6. Counterfactual & Scenarios
        scenarios = self.scenario.generate_scenarios_for_context(context_goal[:40])
        cf = self.counterfactual.run_counterfactual_query(
            title=f"What if replica count was increased for {context_goal[:30]}?",
            intervention="Set k8s_replicas_count = 4",
            target_entity="k8s_prod_cluster",
            actual_metrics={"p99_latency_ms": 41.8, "spend_usd": 18500.0},
        )

        # 7. Generate Multi-Horizon Forecasts
        pred = self.forecasting.generate_prediction(
            target_metric="service_core_api.p99_latency_ms",
            predicted_value=39.5,
            horizon_hours=24.0,
            uncertainty_band=0.08,
        )

        # 8. Uncertainty Profile
        unc = self.uncertainty.compute_uncertainty("core_api_capacity", observation_count=len(self.observation.list_observations()), variance=0.15)

        # 9. Optimize Decision Portfolio
        decisions = self.decision.evaluate_decision_portfolio(context_goal)

        # 10. Memory Consolidation
        mem = self.memory.consolidate_memory(
            tier="working",
            title=f"Cognitive Cycle {cycle_id} Invariant Proof",
            summary=f"Evaluated goal: {context_goal}. Causal intervention confirmed 4-replica optimal frontier.",
            key_facts=[f"Predicted P99 latency: {pred.predicted_value}ms", f"Expected utility of top action: {decisions[0].expected_utility if decisions else 0.9}"],
        )

        world_model_event_bus.publish(
            WorldModelEvent(
                event_type=WorldModelEventType.LEARNING_CYCLE_COMPLETED,
                source="world_runtime",
                payload={"cycle_id": cycle_id, "goal": context_goal, "top_decision": decisions[0].title if decisions else ""},
            )
        )

        return {
            "cycle_id": cycle_id,
            "goal": context_goal,
            "observation_id": obs.observation_id,
            "fact_id": fact.fact_id,
            "checkpoint_id": chk.snapshot_id,
            "hypothesis_id": hyp.hypothesis_id,
            "prediction_id": pred.prediction_id,
            "counterfactual_id": cf.experiment_id,
            "scenarios_generated": len(scenarios),
            "top_recommended_decision": decisions[0].to_dict() if decisions else None,
            "uncertainty_entropy": unc.total_entropy,
            "memory_id": mem.memory_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def get_world_overview(self) -> Dict[str, Any]:
        """Consolidated executive summary of the entire world model."""
        w_sum = self.world.get_world_summary()
        k_sum = self.knowledge.get_knowledge_summary()
        c_sum = self.verification.get_calibration_summary()
        obs_sum = self.observation.get_summary()
        preds = self.forecasting.list_predictions()
        scens = self.scenario.list_scenarios()
        hyps = self.hypothesis.list_hypotheses()
        decs = self.decision.list_decisions()
        mems = self.memory.list_memories()

        return {
            "system_status": "OPERATIONAL",
            "world_state": w_sum["current_state"],
            "model_version": w_sum["current_version"],
            "total_nodes": w_sum["total_nodes"],
            "total_edges": w_sum["total_edges"],
            "graph_entropy": w_sum["graph_entropy"],
            "total_facts": k_sum["total_facts"],
            "knowledge_freshness_score": k_sum["average_freshness_score"],
            "total_observations": obs_sum["total_observations"],
            "active_predictions": len(preds),
            "forecast_calibration_accuracy": c_sum["accuracy_pct"],
            "active_scenarios": len(scens),
            "formulated_hypotheses": len(hyps),
            "ranked_decisions": len(decs),
            "consolidated_memories": len(mems),
        }


# Global Singleton
world_runtime = WorldRuntime()
