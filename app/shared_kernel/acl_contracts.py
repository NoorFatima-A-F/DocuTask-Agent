"""
Anti-Corruption Layer (ACL) Provider Interfaces.
Stable contracts for third-party external boundaries (AI, OCR, Storage, Messaging, Embeddings).
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

@dataclass(frozen=True)
class AiPromptRequest:
    model: str
    prompt: str
    temperature: float = 0.0
    max_tokens: int = 2048
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass(frozen=True)
class AiInferenceResult:
    text: str
    tokens_used: int
    latency_ms: float
    model_version: str
    raw_response: Optional[Dict[str, Any]] = None

class AiProviderContract(ABC):
    @abstractmethod
    async def generate_response(self, request: AiPromptRequest) -> AiInferenceResult:
        pass

@dataclass(frozen=True)
class OcrRequest:
    document_bytes: bytes
    media_type: str = "application/pdf"
    language: str = "eng"

@dataclass(frozen=True)
class OcrExtractionData:
    extracted_text: str
    confidence: float
    latency_ms: float
    page_count: int

class OcrProviderContract(ABC):
    @abstractmethod
    async def extract_text(self, request: OcrRequest) -> OcrExtractionData:
        pass

class MessagingProviderContract(ABC):
    @abstractmethod
    async def publish_message(self, topic: str, message: str) -> bool:
        pass

class EmbeddingProviderContract(ABC):
    @abstractmethod
    async def embed_text(self, text: str) -> List[float]:
        pass

class VectorStoreContract(ABC):
    @abstractmethod
    async def query_nearest(self, vector: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        pass
