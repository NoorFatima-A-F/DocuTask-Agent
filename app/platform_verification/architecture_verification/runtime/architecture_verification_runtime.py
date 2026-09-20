"""
Enterprise Architecture Verification Platform Runtime facade.
"""
from __future__ import annotations
import os
from typing import Optional
import uuid
from app.platform_verification.architecture_verification.core.ast_scanner import EnterpriseASTScanner
from app.platform_verification.architecture_verification.core.dependency_graph import EnterpriseDependencyGraphEngine
from app.platform_verification.architecture_verification.core.evidence_store import EnterpriseArchitectureEvidenceStore
from app.platform_verification.architecture_verification.core.regression_engine import EnterpriseArchitectureRegressionEngine
from app.platform_verification.architecture_verification.core.rule_engine import EnterpriseArchitectureRuleEngine
from app.platform_verification.architecture_verification.core.scoring_engine import EnterpriseArchitectureScoringEngine
from app.platform_verification.architecture_verification.domain.models import (
    ArchitectureEvidencePackage,
    ScanMetadata,
)


class EnterpriseArchitectureVerificationRuntime:
    """Unified facade for AST scanning, graph analysis, rule evaluation, scoring, and regression detection."""

    def __init__(self, base_repo_dir: Optional[str] = None):
        self.base_repo_dir = base_repo_dir or r"c:\Users\User\Desktop\ai_document_processing_platform"
        self.scanner = EnterpriseASTScanner()
        self.graph_engine = EnterpriseDependencyGraphEngine()
        self.rule_engine = EnterpriseArchitectureRuleEngine()
        self.scoring_engine = EnterpriseArchitectureScoringEngine()
        self.regression_engine = EnterpriseArchitectureRegressionEngine()
        self.evidence_store = EnterpriseArchitectureEvidenceStore()
        self._latest_scan_id: Optional[str] = None

    def run_full_scan(self, target_dir: Optional[str] = None, commit_sha: str = "HEAD") -> ArchitectureEvidencePackage:
        scan_dir = target_dir or os.path.join(self.base_repo_dir, "app")
        scan_id = f"ARCH-SCAN-{uuid.uuid4().hex[:8].upper()}"

        # 1. AST Scan
        dependencies, file_metrics, total_files, total_lines = self.scanner.scan_directory(scan_dir)

        # 2. Dependency Graph & Cycles
        graph = self.graph_engine.build_graph(dependencies)
        circular_cycles = self.graph_engine.detect_circular_dependencies(graph)

        # 3. Rule Evaluation
        violations = self.rule_engine.evaluate_rules(
            dependencies=dependencies,
            file_metrics=file_metrics,
            circular_cycles=circular_cycles,
        )

        # 4. Scoring
        score_report = self.scoring_engine.calculate_score(
            violations=violations,
            circular_cycles=circular_cycles,
            total_files=total_files,
        )

        # 5. Package Evidence
        metadata = ScanMetadata(
            scan_id=scan_id,
            repository_root=scan_dir,
            commit_sha=commit_sha,
            total_files_scanned=total_files,
            total_lines_of_code=total_lines,
        )

        formatted_graph = {k: [{"target": t} for t in v] for k, v in graph.items()}

        package = ArchitectureEvidencePackage(
            scan_id=scan_id,
            metadata=metadata,
            dependency_graph=formatted_graph,
            violations=violations,
            circular_cycles=circular_cycles,
            score_report=score_report,
        )

        self.evidence_store.save_evidence(package)
        self._latest_scan_id = scan_id
        return package

    def get_latest_scan(self) -> Optional[ArchitectureEvidencePackage]:
        if not self._latest_scan_id:
            return None
        return self.evidence_store.get_evidence(self._latest_scan_id)
