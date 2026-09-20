"""
Semantic Vector Intelligence Engine
Embeddings, vector indexing, similarity search, and hybrid BM25 + semantic retrieval with RBAC filtering.
"""
import math
from typing import List, Dict, Any, Tuple
from ..models.schemas import KnowledgeAsset, RetrievedSnippet, SecurityClassification, KnowledgeLifecycleState

class SemanticVectorEngine:
    def __init__(self):
        # In-memory vector index mapped to asset_id
        self._index: Dict[str, Dict[str, Any]] = {}

    def _generate_mock_embedding(self, text: str) -> List[float]:
        # Deterministic lightweight pseudo-embedding vector of 16 dimensions
        words = text.lower().split()
        vector = [0.0] * 16
        for i, word in enumerate(words):
            val = sum(ord(c) for c in word) % 100 / 100.0
            vector[i % 16] += val
        # Normalize
        norm = math.sqrt(sum(x*x for x in vector)) or 1.0
        return [round(x / norm, 4) for x in vector]

    def index_asset(self, asset: KnowledgeAsset):
        text = f"{asset.name} {asset.processed_content}"
        vector = self._generate_mock_embedding(text)
        self._index[asset.id] = {
            "asset": asset,
            "vector": vector,
            "keywords": set(text.lower().split())
        }
        asset.state = KnowledgeLifecycleState.AVAILABLE

    def cosine_similarity(self, v1: List[float], v2: List[float]) -> float:
        dot = sum(a * b for a, b in zip(v1, v2))
        return max(0.0, min(1.0, dot))

    def hybrid_search(
        self,
        tenant_id: str,
        query: str,
        top_k: int = 5,
        user_clearance: SecurityClassification = SecurityClassification.CONFIDENTIAL,
        user_roles: List[str] = None,
        filter_tags: List[str] = None
    ) -> List[RetrievedSnippet]:
        user_roles = user_roles or ["member"]
        filter_tags = filter_tags or []
        
        query_vec = self._generate_mock_embedding(query)
        query_tokens = set(query.lower().split())
        
        clearance_hierarchy = {
            SecurityClassification.PUBLIC: 1,
            SecurityClassification.INTERNAL: 2,
            SecurityClassification.CONFIDENTIAL: 3,
            SecurityClassification.RESTRICTED: 4,
            SecurityClassification.STRICT_SECRET: 5,
        }
        user_level = clearance_hierarchy.get(user_clearance, 2)
        
        ranked_results: List[Tuple[float, KnowledgeAsset, str]] = []
        
        for item in self._index.values():
            asset: KnowledgeAsset = item["asset"]
            if asset.tenant_id != tenant_id:
                continue
            
            # Security filter
            asset_level = clearance_hierarchy.get(asset.security_classification, 2)
            if asset_level > user_level:
                continue
            
            # Role check
            if asset.access_policy.allowed_roles and not any(r in asset.access_policy.allowed_roles for r in user_roles):
                continue
            
            # Tag check
            if filter_tags and not any(t in asset.metadata.custom_tags for t in filter_tags):
                continue
            
            # Semantic score
            semantic_score = self.cosine_similarity(query_vec, item["vector"])
            
            # Keyword overlap score
            overlap = len(query_tokens.intersection(item["keywords"]))
            keyword_score = min(1.0, overlap / (len(query_tokens) or 1.0))
            
            # Combined hybrid score (70% semantic, 30% keyword)
            hybrid_score = round(0.7 * semantic_score + 0.3 * keyword_score, 4)
            
            if hybrid_score > 0.05 or overlap > 0:
                matched_via = "HYBRID_SEMANTIC" if semantic_score > 0.3 and keyword_score > 0.2 else ("KEYWORD" if keyword_score > semantic_score else "SEMANTIC")
                ranked_results.append((hybrid_score, asset, matched_via))
                
        ranked_results.sort(key=lambda x: x[0], reverse=True)
        
        snippets = []
        for score, asset, match_type in ranked_results[:top_k]:
            content_snippet = asset.processed_content[:300] + ("..." if len(asset.processed_content) > 300 else "")
            snippets.append(RetrievedSnippet(
                asset_id=asset.id,
                title=asset.name,
                content=content_snippet,
                score=score,
                source_type=asset.source_type,
                security_classification=asset.security_classification,
                matched_via=match_type
            ))
        return snippets
