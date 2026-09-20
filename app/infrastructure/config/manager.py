"""Infrastructure Configuration Manager with Versioning and Rollback Support."""

from typing import Dict, List, Optional
from ..core.exceptions import ConfigurationInvalidError
from .models import InfrastructureManifest
from .validation import ManifestValidator


class ConfigurationManager:
    """Stores, versions, validates, and rolls back declarative infrastructure manifests."""

    def __init__(self) -> None:
        # service_name:environment -> List[InfrastructureManifest] sorted by version/time
        self._history: Dict[str, List[InfrastructureManifest]] = {}

    def _get_key(self, service_name: str, environment: str) -> str:
        return f"{service_name}:{environment}"

    def register_manifest(self, manifest: InfrastructureManifest) -> InfrastructureManifest:
        """Validate and record a new manifest version."""
        ManifestValidator.validate(manifest)

        key = self._get_key(manifest.service_name, manifest.environment)
        if key not in self._history:
            self._history[key] = []
        self._history[key].append(manifest)
        return manifest

    def get_current_manifest(self, service_name: str, environment: str = "PRODUCTION") -> Optional[InfrastructureManifest]:
        """Retrieve latest active manifest for a service."""
        key = self._get_key(service_name, environment)
        history = self._history.get(key, [])
        return history[-1] if history else None

    def list_manifest_history(self, service_name: str, environment: str = "PRODUCTION") -> List[InfrastructureManifest]:
        """Retrieve version history for a service."""
        key = self._get_key(service_name, environment)
        return list(self._history.get(key, []))

    def rollback(self, service_name: str, target_version: str, environment: str = "PRODUCTION") -> InfrastructureManifest:
        """Roll back to a previously deployed manifest version."""
        key = self._get_key(service_name, environment)
        history = self._history.get(key, [])
        target = next((m for m in history if m.version == target_version), None)

        if not target:
            raise ConfigurationInvalidError(
                f"Cannot rollback: version '{target_version}' not found for service '{service_name}' in {environment}."
            )

        # Append as latest active version
        self._history[key].append(target)
        return target
