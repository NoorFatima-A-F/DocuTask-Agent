"""Comprehensive filesystem security and path traversal prevention regression tests."""

import os
from pathlib import Path
import pytest
from app.core.security import (
    resolve_safe_path,
    validate_safe_filename_segment,
    UnsafePathError,
)


class TestPathContainmentAndResolution:
    """Tests strict base directory containment and rejection of path escapes (CWE-22)."""

    def test_normal_subpath_allowed(self, tmp_path: Path):
        base = tmp_path / "app_evidence"
        base.mkdir()
        target = resolve_safe_path(base, "reports/audit_2026.json")
        assert target.is_relative_to(base.resolve())
        assert target.name == "audit_2026.json"

    def test_nested_directory_creation_path(self, tmp_path: Path):
        base = tmp_path / "base"
        base.mkdir()
        target = resolve_safe_path(base, "level1/level2/level3/output.log")
        assert target.is_relative_to(base.resolve())
        assert str(target).endswith(os.path.join("level1", "level2", "level3", "output.log"))

    def test_base_directory_exact_match(self, tmp_path: Path):
        base = tmp_path / "base"
        base.mkdir()
        target = resolve_safe_path(base, "", allow_base=True)
        assert target == base.resolve()

    def test_parent_traversal_rejected(self, tmp_path: Path):
        base = tmp_path / "base"
        base.mkdir()
        with pytest.raises(UnsafePathError) as exc_info:
            resolve_safe_path(base, "../escaped_secret.json")
        assert "escapes trusted base directory" in str(exc_info.value)

    def test_nested_parent_traversal_rejected(self, tmp_path: Path):
        base = tmp_path / "base"
        base.mkdir()
        with pytest.raises(UnsafePathError) as exc_info:
            resolve_safe_path(base, "sub/dir/../../../../etc/passwd")
        assert "escapes trusted base directory" in str(exc_info.value)

    def test_absolute_path_injection_rejected(self, tmp_path: Path):
        base = tmp_path / "base"
        base.mkdir()
        outside_file = tmp_path / "outside_unauthorized.txt"
        with pytest.raises(UnsafePathError) as exc_info:
            resolve_safe_path(base, str(outside_file.resolve()))
        assert "escapes trusted base directory" in str(exc_info.value)

    def test_prefix_collision_attack_rejected(self, tmp_path: Path):
        """Ensures /base_dir/../base_dir_attacker is strictly blocked (guards against naive startswith)."""
        base = tmp_path / "safe_dir"
        base.mkdir()
        attacker_dir = tmp_path / "safe_dir_attacker"
        attacker_dir.mkdir()
        
        with pytest.raises(UnsafePathError):
            resolve_safe_path(base, "../safe_dir_attacker/payload.sh")


class TestFilenameSegmentValidation:
    """Tests filename segment sanitization and illegal character validation."""

    def test_valid_alphanumeric_and_dashes(self):
        assert validate_safe_filename_segment("report-2026_final.json") == "report-2026_final.json"
        assert validate_safe_filename_segment("SIM_RUN_001") == "SIM_RUN_001"
        assert validate_safe_filename_segment("case_study_finance.md") == "case_study_finance.md"

    def test_null_byte_injection_rejected(self):
        with pytest.raises(UnsafePathError):
            validate_safe_filename_segment("report.json\x00.exe")

    def test_forward_and_backward_slash_rejected(self):
        with pytest.raises(UnsafePathError):
            validate_safe_filename_segment("sub/report.json")
        with pytest.raises(UnsafePathError):
            validate_safe_filename_segment("sub\\report.json")

    def test_double_dot_traversal_token_rejected(self):
        with pytest.raises(UnsafePathError):
            validate_safe_filename_segment("..")
        with pytest.raises(UnsafePathError):
            validate_safe_filename_segment("../payload")

    def test_empty_or_whitespace_rejected(self):
        with pytest.raises(UnsafePathError):
            validate_safe_filename_segment("")
        with pytest.raises(UnsafePathError):
            validate_safe_filename_segment("   ")

    def test_special_characters_sanitized(self):
        # Characters like spaces, semicolons, dollar signs are sanitized to underscores
        assert validate_safe_filename_segment("my report;rm -rf") == "my_report_rm_-rf"
