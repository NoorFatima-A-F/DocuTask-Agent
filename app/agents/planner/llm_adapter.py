"""
LLM Planning Adapter Abstraction.
Decouples Planner from Gemini, Vertex AI, or any other LLM provider.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List
from app.agents.planner.context import PlannerRequest


class ILLMPlanningAdapter(ABC):
    """Abstract LLM adapter interface for cognitive planning."""

    @abstractmethod
    async def generate_decomposition(self, prompt: str) -> Dict[str, Any]:
        """Generates raw task decomposition proposals via LLM."""
        pass

    @abstractmethod
    async def rank_candidates(self, prompt: str) -> List[float]:
        """Ranks candidate plans via LLM reflection."""
        pass


class MockLLMPlanningAdapter(ILLMPlanningAdapter):
    """Mock LLM adapter for deterministic planning synthesis and unit testing."""

    async def generate_decomposition(self, prompt: str) -> Dict[str, Any]:
        return {
            "tasks": [
                {"id": "t1_ocr", "name": "OCR Text Extraction", "capability": "OCR", "duration": 5.0},
                {"id": "t2_extract", "name": "LLM Entity Extraction", "capability": "LLM", "duration": 10.0},
                {"id": "t3_validate", "name": "Compliance Check", "capability": "DECISION", "duration": 2.0}
            ]
        }

    async def rank_candidates(self, prompt: str) -> List[float]:
        return [0.95, 0.85]
