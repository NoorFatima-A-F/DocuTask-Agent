"""
API AST Analyzer verifying handler purity, line bounds, and forbidden imports.
"""
from __future__ import annotations
import ast
import os
from typing import List
from app.platform_verification.api_verification.domain.interfaces import IApiASTAnalyzer
from app.platform_verification.api_verification.domain.models import EndpointPurityMetric


class EnterpriseApiASTAnalyzer(IApiASTAnalyzer):
    """Scans FastAPI endpoint routers and verifies that they delegate to application services."""

    def analyze_api_directory(self, root_api_dir: str) -> List[EndpointPurityMetric]:
        metrics: List[EndpointPurityMetric] = []

        for dirpath, _, filenames in os.walk(root_api_dir):
            if any(p in dirpath for p in [".git", "__pycache__", ".pytest_cache"]):
                continue

            for fname in filenames:
                if not fname.endswith(".py"):
                    continue

                full_path = os.path.join(dirpath, fname)
                rel_path = os.path.relpath(full_path, root_api_dir).replace("\\", "/")

                try:
                    with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                        code = f.read()

                    tree = ast.parse(code, filename=rel_path)
                    file_metrics = self._inspect_file_ast(tree, rel_path)
                    metrics.extend(file_metrics)
                except SyntaxError:
                    continue

        return metrics

    def _inspect_file_ast(self, tree: ast.AST, rel_path: str) -> List[EndpointPurityMetric]:
        endpoints: List[EndpointPurityMetric] = []
        forbidden_imports: List[str] = []

        # Check imports for forbidden concrete dependencies
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name in ("google.generativeai", "openai", "celery"):
                        forbidden_imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module in ("google.generativeai", "openai", "celery"):
                    forbidden_imports.append(node.module)

        # Inspect route decorator functions (@router.get, @router.post, etc.)
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                is_route, method, path = self._get_route_info(node)
                if is_route:
                    end_lineno = getattr(node, "end_lineno", node.lineno)
                    line_count = (end_lineno - node.lineno) + 1

                    has_sql = any("sqlalchemy" in imp or "db.query" in imp for imp in forbidden_imports)
                    has_llm = any("generativeai" in imp or "openai" in imp for imp in forbidden_imports)
                    is_bloated = line_count > 100

                    is_pure = not has_sql and not has_llm and not is_bloated

                    endpoints.append(
                        EndpointPurityMetric(
                            endpoint_path=path,
                            http_method=method,
                            file_path=rel_path,
                            line_number=node.lineno,
                            line_count=line_count,
                            has_direct_sql_import=has_sql,
                            has_direct_llm_call=has_llm,
                            has_business_logic_bloat=is_bloated,
                            is_pure=is_pure,
                            violating_imports=forbidden_imports,
                        )
                    )

        return endpoints

    def _get_route_info(self, func: ast.FunctionDef) -> Tuple[bool, str, str]:
        for dec in func.decorator_list:
            if isinstance(dec, ast.Call) and isinstance(dec.func, ast.Attribute):
                if dec.func.attr in ("get", "post", "put", "delete", "patch"):
                    method = dec.func.attr.upper()
                    path = "/"
                    if dec.args and isinstance(dec.args[0], ast.Constant) and isinstance(dec.args[0].value, str):
                        path = dec.args[0].value
                    return True, method, path
        return False, "", ""
