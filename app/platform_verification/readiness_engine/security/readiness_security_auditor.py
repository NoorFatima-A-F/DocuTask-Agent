"""
Readiness Security Auditor (Part 3H.3.2.11).
Audits readiness payloads to guarantee zero leakage of internal database hostnames,
credentials, connection strings, stack traces, and internal IP addresses.
"""
import re
from typing import Dict, Any
from app.platform_verification.readiness_engine.domain.models import (
    ReadinessSecurityReport,
)


class ReadinessSecurityAuditor:
    """
    Scans readiness responses for forbidden sensitive tokens and network topology exposure.
    """

    FORBIDDEN_PATTERNS = {
        "db_host": r"(database_host|db_server|postgres_host)",
        "password_token": r"(password|secret|api_key|access_token|private_key)",
        "connection_string": r"(postgresql:\/\/|redis:\/\/|mongodb:\/\/|amqp:\/\/)",
        "stack_trace": r"(Traceback \(most recent call last\)|File \".*\", line \d+)",
        "internal_ip": r"(\b10\.\d{1,3}\.\d{1,3}\.\d{1,3}\b|\b192\.168\.\d{1,3}\.\d{1,3}\b|\b172\.(1[6-9]|2[0-9]|3[0-1])\.\d{1,3}\.\d{1,3}\b)",
    }

    def __init__(self):
        self._compiled = {
            k: re.compile(v, re.IGNORECASE) for k, v in self.FORBIDDEN_PATTERNS.items()
        }

    def audit_security(self, payload: Dict[str, Any]) -> ReadinessSecurityReport:
        payload_str = str(payload)

        no_db_host = not bool(self._compiled["db_host"].search(payload_str))
        no_password = not bool(self._compiled["password_token"].search(payload_str))
        no_conn_str = not bool(self._compiled["connection_string"].search(payload_str))
        no_stack_trace = not bool(self._compiled["stack_trace"].search(payload_str))
        no_internal_ip = not bool(self._compiled["internal_ip"].search(payload_str))

        leaks = 0
        if not no_db_host: leaks += 1
        if not no_password: leaks += 1
        if not no_conn_str: leaks += 1
        if not no_stack_trace: leaks += 1
        if not no_internal_ip: leaks += 1

        passed = (leaks == 0)

        return ReadinessSecurityReport(
            no_database_host_leak=no_db_host,
            no_password_or_token_leak=no_password,
            no_connection_string_leak=no_conn_str,
            no_stack_trace_leak=no_stack_trace,
            no_internal_ip_leak=no_internal_ip,
            total_leaks_detected=leaks,
            passed=passed,
            details={
                "allowed_keys": list(payload.keys()) if isinstance(payload, dict) else [],
                "security_status": "ZERO_LEAKS_VERIFIED" if passed else "SECURITY_LEAK_DETECTED",
            },
        )
