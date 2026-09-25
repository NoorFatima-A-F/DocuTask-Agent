"""
Vector Embedding Abstraction.
Defines VectorEmbedding model and BaseEmbeddingProvider contract.
Supports Vertex AI Embeddings, Gemini Embeddings, OpenAI Embeddings, and local models.
"""

from abc import ABC, abstractmethod
from typing import List
from pydantic import BaseModel, Field


class VectorEmbedding(BaseModel):
    """Dense vector embedding representation."""

    vector: List[float] = Field(default_factory=list)
    dimension: int = Field(default=768, ge=1)
    model_name: str = Field(default="text-embedding-004")

    model_config = {"frozen": True}


class BaseEmbeddingProvider(ABC):
    """Abstract Base Class for Embedding Providers."""

    @abstractmethod
    async def generate_embedding(self, text: str) -> VectorEmbedding:
        """Generates dense vector embedding for input text."""
        pass
