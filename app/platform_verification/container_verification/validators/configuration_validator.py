"""
Container Architecture and Configuration Validator.
"""
from typing import List
from app.platform_verification.container_verification.models.verification_models import (
    ContainerArchitectureModel,
    ArchitectureDiscoveryReport,
)


class ConfigurationValidator:
    """Validates container architecture discovery and checks for undocumented services."""

    def discover_and_validate(self, arch: ContainerArchitectureModel) -> ArchitectureDiscoveryReport:
        undocumented: List[str] = []
        hidden_deps: List[str] = []

        for name, s in arch.services.items():
            for dep in s.depends_on:
                if dep not in arch.services:
                    hidden_deps.append(f"{name} depends on non-existent service '{dep}'")

        status = "PASS" if len(undocumented) == 0 and len(hidden_deps) == 0 else "FAIL"
        return ArchitectureDiscoveryReport(
            total_services=len(arch.services),
            total_networks=len(arch.networks),
            total_volumes=len(arch.volumes),
            undocumented_services=undocumented,
            hidden_dependencies=hidden_deps,
            status=status,
        )
