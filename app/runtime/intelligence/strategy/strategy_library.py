"""
Strategy Library for Phase 10 (AISLCOP).

Provides search, retrieval, ranking, and promotion management for mined execution strategies.
"""

from __future__ import annotations

import time
from typing import Any, Dict, List, Optional

from app.runtime.intelligence.strategy.strategy_model import ExecutionStrategy


class StrategyLibrary:
    """
    Catalog of mined and promoted execution strategies.
    """

    def __init__(self):
        self._strategies: Dict[str, ExecutionStrategy] = {}
        self._domain_index: Dict[str, List[str]] = {}
        self._promoted_index: Dict[str, str] = {}  # domain -> active promoted strategy_id

    def register_strategy(self, strategy: ExecutionStrategy) -> str:
        self._strategies[strategy.strategy_id] = strategy
        
        domain = strategy.document_domain
        if domain not in self._domain_index:
            self._domain_index[domain] = []
        if strategy.strategy_id not in self._domain_index[domain]:
            self._domain_index[domain].append(strategy.strategy_id)
            
        if strategy.is_promoted:
            self._promoted_index[domain] = strategy.strategy_id

        return strategy.strategy_id

    def get(self, strategy_id: str) -> Optional[ExecutionStrategy]:
        return self._strategies.get(strategy_id)

    def get_active_strategy(self, domain: str) -> Optional[ExecutionStrategy]:
        """Returns the promoted strategy for a domain, or highest-ranking candidate."""
        if domain in self._promoted_index:
            return self._strategies.get(self._promoted_index[domain])
        candidates = self.find_strategies(domain=domain)
        return candidates[0] if candidates else None

    def promote_strategy(self, strategy_id: str) -> bool:
        """Promote a strategy to active status after experimental verification."""
        strategy = self._strategies.get(strategy_id)
        if not strategy:
            return False

        # Demote current active if any
        domain = strategy.document_domain
        current_promoted_id = self._promoted_index.get(domain)
        if current_promoted_id and current_promoted_id in self._strategies:
            self._strategies[current_promoted_id].is_promoted = False

        strategy.is_promoted = True
        strategy.updated_at = time.time()
        self._promoted_index[domain] = strategy_id
        return True

    def find_strategies(
        self,
        domain: Optional[str] = None,
        min_success_rate: float = 0.0,
        promoted_only: bool = False,
    ) -> List[ExecutionStrategy]:
        results: List[ExecutionStrategy] = []
        candidates = self._strategies.values()

        for s in candidates:
            if domain and s.document_domain.lower() != domain.lower():
                continue
            if s.observed_success_rate < min_success_rate:
                continue
            if promoted_only and not s.is_promoted:
                continue
            results.append(s)

        # Sort by observed success rate desc, then latency mean asc
        return sorted(results, key=lambda s: (-s.observed_success_rate, s.latency_profile.mean))

    def list_all(self) -> List[ExecutionStrategy]:
        return list(self._strategies.values())

    def count(self) -> int:
        return len(self._strategies)
