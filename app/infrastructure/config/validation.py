"""Validation Engine for Declarative Infrastructure Manifests."""

from typing import List, Tuple
from ..core.exceptions import ConfigurationInvalidError
from .models import InfrastructureManifest


class ManifestValidator:
    """Validates declarative configuration manifests against platform limits."""

    @classmethod
    def validate(cls, manifest: InfrastructureManifest) -> Tuple[bool, List[str]]:
        errors: List[str] = []

        # Service name format
        if not manifest.service_name or len(manifest.service_name) < 3:
            errors.append("Service name must be at least 3 characters long.")

        # Replicas vs Scaling
        if manifest.scaling.enabled:
            if manifest.scaling.min_replicas > manifest.scaling.max_replicas:
                errors.append(
                    f"Min replicas ({manifest.scaling.min_replicas}) cannot exceed max replicas ({manifest.scaling.max_replicas})."
                )
            if manifest.runtime.replicas < manifest.scaling.min_replicas or manifest.runtime.replicas > manifest.scaling.max_replicas:
                errors.append(
                    f"Initial replicas ({manifest.runtime.replicas}) must be between {manifest.scaling.min_replicas} and {manifest.scaling.max_replicas}."
                )

        # Region check
        if manifest.region.primary not in manifest.region.supported_regions:
            errors.append(
                f"Primary region '{manifest.region.primary}' not in supported regions: {manifest.region.supported_regions}."
            )

        if errors:
            raise ConfigurationInvalidError(
                f"Manifest validation failed with {len(errors)} error(s): {'; '.join(errors)}",
                details={"errors": errors},
            )

        return True, []
