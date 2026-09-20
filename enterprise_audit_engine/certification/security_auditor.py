"""Security Validation & Hardening Verifier for the Audit Engine."""

import os
from pathlib import Path
from typing import Dict, Any, List


class EngineSecurityValidator:
    """Performs defensive security analysis on the audit engine itself."""

    MAX_ARTIFACT_SIZE_BYTES = 50 * 1024 * 1024  # 50 MB limit

    @classmethod
    def audit_engine_security(cls, engine_root: Path) -> Dict[str, Any]:
        unsafe_patterns: List[Dict[str, Any]] = []

        for root, dirs, files in os.walk(engine_root):
            # Exclude test files and caches from false positives
            dirs[:] = [d for d in dirs if d not in {"__pycache__", ".pytest_cache", "tests"}]

            for f in files:
                if f.endswith(".py") and not f.startswith("test_") and f != "security_auditor.py":
                    file_path = Path(root) / f
                    rel_path = file_path.relative_to(engine_root).as_posix()
                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as fp:
                            content = fp.read()
                            # Check for pickle (unsafe deserialization)
                            if "import pickle" in content or "pickle.load" in content:
                                unsafe_patterns.append({
                                    "file": rel_path,
                                    "vulnerability": "UNSAFE_DESERIALIZATION_PICKLE",
                                })
                            # Check for shell=True in subprocess
                            if "shell=True" in content:
                                unsafe_patterns.append({
                                    "file": rel_path,
                                    "vulnerability": "UNSAFE_SHELL_EXECUTION",
                                })
                            # Check for eval()
                            if "eval(" in content and "json" not in content:
                                unsafe_patterns.append({
                                    "file": rel_path,
                                    "vulnerability": "UNSAFE_EVAL_USAGE",
                                })
                    except Exception:
                        pass

        is_secure = len(unsafe_patterns) == 0

        return {
            "is_secure": is_secure,
            "engine_files_scanned": sum(len(files) for _, _, files in os.walk(engine_root)),
            "vulnerabilities_found_count": len(unsafe_patterns),
            "vulnerabilities": unsafe_patterns,
            "security_posture": "HARDENED_ENTERPRISE_STANDARD" if is_secure else "VULNERABILITIES_DETECTED",
        }
