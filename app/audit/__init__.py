"""DocuTask Enterprise Audit Platform & Compliance Evidence Management System (EAP-CEMS) - Phase 8G."""

from .core.events import (
    ActorType,
    AuditSeverity,
    OutcomeType,
    EventCategory,
    AuditEvent,
)
from .core.models import (
    AuditActor,
    AuditResource,
    PolicyContext,
    AIExecutionAuditContext,
    DataAuditEventContext,
)
from .core.context import AuditContext
from .collector.gateway import AuditCollectorGateway
from .collector.normalizer import EventNormalizer
from .integrity.hashing import HashChainCalculator
from .integrity.signatures import AuditSigner
from .integrity.verification import IntegrityVerificationResult, AuditIntegrityVerifier
from .storage.partitions import AuditPartitionManager
from .storage.immutable_store import ImmutableAuditStore
from .storage.repository import AuditRepository
from .evidence.artifacts import EvidenceType, EvidenceArtifact
from .evidence.attachments import EvidenceAttachment
from .evidence.manager import EvidenceBundle, EvidenceManager
from .compliance.frameworks import ComplianceFramework, FrameworkProfile, FRAMEWORK_PROFILES
from .compliance.controls import ControlStatus, ComplianceControl, DEFAULT_COMPLIANCE_CONTROLS
from .compliance.mappings import (
    ControlEvaluationResult,
    ComplianceAssessmentReport,
    ComplianceAssessmentEngine,
)
from .search.filters import AuditSearchFilter
from .search.indexing import AuditInvertedIndex
from .search.engine import (
    AuditSearchResult,
    ExecutionTimelineNode,
    ExecutionTimelineGraph,
    AuditSearchEngine,
)
from .retention.policies import RetentionAction, RetentionPolicy
from .retention.lifecycle import LegalHold, RetentionEvaluationResult, RetentionLifecycleManager
from .investigations.cases import (
    CaseLifecycleState,
    InvestigationCaseNote,
    InvestigationCase,
    InvestigationManager,
)
from .investigations.timeline import TimelineItem, InvestigationTimeline, InvestigationTimelineBuilder
from .exports.formats import AuditExporter
from .exports.reports import AuditReportGenerator
from .analytics.metrics import AuditMetricsSummary, AuditMetricsCollector
from .analytics.dashboards import AuditDashboardSummary, AuditDashboardService
from .sdk.client import AuditSDK, audited
from .api.routes import router as audit_router

__all__ = [
    # Core
    "ActorType",
    "AuditSeverity",
    "OutcomeType",
    "EventCategory",
    "AuditEvent",
    "AuditActor",
    "AuditResource",
    "PolicyContext",
    "AIExecutionAuditContext",
    "DataAuditEventContext",
    "AuditContext",
    # Collector
    "AuditCollectorGateway",
    "EventNormalizer",
    # Integrity
    "HashChainCalculator",
    "AuditSigner",
    "IntegrityVerificationResult",
    "AuditIntegrityVerifier",
    # Storage
    "AuditPartitionManager",
    "ImmutableAuditStore",
    "AuditRepository",
    # Evidence
    "EvidenceType",
    "EvidenceArtifact",
    "EvidenceAttachment",
    "EvidenceBundle",
    "EvidenceManager",
    # Compliance
    "ComplianceFramework",
    "FrameworkProfile",
    "FRAMEWORK_PROFILES",
    "ControlStatus",
    "ComplianceControl",
    "DEFAULT_COMPLIANCE_CONTROLS",
    "ControlEvaluationResult",
    "ComplianceAssessmentReport",
    "ComplianceAssessmentEngine",
    # Search
    "AuditSearchFilter",
    "AuditInvertedIndex",
    "AuditSearchResult",
    "ExecutionTimelineNode",
    "ExecutionTimelineGraph",
    "AuditSearchEngine",
    # Retention
    "RetentionAction",
    "RetentionPolicy",
    "LegalHold",
    "RetentionEvaluationResult",
    "RetentionLifecycleManager",
    # Investigations
    "CaseLifecycleState",
    "InvestigationCaseNote",
    "InvestigationCase",
    "InvestigationManager",
    "TimelineItem",
    "InvestigationTimeline",
    "InvestigationTimelineBuilder",
    # Exports & Analytics
    "AuditExporter",
    "AuditReportGenerator",
    "AuditMetricsSummary",
    "AuditMetricsCollector",
    "AuditDashboardSummary",
    "AuditDashboardService",
    # SDK & API
    "AuditSDK",
    "audited",
    "audit_router",
]
