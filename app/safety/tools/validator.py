"""Tool Safety Validator for Parameters, Paths, and Command Injections."""

import re
from typing import Dict, Any, List, Tuple
from ..gateway.decision import SafetyCategory, ViolationSeverity, SafetyViolation
from .permissions import ToolPermissionManager, ToolDangerLevel


class ToolSafetyValidator:
    """Validates tool invocation safety before actual execution."""

    DANGEROUS_PARAM_PATTERNS = [
        (r"(?i)\b(rm\s+-rf|format\s+[c-z]:|del\s+/[fF])\b", "Destructive system deletion command", ViolationSeverity.CRITICAL),
        (r"(\.\./\.\./|\.\.\\\.\.\\)", "Path traversal directory escape attempt", ViolationSeverity.HIGH),
        (r"(?i)\b(DROP\s+TABLE|DROP\s+DATABASE|TRUNCATE\s+TABLE)\b", "Destructive SQL DDL command", ViolationSeverity.CRITICAL),
        (r"(?i)\b(GRANT\s+ALL|ALTER\s+USER\s+.*SUPERUSER)\b", "Privilege escalation attempt in database", ViolationSeverity.CRITICAL),
    ]

    def __init__(self, permission_manager: ToolPermissionManager = None):
        self.permission_manager = permission_manager or ToolPermissionManager()

    def validate_tool_invocation(
        self,
        tool_name: str,
        parameters: Dict[str, Any],
        user_role: str = "user",
        is_dry_run: bool = False,
    ) -> Tuple[bool, List[SafetyViolation]]:
        violations: List[SafetyViolation] = []

        # 1. Check permissions
        policy = self.permission_manager.get_tool_policy(tool_name)
        if not self.permission_manager.can_invoke(tool_name, user_role, is_dry_run):
            violations.append(
                SafetyViolation(
                    category=SafetyCategory.UNAUTHORIZED_TOOL,
                    severity=ViolationSeverity.HIGH,
                    message=f"Role '{user_role}' is not authorized to execute tool '{tool_name}'",
                    location=f"tool:{tool_name}",
                    rule_id="TOOL-PERM-001",
                    details={"tool_name": tool_name, "required_roles": policy.allowed_roles},
                )
            )

        # 2. Check danger level vs human approval
        if policy.danger_level == ToolDangerLevel.DESTRUCTIVE_HIGH_RISK and policy.requires_human_approval and not is_dry_run:
            violations.append(
                SafetyViolation(
                    category=SafetyCategory.DESTRUCTIVE_TOOL,
                    severity=ViolationSeverity.CRITICAL,
                    message=f"Destructive tool '{tool_name}' requires human approval before execution",
                    location=f"tool:{tool_name}",
                    rule_id="TOOL-HUMAN-001",
                    details={"tool_name": tool_name, "danger_level": policy.danger_level.value},
                )
            )

        # 3. Check parameters for dangerous payloads / traversal
        param_str = str(parameters)
        for pattern, desc, severity in self.DANGEROUS_PARAM_PATTERNS:
            if re.search(pattern, param_str):
                violations.append(
                    SafetyViolation(
                        category=SafetyCategory.DESTRUCTIVE_TOOL,
                        severity=severity,
                        message=f"Dangerous payload in parameters of tool '{tool_name}': {desc}",
                        location=f"tool:{tool_name}",
                        rule_id="TOOL-PAYLOAD-001",
                        evidence=param_str[:120],
                    )
                )

        is_safe = len([v for v in violations if v.severity in [ViolationSeverity.HIGH, ViolationSeverity.CRITICAL]]) == 0
        return is_safe, violations
