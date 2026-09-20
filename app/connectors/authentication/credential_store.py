"""
Enterprise Integration Fabric & Universal Connector Platform (EIF-UCP) - Credential Isolation System.
Enforces multi-tenant credential isolation: Organization -> Workspace -> Connector -> Credential -> SecretProvider.
Credentials and API keys are strictly partitioned and never stored in workflows, prompts, or traces.
"""

from __future__ import annotations

from datetime import datetime, timezone
import json
import logging
from typing import Any, Dict, List, Optional
import uuid

from app.connectors.authentication.secret_provider import InMemoryVaultSecretProvider, SecretProvider
from app.connectors.core.exceptions import CredentialNotFoundError
from app.connectors.core.models import AuthType, CredentialMetadata

logger = logging.getLogger(__name__)


class CredentialStore:
    """
    Tenant-isolated credential repository managing authorization tokens,
    API keys, OAuth refresh tokens, and service account configs.
    """

    def __init__(self, secret_provider: Optional[SecretProvider] = None):
        self._secret_provider = secret_provider or InMemoryVaultSecretProvider()
        # Partitioned index: (org_id, workspace_id, connector_id) -> CredentialMetadata
        self._credentials: Dict[str, CredentialMetadata] = {}

    def _key(self, organization: str, workspace: str, connector: str) -> str:
        return f"{organization}:{workspace}:{connector}"

    def store_credentials(
        self,
        organization: str,
        workspace: str,
        connector: str,
        auth_type: AuthType | str,
        secret_payload: Dict[str, Any],
        owner: str = "system",
        permissions: Optional[List[str]] = None,
        rotation_policy: str = "90_days",
    ) -> CredentialMetadata:
        """
        Securely encrypts and stores raw credentials into SecretProvider
        and registers tenant-isolated metadata.
        """
        a_type = auth_type if isinstance(auth_type, AuthType) else AuthType(auth_type)
        serialized_secret = json.dumps(secret_payload)
        secret_name = f"{organization}_{workspace}_{connector}_creds"

        secret_ref = self._secret_provider.create_secret(
            secret_name=secret_name,
            secret_value=serialized_secret,
            metadata={"org": organization, "ws": workspace, "connector": connector},
        )

        cred_meta = CredentialMetadata(
            id=f"cred-{uuid.uuid4().hex[:8]}",
            connector=connector,
            organization=organization,
            workspace=workspace,
            owner=owner,
            auth_type=a_type,
            permissions=permissions or ["*"],
            rotation_policy=rotation_policy,
            secret_key_ref=secret_ref,
            is_active=True,
        )

        key = self._key(organization, workspace, connector)
        self._credentials[key] = cred_meta
        logger.info(f"Stored credentials for {key} (AuthType={a_type.value})")
        return cred_meta

    def get_metadata(
        self,
        organization: str,
        workspace: str,
        connector: str,
    ) -> Optional[CredentialMetadata]:
        """Retrieves safe credential metadata without exposing secret material."""
        key = self._key(organization, workspace, connector)
        return self._credentials.get(key)

    def resolve_credentials(
        self,
        organization: str,
        workspace: str,
        connector: str,
    ) -> Dict[str, Any]:
        """
        Resolves and decrypts the underlying credential payload for runtime execution.
        """
        key = self._key(organization, workspace, connector)
        cred_meta = self._credentials.get(key)

        if not cred_meta or not cred_meta.is_active:
            raise CredentialNotFoundError(
                f"No active credentials found for organization='{organization}', workspace='{workspace}', connector='{connector}'",
                connector_id=connector,
                details={"org": organization, "ws": workspace},
            )

        raw = self._secret_provider.get_secret(cred_meta.secret_key_ref)
        if not raw:
            raise CredentialNotFoundError(
                f"Secret referenced by '{cred_meta.secret_key_ref}' is missing or expired in SecretProvider",
                connector_id=connector,
            )

        try:
            return json.loads(raw)
        except Exception:
            return {"raw_secret": raw}

    def rotate_credentials(
        self,
        organization: str,
        workspace: str,
        connector: str,
        new_secret_payload: Dict[str, Any],
    ) -> CredentialMetadata:
        """Rotates secrets and updates timestamp."""
        key = self._key(organization, workspace, connector)
        cred_meta = self._credentials.get(key)
        if not cred_meta:
            return self.store_credentials(organization, workspace, connector, AuthType.API_KEY, new_secret_payload)

        serialized = json.dumps(new_secret_payload)
        self._secret_provider.rotate_secret(cred_meta.secret_key_ref, serialized)
        cred_meta.created = datetime.now(timezone.utc)
        logger.info(f"Rotated credentials for {key}")
        return cred_meta

    def revoke_credentials(
        self,
        organization: str,
        workspace: str,
        connector: str,
    ) -> bool:
        """Revokes credentials and destroys the secret payload."""
        key = self._key(organization, workspace, connector)
        cred_meta = self._credentials.get(key)
        if cred_meta:
            cred_meta.is_active = False
            self._secret_provider.revoke_secret(cred_meta.secret_key_ref)
            del self._credentials[key]
            logger.info(f"Revoked credentials for {key}")
            return True
        return False
