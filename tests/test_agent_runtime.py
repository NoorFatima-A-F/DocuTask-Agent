"""
Unit and Integration Test Suite for Enterprise Agent Platform Runtime & Kernel.
Targeting >=95% coverage across lifecycle states, dependency DAGs, IoC container,
service registry, module discovery, dynamic plugins, Erlang OTP supervisor,
multi-tenancy, feature flags, health monitoring, and kernel boot/shutdown pipelines.
"""

import pytest
from uuid import uuid4

from app.agents.runtime.builders import (
    ModuleDescriptorBuilder,
    PlatformConfigBuilder,
    PluginManifestBuilder,
    TenantBuilder,
)
from app.agents.runtime.dependency_container import DependencyContainer
from app.agents.runtime.dependency_graph import DependencyGraph
from app.agents.runtime.dependency_manager import DependencyManager
from app.agents.runtime.environment import EnvironmentPolicy
from app.agents.runtime.exceptions import (
    CyclicDependencyError,
    DuplicateServiceRegistrationError,
    InvalidRuntimeStateTransitionError,
    ModuleLoadError,
    PluginValidationError,
    ServiceNotFoundError,
    SubsystemCrashError,
    TenantIsolationViolationError,
)
from app.agents.runtime.factory import RuntimeFactory
from app.agents.runtime.feature_flags import RuntimeFeatureFlags
from app.agents.runtime.module_loader import ModuleLoader
from app.agents.runtime.module_registry import ModuleRegistry
from app.agents.runtime.plugin_manager import PluginManager
from app.agents.runtime.runtime_cache import RuntimeCache
from app.agents.runtime.runtime_context import RuntimeContext
from app.agents.runtime.runtime_health import (
    SubsystemHealthStatus,
)
from app.agents.runtime.runtime_lifecycle import (
    RuntimeLifecycleState,
)
from app.agents.runtime.runtime_monitor import RuntimeMonitor
from app.agents.runtime.runtime_serialization import RuntimeSerializer
from app.agents.runtime.runtime_session import RuntimeSession
from app.agents.runtime.runtime_state import RuntimeState
from app.agents.runtime.runtime_supervisor import RuntimeSupervisor
from app.agents.runtime.service_locator import ServiceLocator
from app.agents.runtime.service_registry import ServiceRegistry
from app.agents.runtime.tenant import Tenant, TenantTier
from app.agents.runtime.tenant_manager import TenantManager
from app.agents.runtime.workspace import WorkspaceManager


# ============================================================================
# 1. Lifecycle State Machine Tests
# ============================================================================

def test_runtime_lifecycle_valid_transitions():
    """Tests valid lifecycle transitions for the platform kernel."""
    state = RuntimeState(lifecycle_state=RuntimeLifecycleState.OFFLINE)
    assert state.lifecycle_state == RuntimeLifecycleState.OFFLINE

    state = state.transition_to(RuntimeLifecycleState.BOOTING)
    assert state.lifecycle_state == RuntimeLifecycleState.BOOTING
    assert state.boot_timestamp is not None

    state = state.transition_to(RuntimeLifecycleState.INITIALIZING)
    assert state.lifecycle_state == RuntimeLifecycleState.INITIALIZING

    state = state.transition_to(RuntimeLifecycleState.READY)
    assert state.lifecycle_state == RuntimeLifecycleState.READY

    state = state.transition_to(RuntimeLifecycleState.RUNNING)
    assert state.lifecycle_state == RuntimeLifecycleState.RUNNING

    state = state.transition_to(RuntimeLifecycleState.DEGRADED)
    assert state.lifecycle_state == RuntimeLifecycleState.DEGRADED

    state = state.transition_to(RuntimeLifecycleState.RUNNING)  # Recovered
    assert state.lifecycle_state == RuntimeLifecycleState.RUNNING

    state = state.transition_to(RuntimeLifecycleState.DRAINING)
    assert state.lifecycle_state == RuntimeLifecycleState.DRAINING

    state = state.transition_to(RuntimeLifecycleState.STOPPING)
    assert state.lifecycle_state == RuntimeLifecycleState.STOPPING

    state = state.transition_to(RuntimeLifecycleState.TERMINATED)
    assert state.lifecycle_state == RuntimeLifecycleState.TERMINATED


