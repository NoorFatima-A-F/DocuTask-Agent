"""
AMCN-SIP Phase 13.8 - Swarm Runtime
Master coordinator managing the complete society of autonomous agents.
"""

from typing import Any, Dict, List, Optional
from app.runtime.swarm.runtime.agent_registry import AgentRegistry, SwarmAgentProfile
from app.runtime.swarm.runtime.agent_lifecycle import AgentLifecycleManager
from app.runtime.swarm.runtime.agent_directory import AgentDirectory
from app.runtime.swarm.runtime.agent_coordinator import AgentCoordinator
from app.runtime.swarm.communication.communication_bus import CommunicationBus
from app.runtime.swarm.negotiation.negotiation_engine import NegotiationEngine
from app.runtime.swarm.consensus.consensus_engine import ConsensusEngine
from app.runtime.swarm.coalitions.coalition_manager import CoalitionManager
from app.runtime.swarm.marketplace.task_marketplace import TaskMarketplace
from app.runtime.swarm.reputation.reputation_engine import ReputationEngine
from app.runtime.swarm.learning.swarm_learning import CollectiveLearningEngine
from app.runtime.swarm.governance.swarm_governance import SwarmGovernanceEngine
from app.runtime.swarm.explainability.coordination_replay import CoordinationReplayEngine


class SwarmRuntime:
    """
    Master runtime coordinator for autonomous agent societies.
    """

    def __init__(self):
        self.registry = AgentRegistry()
        self.lifecycle = AgentLifecycleManager()
        self.directory = AgentDirectory(self.registry)
        self.coordinator = AgentCoordinator(self.registry, self.directory)
        self.communication = CommunicationBus()
        self.negotiation = NegotiationEngine()
        self.consensus = ConsensusEngine()
        self.coalitions = CoalitionManager()
        self.marketplace = TaskMarketplace()
        self.reputation = ReputationEngine()
        self.learning = CollectiveLearningEngine()
        self.governance = SwarmGovernanceEngine()
        self.replay = CoordinationReplayEngine()

    def get_society_overview(self) -> Dict[str, Any]:
        agents = self.registry.list_agents()
        tasks = self.coordinator.get_all_tasks()
        coalitions = self.coalitions.list_coalitions()
        auctions = self.marketplace.list_auctions()
        agreements = self.negotiation.get_all_agreements()
        decisions = self.consensus.get_all_decisions()

        by_role: Dict[str, int] = {}
        for a in agents:
            r = a.role.value
            by_role[r] = by_role.get(r, 0) + 1

        avg_reputation = sum(a.reputation_score for a in agents) / max(1, len(agents))

        return {
            "total_agents": len(agents),
            "available_agents": len([a for a in agents if a.state.value == "AVAILABLE"]),
            "executing_agents": len([a for a in agents if a.state.value in ("EXECUTING", "ASSIGNED")]),
            "average_reputation": round(avg_reputation, 3),
            "agents_by_role": by_role,
            "active_tasks_count": len([t for t in tasks if t.status in ("ASSIGNED", "EXECUTING")]),
            "completed_tasks_count": len([t for t in tasks if t.status == "COMPLETED"]),
            "total_coalitions": len(coalitions),
            "active_auctions": len([auc for auc in auctions if auc.status == "OPEN"]),
            "agreements_reached": len(agreements),
            "consensus_decisions": len(decisions),
            "governance_grants": len(self.governance.list_grants()),
            "status": "SWARM_SOCIETY_HEALTHY",
        }


_GLOBAL_SWARM_RUNTIME: Optional[SwarmRuntime] = None


def get_swarm_runtime() -> SwarmRuntime:
    global _GLOBAL_SWARM_RUNTIME
    if _GLOBAL_SWARM_RUNTIME is None:
        _GLOBAL_SWARM_RUNTIME = SwarmRuntime()
    return _GLOBAL_SWARM_RUNTIME
