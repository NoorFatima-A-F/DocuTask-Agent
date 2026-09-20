"""
Gold Dataset System & Annotation Loader Module.
Provides curated gold standard ground truth evaluation datasets across document categories.
"""

from typing import Dict, List
from app.validation.schemas import DatasetMetadata, FieldAnnotation, GoldDatasetItem


class DatasetManager:
    """Manager providing gold standard datasets for evaluation runs."""

    @classmethod
    def get_gold_datasets(cls) -> List[GoldDatasetItem]:
        """Returns comprehensive gold evaluation dataset entries."""
        return [
            # 1. Invoice Gold Standard
            GoldDatasetItem(
                metadata=DatasetMetadata(
                    document_id="gold_inv_001",
                    document_type="invoice",
                    page_count=1,
                    language="eng",
                    source="synthetic_gold_standard",
                    difficulty_level="medium"
                ),
                ocr_text=(
                    "INVOICE # INV-2026-901\n"
                    "Date: 2026-08-15\n"
                    "Vendor: Apex Solutions Inc\n"
                    "Customer: Acme Global Enterprises\n"
                    "Total Amount: $5,400.00\n"
                    "Tax Amount: $400.00\n"
                    "Currency: USD"
                ),
                ground_truth_json={
                    "invoice_number": "INV-2026-901",
                    "vendor_name": "Apex Solutions Inc",
                    "customer_name": "Acme Global Enterprises",
                    "invoice_date": "2026-08-15",
                    "total_amount": 5400.00,
                    "currency": "USD",
                    "tax_amount": 400.00
                },
                annotations=[
                    FieldAnnotation(field_name="invoice_number", expected_value="INV-2026-901", data_type="string", required=True),
                    FieldAnnotation(field_name="vendor_name", expected_value="Apex Solutions Inc", data_type="string", required=True),
                    FieldAnnotation(field_name="total_amount", expected_value=5400.00, data_type="number", required=True)
                ]
            ),

            # 2. Receipt Gold Standard
            GoldDatasetItem(
                metadata=DatasetMetadata(
                    document_id="gold_rcp_001",
                    document_type="receipt",
                    page_count=1,
                    language="eng",
                    source="synthetic_gold_standard",
                    difficulty_level="easy"
                ),
                ocr_text=(
                    "METRO RETAIL STORE #402\n"
                    "Date: 2026-08-12\n"
                    "Subtotal: $45.00\n"
                    "Tax: $3.60\n"
                    "Total Paid: $48.60\n"
                    "Payment Method: Credit Card"
                ),
                ground_truth_json={
                    "store_name": "METRO RETAIL STORE #402",
                    "transaction_date": "2026-08-12",
                    "subtotal": 45.00,
                    "tax": 3.60,
                    "total_amount": 48.60,
                    "payment_method": "Credit Card"
                },
                annotations=[
                    FieldAnnotation(field_name="store_name", expected_value="METRO RETAIL STORE #402", data_type="string", required=True),
                    FieldAnnotation(field_name="total_amount", expected_value=48.60, data_type="number", required=True)
                ]
            ),

            # 3. Contract Gold Standard
            GoldDatasetItem(
                metadata=DatasetMetadata(
                    document_id="gold_ctr_001",
                    document_type="contract",
                    page_count=2,
                    language="eng",
                    source="synthetic_gold_standard",
                    difficulty_level="hard"
                ),
                ocr_text=(
                    "SOFTWARE SERVICES AGREEMENT\n"
                    "This Agreement is entered into on 2026-01-01 between TechCorp LLC and Innovate Inc.\n"
                    "Effective Date: 2026-01-01\n"
                    "Expiration Date: 2028-01-01\n"
                    "Governing Law: State of California\n"
                    "Total Agreement Value: $120,000"
                ),
                ground_truth_json={
                    "contract_title": "SOFTWARE SERVICES AGREEMENT",
                    "parties_involved": ["TechCorp LLC", "Innovate Inc"],
                    "effective_date": "2026-01-01",
                    "expiration_date": "2028-01-01",
                    "governing_law": "State of California",
                    "total_value": "$120,000"
                },
                annotations=[
                    FieldAnnotation(field_name="contract_title", expected_value="SOFTWARE SERVICES AGREEMENT", data_type="string", required=True),
                    FieldAnnotation(field_name="governing_law", expected_value="State of California", data_type="string", required=True)
                ]
            ),

            # 4. Identity / Passport Gold Standard
            GoldDatasetItem(
                metadata=DatasetMetadata(
                    document_id="gold_pas_001",
                    document_type="passport",
                    page_count=1,
                    language="eng",
                    source="synthetic_gold_standard",
                    difficulty_level="easy"
                ),
                ocr_text=(
                    "PASSPORT / PASSEPORT\n"
                    "Passport No: P987654321\n"
                    "Surname: SMITH\n"
                    "Given Names: JANE DOE\n"
                    "Nationality: USA\n"
                    "Date of Birth: 1990-05-14\n"
                    "Expiry Date: 2030-05-14"
                ),
                ground_truth_json={
                    "passport_number": "P987654321",
                    "surname": "SMITH",
                    "given_names": "JANE DOE",
                    "nationality": "USA",
                    "date_of_birth": "1990-05-14",
                    "expiry_date": "2030-05-14"
                },
                annotations=[
                    FieldAnnotation(field_name="passport_number", expected_value="P987654321", data_type="string", required=True)
                ]
            ),

            # 5. Medical Report Gold Standard
            GoldDatasetItem(
                metadata=DatasetMetadata(
                    document_id="gold_med_001",
                    document_type="medical_report",
                    page_count=1,
                    language="eng",
                    source="synthetic_gold_standard",
                    difficulty_level="medium"
                ),
                ocr_text=(
                    "CLINICAL HEALTH CENTER\n"
                    "Patient Name: Robert Johnson\n"
                    "Visit Date: 2026-08-10\n"
                    "Physician: Dr. Sarah Jenkins\n"
                    "Diagnosis: Acute Bronchitis\n"
                    "Prescription: Amoxicillin 500mg"
                ),
                ground_truth_json={
                    "patient_name": "Robert Johnson",
                    "doctor_name": "Dr. Sarah Jenkins",
                    "visit_date": "2026-08-10",
                    "diagnosis": "Acute Bronchitis",
                    "prescribed_medications": ["Amoxicillin 500mg"]
                },
                annotations=[
                    FieldAnnotation(field_name="patient_name", expected_value="Robert Johnson", data_type="string", required=True),
                    FieldAnnotation(field_name="diagnosis", expected_value="Acute Bronchitis", data_type="string", required=True)
                ]
            )
        ]

    @classmethod
    def get_by_document_type(cls, document_type: str) -> List[GoldDatasetItem]:
        """Filters gold datasets by document type."""
        key = document_type.lower().strip()
        return [d for d in cls.get_gold_datasets() if d.metadata.document_type.lower() == key]
