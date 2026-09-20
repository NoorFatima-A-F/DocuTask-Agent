"""Release Compatibility Matrix & Semantic Version Evaluation (Req 11, 12)."""
import re
from typing import Any, Dict, List, Optional, Tuple


class ReleaseCompatibilityMatrix:
    """Evaluates cross-system version compatibility before deployment rollout."""

    def __init__(self):
        # Default compatibility constraints
        self.rules = {
            "api_sdk_compat": {"api_major": 1, "min_sdk": "1.0.0", "max_sdk": "2.0.0"},
            "runtime_worker_compat": {"runtime_major": 1, "min_worker": "1.0.0", "max_worker": "2.0.0"},
            "db_schema_compat": {"min_schema_version": "001", "max_schema_version": "999"},
        }

    @staticmethod
    def parse_semver(version: str) -> Tuple[int, int, int]:
        clean = version.lstrip("v").split("-")[0]
        parts = clean.split(".")
        major = int(parts[0]) if len(parts) > 0 and parts[0].isdigit() else 1
        minor = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 0
        patch = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else 0
        return (major, minor, patch)

    def validate_compatibility(
        self,
        platform_version: str,
        api_version: str,
        sdk_version: str,
        worker_version: str,
        db_schema_version: str = "001",
    ) -> Tuple[bool, List[str]]:
        violations: List[str] = []

        api_maj, _, _ = self.parse_semver(api_version)
        sdk_tuple = self.parse_semver(sdk_version)
        min_sdk_tuple = self.parse_semver(self.rules["api_sdk_compat"]["min_sdk"])
        max_sdk_tuple = self.parse_semver(self.rules["api_sdk_compat"]["max_sdk"])

        if sdk_tuple < min_sdk_tuple or sdk_tuple >= max_sdk_tuple:
            violations.append(
                f"SDK version {sdk_version} is incompatible with API {api_version} (Required: >={self.rules['api_sdk_compat']['min_sdk']}, <{self.rules['api_sdk_compat']['max_sdk']})"
            )

        worker_tuple = self.parse_semver(worker_version)
        min_worker = self.parse_semver(self.rules["runtime_worker_compat"]["min_worker"])
        max_worker = self.parse_semver(self.rules["runtime_worker_compat"]["max_worker"])

        if worker_tuple < min_worker or worker_tuple >= max_worker:
            violations.append(
                f"Worker version {worker_version} is incompatible with platform runtime {platform_version}"
            )

        is_valid = len(violations) == 0
        return is_valid, violations
