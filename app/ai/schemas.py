"""
AI Subsystem Pydantic Schemas.
Defines target structured models per document type and API request/response objects.
"""

from datetime import datetime
from enum import StrEnum
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class DocumentTypeEnum(StrEnum):
    """Supported document types for structured AI extraction."""

    INVOICE = "invoice"
    RECEIPT = "receipt"
    RESUME = "resume"
    PASSPORT = "passport"
    DRIVER_LICENSE = "driver_license"
    NATIONAL_ID = "national_id"
    MEDICAL_REPORT = "medical_report"
    INSURANCE_FORM = "insurance_form"
    CONTRACT = "contract"
    BANK_STATEMENT = "bank_statement"
    UTILITY_BILL = "utility_bill"
    RESEARCH_PAPER = "research_paper"
    PURCHASE_ORDER = "purchase_order"
    GENERIC = "generic"


# ---------------------------------------------------------------------------
# Target Document Extraction Pydantic Models
# ---------------------------------------------------------------------------


class InvoiceLineItem(BaseModel):
    description: str = Field(..., description="Line item description")
    quantity: float = Field(1.0, description="Quantity ordered")
    unit_price: float = Field(0.0, description="Unit price per item")
    total_price: float = Field(0.0, description="Total price for line item")


class InvoiceExtraction(BaseModel):
    """Structured output model for Invoice documents."""

    invoice_number: str | None = Field(None, description="Invoice reference identifier")
    vendor_name: str | None = Field(None, description="Vendor or issuing company name")
    customer_name: str | None = Field(None, description="Billed customer name")
    invoice_date: str | None = Field(None, description="Invoice date")
    due_date: str | None = Field(None, description="Payment due date")
    subtotal: float | None = Field(None, description="Amount before tax")
    total_amount: float | None = Field(None, description="Total invoice monetary amount")
    currency: str | None = Field("USD", description="ISO 4217 currency code")
    tax_amount: float | None = Field(None, description="Tax or VAT amount")
    line_items: list[InvoiceLineItem] = Field(default_factory=list, description="Extracted line items")


class ResumeExperience(BaseModel):
    company: str = Field(..., description="Employer company name")
    title: str = Field(..., description="Job title or position held")
    start_date: str | None = Field(None, description="Employment start date")
    end_date: str | None = Field(None, description="Employment end date or 'Present'")
    responsibilities: list[str] = Field(default_factory=list, description="Key duties and achievements")


class ResumeEducation(BaseModel):
    institution: str | None = Field(None, description="School or university")
    degree: str | None = Field(None, description="Degree or qualification")
    field_of_study: str | None = Field(None, description="Major or field")
    start_date: str | None = Field(None, description="Start date")
    end_date: str | None = Field(None, description="End or graduation date")


class ResumeExtraction(BaseModel):
    """Structured output model for Resume documents."""

    full_name: str | None = Field(None, description="Candidate's full name")
    email: str | None = Field(None, description="Contact email address")
    phone: str | None = Field(None, description="Contact phone number")
    location: str | None = Field(None, description="City, State/Country")
    summary: str | None = Field(None, description="Professional summary")
    skills: list[str] = Field(default_factory=list, description="Extracted skills and technologies")
    work_experience: list[ResumeExperience] = Field(default_factory=list, description="Career history")
    education: list[ResumeEducation] = Field(default_factory=list, description="Degrees and educational background")


class ContractExtraction(BaseModel):
    """Structured output model for Contract documents."""

    contract_title: str | None = Field(None, description="Name or title of agreement")
    parties_involved: list[str] = Field(default_factory=list, description="Named contracting parties")
    effective_date: str | None = Field(None, description="Agreement effective start date")
    expiration_date: str | None = Field(None, description="Contract termination or expiration date")
    governing_law: str | None = Field(None, description="Jurisdiction or governing law")
    total_value: str | None = Field(None, description="Total monetary contract value")
    key_clauses: list[str] = Field(default_factory=list, description="Summary of key clauses and terms")


class MedicalReportExtraction(BaseModel):
    """Structured output model for Medical Report documents."""

    patient_name: str | None = Field(None, description="Patient full name")
    patient_dob: str | None = Field(None, description="Patient date of birth")
    doctor_name: str | None = Field(None, description="Attending physician or specialist")
    visit_date: str | None = Field(None, description="Clinical visit date")
    diagnosis: str | None = Field(None, description="Primary clinical diagnosis")
    symptoms: list[str] = Field(default_factory=list, description="Reported patient symptoms")
    prescribed_medications: list[str] = Field(default_factory=list, description="Prescribed drugs and dosage")
    recommendations: str | None = Field(None, description="Follow-up advice and recommendations")


