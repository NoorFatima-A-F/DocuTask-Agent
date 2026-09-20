"""
Phase 3I.4: Enterprise Distributed Tracing Infrastructure Verification — Interfaces
"""
from abc import ABC, abstractmethod
from typing import Dict, Any
from .models import (
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


class ITracingArchitectureVerifier(ABC):
    @abstractmethod
    def verify_tracing_architecture(self) -> TracingArchitectureReport:
        pass


class IContextPropagationVerifier(ABC):
    @abstractmethod
    def verify_context_propagation(self) -> ContextPropagationReport:
        pass


class IWorkflowTraceVerifier(ABC):
    @abstractmethod
    def verify_workflow_trace(self) -> WorkflowTraceReport:
        pass


class IAgentTraceVerifier(ABC):
    @abstractmethod
    def verify_agent_trace(self) -> AgentTraceReport:
        pass


class IDependencyTraceVerifier(ABC):
    @abstractmethod
    def verify_dependency_trace(self) -> DependencyTraceReport:
        pass


class IErrorTraceVerifier(ABC):
    @abstractmethod
    def verify_error_trace(self) -> ErrorTraceReport:
        pass


class ITraceCorrelationVerifier(ABC):
    @abstractmethod
    def verify_correlation(self) -> TraceCorrelationReport:
        pass


class ISamplingStrategyVerifier(ABC):
    @abstractmethod
    def verify_sampling_strategy(self) -> TraceSamplingReport:
        pass


class ITraceSecurityVerifier(ABC):
    @abstractmethod
    def verify_trace_security(self) -> TraceSecurityReport:
        pass


class ITracePerformanceVerifier(ABC):
    @abstractmethod
    def verify_trace_performance(self) -> TracePerformanceReport:
        pass


class IFailureSimulationTraceVerifier(ABC):
    @abstractmethod
    def verify_failure_simulation_traces(self) -> ChaosTraceReport:
        pass


class ITracingQualityScorer(ABC):
    @abstractmethod
    def calculate_certification_score(
        self,
        arch_report: TracingArchitectureReport,
        prop_report: ContextPropagationReport,
        wf_report: WorkflowTraceReport,
        agent_report: AgentTraceReport,
        dep_report: DependencyTraceReport,
        err_report: ErrorTraceReport,
        corr_report: TraceCorrelationReport,
        sample_report: TraceSamplingReport,
        sec_report: TraceSecurityReport,
        perf_report: TracePerformanceReport,
        chaos_report: ChaosTraceReport,
    ) -> TracingCertificationReport:
        pass


class ITracingEvidenceExporter(ABC):
    @abstractmethod
    def export_all_reports(
        self,
        output_dir: str,
        arch_report: TracingArchitectureReport,
        prop_report: ContextPropagationReport,
        wf_report: WorkflowTraceReport,
        agent_report: AgentTraceReport,
        dep_report: DependencyTraceReport,
        err_report: ErrorTraceReport,
        corr_report: TraceCorrelationReport,
        sample_report: TraceSamplingReport,
        sec_report: TraceSecurityReport,
        perf_report: TracePerformanceReport,
        chaos_report: ChaosTraceReport,
        certification_report: TracingCertificationReport,
    ) -> Dict[str, Any]:
        pass
