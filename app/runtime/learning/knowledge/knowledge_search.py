"""
Knowledge Search Engine for Phase 13.5 (ARLP-KIP).
Performs hybrid full-text and semantic keyword searches across indexed knowledge records.
"""

from typing import Dict, Any, List
from pydantic import BaseModel, Field

from app.runtime.learning.knowledge.knowledge_registry import knowledge_registry, KnowledgeRecord


class SearchMatch(BaseModel):
    record: KnowledgeRecord
    score: float
    matched_terms: List[str] = Field(default_factory=list)


class KnowledgeSearchEngine:
    """
    Search engine ranking knowledge records by keyword relevance and confidence weights.
    """

    @classmethod
    def search(cls, query: str) -> List[SearchMatch]:
        terms = [q.lower().strip() for q in query.split() if len(q.strip()) > 0]
        records = knowledge_registry.list_records()
        matches: List[SearchMatch] = []

        for r in records:
            matched_terms = []
            title_lower = r.title.lower()
            tags_lower = [t.lower() for t in r.tags]
            cat_lower = r.category.lower()

            for t in terms:
                if t in title_lower or t in tags_lower or t in cat_lower:
                    matched_terms.append(t)

            if matched_terms or not terms:
                term_score = len(matched_terms) / max(len(terms), 1) if terms else 1.0
                score = round(term_score * 0.7 + r.confidence_score * 0.3, 3)
                matches.append(SearchMatch(record=r, score=score, matched_terms=matched_terms))

        matches.sort(key=lambda m: m.score, reverse=True)
        return matches


knowledge_search_engine = KnowledgeSearchEngine()
