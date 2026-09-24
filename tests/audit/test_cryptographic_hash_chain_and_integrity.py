"""Tests for Cryptographic Hash Chaining, Digital Signatures, and Tamper Detection."""

from app.audit.core.events import AuditEvent
from app.audit.integrity.hashing import HashChainCalculator
from app.audit.integrity.signatures import AuditSigner
from app.audit.integrity.verification import AuditIntegrityVerifier
from app.audit.storage.immutable_store import ImmutableAuditStore


def test_hash_chain_calculation():
    calc = HashChainCalculator()
    event = AuditEvent(
        event_id="aud_1",
        event_type="auth.login",
        tenant_id="tenant_bank",
        actor_id="usr_admin",
        action="login",
        resource_type="auth",
        resource_id="session_1",
    )
    h1 = calc.compute_event_hash(event, previous_hash=HashChainCalculator.GENESIS_HASH)
    assert len(h1) == 64  # SHA-256 hex length

    # Determinism check
    h2 = calc.compute_event_hash(event, previous_hash=HashChainCalculator.GENESIS_HASH)
    assert h1 == h2


def test_audit_signer_signature_verification():
    signer = AuditSigner()
    sample_hash = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    sig = signer.sign_hash(sample_hash)
    assert signer.verify_signature(sample_hash, sig) is True
    assert signer.verify_signature("tampered_hash_value", sig) is False


def test_audit_integrity_verification_success():
    store = ImmutableAuditStore()
    verifier = AuditIntegrityVerifier(signer=store.signer)

    # Append 3 sequential events
    for i in range(3):
        store.append(
            AuditEvent(
                event_id=f"aud_seq_{i}",
                event_type="document.process",
                tenant_id="tenant_audit",
                actor_id="user_1",
                action="process",
                resource_type="document",
                resource_id=f"doc_{i}",
            )
        )

    events = store.get_tenant_events("tenant_audit")
    assert len(events) == 3
    result = verifier.verify_chain(events)
    assert result.is_valid is True
    assert result.total_events_checked == 3
    assert len(result.tampered_event_ids) == 0


def test_audit_integrity_verification_detects_tampering():
    store = ImmutableAuditStore()
    verifier = AuditIntegrityVerifier(signer=store.signer)

    for i in range(3):
        store.append(
            AuditEvent(
                event_id=f"aud_tamper_{i}",
                event_type="document.process",
                tenant_id="tenant_tamper",
                actor_id="user_1",
                action="process",
                resource_type="document",
                resource_id=f"doc_{i}",
            )
        )

    events = store.get_tenant_events("tenant_tamper")
    
    # Tamper with the 2nd event payload
    events[1].action = "MALICIOUS_TAMPERED_ACTION"
    
    result = verifier.verify_chain(events)
    assert result.is_valid is False
    assert "aud_tamper_1" in result.tampered_event_ids
