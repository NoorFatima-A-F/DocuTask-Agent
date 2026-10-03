# Schema Registry Architectural Specification

**Subsystem**: Schema Registry & Document Types  
**Path**: `C:\Users\User\Desktop\ai_document_processing_platform\app\ai\schemas.py`  

---

## 1. Registered Document Schemas

The system supports structured extractions for 13 target document types:

| Document Type Code | Target Pydantic Schema Model | Key Extracted Attributes |
|--------------------|------------------------------|--------------------------|
| `invoice` | `InvoiceExtraction` | `invoice_number`, `vendor_name`, `total_amount`, `currency`, `line_items` |
| `receipt` | `ReceiptExtraction` | `store_name`, `transaction_date`, `subtotal`, `tax`, `total_amount` |
| `resume` | `ResumeExtraction` | `full_name`, `email`, `phone`, `skills`, `work_experience`, `education` |
| `passport` | `PassportExtraction` | `passport_number`, `surname`, `given_names`, `nationality`, `expiry_date` |
| `driver_license` | `DriverLicenseExtraction` | `license_number`, `full_name`, `address`, `issue_date`, `expiry_date` |
| `national_id` | `NationalIDExtraction` | `id_number`, `full_name`, `date_of_birth`, `gender`, `address` |
| `medical_report` | `MedicalReportExtraction` | `patient_name`, `doctor_name`, `diagnosis`, `symptoms`, `prescribed_medications` |
| `insurance_form` | `InsuranceFormExtraction` | `policy_number`, `policyholder_name`, `insurer_name`, `premium_amount` |
| `contract` | `ContractExtraction` | `contract_title`, `parties_involved`, `effective_date`, `expiration_date` |
| `bank_statement` | `BankStatementExtraction` | `bank_name`, `account_number`, `opening_balance`, `closing_balance` |
| `utility_bill` | `UtilityBillExtraction` | `utility_company`, `account_number`, `bill_date`, `amount_due` |
| `research_paper` | `ResearchPaperExtraction` | `title`, `authors`, `abstract`, `keywords`, `publication_date`, `doi` |
| `purchase_order` | `PurchaseOrderExtraction` | `po_number`, `vendor_name`, `order_date`, `total_cost`, `items` |
| `generic` | `GenericExtraction` | `summary`, `key_entities`, `main_topics`, `metadata_fields` |
