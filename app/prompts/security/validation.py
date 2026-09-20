"""Prompt Security & Safety Policy Validator (Phase 8D).

Performs composite static and dynamic security scanning across injection, leakage, and safety policies.
"""

from __future__ import annotations

from typing import List, Tuple
from app.prompts.security.injection import PromptInjectionScanner
from app.prompts.security.leakage import PromptLeakageScanner


class PromptSecurityValidator:
    """Unified security verification engine for enterprise prompt assets."""

    @classmethod
    def validate_security(cls, template_text: str) -> Tuple[bool, List[str]]:
        """Validate template against prompt injection and secret leakage policies."""
        violations: List[str] = []

        # 1. Injection scan
        inj_res = PromptInjectionScanner.scan_template(template_text)
        if not inj_res.is_safe:
            violations.extend([f"Prompt Injection Risk: {p}" for p in inj_res.flagged_patterns])

        # 2. Leakage scan
        leak_res = PromptLeakageScanner.scan_template(template_text)
        if not leak_res.is_safe:
            violations.extend([f"Secret Leakage Detected: {s}" for s in leak_res.detected_secret_types])

        is_passed = len(violations) == 0
        return is_passed, violations
