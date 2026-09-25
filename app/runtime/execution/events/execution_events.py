"""
Phase 13.15: Execution Platform Events and Types
Defines event types, enums, data contracts, and event bus for cyber-physical and real-world execution.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Dict, List, Optional
import uuid


class ToolType(str, Enum):
    REST_API = "rest_api"
    GRAPHQL = "graphql"
    GRPC = "grpc"
    DATABASE = "database"
    CLOUD_SDK = "cloud_sdk"
    CLI = "cli"
    BROWSER = "browser"
    SAAS = "saas"
    KUBERNETES = "kubernetes"
    CYBER_PHYSICAL = "cyber_physical"
    CUSTOM = "custom"


class ToolStatus(str, Enum):
    ACTIVE = "active"
    DEGRADED = "degraded"
    OFFLINE = "offline"
    MAINTENANCE = "maintenance"
    DEPRECATED = "deprecated"


class ConnectorCategory(str, Enum):
    CLOUD = "cloud"
    DATABASE = "database"
    COMMUNICATION = "communication"
    CODE_REPOSITORY = "code_repository"
    CRM_ERP = "crm_erp"
    INFRASTRUCTURE = "infrastructure"
    PAYMENT_FINANCE = "payment_finance"
    BROWSER_VISION = "browser_vision"
    CUSTOM_API = "custom_api"


class ConnectorStatus(str, Enum):
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    AUTHENTICATING = "authenticating"
    ERROR = "error"
    RATE_LIMITED = "rate_limited"


class MissionStatus(str, Enum):
    DRAFT = "draft"
    PLANNING = "planning"
    VALIDATING = "validating"
    SIMULATING = "simulating"
    AWAITING_APPROVAL = "awaiting_approval"
    EXECUTING = "executing"
    VERIFYING = "verifying"
    COMPLETED = "completed"
    FAILED = "failed"
    COMPENSATING = "compensating"
    ROLLED_BACK = "rolled_back"
    CANCELLED = "cancelled"


class WorkflowExecutionMode(str, Enum):
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    DAG = "dag"
    SAGA = "saga"


class StepStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    SIMULATED = "simulated"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"
    COMPENSATING = "compensating"
    COMPENSATED = "compensated"


class RiskLevel(str, Enum):
    MINIMAL = "minimal"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class PolicyDecision(str, Enum):
    ALLOW = "allow"
    DENY = "deny"
    REQUIRE_APPROVAL = "require_approval"
    REQUIRE_SIMULATION = "require_simulation"


class CredentialType(str, Enum):
    API_KEY = "api_key"
    BEARER_TOKEN = "bearer_token"
    OAUTH2 = "oauth2"
    MUTUAL_TLS = "mutual_tls"
    SSH_KEY = "ssh_key"
    AWS_IAM = "aws_iam"
    GCP_ADC = "gcp_adc"
    VAULT_SECRET = "vault_secret"


class ExecutionEventType(str, Enum):
    # Tool Registry Events
    TOOL_REGISTERED = "tool.registered"
    TOOL_UPDATED = "tool.updated"
    TOOL_DEPRECATED = "tool.deprecated"
    TOOL_HEALTH_CHECKED = "tool.health_checked"

    # Connector Events
    CONNECTOR_CREATED = "connector.created"
    CONNECTOR_AUTHENTICATED = "connector.authenticated"
    CONNECTOR_FAILED = "connector.failed"
    CONNECTOR_DISCONNECTED = "connector.disconnected"

    # Browser Events
    BROWSER_SESSION_STARTED = "browser.session_started"
    BROWSER_NAVIGATED = "browser.navigated"
    BROWSER_ACTION_PERFORMED = "browser.action_performed"
    BROWSER_SCREENSHOT_CAPTURED = "browser.screenshot_captured"
    BROWSER_SESSION_CLOSED = "browser.session_closed"

    # Planner Events
    PLAN_GENERATED = "planner.plan_generated"
    PLAN_OPTIMIZED = "planner.plan_optimized"
    PLAN_VALIDATED = "planner.plan_validated"

    # Policy & Governance Events
    POLICY_EVALUATED = "policy.evaluated"
    APPROVAL_REQUESTED = "governance.approval_requested"
    APPROVAL_GRANTED = "governance.approval_granted"
    APPROVAL_REJECTED = "governance.approval_rejected"

    # Simulation Events
    SIMULATION_STARTED = "simulation.started"
    SIMULATION_STEP_COMPLETED = "simulation.step_completed"
    SIMULATION_CONCLUDED = "simulation.concluded"

    # Execution Events
    MISSION_STARTED = "mission.started"
    MISSION_STEP_STARTED = "mission.step_started"
    MISSION_STEP_COMPLETED = "mission.step_completed"
    MISSION_STEP_FAILED = "mission.step_failed"
    MISSION_COMPLETED = "mission.completed"
    MISSION_FAILED = "mission.failed"

    # Verification Events
    VERIFICATION_STARTED = "verification.started"
    VERIFICATION_PASSED = "verification.passed"
    VERIFICATION_FAILED = "verification.failed"

    # Rollback & Compensation Events
    ROLLBACK_TRIGGERED = "rollback.triggered"
    STEP_COMPENSATED = "rollback.step_compensated"
    ROLLBACK_COMPLETED = "rollback.completed"
    ROLLBACK_FAILED = "rollback.failed"

    # Audit & Monitoring Events
    AUDIT_LOG_APPENDED = "audit.log_appended"
    ANOMALY_DETECTED = "monitoring.anomaly_detected"
    METRIC_RECORDED = "monitoring.metric_recorded"


@dataclass
class ExecutionEvent:
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    event_type: ExecutionEventType = ExecutionEventType.MISSION_STARTED
    source: str = "execution_runtime"
    payload: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    correlation_id: Optional[str] = None
    risk_level: RiskLevel = RiskLevel.LOW

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type.value if isinstance(self.event_type, ExecutionEventType) else str(self.event_type),
            "source": self.source,
            "payload": self.payload,
            "timestamp": self.timestamp,
            "correlation_id": self.correlation_id,
            "risk_level": self.risk_level.value if isinstance(self.risk_level, RiskLevel) else str(self.risk_level),
        }


class ExecutionEventBus:
    """In-memory reactive event dispatcher for execution subsystem."""

    def __init__(self):
        self._subscribers: Dict[str, List[Callable[[ExecutionEvent], None]]] = {}
        self._history: List[ExecutionEvent] = []
        self._max_history: int = 1000

    def subscribe(self, event_type: str, handler: Callable[[ExecutionEvent], None]) -> None:
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)

    def subscribe_all(self, handler: Callable[[ExecutionEvent], None]) -> None:
        self.subscribe("*", handler)

    def publish(self, event: ExecutionEvent) -> None:
        self._history.append(event)
        if len(self._history) > self._max_history:
            self._history.pop(0)

        # Dispatch to specific subscribers
        event_key = event.event_type.value if isinstance(event.event_type, ExecutionEventType) else str(event.event_type)
        if event_key in self._subscribers:
            for handler in self._subscribers[event_key]:
                try:
                    handler(event)
                except Exception as e:
                    print(f"Error in execution event handler for {event_key}: {e}")

        # Dispatch to wildcard subscribers
        if "*" in self._subscribers:
            for handler in self._subscribers["*"]:
                try:
                    handler(event)
                except Exception as e:
                    print(f"Error in execution wildcard event handler: {e}")

    def get_history(self, limit: int = 100, event_type: Optional[str] = None) -> List[Dict[str, Any]]:
        filtered = self._history
        if event_type:
            filtered = [
                e for e in filtered
                if (e.event_type.value if isinstance(e.event_type, ExecutionEventType) else str(e.event_type)) == event_type
            ]
        return [e.to_dict() for e in filtered[-limit:]]

    def clear(self) -> None:
        self._history.clear()
        self._subscribers.clear()


# Global Execution Event Bus Singleton
execution_event_bus = ExecutionEventBus()
