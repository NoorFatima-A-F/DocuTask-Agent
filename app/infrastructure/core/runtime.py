"""Infrastructure Runtime Engine for Service Lifecycle and Self-Healing Automation."""

from datetime import datetime, timezone
import logging
import secrets
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

from .environment import EnvironmentManager, EnvironmentType
from .exceptions import InfrastructureError, InvalidStateTransitionError
from .lifecycle import RuntimeLifecycleStateMachine, RuntimeState
from .resources import ResourceManager

logger = logging.getLogger(__name__)


class ServiceInstance(BaseModel):
    """Runtime instance of a managed service."""

    instance_id: str
    service_name: str
    environment: str
    replicas: int = 1
    state: RuntimeState = RuntimeState.CREATED
    version: str = "1.0.0"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    error_message: Optional[str] = None
    recovery_attempts: int = 0
    metadata: Dict[str, Any] = Field(default_factory=dict)


class InfrastructureRuntime:
    """Central cloud-native runtime platform managing services and self-healing lifecycle."""

    def __init__(
        self,
        env_manager: Optional[EnvironmentManager] = None,
        resource_manager: Optional[ResourceManager] = None,
    ) -> None:
        self.env_manager = env_manager or EnvironmentManager()
        self.resource_manager = resource_manager or ResourceManager()
        self._instances: Dict[str, ServiceInstance] = {}

    def deploy(
        self,
        service: str,
        environment: str = "PRODUCTION",
        replicas: int = 1,
        version: str = "1.0.0",
        config: Optional[Dict[str, Any]] = None,
    ) -> ServiceInstance:
        """Deploy a new service instance with environment validation."""
        env_type = EnvironmentType(environment) if environment in EnvironmentType.__members__ else EnvironmentType.PRODUCTION
        allowed, reason = self.env_manager.validate_deployment_allowed(
            requested_replicas=replicas,
            requested_cpu=replicas * 1,
            requested_memory_gb=replicas * 2,
            env_type=env_type,
        )
        if not allowed:
            raise InfrastructureError(f"Deployment rejected: {reason}")

        inst_id = f"srv_{secrets.token_hex(8)}"
        inst = ServiceInstance(
            instance_id=inst_id,
            service_name=service,
            environment=environment,
            replicas=replicas,
            state=RuntimeState.CREATED,
            version=version,
            metadata=config or {},
        )

        # Transition through INITIALIZING -> STARTING -> RUNNING
        inst.state = RuntimeLifecycleStateMachine.transition(inst.state, RuntimeState.INITIALIZING)
        inst.state = RuntimeLifecycleStateMachine.transition(inst.state, RuntimeState.STARTING)
        inst.state = RuntimeLifecycleStateMachine.transition(inst.state, RuntimeState.RUNNING)
        inst.updated_at = datetime.now(timezone.utc)

        self._instances[inst_id] = inst
        logger.info("Deployed service %s (instance %s) in %s [RUNNING]", service, inst_id, environment)
        return inst

    def start_service(self, instance_id: str) -> ServiceInstance:
        inst = self._instances.get(instance_id)
        if not inst:
            raise InfrastructureError(f"Service instance {instance_id} not found.")

        if inst.state == RuntimeState.STOPPED:
            inst.state = RuntimeLifecycleStateMachine.transition(inst.state, RuntimeState.STARTING)
            inst.state = RuntimeLifecycleStateMachine.transition(inst.state, RuntimeState.RUNNING)
            inst.updated_at = datetime.now(timezone.utc)
        return inst

    def stop_service(self, instance_id: str) -> ServiceInstance:
        inst = self._instances.get(instance_id)
        if not inst:
            raise InfrastructureError(f"Service instance {instance_id} not found.")

        inst.state = RuntimeLifecycleStateMachine.transition(inst.state, RuntimeState.STOPPING)
        inst.state = RuntimeLifecycleStateMachine.transition(inst.state, RuntimeState.STOPPED)
        inst.updated_at = datetime.now(timezone.utc)
        return inst

    def restart_service(self, instance_id: str) -> ServiceInstance:
        self.stop_service(instance_id)
        return self.start_service(instance_id)

    def mark_failed(self, instance_id: str, error_msg: str) -> ServiceInstance:
        """Mark a service as failed, triggering self-healing recovery if eligible."""
        inst = self._instances.get(instance_id)
        if not inst:
            raise InfrastructureError(f"Service instance {instance_id} not found.")

        inst.state = RuntimeLifecycleStateMachine.transition(inst.state, RuntimeState.FAILED)
        inst.error_message = error_msg
        inst.updated_at = datetime.now(timezone.utc)

        # Automatic self-healing trigger
        return self.trigger_recovery(instance_id)

    def trigger_recovery(self, instance_id: str) -> ServiceInstance:
        """Execute automated self-healing recovery loop."""
        inst = self._instances.get(instance_id)
        if not inst:
            raise InfrastructureError(f"Service instance {instance_id} not found.")

        logger.warning("Initiating self-healing recovery for service %s", instance_id)
        inst.state = RuntimeLifecycleStateMachine.transition(inst.state, RuntimeState.RECOVERING)
        inst.recovery_attempts += 1

        # Simulate health recovery transition
        inst.state = RuntimeLifecycleStateMachine.transition(inst.state, RuntimeState.RUNNING)
        inst.error_message = None
        inst.updated_at = datetime.now(timezone.utc)
        logger.info("Service %s successfully recovered to RUNNING", instance_id)
        return inst

    def get_instance(self, instance_id: str) -> Optional[ServiceInstance]:
        return self._instances.get(instance_id)

    def list_instances(
        self,
        service_name: Optional[str] = None,
        environment: Optional[str] = None,
        state: Optional[RuntimeState] = None,
    ) -> List[ServiceInstance]:
        items = list(self._instances.values())
        if service_name:
            items = [i for i in items if i.service_name == service_name]
        if environment:
            items = [i for i in items if i.environment == environment]
        if state:
            items = [i for i in items if i.state == state]
        return items
