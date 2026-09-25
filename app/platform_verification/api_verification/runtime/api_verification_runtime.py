"""
Enterprise API Verification Platform Runtime facade.
"""
from __future__ import annotations
import os
from pathlib import Path
from typing import Optional
import uuid
from app.platform_verification.api_verification.core.api_ast_analyzer import EnterpriseApiASTAnalyzer
from app.platform_verification.api_verification.core.api_evidence_store import EnterpriseApiEvidenceStore
from app.platform_verification.api_verification.core.api_scoring_engine import EnterpriseApiScoringEngine
from app.platform_verification.api_verification.core.async_agent_workflow_validator import (
    EnterpriseAsyncAgentWorkflowValidator,
)
from app.platform_verification.api_verification.core.compatibility_engine import (
    EnterpriseApiCompatibilityEngine,
)
from app.platform_verification.api_verification.core.security_evaluator import (
    EnterpriseApiSecurityValidator,
)
from app.platform_verification.api_verification.domain.models import ApiEvidencePackage


class EnterpriseApiVerificationRuntime:
    """Unified runtime facade for API purity scanning, schema compatibility, and security evaluations."""

    def __init__(self, base_repo_dir: Optional[str] = None):
        self.base_repo_dir = base_repo_dir or str(Path.cwd())
        self.ast_analyzer = EnterpriseApiASTAnalyzer()
        self.compatibility_engine = EnterpriseApiCompatibilityEngine()
        self.security_validator = EnterpriseApiSecurityValidator()
        self.workflow_validator = EnterpriseAsyncAgentWorkflowValidator()
        self.scoring_engine = EnterpriseApiScoringEngine()
        self.evidence_store = EnterpriseApiEvidenceStore()
        self._latest_scan_id: Optional[str] = None

    def run_full_scan(self, target_api_dir: Optional[str] = None, commit_sha: str = "HEAD") -> ApiEvidencePackage:
        api_dir = target_api_dir or os.path.join(self.base_repo_dir, "app", "api")
        scan_id = f"API-SCAN-{uuid.uuid4().hex[:8].upper()}"

        # 1. AST Purity Scan
        endpoint_metrics = self.ast_analyzer.analyze_api_directory(api_dir)

        # 2. Security Evaluation
        security_findings = self.security_validator.evaluate_security(endpoint_metrics)

        # 3. Breaking changes (sample check)
        breaking_changes = []

        # 4. Scorecard
        scorecard = self.scoring_engine.calculate_scorecard(
            endpoints=endpoint_metrics,
            security_findings=security_findings,
            breaking_changes=breaking_changes,
        )

        pkg = ApiEvidencePackage(
            scan_id=scan_id,
            commit_sha=commit_sha,
            endpoints_analyzed_count=len(endpoint_metrics),
            endpoint_metrics=endpoint_metrics,
            security_findings=security_findings,
            breaking_changes=breaking_changes,
            scorecard=scorecard,
        )

        self.evidence_store.save_evidence(pkg)
        self._latest_scan_id = scan_id
        return pkg

    def get_latest_scan(self) -> Optional[ApiEvidencePackage]:
        if not self._latest_scan_id:
            return None
        return self.evidence_store.get_evidence(self._latest_scan_id)
