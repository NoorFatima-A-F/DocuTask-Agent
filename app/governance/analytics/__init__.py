"""Enterprise AI Governance Analytics, Dashboards & Reporting Platform (Phase 8I).

Transforms cross-platform governance telemetry into operational, compliance, risk, and business intelligence.
"""

from .events.normalizers import AnalyticsEventType, GovernanceAnalyticsEvent, EventNormalizer
from .events.processors import EventProcessor
from .events.consumer import GovernanceEventConsumer

from .warehouse.models import (
    DimTenant,
    DimUser,
    DimAgent,
    DimModel,
    DimPolicy,
    DimWorkflow,
    DimTime,
    FactGovernanceDecision,
    FactPolicyEvent,
    FactAIExecution,
    FactRiskEvent,
    FactComplianceEvent,
    FactApproval,
)
from .warehouse.schemas import WarehouseQueryFilter, TimeBucketSummary
from .warehouse.repositories import GovernanceDataWarehouseRepository

from .core.metrics import (
    MetricPeriod,
    MetricTrend,
    MetricValue,
    DecisionMetricsSummary,
    PolicyMetricsSummary,
    AgentMetricsSummary,
    ModelMetricsSummary,
    PromptMetricsSummary,
)
from .core.calculators import (
    DecisionMetricsCalculator,
    PolicyMetricsCalculator,
    AgentMetricsCalculator,
    ModelMetricsCalculator,
    PromptMetricsCalculator,
)
from .core.aggregators import TimeSeriesAggregator
from .core.engine import GovernanceMetricsEngine

from .risk.scoring import RiskCategory, RiskScoringModel, RiskScoreBreakdown
from .risk.analyzer import RiskAnalyzer, RiskAnalysisSummary
from .risk.trends import RiskTrendAnalyzer, RiskTrendSignal

from .compliance.evaluator import (
    ComplianceFramework,
    ControlStatus,
    FrameworkComplianceScore,
    ComplianceEvaluator,
)
from .compliance.reports import ComplianceGap, AuditReadinessReport, ComplianceReportingEngine

from .policies.analytics import PolicyAnalyticsEngine, PolicyIntelligenceReport, PolicyUsageStat
from .policies.effectiveness import PolicyEffectivenessEngine, PolicyEffectivenessSummary, PolicyRecommendation

from .ai_systems.agents import AgentPerformanceRecord, AgentSystemAnalytics, AgentAnalyticsEngine
from .ai_systems.models import ModelUsageRecord, ModelSystemAnalytics, ModelAnalyticsEngine
from .ai_systems.workflows import WorkflowAnalyticsRecord, WorkflowSystemAnalytics, WorkflowAnalyticsEngine

from .reporting.templates import (
    ReportType,
    ReportFormat,
    GovernanceReportSection,
    GovernanceReport,
)
from .reporting.generator import ReportGenerator
from .reporting.exporters import ReportExporter

from .dashboards.schemas import (
    ExecutiveDashboardDTO,
    AdministratorDashboardDTO,
    DeveloperDashboardDTO,
)
from .dashboards.services import DashboardService

from .alerts.rules import AlertSeverity, AlertCondition, AlertRule
from .alerts.detector import AlertEvent, AlertDetector

from .sdk.client import GovernanceAnalyticsSDK
from .api.routes import router as governance_analytics_router

__all__ = [
    # Events
    "AnalyticsEventType",
    "GovernanceAnalyticsEvent",
    "EventNormalizer",
    "EventProcessor",
    "GovernanceEventConsumer",
    # Warehouse
    "DimTenant",
    "DimUser",
    "DimAgent",
    "DimModel",
    "DimPolicy",
    "DimWorkflow",
    "DimTime",
    "FactGovernanceDecision",
    "FactPolicyEvent",
    "FactAIExecution",
    "FactRiskEvent",
    "FactComplianceEvent",
    "FactApproval",
    "WarehouseQueryFilter",
    "TimeBucketSummary",
    "GovernanceDataWarehouseRepository",
    # Core Metrics
    "MetricPeriod",
    "MetricTrend",
    "MetricValue",
    "DecisionMetricsSummary",
    "PolicyMetricsSummary",
    "AgentMetricsSummary",
    "ModelMetricsSummary",
    "PromptMetricsSummary",
    "DecisionMetricsCalculator",
    "PolicyMetricsCalculator",
    "AgentMetricsCalculator",
    "ModelMetricsCalculator",
    "PromptMetricsCalculator",
    "TimeSeriesAggregator",
    "GovernanceMetricsEngine",
    # Risk
    "RiskCategory",
    "RiskScoringModel",
    "RiskScoreBreakdown",
    "RiskAnalyzer",
    "RiskAnalysisSummary",
    "RiskTrendAnalyzer",
    "RiskTrendSignal",
    # Compliance
    "ComplianceFramework",
    "ControlStatus",
    "FrameworkComplianceScore",
    "ComplianceEvaluator",
    "ComplianceGap",
    "AuditReadinessReport",
    "ComplianceReportingEngine",
    # Policies
    "PolicyAnalyticsEngine",
    "PolicyIntelligenceReport",
    "PolicyUsageStat",
    "PolicyEffectivenessEngine",
    "PolicyEffectivenessSummary",
    "PolicyRecommendation",
    # AI Systems
    "AgentPerformanceRecord",
    "AgentSystemAnalytics",
    "AgentAnalyticsEngine",
    "ModelUsageRecord",
    "ModelSystemAnalytics",
    "ModelAnalyticsEngine",
    "WorkflowAnalyticsRecord",
    "WorkflowSystemAnalytics",
    "WorkflowAnalyticsEngine",
    # Reporting
    "ReportType",
    "ReportFormat",
    "GovernanceReportSection",
    "GovernanceReport",
    "ReportGenerator",
    "ReportExporter",
    # Dashboards
    "ExecutiveDashboardDTO",
    "AdministratorDashboardDTO",
    "DeveloperDashboardDTO",
    "DashboardService",
    # Alerts
    "AlertSeverity",
    "AlertCondition",
    "AlertRule",
    "AlertEvent",
    "AlertDetector",
    # SDK
    "GovernanceAnalyticsSDK",
    # API
    "governance_analytics_router",
]
