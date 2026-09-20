"""
Explicit Module & Subsystem Registry.
"""
from __future__ import annotations
from typing import Dict, List, Optional
from app.platform_verification.module_boundary.domain.interfaces import IModuleRegistry
from app.platform_verification.module_boundary.domain.models import (
    ModuleManifest,
    ModuleType,
)


class EnterpriseModuleRegistry(IModuleRegistry):
    """Registers and holds explicit boundary manifests for all platform modules."""

    def __init__(self):
        self._modules: Dict[str, ModuleManifest] = {}
        self._initialize_platform_modules()

    def register_module(self, manifest: ModuleManifest) -> None:
        self._modules[manifest.module_name] = manifest

    def get_module(self, module_name: str) -> Optional[ModuleManifest]:
        return self._modules.get(module_name)

    def list_modules(self) -> List[ModuleManifest]:
        return list(self._modules.values())

    def _initialize_platform_modules(self) -> None:
        # 1. Core Module
        self.register_module(
            ModuleManifest(
                module_name="core",
                version="2.4.0",
                module_type=ModuleType.PLATFORM_CORE,
                owner="CorePlatformTeam",
                architecture_domain="Foundational",
                allowed_dependencies=[],
                forbidden_dependencies=["api", "agents", "plugins", "connectors"],
                exported_contracts=["BaseEntity", "DomainEvent", "IPlugin", "IAgent"],
                owned_responsibilities=["Entity abstractions", "Event contracts", "Shared interfaces"],
            )
        )

        # 2. Runtime Module
        self.register_module(
            ModuleManifest(
                module_name="runtime",
                version="2.4.0",
                module_type=ModuleType.RUNTIME_ENGINE,
                owner="RuntimeTeam",
                architecture_domain="Execution",
                allowed_dependencies=["core"],
                forbidden_dependencies=["plugins", "api", "database"],
                exported_contracts=["AgentRuntime", "TaskScheduler", "ContextManager"],
                owned_responsibilities=["Execution orchestration", "Worker lifecycle"],
            )
        )

        # 3. Agents Module
        self.register_module(
            ModuleManifest(
                module_name="agents",
                version="2.4.0",
                module_type=ModuleType.SUBSYSTEM_MODULE,
                owner="AgentSquad",
                architecture_domain="Cognitive",
                allowed_dependencies=["core", "runtime"],
                forbidden_dependencies=["api", "database"],
                exported_contracts=["BaseAgent", "Planner", "AgentRegistry"],
                owned_responsibilities=["Autonomous planning", "Agent coordination"],
            )
        )

        # 4. Knowledge / RAG Module
        self.register_module(
            ModuleManifest(
                module_name="knowledge",
                version="2.4.0",
                module_type=ModuleType.SUBSYSTEM_MODULE,
                owner="KnowledgeTeam",
                architecture_domain="RAG",
                allowed_dependencies=["core"],
                forbidden_dependencies=["api", "agents", "database"],
                exported_contracts=["KnowledgeRetriever", "VectorIndex"],
                owned_responsibilities=["Document chunking", "Embedding retrieval"],
            )
        )

        # 5. Plugins Module
        self.register_module(
            ModuleManifest(
                module_name="plugins",
                version="2.4.0",
                module_type=ModuleType.EXTENSION_PLUGIN,
                owner="EcosystemTeam",
                architecture_domain="Extensions",
                allowed_dependencies=["core"],
                forbidden_dependencies=["runtime", "api", "database", "agents"],
                exported_contracts=["PluginInterface", "ProviderAdapter"],
                owned_responsibilities=["External LLM & OCR provider integrations"],
            )
        )
