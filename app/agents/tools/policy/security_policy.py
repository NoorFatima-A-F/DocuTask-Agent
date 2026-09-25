"""
Security Policy for Advanced Tool Policy Engine.
Enforces execution boundaries, payload size limits, sandbox constraints, and system protection.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set

logger = logging.getLogger(__name__)


@dataclass
class SecurityValidationResult:
    """Security check outcome."""

    is_allowed: bool
    violations: List[str] = field(default_factory=list)
    risk_level: str = "LOW"


class SecurityPolicy:
    """Enforces sandbox integrity and resource constraints on tool invocations."""

    FORBIDDEN_OPERATIONS: Set[str] = {
        "os_system",
        "subprocess_exec",
        "shell_eval",
        "format_drive",
        "rm_rf",
        "modify_system_binaries",
    }

    def __init__(
        self,
        max_payload_bytes: int = 10 * 1024 * 1024,  # 10 MB
        max_execution_seconds: float = 60.0,
        disallowed_tools: Optional[Set[str]] = None,
    ) -> None:
        self.max_payload_bytes = max_payload_bytes
        self.max_execution_seconds = max_execution_seconds
        self.disallowed_tools = disallowed_tools or self.FORBIDDEN_OPERATIONS

    def validate(
        self,
        tool_name: str,
        input_payload: Dict[str, Any],
        is_sandboxed: bool = True,
    ) -> SecurityValidationResult:
        """Evaluates whether a tool invocation conforms to security boundaries."""
        violations: List[str] = []

        # 1. Forbidden tools
        if tool_name.lower() in {t.lower() for t in self.disallowed_tools}:
            violations.append(f"Tool '{tool_name}' is explicitly forbidden under platform security policy.")

        # 2. Payload size check
        payload_str = str(input_payload)
        payload_size = len(payload_str.encode("utf-8"))
        if payload_size > self.max_payload_bytes:
            violations.append(
                f"Payload size ({payload_size} bytes) exceeds maximum limit of {self.max_payload_bytes} bytes."
            )

        # 3. Dangerous input command injection inspection
        dangerous_patterns = ["; rm ", "&& rm", "| cat", "| rm", "; drop table", "__import__", "eval(", "`whoami`", "$(whoami)", "; rm -rf"]
        for k, v in input_payload.items():
            val_str = str(v).lower()
            if any(cmd.lower() in val_str for cmd in dangerous_patterns):
                violations.append(f"Potential injection detected in argument '{k}'.")

        is_allowed = len(violations) == 0
        risk_level = "HIGH" if violations else "LOW"

        if not is_allowed:
            logger.warning("Security policy blocked tool '%s': %s", tool_name, "; ".join(violations))

        return SecurityValidationResult(
            is_allowed=is_allowed,
            violations=violations,
            risk_level=risk_level,
        )
