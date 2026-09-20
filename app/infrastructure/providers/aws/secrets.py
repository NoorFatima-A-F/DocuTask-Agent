"""AWS Secrets Manager Adapter."""

from typing import Dict, Optional
from ..base import SecretProvider


class AWSSecretsManagerProvider(SecretProvider):
    """Manages AWS Secrets Manager secrets."""

    def __init__(self, region: str = "us-east-1") -> None:
        super().__init__("aws")
        self.region = region
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