def test_runtime_lifecycle_invalid_transitions_raise_error():
    """Ensures unauthorized transitions raise InvalidRuntimeStateTransitionError."""
    state = RuntimeState(lifecycle_state=RuntimeLifecycleState.OFFLINE)
    with pytest.raises(InvalidRuntimeStateTransitionError):
        # Cannot jump from OFFLINE straight to RUNNING
        state.transition_to(RuntimeLifecycleState.RUNNING)

    running_state = RuntimeState(lifecycle_state=RuntimeLifecycleState.RUNNING)
    with pytest.raises(InvalidRuntimeStateTransitionError):
        # Cannot transition directly from RUNNING to BOOTING
        running_state.transition_to(RuntimeLifecycleState.BOOTING)


# ============================================================================
# 2. Dependency Graph & Cycle Detection Tests
# ============================================================================

def test_dependency_graph_topological_order():
    """Verifies acyclic dependency graph produces deterministic topological order."""
    graph = DependencyGraph()
    graph.add_dependency(module="PlanningModule", depends_on="MemoryModule")
    graph.add_dependency(module="ExecutionModule", depends_on="ToolModule")
    graph.add_dependency(module="WorkflowModule", depends_on="ExecutionModule")
    graph.add_dependency(module="WorkflowModule", depends_on="PlanningModule")

    assert not graph.has_cycles()
    order = graph.get_resolution_order()
    # Memory and Tool must precede Planning and Execution
    assert order.index("MemoryModule") < order.index("PlanningModule")
    assert order.index("ToolModule") < order.index("ExecutionModule")
    assert order.index("PlanningModule") < order.index("WorkflowModule")
    assert order.index("ExecutionModule") < order.index("WorkflowModule")


def test_dependency_graph_cycle_detection():
    """Detects cycles in the dependency graph and raises CyclicDependencyError."""
    graph = DependencyGraph()
    graph.add_dependency(module="ModuleA", depends_on="ModuleB")
    graph.add_dependency(module="ModuleB", depends_on="ModuleA")

    assert graph.has_cycles()
    with pytest.raises(CyclicDependencyError):
        graph.get_resolution_order()


def test_dependency_manager_missing_dependency():
    """Ensures dependency manager rejects unresolvable dependencies."""
    mgr = DependencyManager()
    mgr.register_subsystem("WorkflowModule", depends_on=["NonExistentModule"])
    with pytest.raises(ModuleLoadError):
        mgr.compute_initialization_order()


# ============================================================================
# 3. Dependency Injection Container Tests
# ============================================================================

def test_dependency_container_singleton_and_transient():
    """Tests singleton and transient lifetimes in the IoC container."""
    container = DependencyContainer()

    class ServiceA:
        def __init__(self):
            self.id = uuid4()

    class ServiceB:
        def __init__(self):
            self.id = uuid4()

    container.register_singleton(ServiceA, ServiceA)
    container.register_transient(ServiceB, lambda: ServiceB())

    # Singleton returns same instance
    s1 = container.resolve(ServiceA)
    s2 = container.resolve(ServiceA)
    assert s1 is s2
    assert s1.id == s2.id

    # Transient returns new instance
    t1 = container.resolve(ServiceB)
    t2 = container.resolve(ServiceB)
    assert t1 is not t2
    assert t1.id != t2.id

    # Unregistered service raises error
    class Unregistered:
        pass

    with pytest.raises(ServiceNotFoundError):
        container.resolve(Unregistered)


