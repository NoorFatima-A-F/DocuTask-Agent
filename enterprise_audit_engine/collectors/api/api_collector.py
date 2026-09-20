"""API Layer & Endpoint Contract Collector."""

import ast
import os
from pathlib import Path
from typing import List, Dict, Any
from ..domain.evidence.models import (
    EvidenceRecord,
    EvidenceClassification,
    EvidenceConfidence,
    EvidenceSourceType,
)
from ..base import BaseCollector


class APICollector(BaseCollector):
    """Inspects API routers, endpoint declarations, HTTP verbs, and Pydantic schema contracts."""

    @property
    def name(self) -> str:
        return "APICollector"

    @property
    def category(self) -> str:
        return "APIDesignAndContracts"

    async def collect(self) -> List[EvidenceRecord]:
        records: List[EvidenceRecord] = []
        app_dir = self.repo_root / "app"

        routes_found: List[Dict[str, Any]] = []
        schemas_found: List[str] = []

        for root, _, files in os.walk(app_dir):
            for f in files:
                if f.endswith(".py"):
                    file_path = Path(root) / f
                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as fp:
                            content = fp.read()
                            tree = ast.parse(content, filename=str(file_path))
                            for node in ast.walk(tree):
                                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                                    # Detect FastAPI route decorators
                                    for dec in node.decorator_list:
                                        if isinstance(dec, ast.Call) and isinstance(dec.func, ast.Attribute):
                                            if dec.func.attr in {"get", "post", "put", "delete", "patch"}:
                                                routes_found.append({
                                                    "function": node.name,
                                                    "method": dec.func.attr.upper(),
                                                    "file": file_path.relative_to(self.repo_root).as_posix(),
                                                })
                                elif isinstance(node, ast.ClassDef):
                                    for base in node.bases:
                                        if isinstance(base, ast.Name) and "BaseModel" in base.id:
                                            schemas_found.append(node.name)
                    except Exception:
                        pass

        payload: Dict[str, Any] = {
            "total_endpoints_discovered": len(routes_found),
            "total_schemas_discovered": len(schemas_found),
            "endpoints": routes_found[:20],
            "schemas_sample": schemas_found[:20],
        }

        classification = (
            EvidenceClassification.VERIFIED_BY_STATIC_ANALYSIS
            if len(routes_found) > 0 and len(schemas_found) > 0
            else EvidenceClassification.PARTIALLY_VERIFIED
        )

        record = EvidenceRecord.create(
            category=self.category,
            collector=self.name,
            source_type=EvidenceSourceType.STATIC_SOURCE_CODE,
            raw_payload=payload,
            summary=f"Discovered {len(routes_found)} FastAPI HTTP endpoints and {len(schemas_found)} Pydantic validation schemas across platform codebase.",
            confidence=EvidenceConfidence.MEDIUM,
            classification=classification,
        )
        records.append(record)
        return records
