"""
AST Dependency Analyzer extracting direct, relative, and dynamic imports.
"""
from __future__ import annotations
import ast
import os
from pathlib import Path
from typing import Any, Dict, List, Tuple
from app.core.security import resolve_safe_path
from app.platform_verification.clean_architecture.core.layer_definitions import classify_module_layer
from app.platform_verification.clean_architecture.domain.interfaces import ICleanArchitectureScanner
from app.platform_verification.clean_architecture.domain.models import (
    ArchitectureLayer,
    CleanArchDependencyEdge,
    ImportType,
)


class EnterpriseCleanArchASTScanner(ICleanArchitectureScanner):
    """Scans Python files and resolves relative and dynamic imports into Clean Architecture layers."""

    def scan_codebase(self, root_dir: str) -> List[CleanArchDependencyEdge]:
        edges: List[CleanArchDependencyEdge] = []
        root_path = Path(root_dir) if root_dir else Path.cwd()

        for dirpath, _, filenames in os.walk(root_path):
            if any(p in dirpath for p in [".git", "__pycache__", ".pytest_cache", "venv", ".venv"]):
                continue

            for fname in filenames:
                if not fname.endswith(".py"):
                    continue

                full_path = resolve_safe_path(root_path, os.path.join(dirpath, fname))
                rel_path = os.path.relpath(full_path, root_path).replace("\\", "/")
                src_mod = rel_path.replace(".py", "").replace("/", ".")
                src_layer = classify_module_layer(src_mod)

                try:
                    with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                        code = f.read()

                    tree = ast.parse(code, filename=rel_path)
                    file_edges = self._extract_edges(tree, src_mod, src_layer, rel_path)
                    edges.extend(file_edges)
                except SyntaxError:
                    continue

        return edges

    def _extract_edges(
        self, tree: ast.AST, src_mod: str, src_layer: ArchitectureLayer, rel_path: str
    ) -> List[CleanArchDependencyEdge]:
        edges: List[CleanArchDependencyEdge] = []

        for node in ast.walk(tree):
            # Direct Imports
            if isinstance(node, ast.Import):
                for alias in node.names:
                    tgt_mod = alias.name
                    edges.append(
                        CleanArchDependencyEdge(
                            source_module=src_mod,
                            source_layer=src_layer,
                            target_module=tgt_mod,
                            target_layer=classify_module_layer(tgt_mod),
                            import_type=ImportType.DIRECT_IMPORT,
                            line_number=node.lineno,
                        )
                    )

            # From Imports (Absolute & Relative)
            elif isinstance(node, ast.ImportFrom):
                tgt_mod = node.module or ""
                itype = ImportType.RELATIVE_IMPORT if node.level > 0 else ImportType.FROM_IMPORT
                edges.append(
                    CleanArchDependencyEdge(
                        source_module=src_mod,
                        source_layer=src_layer,
                        target_module=tgt_mod,
                        target_layer=classify_module_layer(tgt_mod),
                        import_type=itype,
                        line_number=node.lineno,
                    )
                )

            # Dynamic import calls: importlib.import_module(...)
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute) and node.func.attr == "import_module":
                    if node.args and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str):
                        tgt_mod = node.args[0].value
                        edges.append(
                            CleanArchDependencyEdge(
                                source_module=src_mod,
                                source_layer=src_layer,
                                target_module=tgt_mod,
                                target_layer=classify_module_layer(tgt_mod),
                                import_type=ImportType.DYNAMIC_IMPORT,
                                line_number=node.lineno,
                            )
                        )

        return edges
