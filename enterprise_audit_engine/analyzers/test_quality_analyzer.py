"""Test Quality & Assertion Density Analyzer."""

import ast
import os
from pathlib import Path
from typing import Dict, Any


class TestQualityAnalyzer:
    """Evaluates assertion density, weak assertions, and mock usage across test suites."""

    @staticmethod
    def analyze_test_directory(test_dir: Path) -> Dict[str, Any]:
        if not test_dir.exists():
            return {
                "total_test_files": 0,
                "total_test_functions": 0,
                "total_assertions": 0,
                "weak_assertions_count": 0,
                "mock_usages_count": 0,
                "assertion_density": 0.0,
                "quality_rating": "INSUFFICIENT",
            }

        total_files = 0
        total_functions = 0
        total_assertions = 0
        weak_assertions = 0
        mock_usages = 0

        for root, _, files in os.walk(test_dir):
            for f in files:
                if f.startswith("test_") and f.endswith(".py"):
                    total_files += 1
                    file_path = Path(root) / f
                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as fp:
                            content = fp.read()
                            tree = ast.parse(content, filename=str(file_path))
                            for node in ast.walk(tree):
                                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name.startswith("test_"):
                                    total_functions += 1
                                elif isinstance(node, ast.Assert):
                                    total_assertions += 1
                                    # Weak assertions check (e.g. `assert x`, `assert True`)
                                    if isinstance(node.test, ast.Constant):
                                        weak_assertions += 1
                                    elif isinstance(node.test, ast.Name):
                                        weak_assertions += 1
                                elif isinstance(node, ast.Call):
                                    if isinstance(node.func, ast.Attribute) and "mock" in node.func.attr.lower():
                                        mock_usages += 1
                    except Exception:
                        pass

        density = (total_assertions / total_functions) if total_functions > 0 else 0.0
        quality_rating = "HIGH" if density >= 2.0 and weak_assertions == 0 else "MEDIUM" if density >= 1.0 else "LOW"

        return {
            "total_test_files": total_files,
            "total_test_functions": total_functions,
            "total_assertions": total_assertions,
            "weak_assertions_count": weak_assertions,
            "mock_usages_count": mock_usages,
            "assertion_density": round(density, 2),
            "quality_rating": quality_rating,
        }