class ReceiptLineItem(BaseModel):
    description: str = Field(..., description="Item description")
    quantity: float | None = Field(None, description="Quantity purchased")
    unit_price: float | None = Field(None, description="Price per unit")
    total_price: float | None = Field(None, description="Line total")


class ReceiptExtraction(BaseModel):
    """Structured output model for Receipt documents."""

    store_name: str | None = Field(None, description="Store or merchant name")
    transaction_date: str | None = Field(None, description="Date of transaction")
    subtotal: float | None = Field(None, description="Subtotal amount before tax")
    tax: float | None = Field(None, description="Sales tax amount")
    total_amount: float | None = Field(None, description="Final charged total amount")
    payment_method: str | None = Field(None, description="Payment method (Cash, Credit, Debit)")
    line_items: list[ReceiptLineItem] = Field(default_factory=list, description="Purchased items")


class PassportExtraction(BaseModel):
    """Structured output model for Passport identity documents."""

    passport_number: str | None = Field(None, description="Passport number")
    surname: str | None = Field(None, description="Surname/Last name")
    given_names: str | None = Field(None, description="Given names/First name")
    nationality: str | None = Field(None, description="Country of nationality")
    date_of_birth: str | None = Field(None, description="Date of birth")
    place_of_birth: str | None = Field(None, description="Place/City of birth")
    issue_date: str | None = Field(None, description="Date of passport issue")
    expiry_date: str | None = Field(None, description="Date of passport expiration")
    issuing_authority: str | None = Field(None, description="Issuing country or authority")


class DriverLicenseExtraction(BaseModel):
    """Structured output model for Driver License documents."""

    license_number: str | None = Field(None, description="Driver license number")
    full_name: str | None = Field(None, description="Driver full name")
    address: str | None = Field(None, description="Residential address")
    date_of_birth: str | None = Field(None, description="Date of birth")
    issue_date: str | None = Field(None, description="License issue date")
    expiry_date: str | None = Field(None, description="License expiry date")
    license_class: str | None = Field(None, description="License vehicle class")


class NationalIDExtraction(BaseModel):
    """Structured output model for National ID documents."""

    id_number: str | None = Field(None, description="National identification number")
    full_name: str | None = Field(None, description="Individual full name")
    date_of_birth: str | None = Field(None, description="Date of birth")
    gender: str | None = Field(None, description="Gender/Sex")
    address: str | None = Field(None, description="Address or locality")
    expiry_date: str | None = Field(None, description="ID expiration date")


class InsuranceFormExtraction(BaseModel):
    """Structured output model for Insurance Form documents."""

    policy_number: str | None = Field(None, description="Insurance policy number")
    policyholder_name: str | None = Field(None, description="Name of policyholder")
    insurer_name: str | None = Field(None, description="Insurance company name")
    coverage_type: str | None = Field(None, description="Type of coverage (Health, Auto, Life, Property)")
    start_date: str | None = Field(None, description="Coverage start date")
    end_date: str | None = Field(None, description="Coverage end date")
    premium_amount: float | None = Field(None, description="Insurance premium monetary amount")


class BankTransaction(BaseModel):
    date: str | None = Field(None, description="Transaction date")
    description: str | None = Field(None, description="Transaction description")
    amount: float | None = Field(None, description="Signed amount (negative for debits)")
    balance: float | None = Field(None, description="Running balance after the transaction")


class BankStatementExtraction(BaseModel):
    """Structured output model for Bank Statement documents."""

    bank_name: str | None = Field(None, description="Financial institution name")
    account_number: str | None = Field(None, description="Bank account number (masked)")
    account_holder: str | None = Field(None, description="Account holder name")
    statement_period: str | None = Field(None, description="Statement period range")
    opening_balance: float | None = Field(None, description="Period opening balance")
    closing_balance: float | None = Field(None, description="Period closing balance")
    transactions: list[BankTransaction] = Field(default_factory=list, description="Statement transactions list")


