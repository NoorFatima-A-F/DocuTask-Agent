"""
Module Loader & Auto-Discovery.
Implements IModuleLoader; discovers and initializes platform subsystem modules with dependency declarations.
"""

import logging
from typing import Any, Dict, List, Optional
from app.agents.runtime.interfaces import IModuleLoader
from app.agents.runtime.module_registry import ModuleDescriptor, ModuleRegistry

logger = logging.getLogger(__name__)


class ModuleLoader(IModuleLoader):
    """Discovers and instantiates platform subsystem modules."""

    def __init__(self, registry: Optional[ModuleRegistry] = None) -> None:
        self.registry = registry or ModuleRegistry()

    def discover_modules(self) -> List[ModuleDescriptor]:
        """Discovers canonical platform modules with dependency prerequisites."""
        canonical_modules = [
            ModuleDescriptor(
                name="ToolModule",
                version="12.0.0",
                dependencies=[],
                description="Enterprise Tool Registry & Schema Subsystem",
            ),
            ModuleDescriptor(
                name="MemoryModule",
                version="13.0.0",
                dependencies=[],
                description="Enterprise Memory Foundation Subsystem",
            ),
            ModuleDescriptor(
                name="DecisionModule",
                version="15.0.0",
                dependencies=["MemoryModule"],
                description="Enterprise Decision, Policy & Governance Engine",
            ),
            ModuleDescriptor(
                name="PlanningModule",
                version="17.0.0",
                dependencies=["MemoryModule", "DecisionModule", "ToolModule"],
                description="Intelligent Planner & Hierarchical Task Decomposition",
            ),
            ModuleDescriptor(
                name="ExecutionModule",
                version="18.0.0",
                dependencies=["ToolModule", "MemoryModule"],
                description="Stateful Execution Engine & Runtime Scheduler",
            ),
            ModuleDescriptor(
                name="RecoveryModule",
                version="19.0.0",
                dependencies=["ExecutionModule"],
                description="Autonomous Recovery & Self-Healing Engine",
            ),
            ModuleDescriptor(
                name="ReflectionModule",
                version="20.0.0",
                dependencies=["ExecutionModule", "MemoryModule"],
                description="Reflection, Self-Critique & Continuous Adaptation",
            ),
            ModuleDescriptor(
                name="CoordinationModule",
                version="21.0.0",
                dependencies=["ExecutionModule", "PlanningModule"],
                description="Multi-Agent Coordination & Swarm Collaboration",
            ),
            ModuleDescriptor(
                name="WorkflowModule",
                version="22.0.0",
                dependencies=["CoordinationModule", "PlanningModule", "ExecutionModule"],
                description="Workflow Runtime & Orchestration Engine",
            ),
        ]

        for mod in canonical_modules:
            self.registry.register_module(mod)

        return canonical_modules

    async def load_module(self, descriptor: ModuleDescriptor) -> Any:
        """Instantiates a discovered module."""
        logger.info(f"Loading module '{descriptor.name}' v{descriptor.version}")
        # Return generic runtime wrapper or concrete subsystem facade
        instance = {"module": descriptor.name, "version": descriptor.version, "status": "INITIALIZED"}
        self.registry.register_instance(descriptor.name, instance)
        return instance
