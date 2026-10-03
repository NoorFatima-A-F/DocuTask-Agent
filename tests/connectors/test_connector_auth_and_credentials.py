"""
Tests for SecretProvider, CredentialStore, and AuthenticationManager.
"""

import pytest
from app.connectors.authentication.auth_manager import AuthenticationManager
from app.connectors.authentication.credential_store import CredentialStore
from app.connectors.authentication.secret_provider import InMemoryVaultSecretProvider
from app.connectors.core.exceptions import CredentialNotFoundError
from app.connectors.core.models import AuthType


def test_secret_provider_crud_rotation_and_audit():
    vault = InMemoryVaultSecretProvider()

    # Create secret
    ref = vault.create_secret("test_key", "secret_value_123", metadata={"env": "prod"})
    assert ref.startswith("sec-")
    assert vault.get_secret(ref) == "secret_value_123"

    # Rotate secret
    vault.rotate_secret(ref, "secret_value_456")
    assert vault.get_secret(ref) == "secret_value_456"

    # Audit trail
    audit = vault.audit_secret_access(ref)
    actions = [a["action"] for a in audit]
    assert "CREATE" in actions
    assert "GET" in actions
    assert "ROTATE" in actions

    # Expiration
    vault.expire_secret(ref)
    assert vault.get_secret(ref) is None

    # Revocation
    vault.revoke_secret(ref)
    assert vault.get_secret(ref) is None


def test_credential_store_multi_tenant_isolation():
    vault = InMemoryVaultSecretProvider()
    store = CredentialStore(vault)

    # Tenant 1 store
    store.store_credentials(
        organization="org-alpha",
        workspace="ws-finance",
        connector="conn-stripe",
        auth_type=AuthType.BEARER,
        secret_payload={"token": "sk_live_alpha_123"},
    )

    # Tenant 2 store
    store.store_credentials(
        organization="org-beta",
        workspace="ws-billing",
        connector="conn-stripe",
        auth_type=AuthType.BEARER,
        secret_payload={"token": "sk_live_beta_999"},
    )

    # Resolve credentials accurately per tenant
    creds_alpha = store.resolve_credentials("org-alpha", "ws-finance", "conn-stripe")
    creds_beta = store.resolve_credentials("org-beta", "ws-billing", "conn-stripe")

    assert creds_alpha["token"] == "sk_live_alpha_123"
    assert creds_beta["token"] == "sk_live_beta_999"

    # Non-existent tenant lookup raises error
    with pytest.raises(CredentialNotFoundError):
        store.resolve_credentials("org-gamma", "ws-unknown", "conn-stripe")

    # Rotation
    store.rotate_credentials(
        organization="org-alpha",
        workspace="ws-finance",
        connector="conn-stripe",
        new_secret_payload={"token": "sk_live_alpha_rotated"},
    )
    assert store.resolve_credentials("org-alpha", "ws-finance", "conn-stripe")["token"] == "sk_live_alpha_rotated"

    # Revocation
    assert store.revoke_credentials("org-alpha", "ws-finance", "conn-stripe") is True
    with pytest.raises(CredentialNotFoundError):
        store.resolve_credentials("org-alpha", "ws-finance", "conn-stripe")


def test_authentication_manager_headers_and_refresh():
    store = CredentialStore()
    auth_mgr = AuthenticationManager(store)

    # Bearer Header
    bearer_headers = auth_mgr.build_auth_headers(AuthType.BEARER, {"token": "my_jwt_token"})
    assert bearer_headers["Authorization"] == "Bearer my_jwt_token"

    # API Key Header
    api_headers = auth_mgr.build_auth_headers(AuthType.API_KEY, {"api_key": "key-12345", "header_name": "X-Custom-Key"})
    assert api_headers["X-Custom-Key"] == "key-12345"

    # Basic Auth Header
    basic_headers = auth_mgr.build_auth_headers(AuthType.BASIC, {"username": "admin", "password": "password123"})
    assert "Authorization" in basic_headers
    assert basic_headers["Authorization"].startswith("Basic ")

    # OAuth refresh flow
    store.store_credentials(
        organization="org-1",
        workspace="ws-1",
        connector="conn-hubspot",
        auth_type=AuthType.OAUTH2,
        secret_payload={"access_token": "old_tok", "refresh_token": "ref_tok_123"},
    )
    refreshed = auth_mgr.refresh_oauth_token("org-1", "ws-1", "conn-hubspot")
    assert refreshed["access_token"].startswith("refreshed_tok_")
