"""
Platform Bootstrapper.
Performs early hardware/environment checks, configuration parsing, and foundational container bootstrapping.
"""

import logging
from typing import Optional
from app.agents.runtime.configuration import PlatformRuntimeConfig
from app.agents.runtime.dependency_container import DependencyContainer
from app.agents.runtime.dependency_manager import DependencyManager
from app.agents.runtime.runtime_validation import RuntimeValidator
from app.agents.runtime.service_registry import ServiceRegistry

logger = logging.getLogger(__name__)


class PlatformBootstrapper:
    """Foundational bootstrapper executing early pre-flight checks."""

    def __init__(self, config: Optional[PlatformRuntimeConfig] = None) -> None:
        self.config = config or PlatformRuntimeConfig()

    def bootstrap(self) -> DependencyContainer:
        """Executes early pre-flight validation and wires base container."""
        logger.info(f"Bootstrapping Agent Platform Runtime in [{self.config.environment}] environment...")
        RuntimeValidator.validate_configuration(self.config)

        container = DependencyContainer()
        container.register_singleton(PlatformRuntimeConfig, self.config)
        container.register_singleton(ServiceRegistry, ServiceRegistry())
        container.register_singleton(DependencyManager, DependencyManager())

        return container
