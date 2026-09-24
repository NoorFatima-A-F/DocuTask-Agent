"""
AST-based static analysis scanner for Python codebases.
"""
from __future__ import annotations
import ast
import os
from pathlib import Path
from typing import Any, Dict, List, Tuple
from app.core.security import resolve_safe_path
from app.platform_verification.architecture_verification.domain.interfaces import IASTScanner
from app.platform_verification.architecture_verification.domain.models import ArchitectureDependency


class EnterpriseASTScanner(IASTScanner):
    """Extracts module imports, class/function metrics, and AST structures."""

    def scan_directory(self, root_dir: str) -> Tuple[List[ArchitectureDependency], Dict[str, Any], int, int]:
        dependencies: List[ArchitectureDependency] = []
        file_metrics: Dict[str, Any] = {}
        total_files = 0
        total_lines = 0

        root_path = Path(root_dir) if root_dir else Path.cwd()

        for dirpath, _, filenames in os.walk(root_path):
            if any(p in dirpath for p in [".git", "__pycache__", ".pytest_cache", "venv", ".venv"]):
                continue

            for fname in filenames:
                if not fname.endswith(".py"):
                    continue

                total_files += 1
                full_path = resolve_safe_path(root_path, os.path.join(dirpath, fname))
                rel_path = os.path.relpath(full_path, root_path).replace("\\", "/")
                mod_name = rel_path.replace(".py", "").replace("/", ".")

                try:
                    with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                        source_code = f.read()

                    lines = source_code.splitlines()
                    num_lines = len(lines)
                    total_lines += num_lines

                    parsed_ast = ast.parse(source_code, filename=rel_path)

                    # Extract imports
                    imports_in_file = self._extract_imports(parsed_ast, mod_name, rel_path)
                    dependencies.extend(imports_in_file)

                    # Extract class/function sizes
                    class_sizes, func_sizes = self._extract_ast_sizes(parsed_ast)

                    file_metrics[rel_path] = {
                        "module_name": mod_name,
                        "line_count": num_lines,
                        "class_sizes": class_sizes,
                        "function_sizes": func_sizes,
                    }

                except SyntaxError:
                    file_metrics[rel_path] = {
                        "module_name": mod_name,
                        "line_count": 0,
                        "syntax_error": True,
                    }

        return dependencies, file_metrics, total_files, total_lines

    def _extract_imports(self, tree: ast.AST, source_mod: str, rel_path: str) -> List[ArchitectureDependency]:
        deps: List[ArchitectureDependency] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    deps.append(
                        ArchitectureDependency(
                            source_module=source_mod,
                            target_module=alias.name,
                            dependency_type="import",
                            line_number=node.lineno,
                        )
                    )
            elif isinstance(node, ast.ImportFrom):
                target = node.module or ""
                deps.append(
                    ArchitectureDependency(
                        source_module=source_mod,
                        target_module=target,
                        dependency_type="from_import",
                        line_number=node.lineno,
                    )
                )
        return deps

    def _extract_ast_sizes(self, tree: ast.AST) -> Tuple[Dict[str, int], Dict[str, int]]:
        class_sizes: Dict[str, int] = {}
        func_sizes: Dict[str, int] = {}

        for node in ast.iter_child_nodes(tree):
            if isinstance(node, ast.ClassDef):
                end_lineno = getattr(node, "end_lineno", node.lineno)
                class_sizes[node.name] = (end_lineno - node.lineno) + 1
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                end_lineno = getattr(node, "end_lineno", node.lineno)
                func_sizes[node.name] = (end_lineno - node.lineno) + 1

        return class_sizes, func_sizes
