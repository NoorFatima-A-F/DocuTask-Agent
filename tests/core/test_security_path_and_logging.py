"""Unit and regression tests for safe path resolution and log sanitization primitives."""

import os
from pathlib import Path
import pytest
from app.core.security import (
    resolve_safe_path,
    validate_safe_filename_segment,
    sanitize_log_input,
    UnsafePathError,
)


class TestSafePathResolution:
    def test_resolve_safe_path_valid_subpath(self, tmp_path: Path):
        base = tmp_path / "safe_base"
        base.mkdir()
        target = resolve_safe_path(base, "reports/audit.json")
        assert target.is_relative_to(base.resolve())
        assert target.name == "audit.json"

    def test_resolve_safe_path_exact_base(self, tmp_path: Path):
        base = tmp_path / "safe_base"
        base.mkdir()
        target = resolve_safe_path(base, ".", allow_base=True)
        assert target == base.resolve()

    def test_resolve_safe_path_blocks_directory_traversal(self, tmp_path: Path):
        base = tmp_path / "safe_base"
        base.mkdir()
        with pytest.raises(UnsafePathError):
            resolve_safe_path(base, "../escaped.txt")

    def test_resolve_safe_path_blocks_nested_traversal(self, tmp_path: Path):
        base = tmp_path / "safe_base"
        base.mkdir()
        with pytest.raises(UnsafePathError):
            resolve_safe_path(base, "sub/../../outside.json")

    def test_resolve_safe_path_blocks_absolute_escape(self, tmp_path: Path):
        base = tmp_path / "safe_base"
        base.mkdir()
        outside_abs = (tmp_path / "outside_file.txt").resolve()
        with pytest.raises(UnsafePathError):
            resolve_safe_path(base, str(outside_abs))


class TestSafeFilenameValidation:
    def test_valid_filename_segments(self):
        assert validate_safe_filename_segment("audit_report_2026") == "audit_report_2026"
        assert validate_safe_filename_segment("SIM-RUN-A1B2C3D4") == "SIM-RUN-A1B2C3D4"
        assert validate_safe_filename_segment("report.json") == "report.json"

    def test_rejects_path_traversal_characters(self):
        with pytest.raises(UnsafePathError):
            validate_safe_filename_segment("../malicious")
        with pytest.raises(UnsafePathError):
            validate_safe_filename_segment("sub/file.json")
        with pytest.raises(UnsafePathError):
            validate_safe_filename_segment("sub\\file.json")
        with pytest.raises(UnsafePathError):
            validate_safe_filename_segment("null\x00byte")

    def test_rejects_empty_or_whitespace(self):
        with pytest.raises(UnsafePathError):
            validate_safe_filename_segment("")
        with pytest.raises(UnsafePathError):
            validate_safe_filename_segment("   ")


class TestLogSanitization:
    def test_sanitize_normal_text(self):
        assert sanitize_log_input("User logged in successfully") == "User logged in successfully"

    def test_sanitize_removes_newlines_and_crs(self):
        malicious_input = "Admin login\nHTTP/1.1 200 OK\r\nInjected-Header: true"
        cleaned = sanitize_log_input(malicious_input)
        assert "\n" not in cleaned
        assert "\r" not in cleaned
        assert "Injected-Header" in cleaned

    def test_sanitize_handles_none_and_non_strings(self):
        assert sanitize_log_input(None) == ""
        assert sanitize_log_input(12345) == "12345"

    def test_sanitize_truncates_overly_long_strings(self):
        long_str = "A" * 500
        cleaned = sanitize_log_input(long_str)
        assert len(cleaned) <= 256
        assert cleaned.endswith("...")
