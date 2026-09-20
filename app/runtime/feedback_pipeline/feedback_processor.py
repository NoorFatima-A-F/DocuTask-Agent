"""
ARTEICP Feedback Pipeline - Feedback Processor
Ingests field-level human corrections and extracts structured error vectors.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict, field
import uuid
import time


@dataclass
class HumanFeedbackRecord:
    feedback_id: str
    document_id: str
    field_name: str
    extracted_value: str
    corrected_value: str
    confidence_was: float
    model_was: str
    submitted_by: str
    status: str  # INGESTED | REFLECTING | SIMULATING | GOVERNED | COMMITTED_TO_MEMORY
    created_at: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class FeedbackProcessor:
    """Ingests human annotations and initiates closed-loop reflection."""

    def __init__(self):
        self.feedbacks: Dict[str, HumanFeedbackRecord] = {}
        self._seed_feedbacks()

    def _seed_feedbacks(self):
        fb1 = HumanFeedbackRecord(
            feedback_id="fb_inv_001",
            document_id="DOC-INV-2026",
            field_name="total_tax_amount",
            extracted_value="$120.00",
            corrected_value="$142.50",
            confidence_was=0.88,
            model_was="gemini-2.5-flash",
            submitted_by="senior-auditor@enterprise.internal",
            status="COMMITTED_TO_MEMORY",
        )
        self.feedbacks[fb1.feedback_id] = fb1

    def ingest_correction(
        self,
        document_id: str,
        field_name: str,
        extracted_value: str,
        corrected_value: str,
        confidence_was: float = 0.85,
        model_was: str = "gemini-2.5-flash",
        submitted_by: str = "human-operator",
    ) -> HumanFeedbackRecord:
        fb_id = f"fb_{uuid.uuid4().hex[:6]}"
        rec = HumanFeedbackRecord(
            feedback_id=fb_id,
            document_id=document_id,
            field_name=field_name,
            extracted_value=extracted_value,
            corrected_value=corrected_value,
            confidence_was=confidence_was,
            model_was=model_was,
            submitted_by=submitted_by,
            status="INGESTED",
        )
        self.feedbacks[fb_id] = rec
        return rec

    def list_feedbacks(self) -> List[Dict[str, Any]]:
        return [fb.to_dict() for fb in self.feedbacks.values()]
