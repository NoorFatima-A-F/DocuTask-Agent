"""
Automated Pytest Suite for Enterprise Architecture Refactoring & Infrastructure Hardening.
"""

import pytest
from app.core.security import validate_secret_key_strength


def test_secret_management_validation():
    """Verifies secret key strength validator enforcing >= 32 chars and rejecting weak strings."""
    valid_key = "a_very_secure_and_long_jwt_secret_key_string_32_chars_min"
    assert validate_secret_key_strength(valid_key) is True

    # Short secret rejection
    with pytest.raises(ValueError):
        validate_secret_key_strength("short_key_123")

    # Prohibited key rejection
    with pytest.raises(ValueError):
        validate_secret_key_strength("changeme")
