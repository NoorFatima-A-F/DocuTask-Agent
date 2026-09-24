"""
Enterprise Secrets Management & Tamper-Evident Audit Log Test Suite.
Validates:
- Secret retrieval via environment and in-memory vault providers
- Default fallback resolution
- Append-only audit logging with SHA-256 hash chaining
- Audit log integrity verification
- Cryptographic tamper detection when history is modified
"""

import pytest
from app.agents.runtime.enterprise.audit_event import AuditEventType
from app.agents.runtime.enterprise.audit_log import ImmutableRuntimeAuditLog
from app.agents.runtime.enterprise.secret_manager import (
    InMemorySecretProvider,
    SecretManager,
)


def test_secret_manager_in_memory_and_fallback():
    provider = InMemorySecretProvider({"DB_PASSWORD": "super-secure-password"})
    sm = SecretManager(primary_provider=provider)

    assert sm.get_secret("DB_PASSWORD") == "super-secure-password"
    assert sm.get_secret("NON_EXISTENT") is None
    assert sm.get_secret("NON_EXISTENT", default="fallback-val") == "fallback-val"


def test_audit_log_hash_chain_integrity():
    log = ImmutableRuntimeAuditLog()

    e1 = log.append(
        event_type=AuditEventType.RUNTIME_LIFECYCLE,
        actor="system",
        details={"version": "23.0"},
        tenant_id="platform",
    )
    assert e1.prev_hash == ImmutableRuntimeAuditLog.GENESIS_HASH
    assert e1.event_hash

    e2 = log.append(
        event_type=AuditEventType.PLUGIN_MODIFICATION,
        actor="admin@example.com",
        details={"plugin": "ocr"},
        tenant_id="tenant-1",
    )
    assert e2.prev_hash == e1.event_hash

    e3 = log.append(
        event_type=AuditEventType.TENANT_ACTION,
        actor="superadmin",
        details={"tokens": 500000},
        tenant_id="tenant-1",
    )
    assert e3.prev_hash == e2.event_hash

    # Integrity verification must pass
    assert log.verify_integrity()
    assert len(log.list_events()) == 3


def test_audit_log_tamper_detection():
    log = ImmutableRuntimeAuditLog()

    log.append(AuditEventType.SECURITY_VIOLATION, "guard", {"threat": "low"})
    log.append(AuditEventType.RUNTIME_LIFECYCLE, "system", {"clean": True})

    assert log.verify_integrity()

    # Tamper with internal event details
    events = log._events
    # Create tampered copy modifying details
    tampered_event = events[0].model_copy(update={"details": {"threat": "NONE"}})
    events[0] = tampered_event

    # Cryptographic integrity check MUST fail!
    assert not log.verify_integrity()


def test_secret_rotation_and_versioning():

    vault = InMemorySecretProvider()
    sm = SecretManager(primary_provider=vault)

    # Initial version 1
    v1 = sm.rotate_secret("API_KEY", "key_v1")
    assert v1 == 1
    assert sm.get_secret("API_KEY") == "key_v1"
    assert sm.get_secret("API_KEY", version=1) == "key_v1"

    # Rotate to version 2
    v2 = sm.rotate_secret("API_KEY", "key_v2")
    assert v2 == 2
    # Default gets latest version
    assert sm.get_secret("API_KEY") == "key_v2"
    # Specific version still accessible
    assert sm.get_secret("API_KEY", version=1) == "key_v1"

    # Audit records tracked
    assert len(sm.audit_logs) >= 4


def test_secret_expiration_and_revocation():
    import time
    from app.agents.runtime.enterprise.secret_manager import SecretExpiredError, SecretRevokedError

    vault = InMemorySecretProvider()
    sm = SecretManager(primary_provider=vault)

    # Secret expiring in 0.05s
    sm.rotate_secret("TEMP_TOKEN", "token_123", ttl_seconds=0.05)
    assert sm.get_secret("TEMP_TOKEN") == "token_123"

    time.sleep(0.07)
    with pytest.raises(SecretExpiredError):
        sm.get_secret("TEMP_TOKEN")

    # Revocation test
    sm.rotate_secret("REVOKABLE_KEY", "val_xyz")
    assert sm.get_secret("REVOKABLE_KEY") == "val_xyz"

    revoked = sm.revoke_secret("REVOKABLE_KEY")
    assert revoked is True

    with pytest.raises(SecretRevokedError):
        sm.get_secret("REVOKABLE_KEY")

