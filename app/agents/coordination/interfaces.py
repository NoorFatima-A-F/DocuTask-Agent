"""
Interfaces for the Enterprise Multi-Agent Coordination & Collaboration Framework.
Defines abstract contracts for coordinators, supervisors, registries, delegation, and protocols.
"""

from abc import ABC, abstractmethod
from typing import Any, List, Optional
from uuid import UUID


class IAgentCoordinator(ABC):
    """Core contract for distributed multi-agent coordination."""

    @abstractmethod
    async def coordinate(self, request: Any) -> Any:
        """Coordinates multi-agent discovery, delegation, execution, and synthesis."""
        raise NotImplementedError


class IAgentRegistry(ABC):
    """Contract for registering and discovering agent identities and profiles."""

    @abstractmethod
    async def register(self, agent: Any) -> None:
        """Registers an agent."""
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, agent_id: UUID) -> Optional[Any]:
        """Retrieves an agent by UUID."""
        raise NotImplementedError

    @abstractmethod
    async def list_available(self) -> List[Any]:
        """Lists currently available agents."""
        raise NotImplementedError


class ICapabilityMatcher(ABC):
    """Contract for matching task requirements against agent capabilities."""

    @abstractmethod
    def match_capabilities(self, required: Any, candidates: List[Any]) -> List[Any]:
        """Returns scored candidate agents meeting capability constraints."""
        raise NotImplementedError


class IDelegationEngine(ABC):
    """Contract for planning and executing multi-agent delegations."""

    @abstractmethod
    async def delegate_task(self, request: Any) -> Any:
        """Delegates work across single, multiple, or hierarchical agents."""
        raise NotImplementedError


class IMessageRouter(ABC):
    """Contract for routing messages across agents, swarms, and teams."""

    @abstractmethod
    async def send_message(self, message: Any) -> None:
        """Sends a point-to-point, broadcast, or multicast message."""
        raise NotImplementedError


class IConsensusEngine(ABC):
    """Contract for achieving distributed consensus or quorum voting across agent groups."""

    @abstractmethod
    async def reach_consensus(self, topic: str, votes: List[Any]) -> Any:
        """Evaluates votes and resolves consensus outcome."""
        raise NotImplementedError


class ILeaderElectionEngine(ABC):
    """Contract for electing team leaders or coordinator supervisors."""

    @abstractmethod
    async def elect_leader(self, candidates: List[Any]) -> Any:
        """Elects a leader from candidate pool."""
        raise NotImplementedError


class IConflictResolver(ABC):
    """Contract for resolving resource, capability, or schedule conflicts between agents."""

    @abstractmethod
    def resolve_conflict(self, conflict: Any) -> Any:
        """Resolves conflict according to predefined policy."""
        raise NotImplementedError