class UtilityBillExtraction(BaseModel):
    """Structured output model for Utility Bill documents."""

    utility_company: str | None = Field(None, description="Utility provider company name")
    account_number: str | None = Field(None, description="Customer utility account number")
    service_address: str | None = Field(None, description="Service installation address")
    bill_date: str | None = Field(None, description="Billing statement date")
    due_date: str | None = Field(None, description="Payment due date")
    amount_due: float | None = Field(None, description="Total monetary amount due")
    consumption: str | None = Field(None, description="Utility units consumed (kWh, Gallons, m3)")


class ResearchPaperExtraction(BaseModel):
    """Structured output model for Research Paper documents."""

    title: str | None = Field(None, description="Paper title")
    authors: list[str] = Field(default_factory=list, description="Paper authors")
    abstract: str | None = Field(None, description="Executive research abstract")
    keywords: list[str] = Field(default_factory=list, description="Key search terms/keywords")
    publication_date: str | None = Field(None, description="Publication date or year")
    doi: str | None = Field(None, description="Digital Object Identifier (DOI)")
    conclusions: str | None = Field(None, description="Primary research conclusions")


class PurchaseOrderItem(BaseModel):
    description: str = Field(..., description="Item description")
    quantity: float | None = Field(None, description="Quantity ordered")
    unit_price: float | None = Field(None, description="Price per unit")
    total_price: float | None = Field(None, description="Line total")


class PurchaseOrderExtraction(BaseModel):
    """Structured output model for Purchase Order documents."""

    po_number: str | None = Field(None, description="Purchase order reference number")
    vendor_name: str | None = Field(None, description="Target vendor name")
    order_date: str | None = Field(None, description="Order issuance date")
    delivery_date: str | None = Field(None, description="Expected delivery date")
    total_cost: float | None = Field(None, description="Total order monetary cost")
    items: list[PurchaseOrderItem] = Field(default_factory=list, description="Ordered items list")


class GenericExtraction(BaseModel):
    """Structured output model for Generic documents."""

    summary: str = Field(..., description="Executive summary of document contents")
    key_entities: list[str] = Field(default_factory=list, description="Key people, organizations, or products")
    main_topics: list[str] = Field(default_factory=list, description="Main topics covered")
    metadata_fields: dict[str, Any] = Field(default_factory=dict, description="Extracted key-value attributes")


# ---------------------------------------------------------------------------
# API Payload Schemas
# ---------------------------------------------------------------------------


class ExtractionRequest(BaseModel):
    """Payload to trigger AI structured extraction."""

    document_type: str = Field("generic", description="Target document schema type (invoice, resume, contract, etc.)")
    force_reextract: bool = Field(False, description="Bypass cache and force fresh LLM extraction")
    provider: str | None = Field(None, description="LLM provider override (e.g. 'gemini')")
    model: str | None = Field(None, description="Model override (e.g. 'gemini-1.5-pro')")


class ExtractionMetadata(BaseModel):
    """Extraction operational metadata."""

    document_id: UUID
    document_type: str
    provider: str
    model: str
    prompt_version: str = "v1.0"
    created_at: datetime


class ExtractionStatistics(BaseModel):
    """Cost, token usage, and latency statistics."""

    processing_time_ms: int
    input_tokens: int
    output_tokens: int
    estimated_cost: float | None = Field(None, description="USD cost; null when model pricing is unknown")
    retry_count: int = 0


class ExtractionResult(BaseModel):
    """Extraction payload.

    ``final_json`` is the data clients should treat as final: set for auto-accepted
    (COMPLETED) results and after reviewer approval; null while NEEDS_REVIEW or FAILED.
    ``structured_json`` is the raw model output (null on failure).
    """

    status: str = Field(..., description="COMPLETED, NEEDS_REVIEW or FAILED")
    raw_response: str | None = None
    structured_json: dict[str, Any] | None = None
    final_json: dict[str, Any] | None = None
    confidence: float | None = None
    confidence_details: dict[str, Any] | None = Field(
        None, description="Per-field grounding, missing/ungrounded required fields, consistency checks, OCR confidence"
    )
    error_code: str | None = None
    error_message: str | None = None


class ExtractionResponse(BaseModel):
    """Top-level response payload for AI structured extraction."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    metadata: ExtractionMetadata
    statistics: ExtractionStatistics
    result: ExtractionResult


class ValidationErrorResponse(BaseModel):
    """Schema validation error details."""

    error_message: str
    raw_output: str
    retry_count: int
