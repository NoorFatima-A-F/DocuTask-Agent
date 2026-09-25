"""Cryptographic Content-Addressing and Digest Utilities."""
import hashlib
import re


class DigestCalculator:
    """Calculates and validates standard OCI content digests."""

    DIGEST_REGEX = re.compile(r"^(sha256|sha512):[a-f0-9]{64,128}$")

    @classmethod
    def calculate_sha256(cls, data: bytes) -> str:
        """Computes standardized sha256:... digest string."""
        h = hashlib.sha256(data).hexdigest()
        return f"sha256:{h}"

    @classmethod
    def validate_digest_format(cls, digest: str) -> bool:
        """Validates that digest follows standard algorithm:hash format."""
        return bool(cls.DIGEST_REGEX.match(digest.strip()))

    @classmethod
    def verify_content(cls, data: bytes, expected_digest: str) -> bool:
        """Verifies binary content against an expected digest."""
        if not cls.validate_digest_format(expected_digest):
            return False
        algo, exp_hash = expected_digest.split(":", 1)
        if algo == "sha256":
            actual_hash = hashlib.sha256(data).hexdigest()
        elif algo == "sha512":
            actual_hash = hashlib.sha512(data).hexdigest()
        else:
            return False
        return actual_hash.lower() == exp_hash.lower()
