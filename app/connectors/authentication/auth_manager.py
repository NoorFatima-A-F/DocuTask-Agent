"""
Enterprise Integration Fabric & Universal Connector Platform (EIF-UCP) - Authentication Manager.
Orchestrates OAuth2, API Keys, JWT, Bearer tokens, Basic Auth, mTLS, and Service Account lifecycles.
"""

from __future__ import annotations

import base64
from datetime import datetime, timezone
import logging
from typing import Any, Dict, Optional

from app.connectors.authentication.credential_store import CredentialStore
from app.connectors.core.exceptions import AuthenticationError
from app.connectors.core.models import AuthType

logger = logging.getLogger(__name__)


class AuthenticationManager:
    """
    Manages authentication token lifetimes, signature generation, header construction,
    and credential validation across all supported protocols.
    """

    def __init__(self, credential_store: Optional[CredentialStore] = None):
        self._credential_store = credential_store or CredentialStore()

    def validate_credentials(self, auth_type: AuthType, credentials: Dict[str, Any]) -> bool:
        """Validates that mandatory fields for the specified auth type are present."""
        if auth_type == AuthType.NONE:
            return True
        elif auth_type in (AuthType.API_KEY,):
            return "api_key" in credentials or "key" in credentials or "token" in credentials
        elif auth_type in (AuthType.BEARER, AuthType.JWT, AuthType.OAUTH2, AuthType.OAUTH2_PKCE):
            return "access_token" in credentials or "token" in credentials or "api_key" in credentials
        elif auth_type == AuthType.BASIC:
            return "username" in credentials and "password" in credentials
        elif auth_type == AuthType.SERVICE_ACCOUNT:
            return "client_email" in credentials or "private_key" in credentials or "service_account_json" in credentials
        return len(credentials) > 0

    def build_auth_headers(self, auth_type: AuthType, credentials: Dict[str, Any]) -> Dict[str, str]:
        """
        Builds protocol-specific HTTP authentication headers from decrypted credentials.
        """
        headers: Dict[str, str] = {}

        if auth_type == AuthType.NONE:
            return headers

        elif auth_type in (AuthType.BEARER, AuthType.JWT, AuthType.OAUTH2, AuthType.OAUTH2_PKCE):
            token = credentials.get("access_token") or credentials.get("token") or credentials.get("api_key", "")
            headers["Authorization"] = f"Bearer {token}"

        elif auth_type == AuthType.API_KEY:
            header_name = credentials.get("header_name", "X-API-Key")
            key = credentials.get("api_key") or credentials.get("key") or credentials.get("token", "")
            headers[header_name] = key

        elif auth_type == AuthType.BASIC:
            user = credentials.get("username", "")
            pwd = credentials.get("password", "")
            encoded = base64.b64encode(f"{user}:{pwd}".encode("utf-8")).decode("utf-8")
            headers["Authorization"] = f"Basic {encoded}"

        elif auth_type == AuthType.SERVICE_ACCOUNT:
            token = credentials.get("token") or credentials.get("client_email", "sa-token")
            headers["Authorization"] = f"Bearer {token}"

        return headers

    def refresh_oauth_token(
        self,
        organization: str,
        workspace: str,
        connector: str,
    ) -> Dict[str, Any]:
        """
        Refreshes an expired OAuth2 access token using stored refresh_token.
        """
        creds = self._credential_store.resolve_credentials(organization, workspace, connector)
        refresh_token = creds.get("refresh_token")
        if not refresh_token:
            raise AuthenticationError(
                f"No refresh_token present to refresh OAuth session for {connector}",
                connector_id=connector,
            )

        # Simulated OAuth2 token refresh flow
        new_token = f"refreshed_tok_{int(datetime.now(timezone.utc).timestamp())}"
        creds["access_token"] = new_token
        self._credential_store.rotate_credentials(organization, workspace, connector, creds)
        logger.info(f"Refreshed OAuth2 token for {connector}")
        return creds
