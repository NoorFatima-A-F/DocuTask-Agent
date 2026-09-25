"""
Abstract interfaces for Enterprise Reporting & Audit Intelligence System.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from app.platform_verification.reporting_audit.domain.models import (
    AiGovernanceDashboardView,
    AuditPackage,
    AuditReportRecord,
    ComplianceControlMapping,
    EngineeringDashboardView,
    ExecutiveDashboardView,
    NotificationAlert,
    NotificationEventType,
    QualityTrend,
    ReportFormat,
    ReportType,
    SecurityComplianceDashboardView,
    UserRole,
    VerificationSummary,
)


class IReportingDataPipeline(ABC):
    """Ingests raw evidence and metrics to populate normalized reporting models."""

    @abstractmethod
    def ingest_verification_run(self, summary: VerificationSummary) -> None:
        """Ingests a verified execution run."""
        pass

    @abstractmethod
    def get_quality_trends(self, metric_name: str, limit: int = 20) -> List[QualityTrend]:
        """Returns time-series quality trends for a given metric."""
        pass

    @abstractmethod
    def list_recent_summaries(self, limit: int = 10) -> List[VerificationSummary]:
        """Lists recent verification summaries."""
        pass


class IAuditReportGenerator(ABC):
    """Compiles auditable, cryptographically verified reports."""

    @abstractmethod
    def generate_report(
        self,
        report_type: ReportType,
        title: str,
        scope: str,
        data: Dict[str, Any],
        evidence_refs: List[str],
        generated_by: str,
        report_format: ReportFormat = ReportFormat.JSON,
    ) -> AuditReportRecord:
        """Compiles, hashes, and stores an audit report."""
        pass

    @abstractmethod
    def get_report(self, report_id: str) -> Optional[AuditReportRecord]:
        """Retrieves a report by ID."""
        pass


class IComplianceMappingEngine(ABC):
    """Maps verification evidence to regulatory and organizational standards."""

    @abstractmethod
    def register_control(self, control: ComplianceControlMapping) -> None:
        """Registers a compliance control."""
        pass

    @abstractmethod
    def evaluate_compliance(self, framework: Optional[str] = None) -> List[ComplianceControlMapping]:
        """Evaluates compliance state across frameworks."""
        pass


class INotificationService(ABC):
    """Dispatches notifications to role-based stakeholders."""

    @abstractmethod
    def send_alert(
        self,
        event_type: NotificationEventType,
        severity: str,
        title: str,
        message: str,
        roles: List[UserRole],
    ) -> NotificationAlert:
        """Emits an alert."""
        pass

    @abstractmethod
    def list_alerts(self, role: Optional[UserRole] = None) -> List[NotificationAlert]:
        """Retrieves active alerts for a user role."""
        pass


class IAuditExportManager(ABC):
    """Packages and exports full audit packages with cryptographic receipts."""

    @abstractmethod
    def export_audit_package(
        self,
        system_version: str,
        include_reports: List[str],
        evidence_manifest: List[str],
    ) -> AuditPackage:
        """Compiles comprehensive audit package."""
        pass


class IDashboardAggregationEngine(ABC):
    """Builds role-specific dashboard views."""

    @abstractmethod
    def build_executive_dashboard(self) -> ExecutiveDashboardView:
        """Constructs executive view."""
        pass

    @abstractmethod
    def build_engineering_dashboard(self) -> EngineeringDashboardView:
        """Constructs engineering view."""
        pass

    @abstractmethod
    def build_security_dashboard(self) -> SecurityComplianceDashboardView:
        """Constructs security & compliance view."""
        pass

    @abstractmethod
    def build_ai_governance_dashboard(self) -> AiGovernanceDashboardView:
        """Constructs AI governance view."""
        pass
