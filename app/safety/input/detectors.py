"""Malicious Pattern & Command Injection Detectors for Natural Language Inputs."""

import re
from typing import List, Tuple
from ..gateway.decision import SafetyCategory, ViolationSeverity, SafetyViolation


class MaliciousPatternDetector:
    """Detects system sabotage, shell execution strings, and malicious natural language exploit patterns."""

    # Shell commands, destructive instructions & binary exploits embedded in text
    DANGEROUS_PATTERNS = [
        (r"(?i)\b(rm\s+-rf\s+[/~]|del\s+/[fF]\s+/[sS]|format\s+[c-z]:)", "System file destruction attempt", ViolationSeverity.CRITICAL),
        (r"(?i)\b(drop\s+database\b|drop\s+table\b|truncate\s+table\b|delete\s+from\s+\w+\s*;)", "Unconstrained SQL destruction", ViolationSeverity.CRITICAL),
        (r"(?i)(<\s*script\b[^>]*>.*?</\s*script\s*>|javascript:\s*alert)", "Cross-site scripting payload", ViolationSeverity.HIGH),
        (r"(?i)(exec\s*\(\s*compile|eval\s*\(\s*|__import__\s*\(\s*['\"]os['\"]\)|subprocess\.Popen)", "Arbitrary code execution primitive", ViolationSeverity.CRITICAL),
        (r"(?i)(/bin/(sh|bash|zsh|dash)|cmd\.exe|powershell(\.exe)?\s+-enc)", "Direct shell invocation payload", ViolationSeverity.HIGH),
        (r"(?i)\b(curl|wget)\s+https?://[^\s]+\s*\|\s*(sh|bash)", "Remote script execution pipeline", ViolationSeverity.CRITICAL),
    ]

    def scan(self, text: str) -> List[SafetyViolation]:
        violations: List[SafetyViolation] = []
        if not text:
            return violations

        for pattern, desc, severity in self.DANGEROUS_PATTERNS:
            match = re.search(pattern, text)
            if match:
                violations.append(
                    SafetyViolation(
                        category=SafetyCategory.MALICIOUS_INPUT,
                        severity=severity,
                        message=desc,
                        location="input",
                        rule_id="MAL-PAT-001",
                        evidence=match.group(0)[:100],
                    )
                )
        return violations


class CommandInjectionDetector:
    """Specialized detector for prompt-embedded shell/SQL command injections."""

    def __init__(self):
        self.pattern_detector = MaliciousPatternDetector()

    def check(self, text: str) -> Tuple[bool, List[SafetyViolation]]:
        violations = self.pattern_detector.scan(text)
        return len(violations) > 0, violations
