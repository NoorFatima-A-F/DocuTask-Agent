"""
Coordination Factory.
Provides dependency injection factories for creating fully wired CoordinationEngine,
AgentRegistry, and CoordinationRuntime instances.
"""

from app.agents.coordination.agent_registry import AgentRegistry
from app.agents.coordination.coordinator import AgentCoordinator
from app.agents.coordination.delegation_executor import DelegationExecutor
from app.agents.coordination.delegation_planner import DelegationPlanner
from app.agents.coordination.engine import CoordinationEngine
from app.agents.coordination.formation import TeamFormationEngine
from app.agents.coordination.lease_manager import LeaseManager
from app.agents.coordination.manager import CoordinationManager
from app.agents.coordination.metrics import CoordinationMetricsCollector
from app.agents.coordination.orchestrator import CoordinationOrchestrator
from app.agents.coordination.presence import PresenceManager
from app.agents.coordination.repository import InMemoryTeamRepository
from app.agents.coordination.runtime import CoordinationRuntime
from app.agents.coordination.swarm import SwarmEngine


class CoordinationFactory:
    """Factory creating configured CoordinationEngine instances with full dependencies."""

    @staticmethod
    def create_engine(enable_metrics: bool = True) -> CoordinationEngine:
        """Instantiates fully wired CoordinationEngine."""
        registry = AgentRegistry()
        lease_manager = LeaseManager()
        presence_manager = PresenceManager()
        team_repo = InMemoryTeamRepository()

        manager = CoordinationManager(
            registry=registry,
            lease_manager=lease_manager,
            presence_manager=presence_manager,
            team_repository=team_repo
        )

        planner = DelegationPlanner()
        executor = DelegationExecutor(registry=registry)
        formation_engine = TeamFormationEngine()

        coordinator = AgentCoordinator(
            registry=registry,
            planner=planner,
            executor=executor,
            formation_engine=formation_engine
        )

        swarm_engine = SwarmEngine()
        orchestrator = CoordinationOrchestrator(
            registry=registry,
            coordinator=coordinator,
            swarm_engine=swarm_engine
        )

        metrics = CoordinationMetricsCollector() if enable_metrics else None

        return CoordinationEngine(
            manager=manager,
            coordinator=coordinator,
            orchestrator=orchestrator,
            metrics_collector=metrics
        )

    @staticmethod
    def create_runtime() -> CoordinationRuntime:
        """Instantiates production CoordinationRuntime container."""
        engine = CoordinationFactory.create_engine()
        return CoordinationRuntime(engine=engine)
