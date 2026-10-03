"""
Environment Diff Comparator (Phase 82B.6)
=========================================
Compares execution environment fingerprints to detect discrepancies in
OS versions, Python runtimes, C runtime libraries, and dependency packages.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple



@dataclass(frozen=True)
class PackageVersionDelta:
    package_name: str
    base_version: str
    target_version: str
    is_major_shift: bool


@dataclass(frozen=True)
class EnvironmentDiffReport:
    is_identical: bool
    os_match: bool
    python_match: bool
    package_matches_count: int
    package_mismatches_count: int
    package_deltas: Tuple[PackageVersionDelta, ...]
    system_deltas: Dict[str, Any]
    diff_summary: str


class EnvironmentDiffEngine:
    """
    Computes differences between two EnvironmentFingerprints or environment dictionaries.
    """

    @classmethod
    def diff_environments(
        cls,
        base_env: Dict[str, Any],
        target_env: Dict[str, Any],
    ) -> EnvironmentDiffReport:
        """Compare base and target environment specifications."""
        sys_deltas: Dict[str, Any] = {}

        # 1. OS comparison
        base_os = str(base_env.get("os_name", base_env.get("os", "")))
        target_os = str(target_env.get("os_name", target_env.get("os", "")))
        os_match = (base_os == target_os)
        if not os_match:
            sys_deltas["os"] = {"base": base_os, "target": target_os}

        # 2. Python runtime comparison
        base_py = str(base_env.get("python_version", base_env.get("python", "")))
        target_py = str(target_env.get("python_version", target_env.get("python", "")))
        py_match = (base_py == target_py)
        if not py_match:
            sys_deltas["python"] = {"base": base_py, "target": target_py}

        # 3. Packages comparison
        base_pkgs = base_env.get("package_versions", {})
        target_pkgs = target_env.get("package_versions", {})
        all_pkg_names = set(base_pkgs.keys()).union(set(target_pkgs.keys()))

        pkg_deltas: List[PackageVersionDelta] = []
        matches = 0
        mismatches = 0

        for pkg in sorted(all_pkg_names):
            v1 = str(base_pkgs.get(pkg, "NOT_INSTALLED"))
            v2 = str(target_pkgs.get(pkg, "NOT_INSTALLED"))
            if v1 == v2:
                matches += 1
            else:
                mismatches += 1
                is_major = False
                if v1 != "NOT_INSTALLED" and v2 != "NOT_INSTALLED":
                    # Check major version
                    p1 = v1.split(".")[0]
                    p2 = v2.split(".")[0]
                    is_major = (p1 != p2)
                pkg_deltas.append(PackageVersionDelta(
                    package_name=pkg,
                    base_version=v1,
                    target_version=v2,
                    is_major_shift=is_major,
                ))

        identical = os_match and py_match and mismatches == 0
        summary = (
            "Environments are bit-for-bit identical."
            if identical else
            f"Detected {mismatches} package mismatch(es) and {len(sys_deltas)} system delta(s)."
        )

        return EnvironmentDiffReport(
            is_identical=identical,
            os_match=os_match,
            python_match=py_match,
            package_matches_count=matches,
            package_mismatches_count=mismatches,
            package_deltas=tuple(pkg_deltas),
            system_deltas=sys_deltas,
            diff_summary=summary,
        )