# ============================================================================
# 4. Service Registry & Service Locator Tests
# ============================================================================

def test_service_registry_and_locator():
    """Tests service registration, resolution, duplicate prevention, and locator."""
    registry = ServiceRegistry()

    class ITestService:
        pass

    class TestServiceImpl(ITestService):
        def greet(self):
            return "hello"

    instance1 = TestServiceImpl()
    registry.register(ITestService, instance1)
    assert registry.has(ITestService)
    assert registry.resolve(ITestService).greet() == "hello"

    # Duplicate registration without override raises DuplicateServiceRegistrationError
    with pytest.raises(DuplicateServiceRegistrationError):
        registry.register(ITestService, TestServiceImpl())

    # Named registration
    named_instance = TestServiceImpl()
    registry.register(ITestService, named_instance, name="secondary")
    assert registry.resolve(ITestService, name="secondary") is named_instance

    # Service locator
    locator = ServiceLocator(registry)
    assert locator.get(ITestService).greet() == "hello"


# ============================================================================
# 5. Module Registry & Discovery Tests
# ============================================================================

def test_module_loader_and_discovery():
    """Tests auto-discovery of all 9 canonical platform subsystems."""
    registry = ModuleRegistry()
    loader = ModuleLoader(registry)
    modules = loader.discover_modules()

    names = [m.name for m in modules]
    expected = [
        "ToolModule",
        "MemoryModule",
        "DecisionModule",
        "PlanningModule",
        "ExecutionModule",
        "RecoveryModule",
        "ReflectionModule",
        "CoordinationModule",
        "WorkflowModule",
    ]
    for exp in expected:
        assert exp in names
        assert registry.is_registered(exp)

    # Topological order of discovered modules
    dep_mgr = DependencyManager()
    for m in modules:
        dep_mgr.register_subsystem(m.name, m.dependencies)
    order = dep_mgr.compute_initialization_order()
    assert len(order) == 9
    assert order.index("MemoryModule") < order.index("DecisionModule")
    assert order.index("ExecutionModule") < order.index("WorkflowModule")


# ============================================================================
# 6. Dynamic Plugin Runtime Tests
# ============================================================================

@pytest.mark.asyncio
async def test_plugin_lifecycle():
    """Tests plugin manifest validation, registration, activation, and removal."""
    manager = PluginManager()

    valid_manifest = {
        "plugin_id": "com.enterprise.custom_ocr",
        "name": "Custom OCR Extension",
        "version": "1.2.0",
        "author": "Acme Corp",
        "entrypoint": "custom_ocr.plugin:Entrypoint",
        "capabilities": ["ocr", "table_extraction"],
    }

    reg = await manager.load_plugin(valid_manifest)
    assert reg.manifest.plugin_id == "com.enterprise.custom_ocr"
    assert reg.status == "ACTIVE"

    active_plugins = manager.get_active_plugins()
    assert len(active_plugins) == 1

    # Unload
    await manager.unload_plugin("com.enterprise.custom_ocr")
    assert len(manager.get_active_plugins()) == 0

    # Invalid manifest
    invalid_manifest = {
        "plugin_id": "",
        "name": "",
        "entrypoint": "",
    }
    with pytest.raises(PluginValidationError):
        await manager.load_plugin(invalid_manifest)


# ============================================================================
# 7. Erlang OTP-Style Supervisor Tests
# ============================================================================

