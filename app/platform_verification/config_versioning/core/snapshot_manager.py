"""
Immutable Snapshot Manager with Canonical Hashing and Lineage Sealing.
"""
import hashlib
import json
from typing import Any, Dict, Optional
from app.platform_verification.config_versioning.domain.models import (
    ConfigurationSnapshot, EnvironmentTier, EnvironmentFingerprint
)
from app.platform_verification.config_versioning.core.registry import configuration_registry

class SnapshotManager:
    @staticmethod
    def create_snapshot(
        resolved_config: Dict[str, Any],
        environment: EnvironmentTier = EnvironmentTier.INTEGRATION,
        environment_fingerprint: Optional[EnvironmentFingerprint] = None,
        tenant_id: str = "default-tenant",
        semantic_version: str = "1.0.0",
        creator: str = "Enterprise Platform Engineer"
    ) -> ConfigurationSnapshot:
        # Canonical SHA-256 Hashing
        config_bytes = json.dumps(resolved_config, sort_keys=True, default=str).encode("utf-8")
        config_hash = hashlib.sha256(config_bytes).hexdigest()

        dep_bytes = json.dumps(resolved_config.get("dependencies", {}), sort_keys=True).encode("utf-8")
        dep_hash = hashlib.sha256(dep_bytes).hexdigest()

        fp = environment_fingerprint or EnvironmentFingerprint(tier=environment)

        snapshot = ConfigurationSnapshot(
            tenant_id=tenant_id,
            environment=environment,
            semantic_version=semantic_version,
            resolved_configuration=resolved_config,
            configuration_hash=config_hash,
            dependency_manifest_hash=dep_hash,
            environment_fingerprint=fp,
            creator=creator,
            is_frozen=True
        )

        configuration_registry.store_snapshot(snapshot)
        return snapshot

snapshot_manager = SnapshotManager()
