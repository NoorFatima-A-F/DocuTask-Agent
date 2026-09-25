"""
Domain models and schemas for Phase V5 — Enterprise Document Intelligence & AI Extraction Verification Program.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional, Any


class VerificationStatus(str, Enum):
    PASSED = "PASSED"
    FAILED = "FAILED"
    WARNING = "WARNING"
    SKIPPED = "SKIPPED"


class DocumentCategory(str, Enum):
    INVOICE = "INVOICE"
    PURCHASE_ORDER = "PURCHASE_ORDER"
    RECEIPT = "RECEIPT"
    BILL = "BILL"
    BANK_STATEMENT = "BANK_STATEMENT"
    TAX_FORM = "TAX_FORM"
    GOVERNMENT_FORM = "GOVERNMENT_FORM"
    CUSTOMS_DOC = "CUSTOMS_DOC"
    SHIPPING_LABEL = "SHIPPING_LABEL"
    BILL_OF_LADING = "BILL_OF_LADING"
    CONTRACT = "CONTRACT"
    NDA = "NDA"
    LEGAL_AGREEMENT = "LEGAL_AGREEMENT"
    EMPLOYMENT_LETTER = "EMPLOYMENT_LETTER"
    HR_DOCUMENT = "HR_DOCUMENT"
    PAYROLL_REPORT = "PAYROLL_REPORT"
    MEDICAL_REPORT = "MEDICAL_REPORT"
    PRESCRIPTION = "PRESCRIPTION"
    LAB_RESULT = "LAB_RESULT"
    INSURANCE_CLAIM = "INSURANCE_CLAIM"
    IDENTITY_DOC = "IDENTITY_DOC"
    PASSPORT = "PASSPORT"
    DRIVER_LICENSE = "DRIVER_LICENSE"
    UTILITY_BILL = "UTILITY_BILL"
    ACADEMIC_TRANSCRIPT = "ACADEMIC_TRANSCRIPT"
    CERTIFICATE = "CERTIFICATE"
    RESEARCH_PAPER = "RESEARCH_PAPER"
    TECHNICAL_MANUAL = "TECHNICAL_MANUAL"
    MULTIPAGE_PDF = "MULTIPAGE_PDF"
    EMAIL = "EMAIL"
    SCREENSHOT = "SCREENSHOT"
    HANDWRITTEN_NOTE = "HANDWRITTEN_NOTE"
    PRINTED_FORM = "PRINTED_FORM"
    MIXED_LAYOUT = "MIXED_LAYOUT"


class PerturbationType(str, Enum):
    CLEAN = "CLEAN"
    LOW_QUALITY = "LOW_QUALITY"
    BLURRED = "BLURRED"
    ROTATED = "ROTATED"
    CROPPED = "CROPPED"
    FOLDED = "FOLDED"
    OCCLUDED = "OCCLUDED"
    SHADOWED = "SHADOWED"
    WATERMARKED = "WATERMARKED"
    STAMPED = "STAMPED"
    HANDWRITTEN_ANNOTATIONS = "HANDWRITTEN_ANNOTATIONS"
    MULTILINGUAL = "MULTILINGUAL"
    MULTICURRENCY = "MULTICURRENCY"
    MULTI_DATE_FORMAT = "MULTI_DATE_FORMAT"
    MULTI_TEMPLATE = "MULTI_TEMPLATE"


class SectionId(str, Enum):
    SECTION_A_DATASET = "SECTION_A_DATASET"
    SECTION_B_INGESTION = "SECTION_B_INGESTION"
    SECTION_C_CLASSIFICATION = "SECTION_C_CLASSIFICATION"
    SECTION_D_OCR = "SECTION_D_OCR"
    SECTION_E_LAYOUT = "SECTION_E_LAYOUT"
    SECTION_F_EXTRACTION = "SECTION_F_EXTRACTION"
    SECTION_G_SCHEMA = "SECTION_G_SCHEMA"
    SECTION_H_REPAIR = "SECTION_H_REPAIR"
    SECTION_I_GROUNDING = "SECTION_I_GROUNDING"
    SECTION_J_CALIBRATION = "SECTION_J_CALIBRATION"
    SECTION_K_BUSINESS_RULES = "SECTION_K_BUSINESS_RULES"
    SECTION_L_MULTILINGUAL = "SECTION_L_MULTILINGUAL"
    SECTION_M_ROBUSTNESS = "SECTION_M_ROBUSTNESS"
    SECTION_N_PIPELINE = "SECTION_N_PIPELINE"
    SECTION_O_SECURITY = "SECTION_O_SECURITY"
    SECTION_P_PERFORMANCE = "SECTION_P_PERFORMANCE"
    SECTION_Q_REGRESSION = "SECTION_Q_REGRESSION"
    SECTION_R_READINESS = "SECTION_R_READINESS"


@dataclass
class BoundingBox:
    x_min: float
    y_min: float
    x_max: float
    y_max: float
    page: int = 1

    @property
    def area(self) -> float:
        return max(0.0, self.x_max - self.x_min) * max(0.0, self.y_max - self.y_min)

    def iou(self, other: "BoundingBox") -> float:
        if self.page != other.page:
            return 0.0
        inter_x_min = max(self.x_min, other.x_min)
        inter_y_min = max(self.y_min, other.y_min)
        inter_x_max = min(self.x_max, other.x_max)
        inter_y_max = min(self.y_max, other.y_max)
        
        inter_width = max(0.0, inter_x_max - inter_x_min)
        inter_height = max(0.0, inter_y_max - inter_y_min)
        inter_area = inter_width * inter_height

        union_area = self.area + other.area - inter_area
        if union_area <= 0.0:
            return 1.0 if inter_area == 0.0 else 0.0
        return inter_area / union_area

    def to_dict(self) -> Dict[str, Any]:
        return {
            "x_min": self.x_min,
            "y_min": self.y_min,
            "x_max": self.x_max,
            "y_max": self.y_max,
            "page": self.page,
        }


@dataclass
class ExtractedEntity:
    name: str
    value: Any
    confidence: float
    bbox: Optional[BoundingBox] = None
    page: int = 1
    grounding_citation: Optional[str] = None
    normalized_value: Optional[Any] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "value": self.value,
            "confidence": round(self.confidence, 4),
            "bbox": self.bbox.to_dict() if self.bbox else None,
            "page": self.page,
            "grounding_citation": self.grounding_citation,
            "normalized_value": self.normalized_value,
        }


@dataclass
class GroundTruthDocument:
    doc_id: str
    category: DocumentCategory
    perturbation: PerturbationType
    text_content: str
    expected_entities: Dict[str, Any]
    expected_tables: List[List[Dict[str, Any]]] = field(default_factory=list)
    expected_bboxes: Dict[str, BoundingBox] = field(default_factory=dict)
    expected_confidence: float = 0.95
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "doc_id": self.doc_id,
            "category": self.category.value,
            "perturbation": self.perturbation.value,
            "text_content": self.text_content,
            "expected_entities": self.expected_entities,
            "expected_tables": self.expected_tables,
            "expected_bboxes": {k: v.to_dict() for k, v in self.expected_bboxes.items()},
            "expected_confidence": self.expected_confidence,
            "metadata": self.metadata,
        }


@dataclass
class AssertionResult:
    name: str
    passed: bool
    message: str
    execution_time_ms: float = 0.0
    details: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "passed": self.passed,
            "message": self.message,
            "execution_time_ms": round(self.execution_time_ms, 3),
            "details": self.details,
        }


@dataclass
class SectionVerificationResult:
    section_id: SectionId
    title: str
    description: str
    status: VerificationStatus
    score: float
    weight: float
    assertions: List[AssertionResult] = field(default_factory=list)
    metrics: Dict[str, Any] = field(default_factory=dict)
    execution_time_ms: float = 0.0

    @property
    def passed_assertions_count(self) -> int:
        return sum(1 for a in self.assertions if a.passed)

    @property
    def total_assertions_count(self) -> int:
        return len(self.assertions)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "section_id": self.section_id.value,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "score": round(self.score, 2),
            "weight": round(self.weight, 2),
            "passed_assertions": self.passed_assertions_count,
            "total_assertions": self.total_assertions_count,
            "execution_time_ms": round(self.execution_time_ms, 2),
            "metrics": self.metrics,
            "assertions": [a.to_dict() for a in self.assertions],
        }


@dataclass
class ProductionReadinessScorecard:
    sections: Dict[str, SectionVerificationResult] = field(default_factory=dict)
    dimensions: Dict[str, float] = field(default_factory=dict)
    composite_score: float = 100.0
    grade: str = "A+"
    total_assertions: int = 0
    passed_assertions: int = 0
    production_ready: bool = True
    total_execution_time_ms: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "composite_score": round(self.composite_score, 2),
            "grade": self.grade,
            "production_ready": self.production_ready,
            "total_assertions": self.total_assertions,
            "passed_assertions": self.passed_assertions,
            "pass_rate_pct": round((self.passed_assertions / max(1, self.total_assertions)) * 100.0, 2),
            "total_execution_time_ms": round(self.total_execution_time_ms, 2),
            "dimensions": {k: round(v, 2) for k, v in self.dimensions.items()},
            "sections": {k: v.to_dict() for k, v in self.sections.items()},
        }
