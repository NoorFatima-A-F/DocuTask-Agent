"""
Automated CodeQL-Aligned Path Traversal (CWE-22) Security Test Suite.
Tests both sanitize_file_path() (str) and resolve_safe_path() (Path).
"""

import os
from pathlib import Path
import pytest
from app.core.security import (
    sanitize_file_path,
    resolve_safe_path,
    validate_safe_filename_segment,
    UnsafePathError,
)


class TestPathSecurity:
    """Rigorous path injection and traversal security verification suite."""

    @pytest.fixture
    def base_dir(self, tmp_path):
        """Creates a dedicated trusted base directory fixture."""
        d = tmp_path / "trusted_base"
        d.mkdir(parents=True, exist_ok=True)
        return str(d)

    def test_normal_file_pass(self, base_dir):
        """Verify standard relative file path inside base directory passes."""
        safe = sanitize_file_path(base_dir, "invoice.pdf")
        assert safe == os.path.abspath(os.path.join(base_dir, "invoice.pdf"))
        assert os.path.commonpath([base_dir, safe]) == os.path.abspath(base_dir)

        safe_path = resolve_safe_path(base_dir, "invoice.pdf")
        assert safe_path == Path(base_dir) / "invoice.pdf"

    def test_subfolder_normal_pass(self, base_dir):
        """Verify nested subfolder paths inside base directory pass."""
        safe = sanitize_file_path(base_dir, "sub/dir/report.json")
        assert safe == os.path.abspath(os.path.join(base_dir, "sub", "dir", "report.json"))

    def test_parent_traversal_block(self, base_dir):
        """Verify ../ directory escape attempts are blocked."""
        with pytest.raises(UnsafePathError):
            sanitize_file_path(base_dir, "../../etc/passwd")

        with pytest.raises(UnsafePathError):
            resolve_safe_path(base_dir, "../../etc/passwd")

    def test_windows_traversal_block(self, base_dir):
        """Verify ..\\ Windows style directory escape attempts are blocked."""
        with pytest.raises(UnsafePathError):
            sanitize_file_path(base_dir, r"..\..\Windows\system32\cmd.exe")

        with pytest.raises(UnsafePathError):
            resolve_safe_path(base_dir, r"..\..\Windows\system32\cmd.exe")

    def test_absolute_path_block(self, base_dir):
        """Verify absolute paths are blocked from escaping the base directory."""
        with pytest.raises(UnsafePathError):
            sanitize_file_path(base_dir, "/etc/passwd")

        with pytest.raises(UnsafePathError):
            sanitize_file_path(base_dir, "C:\\Windows\\system32\\cmd.exe")

        with pytest.raises(UnsafePathError):
            resolve_safe_path(base_dir, "/etc/passwd")

    def test_prefix_collision_block(self, tmp_path):
        """
        Verify prefix collisions (e.g. base = /safe/export and evil = /safe/export_evil)
        are blocked.
        """
        safe_base = tmp_path / "export"
        safe_base.mkdir()

        with pytest.raises(UnsafePathError):
            # Attempting to access sibling directory via traversal
            sanitize_file_path(str(safe_base), "../export_evil/data.txt")

    def test_null_byte_block(self, base_dir):
        """Verify null byte injections are blocked."""
        with pytest.raises(UnsafePathError) as exc1:
            sanitize_file_path(base_dir, "report.pdf\x00.exe")
        assert "Null byte detected" in str(exc1.value)

        with pytest.raises(UnsafePathError) as exc2:
            resolve_safe_path(base_dir, "report.pdf\x00.exe")
        assert "Null byte detected" in str(exc2.value)

    def test_empty_path_block(self, base_dir):
        """Verify empty or None paths are rejected."""
        with pytest.raises(UnsafePathError):
            sanitize_file_path(base_dir, "")

        with pytest.raises(UnsafePathError):
            sanitize_file_path(base_dir, "   ")

        with pytest.raises(UnsafePathError):
            sanitize_file_path(base_dir, None)  # type: ignore

    def test_allow_base_flag(self, base_dir):
        """Verify allow_base parameter controls whether pointing exactly to base directory is permitted."""
        # By default allow_base=True
        assert sanitize_file_path(base_dir, ".", allow_base=True) == os.path.abspath(base_dir)

        # When allow_base=False, pointing to base must raise UnsafePathError
        with pytest.raises(UnsafePathError):
            sanitize_file_path(base_dir, ".", allow_base=False)

    def test_filename_segment_sanitization(self):
        """Verify validate_safe_filename_segment blocks traversal tokens and strips dangerous chars."""
        assert validate_safe_filename_segment("report_123.pdf") == "report_123.pdf"
        assert validate_safe_filename_segment("my-doc#1 (final)") == "my-doc_1__final_"

        with pytest.raises(UnsafePathError):
            validate_safe_filename_segment("../evil.pdf")

        with pytest.raises(UnsafePathError):
            validate_safe_filename_segment("subdir/file.txt")

        with pytest.raises(UnsafePathError):
            validate_safe_filename_segment("file\x00.txt")
