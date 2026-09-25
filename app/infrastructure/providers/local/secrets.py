"""Local Environment Variable / File-based Secrets Adapter."""

import os
from typing import Dict, Optional
from ..base import SecretProvider


class LocalSecretProvider(SecretProvider):
    """Manages local secrets via in-memory dictionary or OS environment."""

    def __init__(self) -> None:
        super().__init__("local")
        self._secrets: Dict[str, str] = {}

    def get_secret(self, secret_name: str) -> Optional[str]:
        return self._secrets.get(secret_name) or os.environ.get(secret_name)

    def set_secret(self, secret_name: str, secret_value: str) -> bool:
        self._secrets[secret_name] = secret_value
        return True

    def delete_secret(self, secret_name: str) -> bool:
        if secret_name in self._secrets:
            del self._secrets[secret_name]
            return True
        return False
