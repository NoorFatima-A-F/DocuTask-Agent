"""
Enterprise Knowledge Fabric, Memory Intelligence & Retrieval Platform (EKF-MIRP) - Exceptions.
Provides typed, structured exceptions for knowledge management, lifecycle transitions,
embedding generation, vector retrieval, permissions, and graph operations.
"""

from typing import Any, Dict, Optional


class KnowledgeError(Exception):
    """Base exception for all knowledge fabric and memory platform errors."""

    def __init__(self, message: str, knowledge_id: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.knowledge_id = knowledge_id
        self.details = details or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "error_type": self.__class__.__name__,
            "message": self.message,
            "knowledge_id": self.knowledge_id,
            "details": self.details,
        }


class KnowledgeNotFoundError(KnowledgeError):
    """Raised when a requested knowledge object or document is not found."""
    pass


class InvalidKnowledgeStateError(KnowledgeError):
    """Raised when an illegal lifecycle transition is attempted on a knowledge object."""
    pass


class PermissionDeniedError(KnowledgeError):
    """Raised when user or agent lacks ACL permissions to access a knowledge resource."""
    pass


class ClassificationViolationError(KnowledgeError):
    """Raised when a knowledge request violates organizational security classification rules."""
    pass


class ChunkingError(KnowledgeError):
    """Raised when document parsing or chunk segmentation fails."""
    pass


class EmbeddingError(KnowledgeError):
    """Raised when text embedding computation fails on a provider backend."""
    pass


class VectorStoreError(KnowledgeError):
    """Raised when vector indexing, upserting, or similarity search fails."""
    pass


class RetrievalError(KnowledgeError):
    """Raised when hybrid retrieval or ranking fails."""
    pass


class IngestionError(KnowledgeError):
    """Raised when knowledge source ingestion or connector syncing fails."""
    pass


class KnowledgeGraphError(KnowledgeError):
    """Raised when entity extraction or relationship graph query fails."""
    pass
