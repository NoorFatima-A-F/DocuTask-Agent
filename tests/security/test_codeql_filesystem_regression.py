"""
CodeQL Filesystem Security Regression Test Suite.
Validates that sanitize_file_path() and resolve_safe_path() defend against
all CWE-22 Path Traversal and injection attack vectors.
"""

import os
from pathlib import Path
import pytest
from app.core.security import (
    sanitize_file_path,
    resolve_safe_path,
    UnsafePathError,
)


class TestCodeQLFilesystemRegression:
    """Enterprise regression test suite for CodeQL path injection defenses."""

    @pytest.fixture
    def base_dir(self, tmp_path):
        """Creates a dedicated base directory for isolation testing."""
        base = tmp_path / "sandbox_base"
        base.mkdir(parents=True, exist_ok=True)
        return str(base)

    def test_1_normal_path_pass(self, base_dir):
        """1. Normal path: reports/report.json -> PASS"""
        safe_str = sanitize_file_path(base_dir, "reports/report.json")
        expected = os.path.abspath(os.path.join(base_dir, "reports", "report.json"))
        assert safe_str == expected
        assert os.path.commonpath([base_dir, safe_str]) == os.path.abspath(base_dir)

        safe_path = resolve_safe_path(base_dir, "reports/report.json")
        assert safe_path == Path(expected)
        assert safe_path.is_relative_to(Path(base_dir).resolve())

    def test_2_parent_traversal_block(self, base_dir):
        """2. Parent traversal: ../../etc/passwd -> BLOCK"""
        with pytest.raises(UnsafePathError) as exc_info:
            sanitize_file_path(base_dir, "../../etc/passwd")
        assert "escapes trusted base directory" in str(exc_info.value)

        with pytest.raises(UnsafePathError):
            resolve_safe_path(base_dir, "../../etc/passwd")

    def test_3_windows_traversal_block(self, base_dir):
        """3. Windows traversal: ..\\..\\Windows\\system32 -> BLOCK"""
        with pytest.raises(UnsafePathError) as exc_info:
            sanitize_file_path(base_dir, r"..\..\Windows\system32")
        assert "escapes trusted base directory" in str(exc_info.value)

        with pytest.raises(UnsafePathError):
            resolve_safe_path(base_dir, r"..\..\Windows\system32")

    def test_4_absolute_path_block(self, base_dir):
        """4. Absolute path: /etc/passwd -> BLOCK"""
        with pytest.raises(UnsafePathError) as exc_info:
            sanitize_file_path(base_dir, "/etc/passwd")
        assert "escapes trusted base directory" in str(exc_info.value)

        with pytest.raises(UnsafePathError):
            sanitize_file_path(base_dir, "C:\\Windows\\system32\\calc.exe")

        with pytest.raises(UnsafePathError):
            resolve_safe_path(base_dir, "/etc/passwd")

    def test_5_prefix_collision_block(self, tmp_path):
        """5. Prefix collision: /safe/export_evil -> BLOCK"""
        base = tmp_path / "export"
        base.mkdir()
        evil_sibling = tmp_path / "export_evil"
        evil_sibling.mkdir()

        # Attempting to access sibling directory via traversal
        with pytest.raises(UnsafePathError) as exc_info:
            sanitize_file_path(str(base), "../export_evil/payload.sh")
        assert "escapes trusted base directory" in str(exc_info.value)

    def test_6_null_byte_block(self, base_dir):
        """6. Null byte: file.txt\\x00.exe -> BLOCK"""
        with pytest.raises(UnsafePathError) as exc_info:
            sanitize_file_path(base_dir, "file.txt\x00.exe")
        assert "Null byte detected" in str(exc_info.value)

        with pytest.raises(UnsafePathError) as exc_info:
            resolve_safe_path(base_dir, "file.txt\x00.exe")
        assert "Null byte detected" in str(exc_info.value)

    def test_7_empty_path_block(self, base_dir):
        """7. Empty path: '' / None / whitespace -> BLOCK"""
        with pytest.raises(UnsafePathError) as exc_info1:
            sanitize_file_path(base_dir, "")
        assert "Empty path provided" in str(exc_info1.value)

        with pytest.raises(UnsafePathError) as exc_info2:
            sanitize_file_path(base_dir, "    ")
        assert "Empty path provided" in str(exc_info2.value)

        with pytest.raises(UnsafePathError) as exc_info3:
            sanitize_file_path(base_dir, None)  # type: ignore
        assert "Empty or None path provided" in str(exc_info3.value)
