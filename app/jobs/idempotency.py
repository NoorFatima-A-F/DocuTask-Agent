from app.core.security import sanitize_log_input
"""
Idempotency Engine Module.
Guarantees deduplication across uploads, OCR, AI extraction, and DB writes using cryptographic keys.
"""

import hashlib
from typing import Optional
from app.core.logging import logger


class IdempotencyEngine:
    """Engine generating and validating processing idempotency keys."""

    DEFAULT_PROCESSING_VERSION = "v1.0"

    @classmethod
    def generate_key(cls, document_hash: str, processing_version: Optional[str] = None) -> str:
        """
        Generates SHA-256 idempotency key: SHA256(document_hash + processing_version).
        """
        version = processing_version or cls.DEFAULT_PROCESSING_VERSION
        raw_key = f"{document_hash}:{version}"
        idempotency_key = hashlib.sha256(raw_key.encode("utf-8")).hexdigest()
        logger.debug("Generated Idempotency Key: '%s...' for doc hash '%s...'", sanitize_log_input(idempotency_key[:16]), sanitize_log_input(document_hash[:8]))
        return idempotency_key
