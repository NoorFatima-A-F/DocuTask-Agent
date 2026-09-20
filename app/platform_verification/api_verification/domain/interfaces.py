"""
Abstract interfaces for Enterprise API Architecture Verification.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple
from app.platform_verification.api_verification.domain.models import (
    ApiBreakingChange,
    ApiEvidencePackage,
    ApiQualityScorecard,
    ApiSecurityFinding,
    EndpointPurityMetric,
)


class IApiASTAnalyzer(ABC):
    """Parses API endpoint files to verify layer purity and handler simplicity."""

    @abstractmethod
    def analyze_api_directory(self, root_api_dir: str) -> List[EndpointPurityMetric]:
        """Scans API endpoints for forbidden imports, line lengths, and direct DB/LLM calls."""
        pass


class IApiCompatibilityEngine(ABC):
    """Compares OpenAPI specifications across versions to detect breaking changes."""

    @abstractmethod
    def compare_schemas(
        self, old_schema: Dict[str, Any], new_schema: Dict[str, Any], version_before: str, version_after: str
    ) -> List[ApiBreakingChange]:
        """Detects removed fields, altered types, and breaking changes."""
        pass


class IApiSecurityValidator(ABC):
    """Evaluates endpoints against OWASP API Top 10 (BOLA, Auth, Rate Limits, Injection)."""

    @abstractmethod
    def evaluate_security(self, endpoints: List[EndpointPurityMetric]) -> List[ApiSecurityFinding]:
        """Validates API security boundaries."""
        pass


class IAsyncAgentWorkflowValidator(ABC):
    """Verifies that long-running AI/Agent tasks use non-blocking asynchronous patterns."""

    @abstractmethod
    def validate_task_transitions(self, current_state: str, next_state: str) -> Tuple[bool, str]:
        """Validates state machine transitions for AI tasks."""
        pass


class IApiScoringEngine(ABC):
    """Computes weighted multi-dimension API architecture readiness score."""

    @abstractmethod
    def calculate_scorecard(
        self,
        endpoints: List[EndpointPurityMetric],
        security_findings: List[ApiSecurityFinding],
        breaking_changes: List[ApiBreakingChange],
    ) -> ApiQualityScorecard:
        """Calculates dimensional and total score."""
        pass


class IApiEvidenceStore(ABC):
    """Stores and retrieves sealed API architecture evidence packages."""

    @abstractmethod
    def save_evidence(self, package: ApiEvidencePackage) -> str:
        """Saves package."""
        pass

    @abstractmethod
    def get_evidence(self, scan_id: str) -> Optional[ApiEvidencePackage]:
        """Retrieves package by scan ID."""
        pass
