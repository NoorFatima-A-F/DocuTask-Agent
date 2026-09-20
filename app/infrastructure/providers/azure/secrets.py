"""Azure Key Vault Adapter."""

from typing import Dict, Optional
from ..base import SecretProvider


class AzureKeyVaultProvider(SecretProvider):
    """Manages Azure Key Vault secrets."""

    def __init__(self, vault_name: str = "kv-doctask-prod") -> None:
        super().__init__("azure")
        self.vault_name = vault_name
        self._secrets: Dict[str, str] = {}

    def get_secret(self, secret_name: str) -> Optional[str]:
        return self._secrets.get(secret_name)

    def set_secret(self, secret_name: str, secret_value: str) -> bool:
        self._secrets[secret_name] = secret_value
        return True

    def delete_secret(self, secret_name: str) -> bool:
        if secret_name in self._secrets:
            del self._secrets[secret_name]
            return True
        return False
