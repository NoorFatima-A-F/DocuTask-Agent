"""
Abstract interfaces for Clean Architecture & Dependency Validation.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple
from app.platform_verification.clean_architecture.domain.models import (
    ArchitectureExceptionWaiver,
    CleanArchDependencyEdge,
    CleanArchEvidencePackage,
    CleanArchViolation,
    LayerDependencyRule,
    ModuleQualityMetrics,
)


class ICleanArchitectureScanner(ABC):
    """Parses codebase AST to extract all import dependencies, relative paths, and dynamic calls."""

    @abstractmethod
    def scan_codebase(self, root_dir: str) -> List[CleanArchDependencyEdge]:
        """Scans codebase and extracts all dependency edges with layer mappings."""
        pass


class IDependencyRuleEngine(ABC):
    """Validates dependency edges against Clean Architecture inward rules and waivers."""

    @abstractmethod
    def register_layer_rule(self, rule: LayerDependencyRule) -> None:
        """Registers a layer rule."""
        pass

    @abstractmethod
    def evaluate_dependencies(
        self,
        edges: List[CleanArchDependencyEdge],
        waivers: Optional[List[ArchitectureExceptionWaiver]] = None,
    ) -> List[CleanArchViolation]:
        """Evaluates edges and returns violations."""
        pass


class IDomainIsolationVerifier(ABC):
    """Verifies that the Domain layer is completely decoupled from frameworks and DBs."""

    @abstractmethod
    def verify_domain_purity(self, domain_module_path: str) -> Tuple[bool, List[str]]:
        """Verifies domain purity, returning (is_pure, violation_details)."""
        pass


class IDependencyMetricsCalculator(ABC):
    """Calculates Afferent/Efferent coupling, Instability (I), Abstractness (A), and Distance (D)."""

    @abstractmethod
    def calculate_module_metrics(
        self,
        edges: List[CleanArchDependencyEdge],
        module_class_counts: Optional[Dict[str, Tuple[int, int]]] = None,
    ) -> Dict[str, ModuleQualityMetrics]:
        """Calculates metrics for all scanned modules."""
        pass


class ICleanArchEvidenceStore(ABC):
    """Persists and retrieves clean architecture verification evidence."""

    @abstractmethod
    def save_evidence(self, package: CleanArchEvidencePackage) -> str:
        """Saves evidence package."""
        pass

    @abstractmethod
    def get_evidence(self, scan_id: str) -> Optional[CleanArchEvidencePackage]:
        """Retrieves evidence package by ID."""
        pass
