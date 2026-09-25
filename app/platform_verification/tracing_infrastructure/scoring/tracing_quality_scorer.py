"""
Phase 3I.4: 6-Pillar Enterprise Distributed Tracing Quality Scorer
"""
from typing import List
from datetime import datetime, timezone
from ..domain.models import (
    TracingCertificationTier,
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
    TracingPillarScore,
    TracingCertificationReport,
)
from ..domain.interfaces import ITracingQualityScorer


class TracingQualityScorer(ITracingQualityScorer):
    """
    Evaluates 6 core distributed tracing categories:
      - Trace coverage: 20%
      - Context propagation: 20%
      - AI agent visibility: 20%
      - Error diagnosis: 15%
      - Correlation capability: 15%
      - Security: 10%
    """

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
        # 1. Trace Coverage (20%)
        cov_valid = (arch_report.services_instrumented >= 8) and wf_report.workflow_trace_passed and dep_report.external_tracing_passed
        cov_score = 100.0 if cov_valid else 0.0
        cov_weight = 20.0
        cov_weighted = (cov_score * cov_weight) / 100.0

        # 2. Context Propagation & Integrity (20%)
        prop_valid = prop_report.context_propagation_passed and (prop_report.context_integrity_pct >= 99.0) and prop_report.async_queue_propagation_valid
        prop_score = prop_report.context_integrity_pct if prop_valid else 0.0
        prop_weight = 20.0
        prop_weighted = (prop_score * prop_weight) / 100.0

        # 3. AI Agent Visibility (20%)
        ai_valid = (agent_report.ai_observability_score >= 95.0) and agent_report.decision_reconstruction_complete and len(agent_report.agent_spans) >= 6
        ai_score = agent_report.ai_observability_score if ai_valid else 0.0
        ai_weight = 20.0
        ai_weighted = (ai_score * ai_weight) / 100.0

        # 4. Error Diagnosis & Isolation (15%)
        err_valid = err_report.error_diagnosable and err_report.error_trace_passed and chaos_report.all_scenarios_verified
        err_score = 100.0 if err_valid else 0.0
        err_weight = 15.0
        err_weighted = (err_score * err_weight) / 100.0

        # 5. Correlation Capability (15%)
        corr_valid = corr_report.trace_to_log_linking_verified and corr_report.metric_to_trace_jump_verified and sample_report.sampling_passed
        corr_score = corr_report.correlation_score_pct if corr_valid else 0.0
        corr_weight = 15.0
        corr_weighted = (corr_score * corr_weight) / 100.0

        # 6. Security Protection & Overhead (10%)
        sec_valid = sec_report.forbidden_attributes_prevented and sec_report.no_pii_in_spans and perf_report.latency_impact_acceptable
        sec_score = sec_report.security_score_pct if sec_valid else 0.0
        sec_weight = 10.0
        sec_weighted = (sec_score * sec_weight) / 100.0

        total_score = cov_weighted + prop_weighted + ai_weighted + err_weighted + corr_weighted + sec_weighted
        total_score = round(total_score, 2)

        pillar_scores: List[TracingPillarScore] = [
            TracingPillarScore(
                pillar_name="Distributed Trace Coverage & OTel Architecture",
                weight_pct=cov_weight,
                achieved_score_pct=round(cov_score, 2),
                weighted_score_pct=round(cov_weighted, 2),
                status="PASSED" if cov_score >= 95.0 else "NEEDS_IMPROVEMENT"
            ),
            TracingPillarScore(
                pillar_name="Context Propagation & W3C Standard Integrity",
                weight_pct=prop_weight,
                achieved_score_pct=round(prop_score, 2),
                weighted_score_pct=round(prop_weighted, 2),
                status="PASSED" if prop_score >= 95.0 else "NEEDS_IMPROVEMENT"
            ),
            TracingPillarScore(
                pillar_name="AI Agent Autonomous Lifecycle & LLM Visibility",
                weight_pct=ai_weight,
                achieved_score_pct=round(ai_score, 2),
                weighted_score_pct=round(ai_weighted, 2),
                status="PASSED" if ai_score >= 95.0 else "NEEDS_IMPROVEMENT"
            ),
            TracingPillarScore(
                pillar_name="Error Diagnosis & Chaos Root-Cause Isolation",
                weight_pct=err_weight,
                achieved_score_pct=round(err_score, 2),
                weighted_score_pct=round(err_weighted, 2),
                status="PASSED" if err_score >= 95.0 else "NEEDS_IMPROVEMENT"
            ),
            TracingPillarScore(
                pillar_name="Bidirectional Trace, Log & Metric Correlation",
                weight_pct=corr_weight,
                achieved_score_pct=round(corr_score, 2),
                weighted_score_pct=round(corr_weighted, 2),
                status="PASSED" if corr_score >= 95.0 else "NEEDS_IMPROVEMENT"
            ),
            TracingPillarScore(
                pillar_name="Span Security Protection & Low Overhead (<5%)",
                weight_pct=sec_weight,
                achieved_score_pct=round(sec_score, 2),
                weighted_score_pct=round(sec_weighted, 2),
                status="PASSED" if sec_score >= 95.0 else "NEEDS_IMPROVEMENT"
            ),
        ]

        if total_score >= 95.0:
            tier = TracingCertificationTier.ENTERPRISE_TRACING_READY
            granted = True
        elif total_score >= 90.0:
            tier = TracingCertificationTier.PRODUCTION_READY
            granted = True
        elif total_score >= 80.0:
            tier = TracingCertificationTier.IMPROVEMENT_REQUIRED
            granted = False
        else:
            tier = TracingCertificationTier.FAILED
            granted = False

        return TracingCertificationReport(
            report_title="Phase 3I.4 Enterprise Distributed Tracing Certification",
            evaluated_at=datetime.now(timezone.utc).isoformat(),
            certification_tier=tier,
            overall_score_pct=total_score,
            minimum_passing_threshold_pct=95.0,
            pillar_scores=pillar_scores,
            certification_granted=granted,
            auditor="DocuTask Enterprise Observability & SRE Tracing Certification Engine"
        )
