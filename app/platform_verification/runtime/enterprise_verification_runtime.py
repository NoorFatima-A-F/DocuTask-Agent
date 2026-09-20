"""
Enterprise Verification Runtime: Master Dependency Injection Container and Facade.
Assembles and coordinates the 15 specialized core components.
"""
from typing import Dict, List, Any, Optional
from ..components.registry.registry import VerificationRegistry
from ..components.definitions.definition_manager import VerificationDefinitionManager
from ..components.execution.execution_engine import VerificationExecutionEngine
from ..components.datasets.dataset_manager import DatasetManager
from ..components.environments.environment_manager import EnvironmentManager
from ..components.configuration.configuration_manager import ConfigurationManager
from ..components.evidence.evidence_manager import EvidenceManager
from ..components.metrics.metrics_engine import MetricsEngine
from ..components.statistics.statistical_analysis_engine import StatisticalAnalysisEngine
from ..components.gates.quality_gate_engine import QualityGateEngine
from ..components.reporting.reporting_engine import ReportingEngine
from ..components.audit.audit_manager import AuditManager
from ..components.traceability.traceability_manager import TraceabilityManager
from ..components.plugins.plugin_manager import PluginManager
from ..components.orchestrator.orchestrator import VerificationOrchestrator
from ..domain.models import (
    VerificationDefinition,
    VerificationRun,
    DatasetRecord,
    EnvironmentReadiness,
    ConfigurationSnapshot,
    EvidenceItem,
    MetricValue,
    StatisticalSummary,
    QualityGateEvaluation,
    ComplianceCertificate,
    VerificationReport,
    AuditEntry,
    TraceabilityNode,
    PluginDescriptor,
    ComponentHealth,
)

class EnterpriseVerificationRuntime:
    _instance: Optional["EnterpriseVerificationRuntime"] = None

    def __init__(self):
        # 1. Registry
        self.registry = VerificationRegistry()
        # 2. Definition Manager
        self.definition_mgr = VerificationDefinitionManager()
        # 3. Execution Engine
        self.execution_engine = VerificationExecutionEngine()
        # 4. Dataset Manager
        self.dataset_mgr = DatasetManager()
        # 5. Environment Manager
        self.env_mgr = EnvironmentManager()
        # 6. Configuration Manager
        self.config_mgr = ConfigurationManager()
        # 7. Evidence Manager
        self.evidence_mgr = EvidenceManager()
        # 8. Metrics Engine
        self.metrics_engine = MetricsEngine()
        # 9. Statistical Analysis Engine
        self.stats_engine = StatisticalAnalysisEngine()
        # 10. Quality Gate Engine
        self.gate_engine = QualityGateEngine()
        # 11. Reporting Engine
        self.reporting_engine = ReportingEngine()
        # 12. Audit Manager
        self.audit_mgr = AuditManager()
        # 13. Traceability Manager
        self.traceability_mgr = TraceabilityManager()
        # 14. Plugin Manager
        self.plugin_mgr = PluginManager()
        # 15. Orchestrator (Wires all 14 components)
        self.orchestrator = VerificationOrchestrator(
            registry=self.registry,
            definition_mgr=self.definition_mgr,
            execution_engine=self.execution_engine,
            dataset_mgr=self.dataset_mgr,
            env_mgr=self.env_mgr,
            config_mgr=self.config_mgr,
            evidence_mgr=self.evidence_mgr,
            metrics_engine=self.metrics_engine,
            stats_engine=self.stats_engine,
            gate_engine=self.gate_engine,
            reporting_engine=self.reporting_engine,
            audit_mgr=self.audit_mgr,
            traceability_mgr=self.traceability_mgr,
            plugin_mgr=self.plugin_mgr,
        )

    @classmethod
    def get_instance(cls) -> "EnterpriseVerificationRuntime":
        if cls._instance is None:
            cls._instance = EnterpriseVerificationRuntime()
        return cls._instance

    def get_components_health(self) -> List[ComponentHealth]:
        return [
            self.orchestrator.observability.get_health(),
            self.registry.observability.get_health(),
            self.definition_mgr.observability.get_health(),
            self.execution_engine.observability.get_health(),
            self.dataset_mgr.observability.get_health(),
            self.env_mgr.observability.get_health(),
            self.config_mgr.observability.get_health(),
            self.evidence_mgr.observability.get_health(),
            self.metrics_engine.observability.get_health(),
            self.stats_engine.observability.get_health(),
            self.gate_engine.observability.get_health(),
            self.reporting_engine.observability.get_health(),
            self.audit_mgr.observability.get_health(),
            self.traceability_mgr.observability.get_health(),
            self.plugin_mgr.observability.get_health(),
        ]

    def get_overview(self) -> Dict[str, Any]:
        return {
            "platform_name": "DocuTask Enterprise Verification Platform",
            "version": "2.0.0",
            "total_core_components": 15,
            "components_healthy": len(self.get_components_health()),
            "active_definitions": len(self.definition_mgr.list_definitions()),
            "registered_plugins": len(self.registry.list_plugins()),
            "datasets_count": len(self.dataset_mgr.list_datasets()),
            "environments_count": len(self.env_mgr.list_environments()),
            "completed_runs": len(self.orchestrator.list_runs()),
            "audit_ledger_size": len(self.audit_mgr.get_audit_trail()),
            "chain_tamper_verified": self.audit_mgr.verify_chain_integrity()
        }
