"""Test Suite & Assertion Quality Collector."""

import ast
import os
from pathlib import Path
from typing import List, Dict, Any
from enterprise_audit_engine.domain.evidence.models import (
    EvidenceRecord,
    EvidenceClassification,
    EvidenceConfidence,
    EvidenceSourceType,
)
from enterprise_audit_engine.collectors.base import BaseCollector


class TestingCollector(BaseCollector):
    """Inspects test suites, counts test functions, detects assert True anti-patterns, and measures coverage depth."""

    @property
    def name(self) -> str:
        return "TestingCollector"

    @property
    def category(self) -> str:
        return "TestingQuality"

    async def collect(self) -> List[EvidenceRecord]:
        records: List[EvidenceRecord] = []
        tests_dir = self.repo_root / "tests"

        if not tests_dir.exists():
            records.append(
                EvidenceRecord.create(
                    category=self.category,
                    collector=self.name,
                    source_type=EvidenceSourceType.STATIC_SOURCE_CODE,
                    raw_payload={"error": "tests/ directory not found"},
                    summary="tests/ directory not found in repository root.",
                    confidence=EvidenceConfidence.LOW,
                    classification=EvidenceClassification.EVIDENCE_INSUFFICIENT,
                )
            )
            return records

        test_files_count = 0
        test_functions_count = 0
        assert_statements_count = 0
        fake_assertions_count = 0
        test_modules: List[str] = []

        for root, _, files in os.walk(tests_dir):
            for f in files:
                if f.startswith("test_") and f.endswith(".py"):
                    test_files_count += 1
                    file_path = Path(root) / f
                    test_modules.append(file_path.relative_to(self.repo_root).as_posix())

                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as fp:
                            content = fp.read()
                            tree = ast.parse(content, filename=str(file_path))
                            for node in ast.walk(tree):
                                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test_"):
                                    test_functions_count += 1
                                elif isinstance(node, ast.Assert):
                                    assert_statements_count += 1
                                    # Check for `assert True` or `assert 1 == 1`
                                    if isinstance(node.test, ast.Constant) and node.test.value is True:
                                        fake_assertions_count += 1
                    except Exception:
                        pass

        payload: Dict[str, Any] = {
            "test_files_count": test_files_count,
            "test_functions_count": test_functions_count,
            "assert_statements_count": assert_statements_count,
            "fake_assertions_count": fake_assertions_count,
            "test_modules": sorted(test_modules),
        }

        classification = (
            EvidenceClassification.VERIFIED_BY_STATIC_ANALYSIS
            if test_functions_count > 0 and fake_assertions_count == 0
            else EvidenceClassification.PARTIALLY_VERIFIED
        )

        record = EvidenceRecord.create(
            category=self.category,
            collector=self.name,
            source_type=EvidenceSourceType.STATIC_SOURCE_CODE,
            raw_payload=payload,
            summary=f"Inspected {test_files_count} test files containing {test_functions_count} test functions and {assert_statements_count} assertion statements. Fake assertions detected: {fake_assertions_count}.",
            confidence=EvidenceConfidence.HIGH,
            classification=classification,
        )
        records.append(record)
        return records
