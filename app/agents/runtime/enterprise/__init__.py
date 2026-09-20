"""
Enterprise Platform Runtime Capabilities.
Subsystems providing distributed scheduling, version negotiation, rolling upgrades, circuit breaking,
bulkhead isolation, backpressure admission, leader election, secret management, immutable audit logs,
and chaos verification.
"""

from app.agents.runtime.enterprise.admission_controller import (
    AdmissionController,
    RequestSheddedError,
)
from app.agents.runtime.enterprise.audit_event import AuditEventType, RuntimeAuditEvent
from app.agents.runtime.enterprise.audit_log import ImmutableRuntimeAuditLog
from app.agents.runtime.enterprise.backpressure import (
    BackpressureMonitor,
    BackpressureState,
)
from app.agents.runtime.enterprise.chaos_engine import (
    ChaosEngine,
    ChaosExperimentResult,
)
from app.agents.runtime.enterprise.circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerOpenError,
    CircuitState,
)
from app.agents.runtime.enterprise.compatibility_checker import VersionCompatibilityChecker
from app.agents.runtime.enterprise.distributed_scheduler import DistributedScheduler
from app.agents.runtime.enterprise.fault_injector import (
    FaultInjector,
    FaultType,
    InjectedFaultException,
)
from app.agents.runtime.enterprise.leader_election import (
    LeaderElectionCoordinator,
    LeaderLease,
)
from app.agents.runtime.enterprise.migration_manager import MigrationManager
from app.agents.runtime.enterprise.quota_manager import QuotaManager, TenantQuota
from app.agents.runtime.enterprise.resource_isolation import (
    Bulkhead,
    BulkheadCapacityExceededError,
)
from app.agents.runtime.enterprise.rolling_upgrade import (
    DeploymentSlot,
    RollingUpgradeManager,
    UpgradeStatus,
)
from app.agents.runtime.enterprise.scheduler_state import (
    JobPriority,
    JobStatus,
    ScheduledJob,
)
from app.agents.runtime.enterprise.secret_manager import (
    EnvironmentSecretProvider,
    InMemorySecretProvider,
    ISecretProvider,
    SecretManager,
)
from app.agents.runtime.enterprise.version_manager import (
    IncompatibleVersionError,
    RuntimeVersionManager,
)

__all__ = [
    # Scheduler
    "DistributedScheduler",
    "ScheduledJob",
    "JobPriority",
    "JobStatus",
    # Version Negotiation
    "VersionCompatibilityChecker",
    "RuntimeVersionManager",
    "IncompatibleVersionError",
    # Rolling Upgrades
    "RollingUpgradeManager",
    "DeploymentSlot",
    "UpgradeStatus",
    "MigrationManager",
    # Circuit Breaker
    "CircuitBreaker",
    "CircuitState",
    "CircuitBreakerOpenError",
    # Bulkhead & Quota
    "Bulkhead",
    "BulkheadCapacityExceededError",
    "QuotaManager",
    "TenantQuota",
    # Backpressure & Admission
    "BackpressureMonitor",
    "BackpressureState",
    "AdmissionController",
    "RequestSheddedError",
    # Leader Election
    "LeaderElectionCoordinator",
    "LeaderLease",
    # Secrets
    "SecretManager",
    "ISecretProvider",
    "EnvironmentSecretProvider",
    "InMemorySecretProvider",
    # Audit Log
    "ImmutableRuntimeAuditLog",
    "RuntimeAuditEvent",
    "AuditEventType",
    # Chaos
    "ChaosEngine",
    "ChaosExperimentResult",
    "FaultInjector",
    "FaultType",
    "InjectedFaultException",
]
