"""
Content-Addressable Storage (CAS) Adapter.
"""
import hashlib
from typing import Optional, Dict
from pathlib import Path

class ContentAddressableStore:
    def __init__(self, base_path: Optional[Path] = None):
        self._base_path = base_path or Path("./evidence")
        self._memory_store: Dict[str, bytes] = {}

    def put(self, content: bytes) -> str:
        h = hashlib.sha256(content).hexdigest()
        self._memory_store[h] = content
        return h

    def get(self, content_hash: str) -> Optional[bytes]:
        return self._memory_store.get(content_hash)

    def exists(self, content_hash: str) -> bool:
        return content_hash in self._memory_store
