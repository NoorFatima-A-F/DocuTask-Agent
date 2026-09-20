"""
Reference Storage Provider Plugin: Local CAS Storage Provider.
"""
import hashlib
from typing import Any, Dict, List, Optional, Tuple
from app.platform_verification.extension_framework.domain.interfaces import StorageProviderPluginInterface
from app.platform_verification.extension_framework.domain.models import (
    PluginMetadata, PluginCategory, PluginExecutionContext, PluginExecutionResult,
    PluginHealthMetrics, PluginHealthState, PluginPermission, SecurityClassification
)


class LocalCASStoragePlugin(StorageProviderPluginInterface):
    def __init__(self):
        self._store: Dict[str, bytes] = {}
        self._config: Dict[str, Any] = {}

    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            plugin_id="local_cas_storage_plugin",
            name="Local Content-Addressable Storage Plugin",
            version="1.0.0",
            category=PluginCategory.STORAGE,
            author="Storage Engineering Squad",
            description="Provides SHA-256 CAS persistence for evidence artifacts",
            capabilities=["cas_blob_storage", "integrity_verification"],
            granted_permissions=[PluginPermission.ACCESS_STORAGE, PluginPermission.WRITE_EVIDENCE],
            security_classification=SecurityClassification.ENTERPRISE_CERTIFIED
        )

    def initialize(self, context: Dict[str, Any]) -> bool:
        return True

    def validate(self) -> Tuple[bool, List[str]]:
        return True, []

    def configure(self, config: Dict[str, Any]) -> None:
        self._config = config

    def execute(self, context: PluginExecutionContext) -> PluginExecutionResult:
        uri = self.put_artifact("test_key", b"test_payload_evidence")
        return PluginExecutionResult(
            execution_id=context.execution_id,
            plugin_id="local_cas_storage_plugin",
            is_success=True,
            metrics=[{"metric": "bytes_stored", "value": len(b"test_payload_evidence")}],
            raw_evidence={"storage_uri": uri}
        )

    def put_artifact(self, key: str, data: bytes) -> str:
        digest = hashlib.sha256(data).hexdigest()
        self._store[digest] = data
        return f"cas://{digest}"

    def get_artifact(self, key: str) -> Optional[bytes]:
        digest = key.replace("cas://", "")
        return self._store.get(digest)

    def cleanup(self) -> None:
        self._store.clear()

    def health_check(self) -> PluginHealthMetrics:
        return PluginHealthMetrics(
            plugin_id="local_cas_storage_plugin",
            state=PluginHealthState.HEALTHY,
            total_executions=1,
            successful_executions=1
        )
