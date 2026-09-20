"""
Abstract interfaces for SOLID Principle Automated Verification.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple
from app.platform_verification.solid_verification.domain.models import (
    ClassDesignMetrics,
    InterfaceDesignMetrics,
    SolidEvidencePackage,
    SolidQualityScorecard,
    SolidViolation,
)


class ISolidASTAnalyzer(ABC):
    """Parses codebase AST to extract class definitions, methods, attributes, instantiations, and inheritance."""

    @abstractmethod
    def analyze_classes(self, root_dir: str) -> Tuple[Dict[str, ClassDesignMetrics], Dict[str, InterfaceDesignMetrics]]:
        """Extracts class and interface metrics across codebase."""
        pass


class ISolidRuleEvaluator(ABC):
    """Evaluates SRP, OCP, LSP, ISP, and DIP rules on extracted design metrics."""

    @abstractmethod
    def evaluate_srp(self, class_metrics: Dict[str, ClassDesignMetrics]) -> List[SolidViolation]:
        """Evaluates Single Responsibility Principle."""
        pass

    @abstractmethod
    def evaluate_ocp(self, class_metrics: Dict[str, ClassDesignMetrics]) -> List[SolidViolation]:
        """Evaluates Open/Closed Principle."""
        pass

    @abstractmethod
    def evaluate_lsp(self, class_metrics: Dict[str, ClassDesignMetrics]) -> List[SolidViolation]:
        """Evaluates Liskov Substitution Principle."""
        pass

    @abstractmethod
    def evaluate_isp(self, interface_metrics: Dict[str, InterfaceDesignMetrics]) -> List[SolidViolation]:
        """Evaluates Interface Segregation Principle."""
        pass

    @abstractmethod
    def evaluate_dip(self, class_metrics: Dict[str, ClassDesignMetrics]) -> List[SolidViolation]:
        """Evaluates Dependency Inversion Principle."""
        pass


class ISolidScoringEngine(ABC):
    """Computes weighted multi-principle design quality score."""

    @abstractmethod
    def calculate_scorecard(
        self,
        violations: List[SolidViolation],
        total_classes: int,
    ) -> SolidQualityScorecard:
        """Calculates dimensional and total score."""
        pass


class ISolidEvidenceStore(ABC):
    """Stores and retrieves immutable SOLID evidence packages."""

    @abstractmethod
    def save_evidence(self, package: SolidEvidencePackage) -> str:
        """Saves package."""
        pass

    @abstractmethod
    def get_evidence(self, scan_id: str) -> Optional[SolidEvidencePackage]:
        """Retrieves package by scan ID."""
        pass
