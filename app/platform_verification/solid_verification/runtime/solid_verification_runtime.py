"""
Enterprise SOLID Verification Runtime facade.
"""
from __future__ import annotations
import os
from pathlib import Path
from typing import Optional
import uuid
from app.platform_verification.solid_verification.core.ast_class_analyzer import EnterpriseSolidASTAnalyzer
from app.platform_verification.solid_verification.core.solid_evidence_store import EnterpriseSolidEvidenceStore
from app.platform_verification.solid_verification.core.solid_rule_engine import EnterpriseSolidRuleEvaluator
from app.platform_verification.solid_verification.core.solid_scoring_engine import EnterpriseSolidScoringEngine
from app.platform_verification.solid_verification.domain.models import SolidEvidencePackage


class EnterpriseSolidVerificationRuntime:
    """Unified runtime facade for SOLID static analysis, rule evaluations, and scoring."""

    def __init__(self, base_repo_dir: Optional[str] = None):
        self.base_repo_dir = base_repo_dir or str(Path.cwd())
        self.analyzer = EnterpriseSolidASTAnalyzer()
        self.rule_evaluator = EnterpriseSolidRuleEvaluator()
        self.scoring_engine = EnterpriseSolidScoringEngine()
        self.evidence_store = EnterpriseSolidEvidenceStore()
        self._latest_scan_id: Optional[str] = None

    def run_full_scan(self, target_dir: Optional[str] = None, commit_sha: str = "HEAD") -> SolidEvidencePackage:
        scan_dir = target_dir or os.path.join(self.base_repo_dir, "app")
        scan_id = f"SOLID-SCAN-{uuid.uuid4().hex[:8].upper()}"

        # 1. AST Class Analysis
        class_metrics, interface_metrics = self.analyzer.analyze_classes(scan_dir)

        # 2. Evaluate all 5 principles
        violations = []
        violations.extend(self.rule_evaluator.evaluate_srp(class_metrics))
        violations.extend(self.rule_evaluator.evaluate_ocp(class_metrics))
        violations.extend(self.rule_evaluator.evaluate_lsp(class_metrics))
        violations.extend(self.rule_evaluator.evaluate_isp(interface_metrics))
        violations.extend(self.rule_evaluator.evaluate_dip(class_metrics))

        # 3. Compute Scorecard
        scorecard = self.scoring_engine.calculate_scorecard(
            violations=violations,
            total_classes=len(class_metrics),
        )

        package = SolidEvidencePackage(
            scan_id=scan_id,
            commit_sha=commit_sha,
            total_classes_analyzed=len(class_metrics),
            total_interfaces_analyzed=len(interface_metrics),
            class_metrics=class_metrics,
            interface_metrics=interface_metrics,
            violations=violations,
            scorecard=scorecard,
        )

        self.evidence_store.save_evidence(package)
        self._latest_scan_id = scan_id
        return package

    def get_latest_scan(self) -> Optional[SolidEvidencePackage]:
        if not self._latest_scan_id:
            return None
        return self.evidence_store.get_evidence(self._latest_scan_id)
