"""Data Catalog Indexing Engine (Phase 8B)."""

from __future__ import annotations

from typing import Dict, Set
from app.data_governance.registry.models import DataAsset


class CatalogIndex:
    """Inverted and faceted index for fast enterprise catalog lookups."""

    def __init__(self):
        # term -> Set[asset_id]
        self._keyword_index: Dict[str, Set[str]] = {}
        # facet_name -> (facet_value -> Set[asset_id])
        self._facets: Dict[str, Dict[str, Set[str]]] = {
            "classification": {},
            "asset_type": {},
            "department": {},
            "owner": {},
            "source": {},
        }

    def index_asset(self, asset: DataAsset) -> None:
        """Index a data asset into keyword and facet stores."""
        # Index keywords
        text = f"{asset.name} {asset.source} {asset.mime_type} {' '.join(asset.compliance_tags)}".lower()
        for token in text.split():
            clean = token.strip(".,;:\"'()")
            if len(clean) > 2:
                if clean not in self._keyword_index:
                    self._keyword_index[clean] = set()
                self._keyword_index[clean].add(asset.asset_id)

        # Index facets
        self._add_facet("classification", asset.classification.value, asset.asset_id)
        self._add_facet("asset_type", asset.asset_type.value, asset.asset_id)
        self._add_facet("department", asset.owner.department, asset.asset_id)
        self._add_facet("owner", asset.owner.owner_user_id, asset.asset_id)
        self._add_facet("source", asset.source, asset.asset_id)

    def _add_facet(self, facet_name: str, facet_value: str, asset_id: str) -> None:
        if facet_name not in self._facets:
            self._facets[facet_name] = {}
        if facet_value not in self._facets[facet_name]:
            self._facets[facet_name][facet_value] = set()
        self._facets[facet_name][facet_value].add(asset_id)

    def search_keywords(self, query: str) -> Set[str]:
        """Find matching asset IDs for search terms."""
        tokens = query.lower().split()
        if not tokens:
            return set()

        matches = None
        for token in tokens:
            token_matches = self._keyword_index.get(token, set())
            if matches is None:
                matches = set(token_matches)
            else:
                matches &= token_matches
        return matches or set()
