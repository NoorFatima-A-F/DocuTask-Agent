"""Enterprise Infrastructure Developer SDK Client."""

from typing import Any, Dict, Optional

from ..config.manager import ConfigurationManager
from ..core.environment import EnvironmentManager
from ..core.resources import (
    AllocatedResource,
    ResourceCategory,
    ResourceManager,
    ResourceSpecification,
)
from ..core.runtime import InfrastructureRuntime, ServiceInstance
from ..events.publisher import InfrastructureEventPublisher
from ..providers.base import SecretProvider
from ..providers.kubernetes.secrets import KubernetesSecretProvider
from ..services.discovery import ServiceDiscovery
from ..services.health import ServiceHealth, ServiceHealthMonitor
from ..services.registry import ServiceRegistry


class InfrastructureSDK:
    """Unified Developer SDK for cloud-native infrastructure lifecycle management."""

    def __init__(
        self,
        runtime: Optional[InfrastructureRuntime] = None,
        resource_mgr: Optional[ResourceManager] = None,
        env_mgr: Optional[EnvironmentManager] = None,
        config_mgr: Optional[ConfigurationManager] = None,
        service_registry: Optional[ServiceRegistry] = None,
        health_monitor: Optional[ServiceHealthMonitor] = None,
        discovery: Optional[ServiceDiscovery] = None,
        event_publisher: Optional[InfrastructureEventPublisher] = None,
        secret_provider: Optional[SecretProvider] = None,
    ) -> None:
        self.env_mgr = env_mgr or EnvironmentManager()
        self.resource_mgr = resource_mgr or ResourceManager()
        self.runtime = runtime or InfrastructureRuntime(self.env_mgr, self.resource_mgr)
        self.config_mgr = config_mgr or ConfigurationManager()
        self.service_registry = service_registry or ServiceRegistry()
        self.health_monitor = health_monitor or ServiceHealthMonitor()
        self.discovery = discovery or ServiceDiscovery(self.service_registry)
        self.event_publisher = event_publisher or InfrastructureEventPublisher()
        self.secret_provider = secret_provider or KubernetesSecretProvider()

    def deploy_service(
        self,
        name: str,
        replicas: int = 1,
        environment: str = "PRODUCTION",
        version: str = "1.0.0",
        config: Optional[Dict[str, Any]] = None,
        actor: str = "platform_engineer",
    ) -> ServiceInstance:
        """Deploy or upgrade a service across the platform."""
        self.event_publisher.publish(
            event_type="DeploymentStarted",
            service_name=name,
            environment=environment,
            payload={"replicas": replicas, "version": version},
        )

        inst = self.runtime.deploy(
            service=name,
            environment=environment,
            replicas=replicas,
            version=version,
            config=config,
        )

        # Register service metadata
        self.service_registry.register_service(
            name=name,
            version=version,
            environment=environment,
        )

        # Record audit event
        self.event_publisher.record_audit(
            actor=actor,
            action="deploy_service",
            resource=inst.instance_id,
            environment=environment,
            result="SUCCESS",
        )

        self.event_publisher.publish(
            event_type="DeploymentCompleted",
            service_name=name,
            environment=environment,
            payload={"instance_id": inst.instance_id},
        )
        return inst

    def provision_resource(
        self,
        name: str,
        category: ResourceCategory,
        resource_type: str,
        cpu_cores: float = 1.0,
        memory_mb: int = 1024,
        storage_gb: int = 10,
        environment: str = "PRODUCTION",
        actor: str = "platform_engineer",
    ) -> AllocatedResource:
        """Provision a compute, storage, or network infrastructure resource."""
        spec = ResourceSpecification(
            name=name,
            category=category,
            resource_type=resource_type,
            cpu_cores=cpu_cores,
            memory_mb=memory_mb,
            storage_gb=storage_gb,
            environment=environment,
        )
        req = self.resource_mgr.request_resource(spec)
        allocated = self.resource_mgr.allocate_resource(req.resource_id)

        self.event_publisher.publish(
            event_type="ResourceAllocated",
            resource_id=allocated.resource_id,
            environment=environment,
            payload={"name": name, "category": category.value},
        )

        self.event_publisher.record_audit(
            actor=actor,
            action="provision_resource",
            resource=allocated.resource_id,
            environment=environment,
            result="SUCCESS",
        )
        return allocated

    def check_health(self, service_id: str) -> ServiceHealth:
        """Check operational diagnostics for a service."""
        return self.health_monitor.get_health(service_id)

    def get_runtime_status(self, instance_id: str) -> Optional[ServiceInstance]:
        """Query runtime lifecycle status for a service instance."""
        return self.runtime.get_instance(instance_id)

    def restart_service(self, instance_id: str, actor: str = "platform_engineer") -> ServiceInstance:
        """Gracefully restart a running service."""
        inst = self.runtime.restart_service(instance_id)
        self.event_publisher.record_audit(
            actor=actor,
            action="restart_service",
            resource=instance_id,
            environment=inst.environment,
            result="SUCCESS",
        )
        return inst

    def get_secret(self, secret_name: str) -> Optional[str]:
        """Fetch credentials safely via provider abstraction."""
        return self.secret_provider.get_secret(secret_name)
