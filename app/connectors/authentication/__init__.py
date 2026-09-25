"""
Enterprise Integration Fabric - Authentication package.
"""

from app.connectors.authentication.auth_manager import AuthenticationManager
from app.connectors.authentication.credential_store import CredentialStore
from app.connectors.authentication.secret_provider import (
    AWSSecretProvider,
    AzureSecretProvider,
    EnvSecretProvider,
    GCPSecretProvider,
    InMemoryVaultSecretProvider,
    SecretProvider,
)

__all__ = [
    "AuthenticationManager",
    "CredentialStore",
    "SecretProvider",
    "InMemoryVaultSecretProvider",
    "EnvSecretProvider",
    "GCPSecretProvider",
    "AWSSecretProvider",
    "AzureSecretProvider",
]
