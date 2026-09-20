"""
Evidence Search & Discovery Index.
Queries artifacts across execution IDs, categories, and tags.
"""
from typing import Dict, List, Optional
from app.platform_verification.evidence_engine.domain.models import (
    EvidenceArtifact, EvidenceCategory
)
from app.platform_verification.evidence_engine.domain.interfaces import EvidenceSearchInterface
from app.platform_verification.evidence_engine.core.collector import evidence_collector


class EvidenceSearchIndex(EvidenceSearchInterface):
    def __init__(self):
        self._indexed: Dict[str, EvidenceArtifact] = {}

    def index_artifact(self, artifact: EvidenceArtifact) -> None:
        self._indexed[artifact.artifact_id] = artifact

    def search(self, query: str) -> List[EvidenceArtifact]:
        q = query.lower()
        results = []
        for a in self._indexed.values():
            if q in a.artifact_id.lower() or q in a.execution_id.lower() or q in a.category.value.lower():
                results.append(a)
        return results

    def search_artifacts(
        self,
        execution_id: Optional[str] = None,
        category: Optional[EvidenceCategory] = None
    ) -> List[EvidenceArtifact]:
        all_artifacts = list(self._indexed.values())
        if execution_id:
            all_artifacts = [a for a in all_artifacts if a.execution_id == execution_id]
        if category:
            all_artifacts = [a for a in all_artifacts if a.category == category]
        return all_artifacts


evidence_search_index = EvidenceSearchIndex()
