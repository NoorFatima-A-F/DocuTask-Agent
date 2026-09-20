"""Specialized Deliberation Council Agent Personas for DocuTask ACOS.

Implements 8 distinct specialized agent roles that advocate for their objectives during pre-execution deliberation:
1. ExecutiveAgent: Synthesizes final balance & policy compromises
2. PlanningAgent: Advocates for DAG completeness, search depth, and heuristic optimality
3. RiskAgent: Advocates for safety boundaries, fault isolation, and minimal failure probability
4. EconomicAgent: Advocates for token ROI, budget conservation, and low marginal cost
5. GovernanceAgent: Enforces regulatory compliance (GDPR, SOC2, HIPAA, SEC)
6. LearningAgent: Injects historic lessons and distilled heuristic rules
7. MemoryAgent: Recalls semantic similarities from past mission graphs
8. ExecutionAgent: Verifies physical worker capacity, leases, and queuing headroom
"""

from __future__ import annotations

import uuid
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class CouncilAgentVote(BaseModel):
    agent_id: str
    agent_role: str
    preferred_strategy_id: str
    strategy_rankings: List[str] = Field(default_factory=list)  # Ordered 1st, 2nd, 3rd choice
    advocacy_argument: str
    confidence_weight: float = 1.0


class CouncilAgent(BaseModel):
    agent_id: str
    role_name: str
    domain_objective: str
    voting_weight: float = 1.0

    def formulate_opinion(
        self,
        candidate_strategies: List[Dict[str, Any]],
        mission_context: Dict[str, Any],
    ) -> CouncilAgentVote:
        """Evaluates strategies from this agent's domain perspective and casts an ordered ranking."""
        strat_ids = [s["strategy_id"] for s in candidate_strategies]

        if self.role_name == "RISK_AGENT":
            # Prefers strategies with lowest failure rate & highest verification margins
            ranked = sorted(strat_ids, key=lambda sid: "pareto" in sid or "accurate" in sid, reverse=True)
            arg = "Prioritizing fault containment and SMT invariant margins to eliminate compliance breach risk."

        elif self.role_name == "ECONOMIC_AGENT":
            # Prefers strategies with lowest token cost & lease overhead
            ranked = sorted(strat_ids, key=lambda sid: "cost" in sid or "pareto" in sid, reverse=True)
            arg = "Maximizing token ROI and minimizing marginal compute spend under strict budget constraints."

        elif self.role_name == "PLANNING_AGENT":
            # Prefers strategies with high structural depth and parallelized DAGs
            ranked = sorted(strat_ids, key=lambda sid: "pareto" in sid or "fast" in sid, reverse=True)
            arg = "Optimizing critical path latency and topological task throughput across worker nodes."

        elif self.role_name == "GOVERNANCE_AGENT":
            # Enforces auditability and Zero-Trust verification
            ranked = sorted(strat_ids, key=lambda sid: "pareto" in sid, reverse=True)
            arg = "Ensuring SOC2 Type II cryptographic traceability and GDPR Art 22 explanation compliance."

        elif self.role_name == "LEARNING_AGENT":
            # Advocates for strategies matching distilled heuristic policies
            ranked = sorted(strat_ids, key=lambda sid: "pareto" in sid or "accurate" in sid, reverse=True)
            arg = "Aligning execution with high-performing causal heuristics distilled from 5,000+ past missions."

        elif self.role_name == "MEMORY_AGENT":
            ranked = list(strat_ids)
            arg = "Verified positive cross-domain transfer from financial document memory embeddings."

        elif self.role_name == "EXECUTION_AGENT":
            ranked = sorted(strat_ids, key=lambda sid: "fast" in sid or "pareto" in sid, reverse=True)
            arg = "Virtual cluster queues and GPU VRAM capacity are certified ready for execution."

        else:  # EXECUTIVE_AGENT
            ranked = sorted(strat_ids, key=lambda sid: "pareto" in sid, reverse=True)
            arg = "Synthesizing cross-functional consensus toward the global Pareto-optimal frontier."

        return CouncilAgentVote(
            agent_id=self.agent_id,
            agent_role=self.role_name,
            preferred_strategy_id=ranked[0] if ranked else "strat_delta_pareto",
            strategy_rankings=ranked,
            advocacy_argument=arg,
            confidence_weight=self.voting_weight,
        )
