"""
Knowledge Index for Phase 13.5 (ARLP-KIP).
Inverted index providing fast token-based indexing for knowledge search.
"""

from typing import Dict, List, Set
from pydantic import BaseModel, Field


class SearchIndexEntry(BaseModel):
    token: str
    record_ids: List[str] = Field(default_factory=list)


class KnowledgeIndex:
    """
    Inverted index mapping tokens and categories to knowledge records.
    """

    def __init__(self):
        self._index: Dict[str, Set[str]] = {}

    def index_record(self, record_id: str, text: str, tags: List[str]):
        tokens = text.lower().split() + [t.lower() for t in tags]
        for t in tokens:
            clean = t.strip(".,:;!?()[]{}\"'")
            if len(clean) > 2:
                if clean not in self._index:
                    self._index[clean] = set()
                self._index[clean].add(record_id)

    def lookup(self, token: str) -> List[str]:
        return list(self._index.get(token.lower(), set()))


knowledge_index = KnowledgeIndex()
