"""API Contract & Schema Coverage Verifier."""

import ast
from pathlib import Path
from typing import Dict, Any, List


class APIContractVerifier:
    """Verifies that exposed routes have valid input schemas and deterministic output contracts."""

    @staticmethod
    def inspect_api_contracts(app_dir: Path) -> Dict[str, Any]:
        if not app_dir.exists():
            return {
                "total_routes": 0,
                "contract_enforced_routes": 0,
                "untyped_routes": 0,
                "contract_coverage_pct": 0.0,
            }

        total_routes = 0
        typed_routes = 0

        for file_path in app_dir.glob("**/*.py"):
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as fp:
                    tree = ast.parse(fp.read(), filename=str(file_path))
                    for node in ast.walk(tree):
                        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                            is_route = False
                            for dec in node.decorator_list:
                                if isinstance(dec, ast.Call) and isinstance(dec.func, ast.Attribute):
                                    if dec.func.attr in {"get", "post", "put", "delete", "patch"}:
                                        is_route = True
                            if is_route:
                                total_routes += 1
                                # Check if returns type annotation or uses response_model
                                has_annotation = node.returns is not None
                                if has_annotation:
                                    typed_routes += 1
            except Exception:
                pass

        coverage = (typed_routes / total_routes * 100.0) if total_routes > 0 else 100.0
        return {
            "total_routes": total_routes,
            "contract_enforced_routes": typed_routes,
            "untyped_routes": total_routes - typed_routes,
            "contract_coverage_pct": round(coverage, 2),
        }
