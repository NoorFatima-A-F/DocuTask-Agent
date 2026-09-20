"""
Abstract interfaces for Module Boundary & Plugin Architecture Verification.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple
from app.platform_verification.module_boundary.domain.models import (
    ModuleArchitectureEvidencePackage,
    ModuleBoundaryViolation,
    ModuleDependencyEdge,
    ModuleManifest,
    ModuleQualityMetrics,
    PluginContractReport,
)


class IModuleRegistry(ABC):
    """Manages explicit module manifests, boundaries, and dependencies."""

    @abstractmethod
    def register_module(self, manifest: ModuleManifest) -> None:
        """Registers a module manifest."""
        pass

    @abstractmethod
    def get_module(self, module_name: str) -> Optional[ModuleManifest]:
        """Retrieves manifest by name."""
        pass

    @abstractmethod
    def list_modules(self) -> List[ModuleManifest]:
        """Lists all registered modules."""
        pass


class IModuleBoundaryValidator(ABC):
    """Validates module-to-module dependencies against declared allowed/forbidden rules."""

    @abstractmethod
    def validate_dependencies(
        self,
        dependencies: List[ModuleDependencyEdge],
    ) -> List[ModuleBoundaryViolation]:
        """Validates edges against registered module boundaries."""
        pass


class IPluginVerifier(ABC):
    """Verifies plugin interface contracts, dynamic discovery, and failure isolation."""

    @abstractmethod
    def verify_plugin_contract(self, plugin_cls: Any, plugin_manifest: Optional[Dict[str, Any]] = None) -> PluginContractReport:
        """Verifies that a plugin class satisfies lifecycle and execution contracts."""
        pass

    @abstractmethod
    def test_failure_isolation(self, plugin_instance: Any, faulty_input: Any) -> Tuple[bool, str]:
        """Tests that a plugin crash does not crash the host runtime."""
        pass


class ICompatibilityValidator(ABC):
    """Validates semver compatibility between core platform and plugins."""

    @abstractmethod
    def check_compatibility(self, core_version: str, plugin_req_core_version: str) -> bool:
        """Verifies core version satisfies plugin requirement."""
        pass


class IModularityMetricsEngine(ABC):
    """Calculates coupling, cohesion, independence, and extensibility scores."""

    @abstractmethod
    def calculate_metrics(
        self,
        modules: List[ModuleManifest],
        dependencies: List[ModuleDependencyEdge],
    ) -> Dict[str, ModuleQualityMetrics]:
        """Calculates modularity indices per module."""
        pass


class IModuleEvidenceStore(ABC):
    """Persists and retrieves sealed module architecture evidence packages."""

    @abstractmethod
    def save_evidence(self, package: ModuleArchitectureEvidencePackage) -> str:
        """Saves evidence package."""
        pass

    @abstractmethod
    def get_evidence(self, scan_id: str) -> Optional[ModuleArchitectureEvidencePackage]:
        """Retrieves evidence package by scan ID."""
        pass
