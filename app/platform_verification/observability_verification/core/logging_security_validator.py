"""
Structured Logging and PII / Secret Leak Validator.
"""
import re
import json
from typing import List, Dict, Any
from app.platform_verification.observability_verification.domain.models import LoggingQualityReport
from app.platform_verification.observability_verification.domain.interfaces import ILoggingSecurityValidator


class LoggingSecurityValidator(ILoggingSecurityValidator):
    """Validates structured JSON schema logging and detects credential/PII leaks."""

    REQUIRED_FIELDS = {"timestamp", "service", "severity", "request_id", "trace_id", "tenant_id", "event"}

    SECRET_PATTERNS = [
        re.compile(r"""password\s*[:=]\s*['"][^'"]+['"]""", re.IGNORECASE),
        re.compile(r"bearer\s+[a-zA-Z0-9_\-\.]{20,}", re.IGNORECASE),
        re.compile(r"""api_key\s*[:=]\s*['"][^'"]+['"]""", re.IGNORECASE),
    ]

    def validate_logging(self, log_samples: List[Dict[str, Any]]) -> LoggingQualityReport:
        missing_fields = False
        leaks: List[str] = []

        for log in log_samples:
            # Check required fields
            for req in self.REQUIRED_FIELDS:
                if req not in log:
                    missing_fields = True

            # Check leaks in stringified log
            log_str = json.dumps(log)
            for pat in self.SECRET_PATTERNS:
                matches = pat.findall(log_str)
                if matches:
                    leaks.extend(matches)

        score = 100.0
        if missing_fields:
            score -= 30.0
        if leaks:
            score -= (len(leaks) * 25.0)

        score = max(0.0, min(100.0, score))
        status = "PASS" if not missing_fields and len(leaks) == 0 else "FAIL"

        return LoggingQualityReport(
            structured_json_compliant=True,
            required_fields_present=(not missing_fields),
            sensitive_data_leaks_detected=leaks,
            logging_quality_score=score,
            status=status,
        )
