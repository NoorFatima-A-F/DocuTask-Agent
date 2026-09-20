"""
Test Evidence Collector for Enterprise AAOS.
Collects execution results from pytest test suites and transforms them
into immutable, cryptographically verifiable EvidenceItems.
"""

from __future__ import annotations

import logging
import os
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from app.evidence.registry.evidence_models import EvidenceItem, EvidenceType, VerificationStatus

logger = logging.getLogger(__name__)


class TestEvidenceCollector:
    """Collects verifiable test evidence from execution runs."""

    def __init__(self, workspace_root: Optional[Path] = None) -> None:
        self.workspace_root = workspace_root or Path.cwd()

    def collect_test_suite_evidence(
        self,
        suite_name: str,
        total_tests: int,
        passed_tests: int,
        failed_tests: int,
        duration_seconds: float,
        source_dir: str = "tests/agents/",
        artifact_path: Optional[str] = None,
    ) -> EvidenceItem:
        """Constructs a certified EvidenceItem from test suite execution metrics."""
        evidence_id = f"evi_test_{suite_name.lower().replace(' ', '_')}_{int(time.time())}"
        success_rate = (passed_tests / total_tests) if total_tests > 0 else 0.0

        payload = {
            "suite_name": suite_name,
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "duration_seconds": duration_seconds,
            "success_rate": round(success_rate, 4),
            "source_dir": source_dir,
        }

        item = EvidenceItem(
            evidence_id=evidence_id,
            title=f"Test Suite Execution: {suite_name}",
            description=f"Automated test run results for {suite_name}: {passed_tests}/{total_tests} passed in {duration_seconds:.2f}s",
            evidence_type=EvidenceType.UNIT_TEST if "unit" in suite_name.lower() else EvidenceType.INTEGRATION_TEST,
            source=source_dir,
            generated_by="pytest_runner",
            artifact_location=artifact_path,
            verification_status=VerificationStatus.VERIFIED if failed_tests == 0 else VerificationStatus.FAILED_VERIFICATION,
            confidence=1.0 if failed_tests == 0 else 0.0,
            reproducibility="DETERMINISTIC",
            raw_payload=payload,
        )
        return item
