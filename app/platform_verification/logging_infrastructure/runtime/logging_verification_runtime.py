"""
Phase 3I.2: Runtime Orchestrator for Enterprise Logging Infrastructure Verification
"""
from typing import Dict, Any
from ..domain.models import (
    ArchitectureReport,
    StructuredLoggingReport,
    CorrelationReport,
    AgentLoggingReport,
    SecurityReport,
    PerformanceReport,
    FailureTestReport,
    CertificationReport,
)
from ..verifiers.logging_architecture_verifier import LoggingArchitectureVerifier
from ..verifiers.structured_logging_verifier import StructuredLoggingVerifier
from ..verifiers.correlation_verifier import CorrelationVerifier
from ..verifiers.agent_execution_logging_verifier import AgentExecutionLoggingVerifier
from ..verifiers.logging_security_verifier import LoggingSecurityVerifier
from ..verifiers.logging_performance_verifier import LoggingPerformanceVerifier
from ..verifiers.failure_simulation_logging_verifier import FailureSimulationLoggingVerifier
from ..scoring.logging_quality_scorer import LoggingQualityScorer
from ..exporter.logging_evidence_exporter import LoggingEvidenceExporter


class LoggingVerificationRuntime:
    """
    Executes all Phase 3I.2 logging verification checks, performs 6-pillar scoring, and exports signed evidence manifests.
    """

    def __init__(self):
        self.arch_verifier = LoggingArchitectureVerifier()
        self.struct_verifier = StructuredLoggingVerifier()
        self.corr_verifier = CorrelationVerifier()
        self.agent_verifier = AgentExecutionLoggingVerifier()
        self.sec_verifier = LoggingSecurityVerifier()
        self.perf_verifier = LoggingPerformanceVerifier()
        self.failure_verifier = FailureSimulationLoggingVerifier()
        self.scorer = LoggingQualityScorer()
        self.exporter = LoggingEvidenceExporter()

    def run_full_verification(self, export_dir: str = "observability_verification/logging") -> Dict[str, Any]:
        arch_report: ArchitectureReport = self.arch_verifier.verify_logging_architecture()
        struct_report: StructuredLoggingReport = self.struct_verifier.verify_structured_logging()
        corr_report: CorrelationReport = self.corr_verifier.verify_correlation()
        agent_report: AgentLoggingReport = self.agent_verifier.verify_agent_execution_logging()
        sec_report: SecurityReport = self.sec_verifier.verify_security()
        perf_report: PerformanceReport = self.perf_verifier.verify_performance()
        failure_report: FailureTestReport = self.failure_verifier.verify_failure_simulation_logging()

        certification_report: CertificationReport = self.scorer.calculate_certification_score(
            arch_report=arch_report,
            struct_report=struct_report,
            corr_report=corr_report,
            agent_report=agent_report,
            sec_report=sec_report,
            perf_report=perf_report,
            failure_report=failure_report,
        )

        metadata = self.exporter.export_all_reports(
            output_dir=export_dir,
            arch_report=arch_report,
            struct_report=struct_report,
            corr_report=corr_report,
            agent_report=agent_report,
            sec_report=sec_report,
            perf_report=perf_report,
            failure_report=failure_report,
            certification_report=certification_report,
        )

        return {
            "arch_report": arch_report,
            "struct_report": struct_report,
            "corr_report": corr_report,
            "agent_report": agent_report,
            "sec_report": sec_report,
            "perf_report": perf_report,
            "failure_report": failure_report,
            "certification_report": certification_report,
            "metadata": metadata,
        }
