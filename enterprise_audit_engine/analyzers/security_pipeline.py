"""Security Pipeline & Vulnerability Verifier."""

import os
import re
from pathlib import Path
from typing import Dict, Any, List


class SecurityPipelineVerifier:
    """Verifies security controls, secret hygiene, auth mechanisms, and vulnerability scanners."""

    SECRET_PATTERNS = [
        (r"(?i)api[_-]?key\s*=\s*['\"][A-Za-z0-9_\-]{20,}['\"]", "High-entropy API Key"),
        (r"(?i)password\s*=\s*['\"][^'\"]{8,}['\"]", "Hardcoded Password"),
        (r"(?i)secret[_-]?key\s*=\s*['\"][A-Za-z0-9_\-]{16,}['\"]", "Hardcoded Secret Key"),
        (r"ghp_[A-Za-z0-9]{36}", "GitHub Personal Access Token"),
        (r"sk-[A-Za-z0-9]{32,}", "OpenAI Secret Key"),
        (r"AIza[0-9A-Za-z-_]{35}", "Google API Key"),
    ]

    @classmethod
    def scan_security_posture(cls, repo_root: Path) -> Dict[str, Any]:
        secrets_found: List[Dict[str, str]] = []
        has_auth = False
        has_rate_limiting = False
        has_cors_protection = False
        has_sql_injection_guard = True
        has_security_policy = (repo_root / "SECURITY.md").exists() or (repo_root / ".github" / "SECURITY.md").exists()
        has_dependabot = (repo_root / ".github" / "dependabot.yml").exists()

        ignore_dirs = {".git", ".venv", "venv", "node_modules", "audit_output", ".pytest_cache", "__pycache__"}

        for root, dirs, files in os.walk(repo_root):
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            for f in files:
                if f.endswith((".py", ".env", ".json", ".yaml", ".yml", ".ts", ".tsx", ".js")):
                    file_path = Path(root) / f
                    # Skip .env.example / .sample
                    if ".example" in f or ".sample" in f or "test" in root.lower():
                        continue
                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as fp:
                            content = fp.read()
                            rel_path = str(file_path.relative_to(repo_root))

                            # Secret check
                            for pattern, desc in cls.SECRET_PATTERNS:
                                if re.search(pattern, content):
                                    secrets_found.append({
                                        "file": rel_path,
                                        "type": desc,
                                    })

                            lower_content = content.lower()
                            if "jwt" in lower_content or "oauth" in lower_content or "get_current_user" in lower_content:
                                has_auth = True
                            if "limiter" in lower_content or "ratelimit" in lower_content or "slowapi" in lower_content:
                                has_rate_limiting = True
                            if "corsmiddleware" in lower_content or "allow_origins" in lower_content:
                                has_cors_protection = True
                            if "execute(" in lower_content and "%s" not in lower_content and "f\"select" in lower_content:
                                has_sql_injection_guard = False
                    except Exception:
                        pass

        security_score = 0.0
        if not secrets_found:
            security_score += 30.0
        if has_auth:
            security_score += 25.0
        if has_rate_limiting:
            security_score += 15.0
        if has_cors_protection:
            security_score += 10.0
        if has_security_policy:
            security_score += 10.0
        if has_dependabot:
            security_score += 10.0

        risk_level = "CRITICAL" if secrets_found else "HIGH" if security_score < 50.0 else "MEDIUM" if security_score < 80.0 else "LOW"

        return {
            "secrets_detected_count": len(secrets_found),
            "secrets_detected": secrets_found[:5],
            "has_auth": has_auth,
            "has_rate_limiting": has_rate_limiting,
            "has_cors_protection": has_cors_protection,
            "has_sql_injection_guard": has_sql_injection_guard,
            "has_security_policy": has_security_policy,
            "has_dependabot": has_dependabot,
            "security_score": security_score,
            "risk_level": risk_level,
        }
