"""
AI Subsystem Pydantic Schemas.
Defines target structured models per document type and API request/response objects.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


class DocumentTypeEnum(str, Enum):
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
    invoice_number: Optional[str] = Field(None, description="Invoice reference identifier")
    vendor_name: Optional[str] = Field(None, description="Vendor or issuing company name")
    customer_name: Optional[str] = Field(None, description="Billed customer name")
    invoice_date: Optional[str] = Field(None, description="Invoice date")
    due_date: Optional[str] = Field(None, description="Payment due date")
    total_amount: Optional[float] = Field(None, description="Total invoice monetary amount")
    currency: Optional[str] = Field("USD", description="Currency symbol or code")
    tax_amount: Optional[float] = Field(None, description="Tax or VAT amount")
    line_items: List[InvoiceLineItem] = Field(default_factory=list, description="Extracted line items")


class ResumeExperience(BaseModel):
    company: str = Field(..., description="Employer company name")
    title: str = Field(..., description="Job title or position held")
    start_date: Optional[str] = Field(None, description="Employment start date")
    end_date: Optional[str] = Field(None, description="Employment end date or 'Present'")
    responsibilities: List[str] = Field(default_factory=list, description="Key duties and achievements")


class ResumeExtraction(BaseModel):
    """Structured output model for Resume documents."""
    full_name: Optional[str] = Field(None, description="Candidate's full name")
    email: Optional[str] = Field(None, description="Contact email address")
    phone: Optional[str] = Field(None, description="Contact phone number")
    location: Optional[str] = Field(None, description="City, State/Country")
    summary: Optional[str] = Field(None, description="Professional summary")
    skills: List[str] = Field(default_factory=list, description="Extracted skills and technologies")
    work_experience: List[ResumeExperience] = Field(default_factory=list, description="Career history")
    education: List[Dict[str, Any]] = Field(default_factory=list, description="Degrees and educational background")


class ContractExtraction(BaseModel):
    """Structured output model for Contract documents."""
    contract_title: Optional[str] = Field(None, description="Name or title of agreement")
    parties_involved: List[str] = Field(default_factory=list, description="Named contracting parties")
    effective_date: Optional[str] = Field(None, description="Agreement effective start date")
    expiration_date: Optional[str] = Field(None, description="Contract termination or expiration date")
    governing_law: Optional[str] = Field(None, description="Jurisdiction or governing law")
    total_value: Optional[str] = Field(None, description="Total monetary contract value")
    key_clauses: List[str] = Field(default_factory=list, description="Summary of key clauses and terms")


class MedicalReportExtraction(BaseModel):
    """Structured output model for Medical Report documents."""
    patient_name: Optional[str] = Field(None, description="Patient full name")
    patient_dob: Optional[str] = Field(None, description="Patient date of birth")
    doctor_name: Optional[str] = Field(None, description="Attending physician or specialist")
    visit_date: Optional[str] = Field(None, description="Clinical visit date")
    diagnosis: Optional[str] = Field(None, description="Primary clinical diagnosis")
    symptoms: List[str] = Field(default_factory=list, description="Reported patient symptoms")
    prescribed_medications: List[str] = Field(default_factory=list, description="Prescribed drugs and dosage")
    recommendations: Optional[str] = Field(None, description="Follow-up advice and recommendations")


class ReceiptExtraction(BaseModel):
    """Structured output model for Receipt documents."""
    store_name: Optional[str] = Field(None, description="Store or merchant name")
    transaction_date: Optional[str] = Field(None, description="Date of transaction")
    subtotal: Optional[float] = Field(None, description="Subtotal amount before tax")
    tax: Optional[float] = Field(None, description="Sales tax amount")
    total_amount: Optional[float] = Field(None, description="Final charged total amount")
    payment_method: Optional[str] = Field(None, description="Payment method (Cash, Credit, Debit)")
    line_items: List[Dict[str, Any]] = Field(default_factory=list, description="Purchased items")


class PassportExtraction(BaseModel):
    """Structured output model for Passport identity documents."""
    passport_number: Optional[str] = Field(None, description="Passport number")
    surname: Optional[str] = Field(None, description="Surname/Last name")
    given_names: Optional[str] = Field(None, description="Given names/First name")
    nationality: Optional[str] = Field(None, description="Country of nationality")
    date_of_birth: Optional[str] = Field(None, description="Date of birth")
    place_of_birth: Optional[str] = Field(None, description="Place/City of birth")
    issue_date: Optional[str] = Field(None, description="Date of passport issue")
    expiry_date: Optional[str] = Field(None, description="Date of passport expiration")
    issuing_authority: Optional[str] = Field(None, description="Issuing country or authority")


class DriverLicenseExtraction(BaseModel):
    """Structured output model for Driver License documents."""
    license_number: Optional[str] = Field(None, description="Driver license number")
    full_name: Optional[str] = Field(None, description="Driver full name")
    address: Optional[str] = Field(None, description="Residential address")
    date_of_birth: Optional[str] = Field(None, description="Date of birth")
    issue_date: Optional[str] = Field(None, description="License issue date")
    expiry_date: Optional[str] = Field(None, description="License expiry date")
    license_class: Optional[str] = Field(None, description="License vehicle class")


class NationalIDExtraction(BaseModel):
    """Structured output model for National ID documents."""
    id_number: Optional[str] = Field(None, description="National identification number")
    full_name: Optional[str] = Field(None, description="Individual full name")
    date_of_birth: Optional[str] = Field(None, description="Date of birth")
    gender: Optional[str] = Field(None, description="Gender/Sex")
    address: Optional[str] = Field(None, description="Address or locality")
    expiry_date: Optional[str] = Field(None, description="ID expiration date")


class InsuranceFormExtraction(BaseModel):
    """Structured output model for Insurance Form documents."""
    policy_number: Optional[str] = Field(None, description="Insurance policy number")
    policyholder_name: Optional[str] = Field(None, description="Name of policyholder")
    insurer_name: Optional[str] = Field(None, description="Insurance company name")
    coverage_type: Optional[str] = Field(None, description="Type of coverage (Health, Auto, Life, Property)")
    start_date: Optional[str] = Field(None, description="Coverage start date")
    end_date: Optional[str] = Field(None, description="Coverage end date")
    premium_amount: Optional[float] = Field(None, description="Insurance premium monetary amount")


class BankStatementExtraction(BaseModel):
    """Structured output model for Bank Statement documents."""
    bank_name: Optional[str] = Field(None, description="Financial institution name")
    account_number: Optional[str] = Field(None, description="Bank account number (masked)")
    account_holder: Optional[str] = Field(None, description="Account holder name")
    statement_period: Optional[str] = Field(None, description="Statement period range")
    opening_balance: Optional[float] = Field(None, description="Period opening balance")
    closing_balance: Optional[float] = Field(None, description="Period closing balance")
    transactions: List[Dict[str, Any]] = Field(default_factory=list, description="Statement transactions list")


class UtilityBillExtraction(BaseModel):
    """Structured output model for Utility Bill documents."""
    utility_company: Optional[str] = Field(None, description="Utility provider company name")
    account_number: Optional[str] = Field(None, description="Customer utility account number")
    service_address: Optional[str] = Field(None, description="Service installation address")
    bill_date: Optional[str] = Field(None, description="Billing statement date")
    due_date: Optional[str] = Field(None, description="Payment due date")
    amount_due: Optional[float] = Field(None, description="Total monetary amount due")
    consumption: Optional[str] = Field(None, description="Utility units consumed (kWh, Gallons, m3)")


class ResearchPaperExtraction(BaseModel):
    """Structured output model for Research Paper documents."""
    title: Optional[str] = Field(None, description="Paper title")
    authors: List[str] = Field(default_factory=list, description="Paper authors")
    abstract: Optional[str] = Field(None, description="Executive research abstract")
    keywords: List[str] = Field(default_factory=list, description="Key search terms/keywords")
    publication_date: Optional[str] = Field(None, description="Publication date or year")
    doi: Optional[str] = Field(None, description="Digital Object Identifier (DOI)")
    conclusions: Optional[str] = Field(None, description="Primary research conclusions")


class PurchaseOrderExtraction(BaseModel):
    """Structured output model for Purchase Order documents."""
    po_number: Optional[str] = Field(None, description="Purchase order reference number")
    vendor_name: Optional[str] = Field(None, description="Target vendor name")
    order_date: Optional[str] = Field(None, description="Order issuance date")
    delivery_date: Optional[str] = Field(None, description="Expected delivery date")
    total_cost: Optional[float] = Field(None, description="Total order monetary cost")
    items: List[Dict[str, Any]] = Field(default_factory=list, description="Ordered items list")


class GenericExtraction(BaseModel):
    """Structured output model for Generic documents."""
    summary: str = Field(..., description="Executive summary of document contents")
    key_entities: List[str] = Field(default_factory=list, description="Key people, organizations, or products")
    main_topics: List[str] = Field(default_factory=list, description="Main topics covered")
    metadata_fields: Dict[str, Any] = Field(default_factory=dict, description="Extracted key-value attributes")


# ---------------------------------------------------------------------------
# API Payload Schemas
# ---------------------------------------------------------------------------

class ExtractionRequest(BaseModel):
    """Payload to trigger AI structured extraction."""
    document_type: str = Field("generic", description="Target document schema type (invoice, resume, contract, etc.)")
    force_reextract: bool = Field(False, description="Bypass cache and force fresh LLM extraction")
    provider: Optional[str] = Field(None, description="LLM provider override (e.g. 'gemini')")
    model: Optional[str] = Field(None, description="Model override (e.g. 'gemini-1.5-pro')")


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
    estimated_cost: float
    retry_count: int = 0


class ExtractionResult(BaseModel):
    """Extracted data payload."""
    raw_response: str
    structured_json: Dict[str, Any]
    confidence: float = 1.0


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
