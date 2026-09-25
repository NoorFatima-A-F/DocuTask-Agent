"""
Enterprise Multi-Agent Coordination & Collaboration Framework.
Provides agent discovery, capability matching, delegation, communication, consensus,
team formation, and swarm intelligence.
"""

from app.agents.coordination.agent import Agent
from app.agents.coordination.agent_builder import AgentBuilder
from app.agents.coordination.agent_catalog import AgentCatalog
from app.agents.coordination.agent_directory import AgentDirectory
from app.agents.coordination.agent_factory import AgentFactory
from app.agents.coordination.agent_identity import AgentIdentity
from app.agents.coordination.agent_matcher import AgentMatcher
from app.agents.coordination.agent_profile import AgentProfile
from app.agents.coordination.agent_registry import AgentRegistry
from app.agents.coordination.agent_selector import AgentSelector
from app.agents.coordination.auction import AuctionEngine
from app.agents.coordination.builders import DelegationRequestBuilder, TeamBuilder
from app.agents.coordination.cache import CoordinationCache
from app.agents.coordination.capability import AgentSkill, CapabilityProfile
from app.agents.coordination.capability_graph import CapabilityGraph
from app.agents.coordination.capability_matcher import (
    CapabilityMatcher,
    CapabilityMatchResult,
    CapabilityRequirement,
)
from app.agents.coordination.capability_registry import CapabilityRegistry
from app.agents.coordination.collaboration import CollaborationManager, CollaborationPattern
from app.agents.coordination.collaboration_context import CollaborationContext
from app.agents.coordination.collaboration_session import CollaborationSession
from app.agents.coordination.communication import (
    AgentMessage,
    CommunicationPattern,
    MessagePerformative,
)
from app.agents.coordination.conflict_resolution import (
    ConflictRecord,
    ConflictResolutionResult,
    ConflictResolver,
    ConflictType,
)
from app.agents.coordination.consensus import ConsensusEngine, ConsensusOutcome
from app.agents.coordination.context import CoordinationContext, CoordinationRequest, CoordinationResult
from app.agents.coordination.contract_net import ContractNetEngine
from app.agents.coordination.conversation import ConversationThread
from app.agents.coordination.coordinator import AgentCoordinator
from app.agents.coordination.decision_adapter import CoordinationDecisionAdapter
from app.agents.coordination.delegation import (
    DelegationMode,
    DelegationRequest,
    DelegationResult,
    DelegationStatus,
    DelegationTask,
)
from app.agents.coordination.delegation_executor import DelegationExecutor
from app.agents.coordination.delegation_planner import DelegationPlanner
from app.agents.coordination.delegation_policy import DelegationPolicy
from app.agents.coordination.dispatcher import AgentTaskDispatcher
from app.agents.coordination.distributed_state import DistributedStateStore, StateEntry
from app.agents.coordination.engine import CoordinationEngine
from app.agents.coordination.events import (
    AgentAvailableEvent,
    AgentRegisteredEvent,
    AgentSelectedEvent,
    CapabilityMatchedEvent,
    ConflictDetectedEvent,
    ConflictResolvedEvent,
    ConsensusReachedEvent,
    DelegationCompletedEvent,
    DelegationStartedEvent,
    NegotiationCompletedEvent,
    NegotiationStartedEvent,
    SwarmCompletedEvent,
    SwarmStartedEvent,
    TeamCreatedEvent,
    TeamDisbandedEvent,
)
from app.agents.coordination.exceptions import (
    AgentNotFoundError,
    CircularDelegationError,
    ConsensusNotReachedError,
    CoordinationException,
    DuplicateAgentIdError,
    InconsistentSharedStateError,
    InvalidCommunicationRouteError,
    MissingCapabilityError,
    OrphanedTeamError,
    StaleLeaseError,
    UnsupportedProtocolError,
)
from app.agents.coordination.execution_adapter import CoordinationExecutionAdapter
from app.agents.coordination.factory import CoordinationFactory
from app.agents.coordination.formation import TeamFormationEngine
from app.agents.coordination.health_monitor import AgentHealthMonitor, AgentHealthStatus
from app.agents.coordination.heartbeat import AgentHeartbeat
from app.agents.coordination.interfaces import (
    IAgentCoordinator,
    IAgentRegistry,
    ICapabilityMatcher,
    IConflictResolver,
    IConsensusEngine,
    IDelegationEngine,
    ILeaderElectionEngine,
    IMessageRouter,
)
from app.agents.coordination.leader_election import LeaderElectionEngine
from app.agents.coordination.lease_manager import LeaseManager, TaskLease
from app.agents.coordination.lifecycle import AgentLifecycleState, CoordinationLifecycleState
from app.agents.coordination.load_balancer import AgentLoadBalancer, LoadBalancingStrategy
from app.agents.coordination.manager import CoordinationManager
from app.agents.coordination.memory_adapter import CoordinationMemoryAdapter
from app.agents.coordination.message_bus import CoordinationMessageBus
from app.agents.coordination.message_router import MessageRouter
from app.agents.coordination.metadata import (
    CoordinationIdentity,
    CoordinationMetadata,
    CoordinationStatistics,
)
from app.agents.coordination.metrics import CoordinationMetricsCollector, CoordinationMetricsSnapshot
from app.agents.coordination.negotiation import Bid, NegotiationSession
from app.agents.coordination.orchestrator import CoordinationOrchestrator
from app.agents.coordination.planner_adapter import CoordinationPlannerAdapter
from app.agents.coordination.presence import PresenceManager, PresenceState
from app.agents.coordination.protocol import ProtocolState, ProtocolType
from app.agents.coordination.recovery_adapter import CoordinationRecoveryAdapter
from app.agents.coordination.reflection_adapter import CoordinationReflectionAdapter
from app.agents.coordination.repository import InMemoryTeamRepository, TeamRepository
from app.agents.coordination.resource_sharing import ResourceSharingManager, SharedResourceQuota
from app.agents.coordination.runtime import CoordinationRuntime
from app.agents.coordination.scheduler import DistributedAgentScheduler, ScheduledTaskItem
from app.agents.coordination.serialization import CoordinationSerializer
from app.agents.coordination.shared_context import SharedContext, SharedContextRecord
from app.agents.coordination.shared_memory import MemoryReference, SharedMemoryBridge
from app.agents.coordination.supervisor import SupervisorAgent
from app.agents.coordination.swarm import SwarmEngine, SwarmExecutionPattern, SwarmResult, SwarmTask
from app.agents.coordination.task_assignment import AssignmentMatrix, TaskAssignment
from app.agents.coordination.team import Team, TeamMember, TeamRole, TeamType
from app.agents.coordination.telemetry import CoordinationTelemetry
from app.agents.coordination.tool_adapter import CoordinationToolAdapter
from app.agents.coordination.validation import CoordinationValidationReport
from app.agents.coordination.validators import CoordinationValidator
from app.agents.coordination.voting import AgentVote, VotingEngine, VotingResult
from app.agents.coordination.work_stealing import WorkStealingPool

