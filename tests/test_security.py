"""
Unit Tests for Core Security & Cryptography Module.
"""

from datetime import timedelta
import pytest
from app.core.exceptions import TokenException
from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    hash_token,
    verify_password,
)


def test_password_hashing_and_verification():
    """Verifies bcrypt hashing and password verification."""
    password = "TestPassword123!"
    hashed = hash_password(password)
    
    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("WrongPassword123!", hashed) is False


def test_access_token_creation_and_decoding():
    """Verifies JWT access token generation and payload decoding."""
    subject = "user_12345"
    token = create_access_token(subject=subject, expires_delta=timedelta(minutes=15))
    
    payload = decode_token(token, expected_type="access")
    assert payload["sub"] == subject
    assert payload["type"] == "access"


def test_refresh_token_creation_and_decoding():
    """Verifies JWT refresh token generation and expiration calculation."""
    subject = "user_67890"
    raw_token, expires_at = create_refresh_token(subject=subject, expires_delta=timedelta(days=1))
    
    payload = decode_token(raw_token, expected_type="refresh")
    assert payload["sub"] == subject
    assert payload["type"] == "refresh"


def test_token_type_mismatch():
    """Verifies TokenException raised when expecting access token but presented refresh token."""
    subject = "user_mismatch"
    refresh_token, _ = create_refresh_token(subject=subject)
    
    with pytest.raises(TokenException) as exc_info:
        decode_token(refresh_token, expected_type="access")
    assert "Invalid token type" in str(exc_info.value)


def test_invalid_token_decoding():
    """Verifies TokenException raised for malformed tokens."""
    with pytest.raises(TokenException):
        decode_token("invalid.token.structure", expected_type="access")


def test_token_hashing():
    """Verifies SHA-256 token hashing produces consistent deterministic output."""
    raw_token = "some_random_jwt_string"
    hash1 = hash_token(raw_token)
    hash2 = hash_token(raw_token)
    
    assert hash1 == hash2
    assert len(hash1) == 64
