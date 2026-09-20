"""
Enterprise Multi-Agent Intelligence Platform (EMAIP) - Context Engine.
Manages cognitive context construction, compression, relevance ranking,
and token window budgeting.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import json
import logging

logger = logging.getLogger(__name__)


@dataclass
class CognitiveContext:
    """
    Rich structured context container supplied to LLMs, reasoning frameworks,
    and worker agents.
    """
    goal: Dict[str, Any] = field(default_factory=dict)
    workflow_id: Optional[str] = None
    history: List[Dict[str, Any]] = field(default_factory=list)
    memory: List[Dict[str, Any]] = field(default_factory=list)
    policies: List[str] = field(default_factory=list)
    permissions: List[str] = field(default_factory=list)
    budget: Dict[str, Any] = field(default_factory=dict)
    time_remaining_seconds: float = 300.0
    current_state: str = "INITIALIZED"
    previous_results: Dict[str, Any] = field(default_factory=dict)
    estimated_token_count: int = 0
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "goal": self.goal,
            "workflow_id": self.workflow_id,
            "history": self.history,
            "memory": self.memory,
            "policies": self.policies,
            "permissions": self.permissions,
            "budget": self.budget,
            "time_remaining_seconds": self.time_remaining_seconds,
            "current_state": self.current_state,
            "previous_results": self.previous_results,
            "estimated_token_count": self.estimated_token_count,
            "created_at": self.created_at.isoformat(),
        }


class ContextManager:
    """
    Context Engine responsible for assembling, compressing, ranking,
    and budgeting cognitive context across agent turns.
    """

    def __init__(self, max_token_limit: int = 8000):
        self.max_token_limit = max_token_limit

    def estimate_tokens(self, text_or_dict: Any) -> int:
        """Heuristic token estimation: ~4 chars per token."""
        if isinstance(text_or_dict, str):
            text = text_or_dict
        else:
            text = json.dumps(text_or_dict, default=str)
        return max(1, len(text) // 4)

    def build_context(
        self,
        goal: Dict[str, Any],
        workflow_id: Optional[str] = None,
        history: Optional[List[Dict[str, Any]]] = None,
        memory: Optional[List[Dict[str, Any]]] = None,
        policies: Optional[List[str]] = None,
        permissions: Optional[List[str]] = None,
        budget: Optional[Dict[str, Any]] = None,
        time_remaining_seconds: float = 300.0,
        current_state: str = "INITIALIZED",
        previous_results: Optional[Dict[str, Any]] = None,
    ) -> CognitiveContext:
        """
        Constructs and bounds a CognitiveContext container, compressing contents
        if the estimated token count exceeds the configured token budget.
        """
        raw_history = list(history or [])
        raw_memory = list(memory or [])

        context = CognitiveContext(
            goal=goal,
            workflow_id=workflow_id,
            history=raw_history,
            memory=raw_memory,
            policies=policies or ["enterprise_default"],
            permissions=permissions or ["standard"],
            budget=budget or {"max_tokens": self.max_token_limit},
            time_remaining_seconds=time_remaining_seconds,
            current_state=current_state,
            previous_results=previous_results or {},
        )

        context.estimated_token_count = self.estimate_tokens(context.to_dict())

        # If token count exceeds budget, compress
        if context.estimated_token_count > self.max_token_limit:
            context = self.compress_context(context)

        return context

    def compress_context(self, context: CognitiveContext) -> CognitiveContext:
        """
        Compresses context by truncating older history entries and summarizing
        memory records to fit within token boundaries.
        """
        compressed_history = context.history[-5:] if len(context.history) > 5 else context.history
        compressed_memory = context.memory[:3] if len(context.memory) > 3 else context.memory

        compressed = CognitiveContext(
            goal=context.goal,
            workflow_id=context.workflow_id,
            history=compressed_history,
            memory=compressed_memory,
            policies=context.policies,
            permissions=context.permissions,
            budget=context.budget,
            time_remaining_seconds=context.time_remaining_seconds,
            current_state=context.current_state,
            previous_results=context.previous_results,
        )
        compressed.estimated_token_count = self.estimate_tokens(compressed.to_dict())
        logger.info(
            f"Context compressed from {context.estimated_token_count} to "
            f"{compressed.estimated_token_count} tokens"
        )
        return compressed

    def rank_relevance(self, query: str, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Ranks context or memory items by keyword/relevance match against query.
        """
        query_words = set(query.lower().split())

        def score_item(item: Dict[str, Any]) -> int:
            text = json.dumps(item).lower()
            return sum(1 for w in query_words if w in text)

        return sorted(items, key=score_item, reverse=True)