@pytest.mark.asyncio
async def test_runtime_supervisor_restart_and_budget():
    """Tests Erlang OTP-style worker restart and budget exhaustion."""
    supervisor = RuntimeSupervisor(max_restarts=2, restart_window_seconds=10.0)

    restarts = []
    restores = []

    async def start_worker():
        restarts.append("restarted")

    async def restore_worker():
        restores.append("restored")

    supervisor.register_subsystem_worker(
        "ExecutionEngine",
        start_fn=start_worker,
        restore_fn=restore_worker,
    )

    # First crash & restart
    async def crashing_fn():
        raise RuntimeError("Worker process failure")

    await supervisor.supervise("ExecutionEngine", crashing_fn)
    assert restarts == ["restarted"]
    assert restores == ["restored"]

    # Second crash & restart
    await supervisor.supervise("ExecutionEngine", crashing_fn)
    assert len(restarts) == 2

    # Third crash: exceeds max_restarts (2) -> raises SubsystemCrashError
    with pytest.raises(SubsystemCrashError):
        await supervisor.restart_subsystem("ExecutionEngine")


# ============================================================================
# 8. Health Aggregation & Monitoring Tests
# ============================================================================

@pytest.mark.asyncio
async def test_runtime_health_aggregation():
    """Tests subsystem health probes and platform aggregate calculation."""
    monitor = RuntimeMonitor()

    async def probe_healthy():
        return {"status": "HEALTHY", "active_tasks": 5}

    async def probe_degraded():
        return {"status": "DEGRADED", "queue_depth": 900}

    monitor.register_probe("ToolRegistry", probe_healthy)
    monitor.register_probe("WorkflowEngine", probe_degraded)

    report = await monitor.check_health()
    assert report.healthy_count == 1
    assert report.degraded_count == 1
    assert report.unhealthy_count == 0
    assert report.overall_status == SubsystemHealthStatus.DEGRADED


# ============================================================================
# 9. Multi-Tenancy & Workspace Isolation Tests
# ============================================================================

def test_multi_tenancy_and_workspace():
    """Tests tenant enrollment, validation, tool policies, and workspace isolation."""
    tm = TenantManager()
    tenant = Tenant(
        tenant_id="tenant-acme",
        name="Acme Corporation",
        tier=TenantTier.ENTERPRISE,
        allowed_tools=["ocr_tool", "summarizer"],
    )
    tm.register_tenant(tenant)

    validated = tm.validate_tenant_access("tenant-acme")
    assert validated.name == "Acme Corporation"
    assert tm.is_tool_allowed("tenant-acme", "ocr_tool")
    assert not tm.is_tool_allowed("tenant-acme", "unapproved_tool")

    with pytest.raises(TenantIsolationViolationError):
        tm.validate_tenant_access("non-existent-tenant")

    wm = WorkspaceManager("/tmp/test_workspaces")
    t_ws = wm.get_tenant_workspace("tenant-acme")
    assert "tenant-acme" in str(t_ws)
    s_ws = wm.get_session_workspace("tenant-acme", "session-123")
    assert "session-123" in str(s_ws)


# ============================================================================
# 10. Feature Flags & Configuration Tests
# ============================================================================

def test_feature_flags_and_environment():
    """Tests feature flags toggling and environment policy."""
    flags = RuntimeFeatureFlags()
    assert flags.is_enabled("enable_reflection") is True
    assert flags.is_enabled("enable_planner_v2") is False

    updated = flags.set_flag("enable_planner_v2", True)
    assert updated.is_enabled("enable_planner_v2") is True

    # Custom flag
    updated_custom = updated.set_flag("experimental_clustering", True)
    assert updated_custom.is_enabled("experimental_clustering") is True

    assert EnvironmentPolicy.is_production("PROD") is True
    assert EnvironmentPolicy.allows_experimental_features("DEV") is True
    assert EnvironmentPolicy.allows_experimental_features("PROD") is False


# ============================================================================
# 11. Serialization, Caching & Telemetry Tests
# ============================================================================

