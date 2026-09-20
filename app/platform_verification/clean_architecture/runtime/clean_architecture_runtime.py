"""
Enterprise Clean Architecture Runtime facade.
"""
from __future__ import annotations
import os
from typing import Dict, List, Optional
import uuid
from app.platform_verification.clean_architecture.core.ast_dependency_analyzer import EnterpriseCleanArchASTScanner
from app.platform_verification.clean_architecture.core.domain_isolation_verifier import EnterpriseDomainIsolationVerifier
from app.platform_verification.clean_architecture.core.evidence_store import EnterpriseCleanArchEvidenceStore
from app.platform_verification.clean_architecture.core.metrics_calculator import EnterpriseDependencyMetricsCalculator
from app.platform_verification.clean_architecture.core.rule_engine import EnterpriseDependencyRuleEngine
from app.platform_verification.clean_architecture.domain.models import (
    ArchitectureExceptionWaiver,
    CleanArchEvidencePackage,
)


class EnterpriseCleanArchitectureRuntime:
    """Unified runtime facade for Clean Architecture scanning, metrics, and rule evaluation."""

    def __init__(self, base_repo_dir: Optional[str] = None):
        self.base_repo_dir = base_repo_dir or r"c:\Users\User\Desktop\ai_document_processing_platform"
        self.scanner = EnterpriseCleanArchASTScanner()
        self.rule_engine = EnterpriseDependencyRuleEngine()
        self.metrics_calculator = EnterpriseDependencyMetricsCalculator()
        self.domain_verifier = EnterpriseDomainIsolationVerifier()
        self.evidence_store = EnterpriseCleanArchEvidenceStore()
        self._waivers: List[ArchitectureExceptionWaiver] = []
        self._latest_scan_id: Optional[str] = None

    def add_waiver(self, waiver: ArchitectureExceptionWaiver) -> None:
        self._waivers.append(waiver)

    def run_full_validation(
        self, target_dir: Optional[str] = None, commit_sha: str = "HEAD"
    ) -> CleanArchEvidencePackage:
        scan_dir = target_dir or os.path.join(self.base_repo_dir, "app")
        scan_id = f"CLEAN-ARCH-{uuid.uuid4().hex[:8].upper()}"

        # 1. AST Scan
        edges = self.scanner.scan_codebase(scan_dir)

        # 2. Evaluate Layer Rules & Waivers
        violations = self.rule_engine.evaluate_dependencies(edges=edges, waivers=self._waivers)

        # 3. Calculate Coupling & Instability Metrics
        module_metrics = self.metrics_calculator.calculate_module_metrics(edges=edges)

        # 4. Domain Isolation Check
        is_pure, domain_violations = self.domain_verifier.verify_domain_purity()

        certified = len(violations) == 0 and is_pure

        unique_modules = {e.source_module for e in edges}

        package = CleanArchEvidencePackage(
            scan_id=scan_id,
            commit_sha=commit_sha,
            total_modules_analyzed=len(unique_modules),
            total_dependencies_extracted=len(edges),
            violations=violations,
            circular_dependency_cycles=[],
            module_metrics=module_metrics,
            active_waivers=[w for w in self._waivers if w.is_active()],
            clean_architecture_certified=certified,
        )

        self.evidence_store.save_evidence(package)
        self._latest_scan_id = scan_id
        return package

    def get_latest_scan(self) -> Optional[CleanArchEvidencePackage]:
        if not self._latest_scan_id:
            return None
        return self.evidence_store.get_evidence(self._latest_scan_id)
