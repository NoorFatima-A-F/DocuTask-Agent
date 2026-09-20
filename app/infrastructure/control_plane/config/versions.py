"""Compatibility Matrix for Control Plane, Kubernetes, and Data Plane Versions."""

from typing import Dict, List, Optional, Tuple
from packaging import version


class CompatibilityMatrix:
    """Validates multi-version compatibility across control plane, Kubernetes, and data planes."""

    SUPPORTED_K8S_MIN = "1.28.0"
    SUPPORTED_K8S_MAX = "1.32.0"
    SUPPORTED_CONTROL_PLANE_MIN = "3.0.0"
    SUPPORTED_CONTROL_PLANE_MAX = "3.5.0"
    SUPPORTED_DATA_PLANE_MIN = "3.0.0"
    SUPPORTED_DATA_PLANE_MAX = "3.5.0"

    @classmethod
    def validate_cluster_versions(
        cls,
        k8s_version: str,
        control_plane_version: str,
        data_plane_version: str,
    ) -> Tuple[bool, List[str]]:
        """Validate if a cluster version tuple is compatible with the platform."""
        errors = []

        try:
            k8s_v = version.parse(k8s_version)
            if not (version.parse(cls.SUPPORTED_K8S_MIN) <= k8s_v <= version.parse(cls.SUPPORTED_K8S_MAX)):
                errors.append(
                    f"Kubernetes version '{k8s_version}' is outside supported range "
                    f"[{cls.SUPPORTED_K8S_MIN} - {cls.SUPPORTED_K8S_MAX}]."
                )
        except Exception:
            errors.append(f"Invalid Kubernetes version format: '{k8s_version}'.")

        try:
            cp_v = version.parse(control_plane_version)
            if not (version.parse(cls.SUPPORTED_CONTROL_PLANE_MIN) <= cp_v <= version.parse(cls.SUPPORTED_CONTROL_PLANE_MAX)):
                errors.append(
                    f"Control Plane version '{control_plane_version}' is outside supported range "
                    f"[{cls.SUPPORTED_CONTROL_PLANE_MIN} - {cls.SUPPORTED_CONTROL_PLANE_MAX}]."
                )
        except Exception:
            errors.append(f"Invalid Control Plane version format: '{control_plane_version}'.")

        try:
            dp_v = version.parse(data_plane_version)
            if not (version.parse(cls.SUPPORTED_DATA_PLANE_MIN) <= dp_v <= version.parse(cls.SUPPORTED_DATA_PLANE_MAX)):
                errors.append(
                    f"Data Plane version '{data_plane_version}' is outside supported range "
                    f"[{cls.SUPPORTED_DATA_PLANE_MIN} - {cls.SUPPORTED_DATA_PLANE_MAX}]."
                )
        except Exception:
            errors.append(f"Invalid Data Plane version format: '{data_plane_version}'.")

        return len(errors) == 0, errors
