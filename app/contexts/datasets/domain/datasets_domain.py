from dataclasses import dataclass
from app.shared_kernel import BaseEntity, DomainEvent

@dataclass
class DatasetRegistered(DomainEvent):
    dataset_id: str = ""
    category: str = ""
    sha256: str = ""

@dataclass
class DatasetAggregate(BaseEntity):
    name: str = ""
    category: str = "GOLDEN"
    sha256_checksum: str = ""
    size_bytes: int = 0
