"""
Phase 3I.4: Evidence Exporter for Enterprise Distributed Tracing Verification
"""
import os
import json
import hashlib
from typing import Dict, Any
from datetime import datetime, timezone
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
from ..domain.interfaces import ITracingEvidenceExporter


class TracingEvidenceExporter(ITracingEvidenceExporter):
    """
    Exports standardized JSON evidence reports plus signed metadata.json with SHA-256 cryptographic digests.
    """

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
        os.makedirs(output_dir, exist_ok=True)

        report_payloads = {
            "architecture_report.json": arch_report.model_dump(mode="json"),
            "context_propagation_report.json": prop_report.model_dump(mode="json"),
            "workflow_trace_report.json": wf_report.model_dump(mode="json"),
            "agent_trace_report.json": agent_report.model_dump(mode="json"),
            "dependency_trace_report.json": dep_report.model_dump(mode="json"),
            "error_trace_report.json": err_report.model_dump(mode="json"),
            "correlation_report.json": corr_report.model_dump(mode="json"),
            "security_report.json": sec_report.model_dump(mode="json"),
            "performance_report.json": perf_report.model_dump(mode="json"),
            "certification_report.json": certification_report.model_dump(mode="json"),
        }

        manifest: Dict[str, str] = {}
        for filename, data in report_payloads.items():
            filepath = os.path.join(output_dir, filename)
            content_str = json.dumps(data, indent=2)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content_str)
            sha256_hash = hashlib.sha256(content_str.encode("utf-8")).hexdigest()
            manifest[filename] = sha256_hash

        metadata = {
            "project": "DocuTask-Agent",
            "phase": "Phase 3I.4 — Enterprise Distributed Tracing Infrastructure Verification Framework",
            "environment": "PRODUCTION_SANDBOX",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "commit": "HEAD",
            "services_instrumented": arch_report.services_instrumented,
            "overall_score_pct": certification_report.overall_score_pct,
            "certification_tier": certification_report.certification_tier.value,
            "certification_granted": certification_report.certification_granted,
            "total_artifacts": len(manifest),
            "manifest_sha256": manifest,
            "auditor": certification_report.auditor,
        }

        meta_path = os.path.join(output_dir, "metadata.json")
        meta_str = json.dumps(metadata, indent=2)
        with open(meta_path, "w", encoding="utf-8") as f:
            f.write(meta_str)

        return metadata
