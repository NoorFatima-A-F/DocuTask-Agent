"""Platform Configuration Management Package."""
from .validation import SecretReferenceResolver
from .versions import VersionedConfiguration

__all__ = [
    "VersionedConfiguration",
    "SecretReferenceResolver",
]
