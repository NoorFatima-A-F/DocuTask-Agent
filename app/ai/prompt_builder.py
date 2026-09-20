"""
Prompt Builder Module.
Constructs document-specific extraction prompts, system instructions, and target JSON schemas.
Includes prompt injection sanitization.
"""

from typing import Any, Dict, Type
from pydantic import BaseModel

from app.ai.exceptions import AIPromptException
from app.ai.schemas import (
    BankStatementExtraction,
    ContractExtraction,
    DriverLicenseExtraction,
    GenericExtraction,
    InsuranceFormExtraction,
    InvoiceExtraction,
    MedicalReportExtraction,
    NationalIDExtraction,
    PassportExtraction,
    PurchaseOrderExtraction,
    ReceiptExtraction,
    ResearchPaperExtraction,
    ResumeExtraction,
    UtilityBillExtraction,
)


class PromptBuilder:
    """Builder constructing prompts for structured document extraction."""

    DOCUMENT_MODEL_MAP: Dict[str, Type[BaseModel]] = {
        "invoice": InvoiceExtraction,
        "receipt": ReceiptExtraction,
        "resume": ResumeExtraction,
        "passport": PassportExtraction,
        "driver_license": DriverLicenseExtraction,
        "national_id": NationalIDExtraction,
        "medical_report": MedicalReportExtraction,
        "insurance_form": InsuranceFormExtraction,
        "contract": ContractExtraction,
        "bank_statement": BankStatementExtraction,
        "utility_bill": UtilityBillExtraction,
        "research_paper": ResearchPaperExtraction,
        "purchase_order": PurchaseOrderExtraction,
        "generic": GenericExtraction,
    }

    @classmethod
    def get_target_model(cls, document_type: str) -> Type[BaseModel]:
        """Retrieves target Pydantic model for document type."""
        key = document_type.lower().strip()
        if key not in cls.DOCUMENT_MODEL_MAP:
            return GenericExtraction
        return cls.DOCUMENT_MODEL_MAP[key]

    @classmethod
    def get_json_schema(cls, document_type: str) -> Dict[str, Any]:
        """Generates JSON schema dict for document type."""
        model_cls = cls.get_target_model(document_type)
        return model_cls.model_json_schema()

    @classmethod
    def sanitize_text(cls, text: str) -> str:
        """
        Sanitizes document text to prevent prompt injection attacks.
        Strips control characters and system prompt override attempts.
        """
        if not text:
            return ""
        # Remove common prompt injection pattern tags
        sanitized = text.replace("SYSTEM:", "DOCUMENT_CONTENT:").replace("USER:", "DOCUMENT_CONTENT:")
        sanitized = sanitized.replace("<|im_start|>", "").replace("<|im_end|>", "")
        return sanitized.strip()

    @classmethod
    def build_system_instruction(cls, document_type: str) -> str:
        """Constructs system instruction context."""
        doc_type_clean = document_type.lower().strip()
        
        instructions = (
            "You are an expert AI Document Processing System specializing in accurate structured information extraction.\n"
            f"Your task is to analyze the provided document content and extract structured data for document type: '{doc_type_clean}'.\n\n"
            "STRICT EXTRACTION RULES:\n"
            "1. Extract ONLY facts directly present in or clearly inferable from the document text.\n"
            "2. Do NOT invent, hallucinate, or assume missing information.\n"
            "3. If a requested field is absent from the document, set its value to null or an empty array.\n"
            "4. Ensure numbers, monetary amounts, and dates are formatted cleanly.\n"
            "5. Respond strictly with a single valid JSON object."
        )
        return instructions

    @classmethod
    def build_prompt(cls, document_text: str, document_type: str) -> str:
        """Constructs final user prompt containing sanitized document text."""
        sanitized_content = cls.sanitize_text(document_text)
        
        prompt = (
            f"DOCUMENT CONTENT TO PROCESS:\n"
            f"=========================================\n"
            f"{sanitized_content}\n"
            f"=========================================\n\n"
            f"Extract all relevant fields according to the JSON schema for document type '{document_type}'."
        )
        return prompt
