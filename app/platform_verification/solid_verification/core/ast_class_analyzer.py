"""
AST Class & Method Analyzer extracting CK metrics and SOLID indicators.
"""
from __future__ import annotations
import ast
import os
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple
from app.core.security import resolve_safe_path
from app.platform_verification.solid_verification.domain.interfaces import ISolidASTAnalyzer
from app.platform_verification.solid_verification.domain.models import (
    ClassDesignMetrics,
    InterfaceDesignMetrics,
)


class EnterpriseSolidASTAnalyzer(ISolidASTAnalyzer):
    """Analyzes class structures, responsibility domains, instantiations, and method complexities."""

    def analyze_classes(self, root_dir: str) -> Tuple[Dict[str, ClassDesignMetrics], Dict[str, InterfaceDesignMetrics]]:
        class_metrics: Dict[str, ClassDesignMetrics] = {}
        interface_metrics: Dict[str, InterfaceDesignMetrics] = {}
        root_path = Path(root_dir) if root_dir else Path.cwd()

        for dirpath, _, filenames in os.walk(root_path):
            if any(p in dirpath for p in [".git", "__pycache__", ".pytest_cache", "venv", ".venv"]):
                continue

            for fname in filenames:
                if not fname.endswith(".py"):
                    continue

                full_path = Path(dirpath) / fname
                rel_path = os.path.relpath(full_path, root_path).replace("\\", "/")

                try:
                    with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                        code = f.read()

                    tree = ast.parse(code, filename=rel_path)
                    for node in ast.iter_child_nodes(tree):
                        if isinstance(node, ast.ClassDef):
                            cm, im = self._analyze_class_node(node, rel_path)
                            if cm:
                                class_metrics[f"{rel_path}:{node.name}"] = cm
                            if im:
                                interface_metrics[f"{rel_path}:{node.name}"] = im
                except SyntaxError:
                    continue

        return class_metrics, interface_metrics

    def _analyze_class_node(
        self, node: ast.ClassDef, rel_path: str
    ) -> Tuple[Optional[ClassDesignMetrics], Optional[InterfaceDesignMetrics]]:
        end_lineno = getattr(node, "end_lineno", node.lineno)
        line_count = (end_lineno - node.lineno) + 1

        methods: List[ast.FunctionDef] = []
        attributes: Set[str] = set()
        constructor_param_count = 0
        wmc = 0
        responsibilities: Set[str] = set()
        has_type_switch = False
        has_unsupported_op = False
        has_direct_instantiation = False

        is_interface = False
        if any(base.id in ("ABC", "Protocol") for base in node.bases if isinstance(base, ast.Name)):
            is_interface = True

        for item in node.body:
            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                methods.append(item)
                # Compute method complexity (cyclomatic complexity approximation)
                wmc += self._compute_cyclomatic_complexity(item)

                if item.name == "__init__":
                    constructor_param_count = len(item.args.args) - 1  # exclude self

                # Inspect method body for responsibilities and violations
                m_res = self._detect_method_responsibilities(item.name)
                responsibilities.update(m_res)

                if self._has_type_switching(item):
                    has_type_switch = True

                if self._raises_unsupported_operation(item):
                    has_unsupported_op = True

                if self._has_direct_concrete_instantiation(item, rel_path):
                    has_direct_instantiation = True

            elif isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name):
                        attributes.add(target.id)

        cbo = max(1, constructor_param_count + len(responsibilities))
        lcom = round(min(1.0, max(0.0, (len(responsibilities) - 1) / max(1, len(methods)))), 2)
        rfc = len(methods) + cbo
        dit = len(node.bases)

        cm = ClassDesignMetrics(
            class_name=node.name,
            file_path=rel_path,
            line_count=line_count,
            method_count=len(methods),
            attribute_count=len(attributes),
            constructor_param_count=constructor_param_count,
            wmc_weighted_methods=wmc,
            cbo_coupling_between_objects=cbo,
            lcom_lack_of_cohesion=lcom,
            rfc_response_for_class=rfc,
            dit_depth_of_inheritance=dit,
            noc_number_of_children=0,
            detected_responsibilities=list(responsibilities),
            has_type_switch_violation=has_type_switch,
            has_unsupported_operation_override=has_unsupported_op,
            has_direct_instantiation_violation=has_direct_instantiation,
        )

        im = None
        if is_interface or len(methods) >= 6:
            im = InterfaceDesignMetrics(
                interface_name=node.name,
                file_path=rel_path,
                total_methods=len(methods),
                implementations_count=1,
                avg_usage_ratio=0.8 if len(methods) < 10 else 0.4,
                is_oversized=len(methods) >= 12,
            )

        return cm, im

    def _compute_cyclomatic_complexity(self, func: ast.FunctionDef) -> int:
        complexity = 1
        for node in ast.walk(func):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.ExceptHandler, ast.With, ast.Assert)):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                complexity += len(node.values) - 1
        return complexity

    def _detect_method_responsibilities(self, method_name: str) -> List[str]:
        m = method_name.lower()
        res = []
        if any(k in m for k in ["upload", "download", "s3", "storage"]):
            res.append("Storage")
        if any(k in m for k in ["ocr", "extract", "parse", "vision"]):
            res.append("OCR/Extraction")
        if any(k in m for k in ["embed", "vector", "embedding"]):
            res.append("Embedding")
        if any(k in m for k in ["email", "notify", "slack", "sms"]):
            res.append("Notification")
        if any(k in m for k in ["save", "persist", "db", "insert", "delete"]):
            res.append("Persistence")
        if any(k in m for k in ["auth", "token", "login", "encrypt"]):
            res.append("Security")
        if any(k in m for k in ["report", "html", "pdf", "export"]):
            res.append("Reporting")
        return res

    def _has_type_switching(self, func: ast.FunctionDef) -> bool:
        for node in ast.walk(func):
            if isinstance(node, ast.If):
                # Look for if provider == "gemini" elif provider == "openai"
                if isinstance(node.test, ast.Compare):
                    if len(node.orelse) > 0 and any(isinstance(o, ast.If) for o in node.orelse):
                        return True
        return False

    def _raises_unsupported_operation(self, func: ast.FunctionDef) -> bool:
        for node in ast.walk(func):
            if isinstance(node, ast.Raise) and node.exc:
                if isinstance(node.exc, ast.Call) and isinstance(node.exc.func, ast.Name):
                    if node.exc.func.id in ("NotImplementedError", "UnsupportedOperationError"):
                        return True
        return False

    def _has_direct_concrete_instantiation(self, func: ast.FunctionDef, rel_path: str) -> bool:
        # Check if high level (domain, application) instantiates concrete vendor SDKs
        if "domain" in rel_path or "application" in rel_path:
            for node in ast.walk(func):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                    if node.func.id in ("GeminiClient", "OpenAIClient", "DatabaseSession", "RedisClient"):
                        return True
        return False