__all__ = [
    "Agent",
    "AgentIdentity",
    "AgentProfile",
    "AgentRegistry",
    "AgentDirectory",
    "AgentCatalog",
    "AgentFactory",
    "AgentBuilder",
    "AgentSelector",
    "AgentMatcher",
    "AgentLifecycleState",
    "CoordinationLifecycleState",
    "CapabilityProfile",
    "AgentSkill",
    "CapabilityRegistry",
    "CapabilityGraph",
    "CapabilityMatcher",
    "CapabilityRequirement",
    "CapabilityMatchResult",
    "DelegationMode",
    "DelegationStatus",
    "DelegationTask",
    "DelegationRequest",
    "DelegationResult",
    "DelegationPolicy",
    "DelegationPlanner",
    "DelegationExecutor",
    "CollaborationContext",
    "CollaborationSession",
    "CollaborationManager",
    "CollaborationPattern",
    "AgentMessage",
    "MessagePerformative",
    "CommunicationPattern",
    "ConversationThread",
    "MessageRouter",
    "CoordinationMessageBus",
    "ProtocolType",
    "ProtocolState",
    "Bid",
    "NegotiationSession",
    "ContractNetEngine",
    "AuctionEngine",
    "AgentVote",
    "VotingResult",
    "VotingEngine",
    "ConsensusEngine",
    "ConsensusOutcome",
    "LeaderElectionEngine",
    "ConflictType",
    "ConflictRecord",
    "ConflictResolutionResult",
    "ConflictResolver",
    "Team",
    "TeamRole",
    "TeamType",
    "TeamMember",
    "TeamFormationEngine",
    "SwarmEngine",
    "SwarmExecutionPattern",
    "SwarmTask",
    "SwarmResult",
    "SharedContext",
    "SharedContextRecord",
    "MemoryReference",
    "SharedMemoryBridge",
    "DistributedStateStore",
    "StateEntry",
    "TaskAssignment",
    "AssignmentMatrix",
    "AgentLoadBalancer",
    "LoadBalancingStrategy",
    "WorkStealingPool",
    "ResourceSharingManager",
    "SharedResourceQuota",
    "AgentHeartbeat",
    "AgentHealthMonitor",
    "AgentHealthStatus",
    "PresenceManager",
    "PresenceState",
    "TaskLease",
    "LeaseManager",
    "ScheduledTaskItem",
    "DistributedAgentScheduler",
    "AgentTaskDispatcher",
    "SupervisorAgent",
    "AgentCoordinator",
    "CoordinationOrchestrator",
    "CoordinationManager",
    "CoordinationEngine",
    "CoordinationRuntime",
    "CoordinationFactory",
    "CoordinationTelemetry",
    "CoordinationMetricsCollector",
    "CoordinationMetricsSnapshot",
    "CoordinationSerializer",
    "DelegationRequestBuilder",
    "TeamBuilder",
    "CoordinationValidator",
    "CoordinationValidationReport",
    "CoordinationContext",
    "CoordinationRequest",
    "CoordinationResult",
    "CoordinationIdentity",
    "CoordinationMetadata",
    "CoordinationStatistics",
    "CoordinationExecutionAdapter",
    "CoordinationPlannerAdapter",
    "CoordinationRecoveryAdapter",
    "CoordinationReflectionAdapter",
    "CoordinationDecisionAdapter",
    "CoordinationMemoryAdapter",
    "CoordinationToolAdapter",
    "CoordinationCache",
    "InMemoryTeamRepository",
    "TeamRepository",
    "CoordinationException",
    "DuplicateAgentIdError",
    "AgentNotFoundError",
    "MissingCapabilityError",
    "CircularDelegationError",
    "OrphanedTeamError",
    "InvalidCommunicationRouteError",
    "StaleLeaseError",
    "InconsistentSharedStateError",
    "UnsupportedProtocolError",
    "ConsensusNotReachedError",
]
