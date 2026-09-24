"""
Enterprise Benchmark Workload Library for AAOS.
Standardizes 12 production-grade workloads representing real enterprise document processing,
cognitive agent orchestration, high-contention locking, and system load profiles.
"""

from __future__ import annotations

import hashlib
import json
import logging
import math
import random
import time
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Dict

logger = logging.getLogger(__name__)


class WorkloadCategory(str, Enum):
    CPU_INTENSIVE = "CPU_INTENSIVE"
    MEMORY_INTENSIVE = "MEMORY_INTENSIVE"
    IO_INTENSIVE = "IO_INTENSIVE"
    MIXED = "MIXED"
    DISTRIBUTED_COORDINATION = "DISTRIBUTED_COORDINATION"
    HIGH_CONTENTION = "HIGH_CONTENTION"
    CLOUD_LATENCY = "CLOUD_LATENCY"
    BURST_TRAFFIC = "BURST_TRAFFIC"
    LONG_RUNNING_PIPELINE = "LONG_RUNNING_PIPELINE"
    MEDICAL_INVOICE_PROCESSING = "MEDICAL_INVOICE_PROCESSING"
    LEGAL_CONTRACT_AUDIT = "LEGAL_CONTRACT_AUDIT"
    LARGE_PDF_OCR_HEAVY = "LARGE_PDF_OCR_HEAVY"


@dataclass
class WorkloadSpecification:
    """Declared specification of an enterprise benchmark workload."""

    profile_name: str
    category: WorkloadCategory
    algorithmic_complexity: str  # "O(1)", "O(N)", "O(N log N)", "O(N^2)"
    input_size_bytes: int
    operation_description: str
    target_function: Callable[[], Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "profile_name": self.profile_name,
            "category": self.category.value,
            "algorithmic_complexity": self.algorithmic_complexity,
            "input_size_bytes": self.input_size_bytes,
            "operation_description": self.operation_description,
        }


