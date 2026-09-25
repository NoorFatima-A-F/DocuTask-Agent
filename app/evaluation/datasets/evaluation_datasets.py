"""Curated evaluation datasets with ground truth annotations for benchmarking."""

from typing import Any, Dict, List
from pydantic import BaseModel, Field


class GroundTruthSample(BaseModel):
    sample_id: str
    document_type: str
    difficulty: str = "Medium"
    ground_truth_fields: Dict[str, Any] = Field(default_factory=dict)
    raw_ocr_text: str = ""


class BenchmarkDataset(BaseModel):
    dataset_id: str
    name: str
    domain: str
    total_samples: int
    samples: List[GroundTruthSample] = Field(default_factory=list)


INVOICE_BENCHMARK_DATASET: List[Dict[str, Any]] = [
    {
        "id": "INV-EVAL-001",
        "type": "StandardDigitalInvoice",
        "vendor": "Acme Global Solutions Inc.",
        "invoice_number": "INV-2026-8891",
        "date": "2026-08-15",
        "total_amount": 14500.50,
        "tax_amount": 1160.04,
        "line_items_count": 8,
        "currency": "USD",
        "difficulty": "Easy",
    },
    {
        "id": "INV-EVAL-002",
        "type": "MultiPageNoisyScan",
        "vendor": "BioTech Laboratories GmbH",
        "invoice_number": "DE-99412-B",
        "date": "2026-07-22",
        "total_amount": 89450.00,
        "tax_amount": 14282.00,
        "line_items_count": 24,
        "currency": "EUR",
        "difficulty": "Hard",
    },
    {
        "id": "INV-EVAL-003",
        "type": "MultilingualReceipt",
        "vendor": "Tokyo Logistics K.K.",
        "invoice_number": "TK-4410",
        "date": "2026-09-01",
        "total_amount": 1250000.0,
        "tax_amount": 125000.0,
        "line_items_count": 5,
        "currency": "JPY",
        "difficulty": "Medium",
    },
]

RESUME_BENCHMARK_DATASET: List[Dict[str, Any]] = [
    {
        "id": "RES-EVAL-001",
        "candidate": "Alex Rivera",
        "role_target": "Principal AI Engineer",
        "experience_years": 9,
        "top_skills": ["Python", "PyTorch", "Distributed Systems", "FastAPI", "LLMOps"],
        "education": "M.S. Computer Science",
        "ranking_score": 96.5,
    },
    {
        "id": "RES-EVAL-002",
        "candidate": "Sophia Chen",
        "role_target": "Senior Cloud SRE",
        "experience_years": 7,
        "top_skills": ["Kubernetes", "Terraform", "AWS", "Prometheus", "Chaos Engineering"],
        "education": "B.S. Software Engineering",
        "ranking_score": 94.0,
    },
]

CONTRACT_BENCHMARK_DATASET: List[Dict[str, Any]] = [
    {
        "id": "CON-EVAL-001",
        "title": "Master Cloud Services Agreement",
        "parties": ["Nexus Enterprise Corp", "Apex Data Systems"],
        "effective_date": "2026-01-01",
        "expiry_date": "2029-01-01",
        "governing_law": "State of Delaware",
        "liability_cap_present": True,
        "risk_rating": "Low",
    },
    {
        "id": "CON-EVAL-002",
        "title": "Non-Disclosure & Confidentiality Agreement",
        "parties": ["Global AI Innovations", "Stealth Venture Partners"],
        "effective_date": "2026-06-15",
        "expiry_date": "2028-06-15",
        "governing_law": "England and Wales",
        "liability_cap_present": False,
        "risk_rating": "Medium",
    },
]

MEDICAL_BENCHMARK_DATASET: List[Dict[str, Any]] = [
    {
        "id": "MED-EVAL-001",
        "report_type": "PriorAuthorizationRequest",
        "patient_id_hashed": "d3b07384d113edec49eaa6238ad5ff00",
        "diagnosis_code": "M54.5",
        "procedure_code": "72148",
        "clinical_justification_valid": True,
        "urgency": "Standard",
        "decision": "APPROVED",
    }
]

# Structured Benchmark Datasets
INVOICE_GROUND_TRUTH = BenchmarkDataset(
    dataset_id="DATASET-01-INVOICE",
    name="Enterprise Invoices & Financial Receipts",
    domain="Finance & Accounts Payable",
    total_samples=len(INVOICE_BENCHMARK_DATASET),
    samples=[
        GroundTruthSample(
            sample_id=item["id"],
            document_type=item["type"],
            difficulty=item.get("difficulty", "Medium"),
            ground_truth_fields=item,
            raw_ocr_text=f"Vendor: {item['vendor']} Invoice: {item['invoice_number']} Total: {item['total_amount']}",
        )
        for item in INVOICE_BENCHMARK_DATASET
    ],
)

RESUME_GROUND_TRUTH = BenchmarkDataset(
    dataset_id="DATASET-02-RESUME",
    name="Technical Talent Resumes & Profiles",
    domain="Human Resources & Recruiting",
    total_samples=len(RESUME_BENCHMARK_DATASET),
    samples=[
        GroundTruthSample(
            sample_id=item["id"],
            document_type="Resume",
            difficulty="Medium",
            ground_truth_fields=item,
            raw_ocr_text=f"Candidate: {item['candidate']} Target: {item['role_target']} Skills: {', '.join(item['top_skills'])}",
        )
        for item in RESUME_BENCHMARK_DATASET
    ],
)

CONTRACT_GROUND_TRUTH = BenchmarkDataset(
    dataset_id="DATASET-03-CONTRACT",
    name="Enterprise Legal Master Service Agreements",
    domain="Legal & Compliance",
    total_samples=len(CONTRACT_BENCHMARK_DATASET),
    samples=[
        GroundTruthSample(
            sample_id=item["id"],
            document_type="Contract",
            difficulty=item.get("risk_rating", "Medium"),
            ground_truth_fields=item,
            raw_ocr_text=f"Agreement: {item['title']} Parties: {', '.join(item['parties'])} Law: {item['governing_law']}",
        )
        for item in CONTRACT_BENCHMARK_DATASET
    ],
)

HEALTHCARE_GROUND_TRUTH = BenchmarkDataset(
    dataset_id="DATASET-04-HEALTHCARE",
    name="Healthcare Clinical Records & Authorizations",
    domain="Healthcare & Medical Coding",
    total_samples=len(MEDICAL_BENCHMARK_DATASET),
    samples=[
        GroundTruthSample(
            sample_id=item["id"],
            document_type=item["report_type"],
            difficulty=item.get("urgency", "Standard"),
            ground_truth_fields=item,
            raw_ocr_text=f"Auth: {item['report_type']} Code: {item['diagnosis_code']} Decision: {item['decision']}",
        )
        for item in MEDICAL_BENCHMARK_DATASET
    ],
)

ALL_DATASETS = [
    INVOICE_GROUND_TRUTH,
    RESUME_GROUND_TRUTH,
    CONTRACT_GROUND_TRUTH,
    HEALTHCARE_GROUND_TRUTH,
]
