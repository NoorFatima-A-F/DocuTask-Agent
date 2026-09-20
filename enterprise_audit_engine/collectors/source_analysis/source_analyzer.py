"""Source Code Complexity, Import & Modularity Analyzer."""

import ast
import os
from pathlib import Path
from typing import List, Dict, Any, Set
from ..domain.evidence.models import (
    EvidenceRecord,
    EvidenceClassification,
    EvidenceConfidence,
    EvidenceSourceType,
)
from ..base import BaseCollector


class SourceAnalyzer(BaseCollector):
    """Analyzes AST syntax, package structure, class definitions, and import graphs."""

    @property
    def name(self) -> str:
        return "SourceAnalyzer"

    @property
    def category(self) -> str:
        return "SourceCodeAnalysis"

    async def collect(self) -> List[EvidenceRecord]:
        records: List[EvidenceRecord] = []
        app_dir = self.repo_root / "app"

        if not app_dir.exists():
            records.append(
                EvidenceRecord.create(
                    category=self.category,
                    collector=self.name,
                    source_type=EvidenceSourceType.STATIC_SOURCE_CODE,
                    raw_payload={"error": "app/ directory not found"},
                    summary="app/ directory not found in repository root.",
                    confidence=EvidenceConfidence.LOW,
                    classification=EvidenceClassification.EVIDENCE_INSUFFICIENT,
                )
            )
            return records

        total_modules = 0
        total_classes = 0
        total_functions = 0
        packages: Set[str] = set()
        syntax_errors: List[str] = []

        for root, _, files in os.walk(app_dir):
            rel_pkg = Path(root).relative_to(self.repo_root).as_posix()
            packages.add(rel_pkg)

            for f in files:
                if f.endswith(".py"):
                    total_modules += 1
                    file_path = Path(root) / f
                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as fp:
                            content = fp.read()
                            tree = ast.parse(content, filename=str(file_path))
                            for node in ast.walk(tree):
                                if isinstance(node, ast.ClassDef):
                                    total_classes += 1
                                elif isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
                                    total_functions += 1
                    except Exception as ex:
                        syntax_errors.append(f"{file_path.name}: {str(ex)}")

        payload: Dict[str, Any] = {
            "total_python_modules": total_modules,
            "total_classes": total_classes,
            "total_functions": total_functions,
            "packages_count": len(packages),
            "packages": sorted(list(packages))[:20],
            "syntax_errors_count": len(syntax_errors),
            "syntax_errors": syntax_errors,
        }

        classification = (
            EvidenceClassification.VERIFIED_BY_STATIC_ANALYSIS
            if len(syntax_errors) == 0
            else EvidenceClassification.PARTIALLY_VERIFIED
        )

        record = EvidenceRecord.create(
            category=self.category,
            collector=self.name,
            source_type=EvidenceSourceType.STATIC_SOURCE_CODE,
            raw_payload=payload,
            summary=f"Parsed {total_modules} Python modules across {len(packages)} packages ({total_classes} classes, {total_functions} functions). Syntax errors: {len(syntax_errors)}.",
            confidence=EvidenceConfidence.MEDIUM,
            classification=classification,
        )
        records.append(record)
        return records
