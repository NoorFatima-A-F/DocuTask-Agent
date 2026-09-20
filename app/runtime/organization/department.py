"""
AMAEOP Pillar 1 - Specialized Enterprise Department Model
Defines organizational departments (Executive, OCR, Extraction, Validation, Memory, Research, Governance, QA).
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict, field
import time


@dataclass
class DepartmentKPIs:
    throughput_items_per_min: float
    avg_latency_ms: float
    accuracy_rate_pct: float
    sla_compliance_pct: float
    error_rate_pct: float
    resource_utilization_pct: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Department:
    department_id: str
    name: str
    head_agent: str
    role_description: str
    parent_department_id: Optional[str]
    sub_departments: List[str]
    active_workers: int
    concurrency_limit: int
    queue_depth: int
    health_score: float  # 0.0 - 100.0
    sla_target_ms: float
    budget_allocated_usd: float
    budget_spent_usd: float
    kpis: DepartmentKPIs
    responsibilities: List[str]
    owned_resources: List[str]
    status: str = "ACTIVE"  # ACTIVE | ELEVATED_LOAD | THROTTLED | INCIDENT_RECOVERY
    updated_at: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


CANONICAL_DEPARTMENTS: Dict[str, Department] = {
    "dept_executive": Department(
        department_id="dept_executive",
        name="Executive Coordination & Strategy",
        head_agent="Chief Executive Agent",
        role_description="Enterprise mission intake, strategic prioritization, cross-department conflict resolution and governance alignment.",
        parent_department_id=None,
        sub_departments=["dept_ocr", "dept_extraction", "dept_validation", "dept_memory", "dept_research", "dept_governance", "dept_qa"],
        active_workers=2,
        concurrency_limit=8,
        queue_depth=1,
        health_score=99.2,
        sla_target_ms=100.0,
        budget_allocated_usd=50.0,
        budget_spent_usd=2.14,
        kpis=DepartmentKPIs(
            throughput_items_per_min=120.0,
            avg_latency_ms=35.0,
            accuracy_rate_pct=99.8,
            sla_compliance_pct=100.0,
            error_rate_pct=0.0,
            resource_utilization_pct=35.0,
        ),
        responsibilities=[
            "Mission intake and portfolio arbitration",
            "Organization-wide resource budgeting",
            "Executive sign-off and strategic alignment",
            "Emergency escalation handling"
        ],
        owned_resources=["Executive Decision Authority", "Strategic Budget Pool", "Root Escalation Bus"],
    ),
    "dept_ocr": Department(
        department_id="dept_ocr",
        name="Optical Perception & Document Ingestion",
        head_agent="Lead Vision Agent",
        role_description="Preprocesses raw documents, de-skews, de-warps, extracts layout bounding boxes and runs multi-engine OCR.",
        parent_department_id="dept_executive",
        sub_departments=[],
        active_workers=4,
        concurrency_limit=12,
        queue_depth=3,
        health_score=96.5,
        sla_target_ms=250.0,
        budget_allocated_usd=30.0,
        budget_spent_usd=4.82,
        kpis=DepartmentKPIs(
            throughput_items_per_min=180.0,
            avg_latency_ms=180.0,
            accuracy_rate_pct=98.5,
            sla_compliance_pct=99.1,
            error_rate_pct=0.8,
            resource_utilization_pct=65.0,
        ),
        responsibilities=[
            "Multi-format document ingestion (PDF, TIFF, JPEG)",
            "Resolution enhancement and contrast normalization",
            "LayoutLM bounding box tokenization",
            "Specialized OCR routing (Tesseract, Cloud Vision, LayoutLM)"
        ],
        owned_resources=["GPU Ingestion Cluster", "OCR Model Pool", "Bilateral Filter Cache"],
    ),
    "dept_extraction": Department(
        department_id="dept_extraction",
        name="Structured Intelligence & Semantic Extraction",
        head_agent="Lead Extraction Specialist",
        role_description="Transforms visual-text tokens into validated domain schemas via Gemini models and adaptive reasoning.",
        parent_department_id="dept_executive",
        sub_departments=[],
        active_workers=6,
        concurrency_limit=20,
        queue_depth=4,
        health_score=98.1,
        sla_target_ms=600.0,
        budget_allocated_usd=80.0,
        budget_spent_usd=12.45,
        kpis=DepartmentKPIs(
            throughput_items_per_min=240.0,
            avg_latency_ms=450.0,
            accuracy_rate_pct=99.1,
            sla_compliance_pct=98.9,
            error_rate_pct=0.5,
            resource_utilization_pct=72.5,
        ),
        responsibilities=[
            "Key-value entity resolution",
            "Nested line-item table parsing",
            "Multi-modal prompt synthesis",
            "Pareto model selection (Flash vs Pro)"
        ],
        owned_resources=["Gemini LLM Quota", "Context Window Optimizer", "Extraction Prompt Library"],
    ),
    "dept_validation": Department(
        department_id="dept_validation",
        name="Mathematical & Cross-Field Invariant Validation",
        head_agent="Lead Verification Auditor",
        role_description="Executes deterministic arithmetic verification, cross-field integrity checks, and Zero-Fabrication Sentinel enforcement.",
        parent_department_id="dept_executive",
        sub_departments=[],
        active_workers=3,
        concurrency_limit=16,
        queue_depth=1,
        health_score=99.8,
        sla_target_ms=80.0,
        budget_allocated_usd=20.0,
        budget_spent_usd=1.12,
        kpis=DepartmentKPIs(
            throughput_items_per_min=320.0,
            avg_latency_ms=45.0,
            accuracy_rate_pct=100.0,
            sla_compliance_pct=100.0,
            error_rate_pct=0.0,
            resource_utilization_pct=28.0,
        ),
        responsibilities=[
            "Arithmetic balance validation (Subtotal + Tax == Total)",
            "Cross-document entity consistency checks",
            "Zero-Fabrication bounding-box anchor validation",
            "Confidence interval verification"
        ],
        owned_resources=["Invariant Solver Engine", "Zero-Fabrication Sentinel", "Z3 SMT Theorem Prover"],
    ),
    "dept_memory": Department(
        department_id="dept_memory",
        name="Enterprise Memory & Context Storage",
        head_agent="Chief Knowledge Custodian",
        role_description="Indexes domain entities, vendor historical structures, vector embeddings, and cross-mission knowledge graphs.",
        parent_department_id="dept_executive",
        sub_departments=[],
        active_workers=2,
        concurrency_limit=10,
        queue_depth=0,
        health_score=99.5,
        sla_target_ms=50.0,
        budget_allocated_usd=25.0,
        budget_spent_usd=1.95,
        kpis=DepartmentKPIs(
            throughput_items_per_min=400.0,
            avg_latency_ms=30.0,
            accuracy_rate_pct=99.4,
            sla_compliance_pct=99.9,
            error_rate_pct=0.1,
            resource_utilization_pct=22.0,
        ),
        responsibilities=[
            "Vector embedding storage and similarity indexing",
            "Vendor layout memory lookup",
            "Episodic mission context retrieval",
            "Knowledge graph updates and deduplication"
        ],
        owned_resources=["Vector Memory Store", "Vendor Historical Graph", "Fast HNSW Index"],
    ),
    "dept_research": Department(
        department_id="dept_research",
        name="Research & Strategic Policy Synthesis",
        head_agent="Director of Autonomous Research",
        role_description="Performs counterfactual simulations, policy exploration, causal graph discovery, and continuous optimization.",
        parent_department_id="dept_executive",
        sub_departments=[],
        active_workers=2,
        concurrency_limit=6,
        queue_depth=1,
        health_score=97.4,
        sla_target_ms=1200.0,
        budget_allocated_usd=40.0,
        budget_spent_usd=5.60,
        kpis=DepartmentKPIs(
            throughput_items_per_min=60.0,
            avg_latency_ms=850.0,
            accuracy_rate_pct=97.9,
            sla_compliance_pct=98.2,
            error_rate_pct=1.1,
            resource_utilization_pct=55.0,
        ),
        responsibilities=[
            "Counterfactual replay simulations",
            "Causal effect estimation (Do-calculus)",
            "Dynamic policy synthesis and benchmarking",
            "Prompt refinement hypotheses generation"
        ],
        owned_resources=["Digital Twin Simulation Engine", "Causal Discovery Graph", "Policy Evolution Arena"],
    ),
    "dept_governance": Department(
        department_id="dept_governance",
        name="Corporate Governance & Regulatory Compliance",
        head_agent="Chief Governance Officer",
        role_description="Guarantees enterprise policy compliance, dual-key authorizations, data sovereignty, and ethical alignment.",
        parent_department_id="dept_executive",
        sub_departments=[],
        active_workers=2,
        concurrency_limit=8,
        queue_depth=0,
        health_score=100.0,
        sla_target_ms=75.0,
        budget_allocated_usd=15.0,
        budget_spent_usd=0.85,
        kpis=DepartmentKPIs(
            throughput_items_per_min=200.0,
            avg_latency_ms=40.0,
            accuracy_rate_pct=100.0,
            sla_compliance_pct=100.0,
            error_rate_pct=0.0,
            resource_utilization_pct=18.0,
        ),
        responsibilities=[
            "Dual-key cryptographic sign-off",
            "Data residency and privacy compliance",
            "Audit trail provenance signing (ED25519)",
            "Policy exception authorization"
        ],
        owned_resources=["ED25519 Signing HSM", "Compliance Rule Matrix", "Enterprise Audit Vault"],
    ),
    "dept_qa": Department(
        department_id="dept_qa",
        name="Continuous Quality Assurance & Calibration",
        head_agent="Lead QA Sentinel",
        role_description="Executes automated multi-corpus benchmarking, reliability calibration, drift detection, and post-processing verification.",
        parent_department_id="dept_executive",
        sub_departments=[],
        active_workers=3,
        concurrency_limit=12,
        queue_depth=2,
        health_score=98.9,
        sla_target_ms=150.0,
        budget_allocated_usd=30.0,
        budget_spent_usd=3.40,
        kpis=DepartmentKPIs(
            throughput_items_per_min=220.0,
            avg_latency_ms=110.0,
            accuracy_rate_pct=99.6,
            sla_compliance_pct=99.5,
            error_rate_pct=0.2,
            resource_utilization_pct=48.0,
        ),
        responsibilities=[
            "Regression and invariant test suite execution",
            "Confidence calibration & ECE verification",
            "Data distribution drift detection",
            "Corpus-wide benchmark scoring"
        ],
        owned_resources=["Benchmark Corpus Runner", "Drift Detection Engine", "Calibration Curve Evaluator"],
    ),
}
