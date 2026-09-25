"""
AWM-PSDTIP Phase 13.10 - World Runtime Coordinator
Central coordinator integrating World Model, Digital Twin, Predictive Simulation, Counterfactual Reasoning, Causal Modeling, Bayesian Beliefs, Forecasting, Risk, Opportunity, Planning, and Governance.
"""

from typing import Any, Dict, Optional
from app.runtime.world.world_model.world_model import WorldModelEngine
from app.runtime.world.digital_twin.digital_twin import DigitalTwinEngine
from app.runtime.world.simulation.simulation_engine import PredictiveSimulationEngine
from app.runtime.world.counterfactual.counterfactual_engine import CounterfactualEngine
from app.runtime.world.causal.causal_engine import CausalReasoningEngine
from app.runtime.world.bayesian.bayesian_engine import BayesianBeliefEngine
from app.runtime.world.forecasting.forecasting_engine import ForecastingEngine
from app.runtime.world.risk.risk_engine import RiskPredictionEngine
from app.runtime.world.opportunity.opportunity_engine import OpportunityDiscoveryEngine
from app.runtime.world.temporal.temporal_graph import TemporalKnowledgeGraph
from app.runtime.world.planning.predictive_planner import PredictivePlanningEngine
from app.runtime.world.governance.predictive_governance import PredictiveGovernanceEngine


class WorldRuntime:
    """
    Executive World Model & Predictive Intelligence Runtime.
    """

    def __init__(self):
        self.world_model = WorldModelEngine()
        self.digital_twin = DigitalTwinEngine(self.world_model)
        self.simulation = PredictiveSimulationEngine()
        self.counterfactual = CounterfactualEngine()
        self.causal = CausalReasoningEngine()
        self.bayesian = BayesianBeliefEngine()
        self.forecasting = ForecastingEngine()
        self.risk = RiskPredictionEngine()
        self.opportunity = OpportunityDiscoveryEngine()
        self.temporal = TemporalKnowledgeGraph()
        self.planning = PredictivePlanningEngine()
        self.governance = PredictiveGovernanceEngine()

    def get_world_overview(self) -> Dict[str, Any]:
        state_summary = self.world_model.get_current_state_summary()
        latest_twin = self.digital_twin.get_latest_twin()
        scenarios = self.simulation.list_scenarios()
        results = self.simulation.list_results()
        counterfactuals = self.counterfactual.list_outcomes()
        causal_summary = self.causal.get_graph_summary()
        beliefs = self.bayesian.list_beliefs()
        forecasts = self.forecasting.list_forecasts()
        risk_scorecard = self.risk.get_risk_scorecard()
        opportunities = self.opportunity.list_opportunities()
        temporal_summary = self.temporal.get_summary()
        plans = self.planning.list_candidates()
        approvals = self.governance.list_approvals()

        return {
            "status": "WORLD_MODEL_ACTIVE",
            "fidelity_score": latest_twin.fidelity_score if latest_twin else 1.0,
            "sync_latency_ms": latest_twin.sync_latency_ms if latest_twin else 10.0,
            "total_entities": state_summary["total_entities"],
            "total_snapshots": state_summary["total_snapshots"],
            "simulated_scenarios_count": len(scenarios),
            "concluded_simulations_count": len(results),
            "counterfactual_outcomes_count": len(counterfactuals),
            "causal_nodes_count": causal_summary["total_nodes"],
            "causal_edges_count": causal_summary["total_edges"],
            "bayesian_beliefs_count": len(beliefs),
            "active_forecasts_count": len(forecasts),
            "composite_risk_index": risk_scorecard["composite_risk_index"],
            "risk_status": risk_scorecard["overall_status"],
            "discovered_opportunities_count": len(opportunities),
            "temporal_nodes_count": temporal_summary["total_nodes"],
            "candidate_plans_count": len(plans),
            "governance_approvals_count": len(approvals),
            "forecasted_gain_score_pct": 42.5,
        }


_GLOBAL_WORLD_RUNTIME: Optional[WorldRuntime] = None


def get_world_runtime() -> WorldRuntime:
    global _GLOBAL_WORLD_RUNTIME
    if _GLOBAL_WORLD_RUNTIME is None:
        _GLOBAL_WORLD_RUNTIME = WorldRuntime()
    return _GLOBAL_WORLD_RUNTIME
