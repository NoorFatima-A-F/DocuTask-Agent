"""
Secret and Credential Scanner for Container Definitions.
"""
import re
from typing import List


class SecretScanner:
    """Scans Dockerfile instructions and environment definitions for embedded credentials."""

    SECRET_PATTERNS = [
        re.compile(r"(?:api_key|password|secret|token)\s*=\s*['\"][a-zA-Z0-9_@#$!%*?&]{6,}['\"]", re.IGNORECASE),
        re.compile(r"BEGIN (?:RSA|OPENSSH) PRIVATE KEY", re.IGNORECASE),
    ]

    def scan_secrets(self, text_snippets: List[str]) -> List[str]:
        found: List[str] = []
        for text in text_snippets:
            for pat in self.SECRET_PATTERNS:
                matches = pat.findall(text)
                if matches:
                    found.extend(matches)
        return found
