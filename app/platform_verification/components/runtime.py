"""
Enterprise Verification Runtime: Dependency Injection Container and Facade.
Coordinates all 16 specialized core components with clean separation of concerns.
"""
from typing import Dict, Any, Optional

from .orchestrator.orchestrator import VerificationOrchestrator
from .registry.registry import VerificationRegistry
from .definitions.definition_manager import VerificationDefinitionManager
from .execution.execution_engine import VerificationExecutionEngine
from .datasets.dataset_manager import DatasetManager
from .environments.environment_manager import EnvironmentManager
from .configuration.configuration_manager import ConfigurationManager
from .evidence.evidence_manager import EvidenceManager
from .metrics.metrics_engine import MetricsEngine
from .statistics.statistical_analysis_engine import StatisticalAnalysisEngine
from .gates.quality_gate_engine import QualityGateEngine
from .certification.certification_engine import CertificationEngine
from .reporting.reporting_engine import ReportingEngine
from .audit.audit_manager import AuditManager
from .traceability.traceability_manager import TraceabilityManager
from .plugins.plugin_manager import PluginManager

class EnterpriseVerificationRuntime:
    """Master runtime assembling and exposing all 16 core components."""

    def __init__(self):
        self.registry = VerificationRegistry()
        self.definition_manager = VerificationDefinitionManager()
        self.execution_engine = VerificationExecutionEngine()
        self.dataset_manager = DatasetManager()
        self.environment_manager = EnvironmentManager()
        self.configuration_manager = ConfigurationManager()
        self.evidence_manager = EvidenceManager()
        self.metrics_engine = MetricsEngine()
        self.statistical_analysis_engine = StatisticalAnalysisEngine()
        self.quality_gate_engine = QualityGateEngine()
        self.certification_engine = CertificationEngine()
        self.reporting_engine = ReportingEngine()
        self.audit_manager = AuditManager()
        self.traceability_manager = TraceabilityManager()
        self.plugin_manager = PluginManager()
        self.orchestrator = VerificationOrchestrator(
            registry=self.registry,
            definition_manager=self.definition_manager,
            execution_engine=self.execution_engine,
            dataset_manager=self.dataset_manager,
            environment_manager=self.environment_manager,
            configuration_manager=self.configuration_manager,
            evidence_manager=self.evidence_manager,
            metrics_engine=self.metrics_engine,
            statistical_analysis_engine=self.statistical_analysis_engine,
            quality_gate_engine=self.quality_gate_engine,
            certification_engine=self.certification_engine,
            reporting_engine=self.reporting_engine,
            audit_manager=self.audit_manager,
            traceability_manager=self.traceability_manager,
            plugin_manager=self.plugin_manager,
        )

_runtime_instance: Optional[EnterpriseVerificationRuntime] = None

def get_verification_runtime() -> EnterpriseVerificationRuntime:
    global _runtime_instance
    if _runtime_instance is None:
        _runtime_instance = EnterpriseVerificationRuntime()
    return _runtime_instance
