"""
Neutral File and Storage Contracts.
Standardizes storage abstractions for Evidence, Datasets, Artifacts, and Snapshots without cloud SDK coupling.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Dict, Any, AsyncIterator

class StorageType(str, Enum):
    ARTIFACT = "ARTIFACT"
    EVIDENCE = "EVIDENCE"
    DATASET = "DATASET"
    SNAPSHOT = "SNAPSHOT"
    TEMPORARY = "TEMPORARY"

@dataclass(frozen=True)
class FileMetadata:
    storage_key: str
    size_bytes: int
    sha256_hash: str
    media_type: str = "application/octet-stream"
    metadata: Dict[str, Any] = field(default_factory=dict)

class FileStorageContract(ABC):
    @abstractmethod
    async def put(self, key: str, data: bytes, media_type: str = "application/octet-stream") -> FileMetadata:
        pass

    @abstractmethod
    async def get(self, key: str) -> Optional[bytes]:
        pass

    @abstractmethod
    async def exists(self, key: str) -> bool:
        pass

    @abstractmethod
    async def delete(self, key: str) -> bool:
        pass

class ArtifactStorageContract(FileStorageContract):
    pass

class EvidenceStorageContract(FileStorageContract):
    pass

class DatasetStorageContract(FileStorageContract):
    pass

class TemporaryStorageContract(FileStorageContract):
    pass