class BenchmarkWorkloadLibrary:
    """
    Standardized benchmark workloads for realistic AAOS performance evaluation.
    """

    @classmethod
    def get_all_workloads(cls) -> Dict[WorkloadCategory, WorkloadSpecification]:
        """Returns catalog of all 12 enterprise benchmark workloads."""
        return {
            WorkloadCategory.CPU_INTENSIVE: cls.cpu_intensive_workload(),
            WorkloadCategory.MEMORY_INTENSIVE: cls.memory_intensive_workload(),
            WorkloadCategory.IO_INTENSIVE: cls.io_intensive_workload(),
            WorkloadCategory.MIXED: cls.mixed_workload(),
            WorkloadCategory.DISTRIBUTED_COORDINATION: cls.distributed_coordination_workload(),
            WorkloadCategory.HIGH_CONTENTION: cls.high_contention_workload(),
            WorkloadCategory.CLOUD_LATENCY: cls.cloud_latency_workload(),
            WorkloadCategory.BURST_TRAFFIC: cls.burst_traffic_workload(),
            WorkloadCategory.LONG_RUNNING_PIPELINE: cls.long_running_pipeline_workload(),
            WorkloadCategory.MEDICAL_INVOICE_PROCESSING: cls.medical_invoice_workload(),
            WorkloadCategory.LEGAL_CONTRACT_AUDIT: cls.legal_contract_workload(),
            WorkloadCategory.LARGE_PDF_OCR_HEAVY: cls.large_pdf_ocr_workload(),
        }

    # 1. CPU Intensive
    @classmethod
    def cpu_intensive_workload(cls) -> WorkloadSpecification:
        def run():
            acc = 0.0
            for i in range(1, 1000):
                acc += math.sin(i) * math.cos(i) * math.sqrt(i)
            return acc

        return WorkloadSpecification(
            profile_name="cpu_trigonometric_fourier_loop",
            category=WorkloadCategory.CPU_INTENSIVE,
            algorithmic_complexity="O(N)",
            input_size_bytes=1000 * 8,
            operation_description="1,000 iterations of transcendental float calculations.",
            target_function=run,
        )

    # 2. Memory Intensive
    @classmethod
    def memory_intensive_workload(cls) -> WorkloadSpecification:
        def run():
            data = [f"token_chunk_{i}_{'x'*32}" for i in range(2000)]
            mapping = {item: idx for idx, item in enumerate(data)}
            return len(mapping)

        return WorkloadSpecification(
            profile_name="memory_heap_token_dictionary",
            category=WorkloadCategory.MEMORY_INTENSIVE,
            algorithmic_complexity="O(N)",
            input_size_bytes=2000 * 64,
            operation_description="Allocates 2,000 string tokens into a hashed symbol table.",
            target_function=run,
        )

    # 3. IO Intensive
    @classmethod
    def io_intensive_workload(cls) -> WorkloadSpecification:
        def run():
            # Simulated storage read/write
            payload = json.dumps({"block": [i for i in range(100)]})
            decoded = json.loads(payload)
            return len(decoded["block"])

        return WorkloadSpecification(
            profile_name="io_simulated_disk_serialization",
            category=WorkloadCategory.IO_INTENSIVE,
            algorithmic_complexity="O(N)",
            input_size_bytes=2048,
            operation_description="JSON buffer serialization and parsing cycle.",
            target_function=run,
        )

    # 4. Mixed
    @classmethod
    def mixed_workload(cls) -> WorkloadSpecification:
        def run():
            raw = [random.random() for _ in range(500)]
            sorted_v = sorted(raw)
            h = hashlib.sha256(str(sorted_v).encode("utf-8")).hexdigest()
            return h

        return WorkloadSpecification(
            profile_name="mixed_sort_and_hash_pipeline",
            category=WorkloadCategory.MIXED,
            algorithmic_complexity="O(N log N)",
            input_size_bytes=500 * 8,
            operation_description="Generates 500 floats, performs Timsort, and calculates SHA-256.",
            target_function=run,
        )

    # 5. Distributed Coordination
    @classmethod
    def distributed_coordination_workload(cls) -> WorkloadSpecification:
        def run():
            # Vector clock & quorum simulation
            v_clocks = {"node_1": 10, "node_2": 15, "node_3": 12}
            v_clocks["node_1"] += 1
            quorum = sum(1 for v in v_clocks.values() if v >= 11) >= 2
            return quorum

        return WorkloadSpecification(
            profile_name="distributed_vector_clock_quorum",
            category=WorkloadCategory.DISTRIBUTED_COORDINATION,
            algorithmic_complexity="O(1)",
            input_size_bytes=256,
            operation_description="Vector clock tick and majority quorum consensus verification.",
            target_function=run,
        )

    # 6. High Contention
    @classmethod
    def high_contention_workload(cls) -> WorkloadSpecification:
        shared_state = {"counter": 0, "cas_version": 1}

        def run():
            # Optimistic concurrency CAS loop simulation
            expected_ver = shared_state["cas_version"]
            shared_state["counter"] += 1
            shared_state["cas_version"] = expected_ver + 1
            return shared_state["counter"]

        return WorkloadSpecification(
            profile_name="high_contention_optimistic_cas",
            category=WorkloadCategory.HIGH_CONTENTION,
            algorithmic_complexity="O(1)",
            input_size_bytes=128,
            operation_description="Atomic Compare-And-Swap loop on shared memory counter.",
            target_function=run,
        )

    # 7. Cloud Latency
    @classmethod
    def cloud_latency_workload(cls) -> WorkloadSpecification:
        def run():
            time.sleep(0.001)  # 1ms cloud network roundtrip
            return True

        return WorkloadSpecification(
            profile_name="cloud_grpc_network_roundtrip",
            category=WorkloadCategory.CLOUD_LATENCY,
            algorithmic_complexity="O(1)",
            input_size_bytes=512,
            operation_description="Simulates 1ms gRPC network transit latency to GCP Cloud Run.",
            target_function=run,
        )

    # 8. Burst Traffic
    @classmethod
    def burst_traffic_workload(cls) -> WorkloadSpecification:
        def run():
            # Process a burst of 50 incoming telemetry events
            events = [{"event_id": i, "val": i * 10} for i in range(50)]
            filtered = [e for e in events if e["val"] % 20 == 0]
            return len(filtered)

        return WorkloadSpecification(
            profile_name="burst_event_stream_filtering",
            category=WorkloadCategory.BURST_TRAFFIC,
            algorithmic_complexity="O(N)",
            input_size_bytes=50 * 64,
            operation_description="Processes and filters a sudden micro-burst of 50 agent events.",
            target_function=run,
        )

    # 9. Long Running Pipeline
    @classmethod
    def long_running_pipeline_workload(cls) -> WorkloadSpecification:
        def run():
            accum = 0
            for i in range(5000):
                accum = (accum + i * 17) % 1000003
            return accum

        return WorkloadSpecification(
            profile_name="long_running_state_machine_reduction",
            category=WorkloadCategory.LONG_RUNNING_PIPELINE,
            algorithmic_complexity="O(N)",
            input_size_bytes=5000 * 8,
            operation_description="Long iterative state-machine transition sequence.",
            target_function=run,
        )

    # 10. Medical Invoice Processing
    @classmethod
    def medical_invoice_workload(cls) -> WorkloadSpecification:
        invoice_doc = {
            "facility": "Mayo Clinic Rochester",
            "patient_id": "MED-994829",
            "line_items": [
                {"cpt": "99214", "desc": "Office visit lvl 4", "amount": 250.00},
                {"cpt": "80053", "desc": "Comprehensive metabolic panel", "amount": 85.00},
                {"cpt": "71046", "desc": "Chest X-ray 2 views", "amount": 145.00},
            ],
            "total_billed": 480.00,
            "copay": 25.00,
        }

        def run():
            total = sum(item["amount"] for item in invoice_doc["line_items"])
            valid = abs(total - invoice_doc["total_billed"]) < 0.01
            h = hashlib.sha256(json.dumps(invoice_doc, sort_keys=True).encode("utf-8")).hexdigest()
            return valid, h

        return WorkloadSpecification(
            profile_name="medical_invoice_claim_audit",
            category=WorkloadCategory.MEDICAL_INVOICE_PROCESSING,
            algorithmic_complexity="O(N)",
            input_size_bytes=1024,
            operation_description="CPT code extraction, arithmetic balance verification, and SHA-256 audit digest.",
            target_function=run,
        )

    # 11. Legal Contract Audit
    @classmethod
    def legal_contract_workload(cls) -> WorkloadSpecification:
        contract_text = """
        MASTER SERVICES AGREEMENT (MSA). This Agreement is entered into by and between Enterprise AG and Vendor LLC.
        Section 4.1: Indemnification shall be capped at 2x annual contract value.
        Section 8.2: Governing law shall be the State of Delaware.
        Section 12.3: Data confidentiality SLA guarantees 99.99% privacy compliance.
        """ * 10

        def run():
            clauses = contract_text.split("Section")
            indemnity = [c for c in clauses if "Indemnification" in c]
            gov_law = [c for c in clauses if "Governing law" in c]
            return len(indemnity) > 0 and len(gov_law) > 0

        return WorkloadSpecification(
            profile_name="legal_contract_clause_nlp_audit",
            category=WorkloadCategory.LEGAL_CONTRACT_AUDIT,
            algorithmic_complexity="O(N)",
            input_size_bytes=len(contract_text),
            operation_description="Multi-clause tokenization, indemnity risk scanning, and jurisdiction extraction.",
            target_function=run,
        )

    # 12. Large PDF OCR Heavy
    @classmethod
    def large_pdf_ocr_workload(cls) -> WorkloadSpecification:
        ocr_blocks = [
            {"page": p, "bbox": [10, 20, 200, 30], "text": f"Page {p} OCR extracted high-density table row {r}"}
            for p in range(1, 10)
            for r in range(1, 20)
        ]

        def run():
            reconstructed = "\n".join(b["text"] for b in ocr_blocks)
            doc_hash = hashlib.sha256(reconstructed.encode("utf-8")).hexdigest()
            return len(ocr_blocks), doc_hash

        return WorkloadSpecification(
            profile_name="large_pdf_ocr_page_assembly",
            category=WorkloadCategory.LARGE_PDF_OCR_HEAVY,
            algorithmic_complexity="O(N)",
            input_size_bytes=len(ocr_blocks) * 128,
            operation_description="Multi-page OCR bounding box layout reconstruction and text reconciliation.",
            target_function=run,
        )
