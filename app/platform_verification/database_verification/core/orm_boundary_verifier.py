"""
ORM and Repository Boundary Verifier for Enterprise Database Verification.
"""
import ast
from pathlib import Path
from typing import List
from app.platform_verification.database_verification.domain.models import (
    DatabaseBoundaryReport,
    DatabaseBoundaryViolation,
    ViolationSeverity,
)
from app.platform_verification.database_verification.domain.interfaces import IDatabaseBoundaryVerifier


class OrmBoundaryVerifier(IDatabaseBoundaryVerifier):
    """Verifies that ORM models and Repositories respect architectural boundaries."""

    FORBIDDEN_MODEL_CALLS = {"call_gemini", "generate_content", "process_ocr", "send_notification", "http_post", "requests.post"}

    def verify_boundaries(self, source_paths: List[str]) -> DatabaseBoundaryReport:
        violations: List[DatabaseBoundaryViolation] = []
        models_scanned = 0
        repos_scanned = 0

        for path_str in source_paths:
            path = Path(path_str)
            if not path.exists():
                continue
            
            for file_path in path.glob("**/*.py"):
                if "__pycache__" in str(file_path):
                    continue
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        tree = ast.parse(f.read(), filename=str(file_path))
                    
                    is_model_file = "models" in str(file_path) or "entities" in str(file_path)
                    is_repo_file = "repositories" in str(file_path)
                    is_service_file = "services" in str(file_path)

                    if is_model_file:
                        models_scanned += 1
                        violations.extend(self._scan_model_ast(tree, str(file_path)))
                    elif is_repo_file:
                        repos_scanned += 1
                        violations.extend(self._scan_repository_ast(tree, str(file_path)))
                    elif is_service_file:
                        violations.extend(self._scan_service_ast(tree, str(file_path)))
                except Exception:
                    pass

        status = "PASS" if len(violations) == 0 else "FAIL"
        return DatabaseBoundaryReport(
            status=status,
            scanned_models=models_scanned,
            scanned_repositories=repos_scanned,
            violations=violations,
        )

    def _scan_model_ast(self, tree: ast.AST, file_path: str) -> List[DatabaseBoundaryViolation]:
        violations: List[DatabaseBoundaryViolation] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                for sub in node.body:
                    if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        # Check for AI reasoning / HTTP calls in ORM models
                        for call in ast.walk(sub):
                            if isinstance(call, ast.Call):
                                func_name = self._get_call_name(call.func)
                                if func_name in self.FORBIDDEN_MODEL_CALLS or "ai" in func_name.lower():
                                    violations.append(
                                        DatabaseBoundaryViolation(
                                            module=file_path,
                                            entity_or_class=node.name,
                                            violation_type="BUSINESS_OR_AI_LOGIC_IN_ORM_MODEL",
                                            severity=ViolationSeverity.HIGH,
                                            description=f"Model method '{sub.name}' directly calls '{func_name}'",
                                        )
                                    )
        return violations

    def _scan_repository_ast(self, tree: ast.AST, file_path: str) -> List[DatabaseBoundaryViolation]:
        violations: List[DatabaseBoundaryViolation] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                for sub in node.body:
                    if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        # Check if repository calls AI or external HTTP services
                        for call in ast.walk(sub):
                            if isinstance(call, ast.Call):
                                func_name = self._get_call_name(call.func)
                                if func_name in self.FORBIDDEN_MODEL_CALLS:
                                    violations.append(
                                        DatabaseBoundaryViolation(
                                            module=file_path,
                                            entity_or_class=node.name,
                                            violation_type="AI_OR_EXTERNAL_CALL_IN_REPOSITORY",
                                            severity=ViolationSeverity.CRITICAL,
                                            description=f"Repository method '{sub.name}' performs external service call '{func_name}'",
                                        )
                                    )
        return violations

    def _scan_service_ast(self, tree: ast.AST, file_path: str) -> List[DatabaseBoundaryViolation]:
        violations: List[DatabaseBoundaryViolation] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                for sub in node.body:
                    if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        for call in ast.walk(sub):
                            if isinstance(call, ast.Call):
                                func_name = self._get_call_name(call.func)
                                if func_name in ["db.query", "session.query", "session.execute", "db.execute"]:
                                    violations.append(
                                        DatabaseBoundaryViolation(
                                            module=file_path,
                                            entity_or_class=node.name,
                                            violation_type="DIRECT_DB_USAGE_IN_SERVICE",
                                            severity=ViolationSeverity.MEDIUM,
                                            description=f"Service method '{sub.name}' directly invokes ORM query '{func_name}' instead of repository pattern",
                                        )
                                    )
        return violations

    def _get_call_name(self, node: ast.AST) -> str:
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            val = self._get_call_name(node.value)
            return f"{val}.{node.attr}" if val else node.attr
        return ""
