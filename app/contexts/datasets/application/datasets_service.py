from typing import Union
import hashlib
from ..domain.datasets_domain import DatasetAggregate, DatasetRegistered
from app.shared_kernel import Result, Ok, get_event_bus

class DatasetService:
    def __init__(self, repo):
        self.repo = repo

    async def register_dataset(self, dataset_id: str, name: str, category: str, content: Union[bytes, str]) -> Result[DatasetAggregate, str]:
        raw = content if isinstance(content, bytes) else content.encode("utf-8")
        h = hashlib.sha256(raw).hexdigest()
        agg = DatasetAggregate(id=dataset_id, name=name, category=category, sha256_checksum=h, size_bytes=len(raw))
        self.repo.save(agg)
        await get_event_bus().publish(DatasetRegistered(dataset_id=dataset_id, category=category, sha256=h))
        return Ok(agg)
