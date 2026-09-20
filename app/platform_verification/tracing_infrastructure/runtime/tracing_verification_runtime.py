"""
Phase 3I.4: Runtime Orchestrator for Enterprise Distributed Tracing Verification
"""
from typing import Dict, Any
from ..domain.models import (
    TracingArchitectureReport,
    ContextPropagationReport,
    WorkflowTraceReport,
    AgentTraceReport,
    DependencyTraceReport,
    ErrorTraceReport,
    TraceCorrelationReport,
    TraceSamplingReport,
    TraceSecurityReport,
    TracePerformanceReport,
    ChaosTraceReport,
    TracingCertificationReport,
)
from ..verifiers.tracing_architecture_verifier import TracingArchitectureVerifier
from ..verifiers.context_propagation_verifier import ContextPropagationVerifier
from ..verifiers.api_workflow_trace_verifier import WorkflowTraceVerifier
from ..verifiers.ai_agent_trace_verifier import AgentTraceVerifier
from ..verifiers.external_dependency_trace_verifier import ExternalDependencyTraceVerifier
from ..verifiers.error_diagnostic_trace_verifier import ErrorDiagnosticTraceVerifier
from ..verifiers.trace_log_metric_correlation_verifier import TraceCorrelationVerifier
from ..verifiers.sampling_strategy_verifier import SamplingStrategyVerifier
from ..verifiers.trace_security_verifier import TraceSecurityVerifier
from ..verifiers.trace_performance_verifier import TracePerformanceVerifier
from ..verifiers.failure_simulation_trace_verifier import FailureSimulationTraceVerifier
from ..scoring.tracing_quality_scorer import TracingQualityScorer
from ..exporter.tracing_evidence_exporter import TracingEvidenceExporter


class TracingVerificationRuntime:
    """
    Orchestrates all Phase 3I.4 distributed tracing verification engines, executes 6-pillar quality scoring, and exports signed evidence manifests.
    """

    def __init__(self):
        self.arch_verifier = TracingArchitectureVerifier()
        self.prop_verifier = ContextPropagationVerifier()
        self.wf_verifier = WorkflowTraceVerifier()
        self.agent_verifier = AgentTraceVerifier()
        self.dep_verifier = ExternalDependencyTraceVerifier()
        self.err_verifier = ErrorDiagnosticTraceVerifier()
        self.corr_verifier = TraceCorrelationVerifier()
        self.sample_verifier = SamplingStrategyVerifier()
        self.sec_verifier = TraceSecurityVerifier()
        self.perf_verifier = TracePerformanceVerifier()
        self.chaos_verifier = FailureSimulationTraceVerifier()
        self.scorer = TracingQualityScorer()
        self.exporter = TracingEvidenceExporter()

    def run_full_verification(self, export_dir: str = "observability_verification/tracing") -> Dict[str, Any]:
        arch_report: TracingArchitectureReport = self.arch_verifier.verify_tracing_architecture()
        prop_report: ContextPropagationReport = self.prop_verifier.verify_context_propagation()
        wf_report: WorkflowTraceReport = self.wf_verifier.verify_workflow_trace()
        agent_report: AgentTraceReport = self.agent_verifier.verify_agent_trace()
        dep_report: DependencyTraceReport = self.dep_verifier.verify_dependency_trace()
        err_report: ErrorTraceReport = self.err_verifier.verify_error_trace()
        corr_report: TraceCorrelationReport = self.corr_verifier.verify_correlation()
        sample_report: TraceSamplingReport = self.sample_verifier.verify_sampling_strategy()
        sec_report: TraceSecurityReport = self.sec_verifier.verify_trace_security()
        perf_report: TracePerformanceReport = self.perf_verifier.verify_trace_performance()
        chaos_report: ChaosTraceReport = self.chaos_verifier.verify_failure_simulation_traces()

        certification_report: TracingCertificationReport = self.scorer.calculate_certification_score(
            arch_report=arch_report,
            prop_report=prop_report,
            wf_report=wf_report,
            agent_report=agent_report,
            dep_report=dep_report,
            err_report=err_report,
            corr_report=corr_report,
            sample_report=sample_report,
            sec_report=sec_report,
            perf_report=perf_report,
            chaos_report=chaos_report,
        )

        metadata = self.exporter.export_all_reports(
            output_dir=export_dir,
            arch_report=arch_report,
            prop_report=prop_report,
            wf_report=wf_report,
            agent_report=agent_report,
            dep_report=dep_report,
            err_report=err_report,
            corr_report=corr_report,
            sample_report=sample_report,
            sec_report=sec_report,
            perf_report=perf_report,
            chaos_report=chaos_report,
            certification_report=certification_report,
        )

        return {
            "arch_report": arch_report,
            "prop_report": prop_report,
            "wf_report": wf_report,
            "agent_report": agent_report,
            "dep_report": dep_report,
            "err_report": err_report,
            "corr_report": corr_report,
            "sample_report": sample_report,
            "sec_report": sec_report,
            "perf_report": perf_report,
            "chaos_report": chaos_report,
            "certification_report": certification_report,
            "metadata": metadata,
        }
