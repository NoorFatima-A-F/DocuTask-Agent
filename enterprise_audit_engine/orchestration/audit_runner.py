"""Audit Orchestrator & Execution Engine."""

import os
import subprocess
import time
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime, timezone

from ..domain.evidence.models import (
    EvidenceRecord,
    AuditReportManifest,
    AuditRunMetadata,
    CollectorHealthStatus,
    CollectorExecutionManifest,
    AuditFinding,
    EvidenceClassification,
    EvidenceConfidence,
    EvidenceSourceType,
)
from ..collectors import ALL_COLLECTORS
from ..storage.evidence_store import EvidenceStore
from ..reporters.report_generator import ReportGenerator
from ..analyzers.confidence_engine import ConfidenceEngine
from ..analyzers.verification_strength_model import VerificationStrengthModel
from ..governance.provenance_tracker import ProvenanceTracker
from ..governance.claim_validator import ClaimValidator


class AuditRunner:
    """Coordinates collectors, evidence persistence, provenance, and report generation."""

    def __init__(self, repo_root: Path, output_dir: Path):
        self.repo_root = repo_root
        self.output_dir = output_dir
        self.evidence_dir = output_dir / "audit-evidence"
        self.reports_dir = output_dir / "audit-reports"
        self.store = EvidenceStore(self.evidence_dir)
        self.reporter = ReportGenerator(self.reports_dir)
        self.metadata = self._build_metadata()
        self.provenance = ProvenanceTracker(self.metadata)

    def _get_git_commit(self) -> str:
        try:
            res = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=str(self.repo_root),
                capture_output=True,
                text=True,
                timeout=5,
            )
            if res.returncode == 0:
                return res.stdout.strip()
        except Exception:
            pass
        return "HEAD"

    def _build_metadata(self) -> AuditRunMetadata:
        commit_hash = self._get_git_commit()
        return AuditRunMetadata(
            git_commit_hash=commit_hash,
            repository_url="https://github.com/NoorFatima-A-F/DocuTask-Agent",
            engine_version="2.0.0",
            python_version="3.12",
            os_information=os.name,
            executor_identity="Enterprise-Audit-Engine-Automated-Runner",
        )

    async def run_full_audit(self) -> Dict[str, Any]:
        """Executes all registered collectors, persists evidence, and generates verified reports."""
        collected_records: List[EvidenceRecord] = []
        collector_health_statuses: List[CollectorHealthStatus] = []
        start_time = time.perf_counter()

        for collector_cls in ALL_COLLECTORS:
            collector = collector_cls(self.repo_root)
            col_start = time.perf_counter()
            col_name = getattr(collector, "name", collector_cls.__name__)
            try:
                records = await collector.collect()
                col_duration = (time.perf_counter() - col_start) * 1000.0

                for r in records:
                    self.store.save_evidence(r)
                    collected_records.append(r)
                    self.provenance.record_step(
                        step_name=f"Collect:{col_name}",
                        input_artifact=str(self.repo_root),
                        output_evidence_id=r.id,
                        command_executed=r.command,
                        duration_ms=r.duration_ms or col_duration,
                    )

                collector_health_statuses.append(
                    CollectorHealthStatus(
                        collector_name=col_name,
                        execution_attempted=True,
                        execution_completed=True,
                        duration_ms=col_duration,
                        evidence_generated_count=len(records),
                    )
                )
            except Exception as ex:
                col_duration = (time.perf_counter() - col_start) * 1000.0
                err_record = EvidenceRecord.create(
                    category=getattr(collector, "category", "AuditFramework"),
                    collector=col_name,
                    source_type=EvidenceSourceType.STATIC_SOURCE_CODE,
                    summary=f"Collector execution error: {str(ex)}",
                    confidence=EvidenceConfidence.NONE,
                    classification=EvidenceClassification.EVIDENCE_INSUFFICIENT,
                )
                self.store.save_evidence(err_record)
                collected_records.append(err_record)

                collector_health_statuses.append(
                    CollectorHealthStatus(
                        collector_name=col_name,
                        execution_attempted=True,
                        execution_completed=False,
                        exception_message=str(ex),
                        duration_ms=col_duration,
                        evidence_generated_count=1,
                    )
                )

        total_duration_ms = (time.perf_counter() - start_time) * 1000.0
        self.metadata.timestamp_end = datetime.now(timezone.utc).isoformat()

        exec_manifest = CollectorExecutionManifest(
            run_id=self.metadata.run_id,
            collectors=collector_health_statuses,
            total_duration_ms=total_duration_ms,
            all_collectors_healthy=all(c.execution_completed for c in collector_health_statuses),
        )

        # Build domain findings and scorecards
        subsystems = {r.category for r in collected_records}
        scorecards = {
            sub: VerificationStrengthModel.evaluate_subsystem(
                sub, [r for r in collected_records if r.category == sub]
            )
            for sub in subsystems
        }

        # Build formal AuditFindings
        findings: List[AuditFinding] = []
        for sub, card in scorecards.items():
            matching_ids = [r.id for r in collected_records if r.category == sub]
            findings.append(
                AuditFinding(
                    subsystem=sub,
                    claim=f"Subsystem '{sub}' verification evaluated to {card.classification.value}",
                    evidence_ids=matching_ids,
                    classification=card.classification,
                    confidence=card.confidence,
                    risk_level="HIGH" if card.classification == EvidenceClassification.CRITICAL_FINDING else "LOW",
                    analysis=card.justification,
                )
            )

        # Validate all findings against strict evidence truth criteria
        ClaimValidator.validate_all_findings(findings, collected_records)

        # Generate all reports
        provenance_data = self.provenance.export_provenance_manifest()
        report_files = self.reporter.generate_all_reports(
            records=collected_records,
            scorecards=scorecards,
            metadata=self.metadata,
            exec_manifest=exec_manifest,
            provenance_data=provenance_data,
        )

        # Create and persist tamper-evident Manifest
        manifest = AuditReportManifest(
            run_id=self.metadata.run_id,
            metadata=self.metadata,
            execution_manifest=exec_manifest,
            total_evidence_collected=len(collected_records),
            findings_count=len(findings),
            maturity_scorecard={
                sub: card.classification.value for sub, card in scorecards.items()
            },
            evidence_hashes=[r.content_hash for r in collected_records],
        )
        self.store.save_manifest(manifest)

        overall_classification = ConfidenceEngine.classify_subsystem(collected_records)
        overall_confidence = ConfidenceEngine.calculate_confidence(collected_records)

        return {
            "run_id": self.metadata.run_id,
            "total_evidence": len(collected_records),
            "scorecards": {sub: card.model_dump() for sub, card in scorecards.items()},
            "overall_classification": overall_classification.value,
            "overall_confidence": overall_confidence.value,
            "evidence_dir": str(self.evidence_dir),
            "reports_dir": str(self.reports_dir),
            "report_files": {k: str(v) for k, v in report_files.items()},
            "collector_manifest": exec_manifest.model_dump(),
        }
