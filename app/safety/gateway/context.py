"""Safety Execution Context & Source Trust Models."""

from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timezone
import uuid


class SourceTrustLevel(str, Enum):
    """Trust tier of the input or document source."""
    SYSTEM = "SYSTEM"                  # Core system prompt / platform trusted (highest)
    DEVELOPER = "DEVELOPER"            # Developer configuration / verified template
    ORGANIZATION = "ORGANIZATION"      # Authenticated internal organization knowledge
    USER = "USER"                      # Authenticated end-user prompt
    DOCUMENT = "DOCUMENT"              # Parsed third-party document / PDF / OCR output
    EXTERNAL = "EXTERNAL"              # External web page / third-party API / email
    UNKNOWN = "UNKNOWN"                # Untrusted / unauthenticated origin (lowest)


class ModelContext(BaseModel):
    """Model information for safety evaluation."""
    model_id: str
    model_name: Optional[str] = None
    provider: Optional[str] = None
    risk_tier: Optional[str] = "LOW"
    capabilities: List[str] = Field(default_factory=list)
    temperature: Optional[float] = 0.7


class PromptContext(BaseModel):
    """Prompt information for safety evaluation."""
    prompt_id: Optional[str] = None
    version_id: Optional[str] = None
    template_name: Optional[str] = None
    variables: Dict[str, Any] = Field(default_factory=dict)
    system_prompt: Optional[str] = None


class ToolContext(BaseModel):
    """Tool invocation context for safety sandboxing."""
    tool_name: str
    tool_id: Optional[str] = None
    danger_level: Optional[str] = "SAFE_READ"
    parameters: Dict[str, Any] = Field(default_factory=dict)
    is_dry_run: bool = False


class DataContext(BaseModel):
    """Data sensitivity and classification context."""
    asset_id: Optional[str] = None
    data_classification: Optional[str] = "INTERNAL"
    pii_types_detected: List[str] = Field(default_factory=list)
    compliance_tags: List[str] = Field(default_factory=list)


class KnowledgeChunk(BaseModel):
    """Retrieved knowledge/RAG chunk with trust level."""
    chunk_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    content: str
    source_name: Optional[str] = None
    source_type: Optional[str] = "DOCUMENT"
    trust_level: SourceTrustLevel = SourceTrustLevel.DOCUMENT
    metadata: Dict[str, Any] = Field(default_factory=dict)


class SafetyContext(BaseModel):
    """Comprehensive request context for all AI safety pipeline stages."""
    context_id: str = Field(default_factory=lambda: f"ctx_{uuid.uuid4().hex[:12]}")
    tenant_id: str
    user_id: Optional[str] = None
    agent_id: Optional[str] = None
    session_id: Optional[str] = None
    
    # Input content
    raw_input: str = ""
    processed_input: Optional[str] = None
    source_trust: SourceTrustLevel = SourceTrustLevel.USER
    
    # Sub-contexts
    model_context: Optional[ModelContext] = None
    prompt_context: Optional[PromptContext] = None
    tool_contexts: List[ToolContext] = Field(default_factory=list)
    data_context: Optional[DataContext] = None
    knowledge_chunks: List[KnowledgeChunk] = Field(default_factory=list)
    
    # Output content (for post-execution)
    generated_output: Optional[str] = None
    sanitized_output: Optional[str] = None
    
    # Execution metadata
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = Field(default_factory=dict)
