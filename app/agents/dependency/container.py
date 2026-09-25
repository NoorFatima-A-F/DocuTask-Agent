"""
Agent Dependency Injection Container.
Provides clean dependency inversion and factory instantiation for DocumentAgent
and its 12 architectural subcomponents.
"""

from app.agents.config import AgentConfig
from app.agents.document_agent import DocumentAgent
from app.agents.interfaces.event_bus import AgentEventBus
from app.agents.interfaces.executor import AgentExecutor
from app.agents.interfaces.goal_manager import AgentGoalManager
from app.agents.interfaces.memory import AgentMemory
from app.agents.interfaces.observer import AgentObserver
from app.agents.interfaces.planner import AgentPlanner
from app.agents.interfaces.recovery import AgentRecoveryEngine
from app.agents.interfaces.reflector import AgentReflector
from app.agents.interfaces.state_manager import AgentStateManager
from app.agents.interfaces.tool_selector import AgentToolSelector
from app.agents.interfaces.workflow_manager import AgentWorkflowManager
from app.agents.metrics import AgentMetricsCollector
from app.agents.observability import AgentObservabilityHook


class AgentContainer:
    """Dependency Injection Factory Container for Autonomous Agents."""

    def __init__(self, default_config: AgentConfig | None = None):
        self.default_config = default_config or AgentConfig()
        self._planner: AgentPlanner | None = None
        self._executor: AgentExecutor | None = None
        self._observer: AgentObserver | None = None
        self._reflector: AgentReflector | None = None
        self._memory: AgentMemory | None = None
        self._recovery_engine: AgentRecoveryEngine | None = None
        self._tool_selector: AgentToolSelector | None = None
        self._workflow_manager: AgentWorkflowManager | None = None
        self._goal_manager: AgentGoalManager | None = None
        self._state_manager: AgentStateManager | None = None
        self._event_bus: AgentEventBus | None = None
        self._metrics_collector: AgentMetricsCollector | None = None
        self._observability_hook: AgentObservabilityHook | None = None

    def register_planner(self, planner: AgentPlanner) -> "AgentContainer":
        self._planner = planner
        return self

    def register_executor(self, executor: AgentExecutor) -> "AgentContainer":
        self._executor = executor
        return self

    def register_observer(self, observer: AgentObserver) -> "AgentContainer":
        self._observer = observer
        return self

    def register_reflector(self, reflector: AgentReflector) -> "AgentContainer":
        self._reflector = reflector
        return self

    def register_memory(self, memory: AgentMemory) -> "AgentContainer":
        self._memory = memory
        return self

    def register_recovery_engine(self, engine: AgentRecoveryEngine) -> "AgentContainer":
        self._recovery_engine = engine
        return self

    def register_tool_selector(self, selector: AgentToolSelector) -> "AgentContainer":
        self._tool_selector = selector
        return self

    def register_workflow_manager(self, manager: AgentWorkflowManager) -> "AgentContainer":
        self._workflow_manager = manager
        return self

    def register_goal_manager(self, manager: AgentGoalManager) -> "AgentContainer":
        self._goal_manager = manager
        return self

    def register_state_manager(self, manager: AgentStateManager) -> "AgentContainer":
        self._state_manager = manager
        return self

    def register_event_bus(self, event_bus: AgentEventBus) -> "AgentContainer":
        self._event_bus = event_bus
        return self

    def register_metrics_collector(self, metrics: AgentMetricsCollector) -> "AgentContainer":
        self._metrics_collector = metrics
        return self

    def register_observability_hook(self, hook: AgentObservabilityHook) -> "AgentContainer":
        self._observability_hook = hook
        return self

    def create_document_agent(self, config_override: AgentConfig | None = None) -> DocumentAgent:
        """Instantiates a fully wired DocumentAgent with all registered dependencies."""
        config = config_override or self.default_config
        return DocumentAgent(
            config=config,
            planner=self._planner,
            executor=self._executor,
            observer=self._observer,
            reflector=self._reflector,
            memory=self._memory,
            recovery_engine=self._recovery_engine,
            tool_selector=self._tool_selector,
            workflow_manager=self._workflow_manager,
            goal_manager=self._goal_manager,
            state_manager=self._state_manager,
            event_bus=self._event_bus,
            metrics_collector=self._metrics_collector,
            observability_hook=self._observability_hook
        )
