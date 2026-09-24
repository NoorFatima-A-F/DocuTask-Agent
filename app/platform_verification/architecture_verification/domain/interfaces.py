"""
Abstract interfaces for Enterprise Architecture Verification Framework.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple
from app.platform_verification.architecture_verification.domain.models import (
    ArchitectureDependency,
    ArchitectureEvidencePackage,
    ArchitectureRegressionReport,
    ArchitectureRule,
    ArchitectureScoreReport,
    ArchitectureViolation,
    CircularDependencyCycle,
)


class IASTScanner(ABC):
    """Parses Python source files using AST to extract imports, class/function metrics, and dependencies."""

    @abstractmethod
    def scan_directory(self, root_dir: str) -> Tuple[List[ArchitectureDependency], Dict[str, Any], int, int]:
        """Scans directory and returns (dependencies, file_metrics, total_files, total_lines)."""
        pass


class IDependencyGraphEngine(ABC):
    """Constructs directed dependency graph and detects cycles."""

    @abstractmethod
    def build_graph(self, dependencies: List[ArchitectureDependency]) -> Dict[str, List[str]]:
        """Constructs adjacency list graph."""
        pass

    @abstractmethod
    def detect_circular_dependencies(self, graph: Dict[str, List[str]]) -> List[CircularDependencyCycle]:
        """Finds all cycles in dependency graph."""
        pass


class IArchitectureRuleEngine(ABC):
    """Evaluates configurable architecture rules against extracted dependencies and metrics."""

    @abstractmethod
    def register_rule(self, rule: ArchitectureRule) -> None:
        """Registers a rule."""
        pass

    @abstractmethod
    def evaluate_rules(
        self,
        dependencies: List[ArchitectureDependency],
        file_metrics: Dict[str, Any],
        circular_cycles: List[CircularDependencyCycle],
    ) -> List[ArchitectureViolation]:
        """Evaluates all registered rules and returns list of violations."""
        pass


class IArchitectureScoringEngine(ABC):
    """Computes weighted multi-dimension architectural readiness score."""

    @abstractmethod
    def calculate_score(
        self,
        violations: List[ArchitectureViolation],
        circular_cycles: List[CircularDependencyCycle],
        total_files: int,
    ) -> ArchitectureScoreReport:
        """Calculates dimensional and aggregate architecture score."""
        pass


class IArchitectureRegressionEngine(ABC):
    """Compares current architecture scan against a baseline scan."""

    @abstractmethod
    def detect_regression(
        self,
        baseline_evidence: ArchitectureEvidencePackage,
        current_evidence: ArchitectureEvidencePackage,
    ) -> ArchitectureRegressionReport:
        """Determines if current scan regressed from baseline."""
        pass


class IArchitectureEvidenceStore(ABC):
    """Persists and retrieves immutable architecture evidence packages."""

    @abstractmethod
    def save_evidence(self, package: ArchitectureEvidencePackage) -> str:
        """Saves package and returns package ID."""
        pass

    @abstractmethod
    def get_evidence(self, scan_id: str) -> Optional[ArchitectureEvidencePackage]:
        """Retrieves package by scan ID."""
        pass
