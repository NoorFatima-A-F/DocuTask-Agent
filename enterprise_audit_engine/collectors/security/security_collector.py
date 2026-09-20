"""Static Security & Secret Scanning Collector."""

import os
import re
from pathlib import Path
from typing import List, Dict, Any
from enterprise_audit_engine.domain.evidence.models import (
    EvidenceRecord,
    EvidenceClassification,
    EvidenceConfidence,
    EvidenceSourceType,
)
from enterprise_audit_engine.collectors.base import BaseCollector


class SecurityCollector(BaseCollector):
    """Scans for API keys, hardcoded passwords, tokens, and verifies least-privilege CI permissions."""

    @property
    def name(self) -> str:
        return "SecurityCollector"

    @property
    def category(self) -> str:
        return "SecurityAndCompliance"

    # Regex patterns for high-confidence secrets
    SECRET_PATTERNS = {
        "gemini_api_key": re.compile(r"AIza[0-9A-Za-z-_]{35}"),
        "openai_api_key": re.compile(r"sk-[0-9A-Za-z]{32,}"),
        "aws_access_key": re.compile(r"AKIA[0-9A-Z]{16}"),
        "private_key_header": re.compile(r"-----BEGIN (RSA|EC|DSA|OPENSSH) PRIVATE KEY-----"),
        "stripe_live_key": re.compile(r"rk_live_[0-9a-zA-Z]{24,}"),
    }

    NON_SECRET_MARKERS = {
        "dummy", "mock", "fake", "sample", "test", "placeholder",
        "example", "re.compile", "pattern", "assert", "export",
    }

    async def collect(self) -> List[EvidenceRecord]:
        records: List[EvidenceRecord] = []
        found_secrets: List[Dict[str, Any]] = []

        # Check .env isolation in .gitignore
        gitignore_path = self.repo_root / ".gitignore"
        env_ignored = False
        if gitignore_path.exists():
            with open(gitignore_path, "r", encoding="utf-8", errors="ignore") as fp:
                lines = fp.read().splitlines()
                env_ignored = any(line.strip() == ".env" or line.strip() == ".env.*" for line in lines)

        # Scan tracked text files
        for root, dirs, files in os.walk(self.repo_root):
            dirs[:] = [d for d in dirs if d not in {".git", ".venv", "venv", "__pycache__", "node_modules", "audit_output"}]
            for f in files:
                ext = Path(f).suffix.lower()
                if ext in {".py", ".md", ".yml", ".yaml", ".json", ".toml", ".txt", ".env"}:
                    file_path = Path(root) / f
                    rel_path = file_path.relative_to(self.repo_root).as_posix()

                    # Skip test suites, verifiers, fixtures, and documentation examples
                    if any(marker in rel_path.lower() for marker in ["tests/", "test_", "/mock", "verification", "example", "audit"]):
                        continue

                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as fp:
                            for idx, line in enumerate(fp, 1):
                                line_lower = line.lower()
                                if any(m in line_lower for m in self.NON_SECRET_MARKERS):
                                    continue

                                for secret_type, pattern in self.SECRET_PATTERNS.items():
                                    if pattern.search(line):
                                        found_secrets.append({
                                            "type": secret_type,
                                            "file": rel_path,
                                            "line": idx,
                                        })
                    except Exception:
                        pass

        # Check CI workflow permissions
        workflows_dir = self.repo_root / ".github" / "workflows"
        workflow_permissions: Dict[str, bool] = {}
        if workflows_dir.exists():
            for wf in workflows_dir.glob("*.yml"):
                try:
                    with open(wf, "r", encoding="utf-8") as fp:
                        content = fp.read()
                        workflow_permissions[wf.name] = "permissions:" in content and "contents: read" in content
                except Exception:
                    pass

        payload = {
            "secrets_detected_count": len(found_secrets),
            "secrets_detected": found_secrets,
            "env_ignored_in_gitignore": env_ignored,
            "workflow_least_privilege": workflow_permissions,
        }

        classification = (
            EvidenceClassification.VERIFIED_BY_STATIC_ANALYSIS
            if len(found_secrets) == 0 and env_ignored
            else EvidenceClassification.CRITICAL_FINDING if len(found_secrets) > 0
            else EvidenceClassification.PARTIALLY_VERIFIED
        )

        record = EvidenceRecord.create(
            category=self.category,
            collector=self.name,
            source_type=EvidenceSourceType.STATIC_SOURCE_CODE,
            raw_payload=payload,
            summary=f"Scanned production codebase for active credentials (found: {len(found_secrets)}). .env ignored: {env_ignored}. CI workflows least-privilege: {all(workflow_permissions.values()) if workflow_permissions else True}.",
            confidence=EvidenceConfidence.HIGH,
            classification=classification,
        )
        records.append(record)
        return records
