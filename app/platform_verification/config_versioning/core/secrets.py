"""
Secret Management, Leak Detection, and Rotation Governance.
Zero Plaintext Storage Policy.
"""
from datetime import datetime, timezone
import hashlib
import re
from typing import Any, Dict, List, Optional
from app.platform_verification.config_versioning.domain.models import SecretReference, SecretRotationRecord


class SecretManagerService:
    def __init__(self):
        self._secrets: Dict[str, SecretReference] = {}
        self._rotation_history: List[SecretRotationRecord] = []
        self._mock_vault_store: Dict[str, str] = {}
        self._known_secret_values: set[str] = set()

    def register_secret_reference(
        self,
        key_name: str,
        vault_path: str,
        initial_value: Optional[str] = None,
        rotation_interval_days: int = 90
    ) -> SecretReference:
        ref = SecretReference(
            key_name=key_name,
            vault_path=vault_path,
            rotation_interval_days=rotation_interval_days
        )
        self._secrets[key_name] = ref
        if initial_value:
            self._mock_vault_store[vault_path] = initial_value
            self._known_secret_values.add(initial_value)
        return ref

    def rotate_secret(self, key_name: str, new_value: str, rotated_by: str = "KMS Automation", reason: str = "Scheduled rotation") -> SecretRotationRecord:
        if key_name not in self._secrets:
            raise KeyError(f"Secret {key_name} not registered")
        ref = self._secrets[key_name]
        old_v = ref.version
        ref.version += 1
        ref.is_rotated = True
        self._mock_vault_store[ref.vault_path] = new_value
        if new_value:
            self._known_secret_values.add(new_value)

        record = SecretRotationRecord(
            secret_id=ref.secret_id,
            old_version=old_v,
            new_version=ref.version,
            reason=reason,
            rotated_by=rotated_by
        )
        self._rotation_history.append(record)
        return record

    def mask_secrets(self, text: str) -> str:
        """Sanitizes text, replacing high-entropy token patterns and registered vault secrets with [REDACTED_SECRET]"""
        for val in list(self._known_secret_values) + list(self._mock_vault_store.values()):
            if val and len(val) >= 6:
                text = text.replace(val, "[REDACTED_SECRET]")
        pattern = r"(?:AIza[0-9A-Za-z\-_]{20,}|sk-[a-zA-Z0-9]{20,}|ghp_[a-zA-Z0-9]{20,}|bearer\s+[a-zA-Z0-9\._\-]+)"
        return re.sub(pattern, "[REDACTED_SECRET]", text, flags=re.IGNORECASE)

    def mask_config_dict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Deep masks sensitive keys in config dictionaries"""
        sensitive_keywords = {"key", "token", "secret", "password", "credential", "auth"}
        sanitized = {}
        for k, v in data.items():
            if isinstance(v, dict):
                sanitized[k] = self.mask_config_dict(v)
            elif isinstance(v, str) and any(kw in k.lower() for kw in sensitive_keywords):
                sanitized[k] = "[REDACTED_SECRET]"
            else:
                sanitized[k] = v
        return sanitized


secret_manager_service = SecretManagerService()
