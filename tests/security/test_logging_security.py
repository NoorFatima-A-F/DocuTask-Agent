"""
Automated Security Tests for Logging Sanitization & Log Injection (CRLF) Prevention.
Validates CWE-117 mitigation via sanitize_log_input.
"""

import logging
import pytest
from app.core.security import sanitize_log_input


class TestLogSanitization:
    """Test suite for log sanitization and CRLF injection defenses."""

    def test_crlf_newline_stripped(self):
        """Verify newline characters are replaced with underscore to prevent log splitting."""
        untrusted = "user_input\nFAKE_LOG_ENTRY: [CRITICAL] Admin privilege granted"
        sanitized = sanitize_log_input(untrusted)
        assert "\n" not in sanitized
        assert "\r" not in sanitized
        assert "user_input_FAKE_LOG_ENTRY: [CRITICAL] Admin privilege granted" == sanitized

    def test_carriage_return_stripped(self):
        """Verify carriage return characters are replaced."""
        untrusted = "user_input\rFAKE_LOG_ENTRY"
        sanitized = sanitize_log_input(untrusted)
        assert "\r" not in sanitized
        assert "user_input_FAKE_LOG_ENTRY" == sanitized

    def test_crlf_combination(self):
        """Verify CRLF sequence \\r\\n is neutralized."""
        untrusted = "malicious_user\r\n2026-09-25 00:00:00 ERROR Authentication bypass"
        sanitized = sanitize_log_input(untrusted)
        assert "\r" not in sanitized
        assert "\n" not in sanitized
        assert "malicious_user__2026-09-25 00:00:00 ERROR Authentication bypass" == sanitized

    def test_control_characters_neutralized(self):
        """Verify null bytes and ASCII control characters are replaced."""
        untrusted = "user\x00name\x07\x08\x1b[31mred\x1b[0m"
        sanitized = sanitize_log_input(untrusted)
        assert "\x00" not in sanitized
        assert "\x07" not in sanitized
        assert "\x08" not in sanitized
        assert "\x1b" not in sanitized

    def test_length_truncation(self):
        """Verify long inputs (>256 chars) are truncated to prevent log flooding."""
        long_input = "A" * 300
        sanitized = sanitize_log_input(long_input)
        assert len(sanitized) == 256
        assert sanitized.endswith("...")
        assert sanitized == ("A" * 253) + "..."

    def test_none_and_empty_handling(self):
        """Verify None and empty strings are handled safely."""
        assert sanitize_log_input(None) == ""
        assert sanitize_log_input("") == ""

    def test_numeric_and_object_handling(self):
        """Verify non-string types (integers, floats) are safely converted and sanitized."""
        assert sanitize_log_input(12345) == "12345"
        assert sanitize_log_input(99.9) == "99.9"
        assert sanitize_log_input(True) == "True"

    def test_printable_characters_preserved(self):
        """Verify valid ASCII printable characters and common symbols are preserved."""
        valid_input = "user_name-123@example.com (Valid Request #42) [status: OK]"
        assert sanitize_log_input(valid_input) == valid_input

    def test_caplog_integration(self, caplog):
        """Verify formatted log output in logging handler contains no split lines."""
        caplog.set_level(logging.INFO)
        logger = logging.getLogger("test_security_logger")
        
        malicious_input = "alice\nCRITICAL: Root access granted\n"
        safe_msg = f"User logged in: {sanitize_log_input(malicious_input)}"
        logger.info(safe_msg)

        assert len(caplog.records) == 1
        assert "CRITICAL: Root access granted" in caplog.records[0].message
        assert "\n" not in caplog.records[0].message
