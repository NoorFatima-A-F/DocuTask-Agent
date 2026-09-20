"""Review Evidence Package for Human Decision-Makers."""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timezone
import uuid


class SourceCitation(BaseModel):
    source_id: str
    document_name: str
    snippet: str
    confidence: float = 1.0
    location: Optional[str] = None


class ReviewEvidencePackage(BaseModel):
    """Immutable, comprehensive evidence package for transparent human decision-making."""
    package_id: str = Field(default_factory=lambda: f"evd_{uuid.uuid4().hex[:10]}")
    review_id: str
    tenant_id: str
    
    # AI Decision Summary & Explanation
    action_type: str
    proposed_output: Any
    explanation: Optional[str] = None
    reasoning_summary: Optional[str] = None
    
    # Quantitative Risk & Quality Scores
    risk_score: float = 0.0
    confidence_score: float = 1.0
    grounding_score: Optional[float] = 1.0
    trust_score: float = 1.0
    
    # Provenance & Lineage
    model_id: Optional[str] = None
    prompt_id: Optional[str] = None
    prompt_version: Optional[str] = None
    data_classification: str = "INTERNAL"
    
    # Knowledge & Grounding Citations
    citations: List[SourceCitation] = Field(default_factory=list)
    
    # Policy and Safety Evidence
    triggered_policies: List[str] = Field(default_factory=list)
    safety_checks_passed: List[str] = Field(default_factory=list)
    safety_flags: List[str] = Field(default_factory=list)
    
    # Timing & Metadata
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    raw_payload_hash: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