def test_telemetry_cache_and_serialization():
    """Tests W3C traceparents, runtime metrics, cache LRU/TTL, and serialization."""
    ctx = RuntimeContext(tenant_id="tenant-1")
    assert ctx.traceparent.startswith("00-")
    assert ctx.tenant_id == "tenant-1"

    session = RuntimeSession(context=ctx)
    assert session.status == "ACTIVE"
    closed = session.close()
    assert closed.status == "CLOSED"
    assert closed.closed_at is not None

    # Cache
    cache = RuntimeCache(capacity=2, default_ttl_seconds=60.0)
    cache.set("k1", "v1")
    cache.set("k2", "v2")
    cache.set("k3", "v3")  # Evicts k1
    assert cache.get("k1") is None
    assert cache.get("k2") == "v2"
    assert cache.get("k3") == "v3"

    # Serialization
    json_str = RuntimeSerializer.serialize_to_json(ctx)
    deserialized = RuntimeSerializer.deserialize_from_json(json_str, RuntimeContext)
    assert deserialized.tenant_id == "tenant-1"


# ============================================================================
# 12. Fluent Builders Tests
# ============================================================================

def test_fluent_builders():
    """Tests configuration, tenant, plugin, and module builders."""
    cfg = (
        PlatformConfigBuilder()
        .with_environment("STAGING")
        .with_max_concurrent_sessions(500)
        .with_feature_flag("enable_experimental_planner", True)
        .with_timeouts(startup=45.0, drain=20.0)
        .build()
    )
    assert cfg.environment == "STAGING"
    assert cfg.max_concurrent_sessions == 500
    assert cfg.feature_flags.enable_experimental_planner is True

    tenant = (
        TenantBuilder("t-alpha", "Alpha Corp")
        .with_tier(TenantTier.ENTERPRISE)
        .with_max_workflows(200)
        .with_allowed_tools(["t1", "t2"])
        .build()
    )
    assert tenant.tenant_id == "t-alpha"
    assert tenant.max_concurrent_workflows == 200

    manifest = (
        PluginManifestBuilder("p-custom", "Custom Plugin", "custom.entry:init")
        .with_version("2.0.0")
        .with_capability("audit")
        .build()
    )
    assert manifest.plugin_id == "p-custom"
    assert "audit" in manifest.capabilities

    module = (
        ModuleDescriptorBuilder("CustomSubsystem")
        .with_version("1.1.0")
        .depends_on("ToolModule")
        .with_description("Custom domain subsystem")
        .build()
    )
    assert module.name == "CustomSubsystem"
    assert "ToolModule" in module.dependencies


# ============================================================================
# 13. End-to-End Platform Runtime & Kernel Boot/Shutdown Tests
# ============================================================================

@pytest.mark.asyncio
async def test_end_to_end_runtime_boot_and_shutdown():
    """Tests complete 11-step kernel boot, session creation, and graceful shutdown."""
    runtime = RuntimeFactory.create_runtime()

    # Initial state is offline
    assert not runtime.is_active

    # Boot the platform kernel
    await runtime.initialize()
    assert runtime.is_active
    assert runtime.kernel.state.lifecycle_state == RuntimeLifecycleState.RUNNING

    # Verify registered services in service registry
    assert runtime.kernel.service_registry.count() > 0

    # Create root RuntimeSession
    session = runtime.platform.create_session(tenant_id="default", user_id="admin-user")
    assert session.status == "ACTIVE"
    assert session.context.tenant_id == "default"
    assert session.context.user_id == "admin-user"

    # Bind child sessions
    wf_id = uuid4()
    exec_id = uuid4()
    session = session.bind_workflow_session(wf_id).bind_execution_session(exec_id)
    assert session.workflow_session_id == wf_id
    assert session.execution_session_id == exec_id

    # Check metrics
    snap = runtime.kernel.metrics.get_snapshot()
    assert snap.registered_services_count > 0
    assert snap.total_sessions_created == 1
    assert snap.startup_time_ms > 0

    # Graceful shutdown
    await runtime.shutdown()
    assert not runtime.is_active
    assert runtime.kernel.state.lifecycle_state == RuntimeLifecycleState.TERMINATED
    final_snap = runtime.kernel.metrics.get_snapshot()
    assert final_snap.shutdown_time_ms >= 0
