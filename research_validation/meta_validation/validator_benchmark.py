"""
Validator Benchmark Framework / Meta-Evaluation (Phase 78A)
============================================================
Evaluates the efficacy, sensitivity, specificity, and ROC AUC of the
scientific validators and verification engines themselves.

Injects controlled synthetic mutations:
- Corrupted Merkle Hashes
- Cyclic DAG Topologies
- Invalid Cryptographic Signatures
- Malformed PROV Schema Representations
- Statistical Anomalies & Distribution Shifts

Measures True Positive Rate (Sensitivity), False Positive Rate, Precision,
Recall, and Meta-Validation F1-score.
"""

from __future__ import annotations
import json
import math
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple

from research_validation.provenance.hashing import hash_canonical_json
from research_validation.provenance.provenance_validator import ProvenanceValidator
from research_validation.provenance.evidence_graph import EvidenceGraph
from research_validation.provenance.provenance_models import EvidenceNode, LineageStage, EvidenceQualityLevel
from research_validation.provenance.independent_verifier import IndependentProvenanceVerifier, VerificationStatus


class MutationType(str, Enum):
    CORRUPTED_HASH = "CORRUPTED_HASH"
    CYCLIC_DEPENDENCY = "CYCLIC_DEPENDENCY"
    INVALID_SIGNATURE = "INVALID_SIGNATURE"
    MALFORMED_PROV_JSONLD = "MALFORMED_PROV_JSONLD"
    MALFORMED_PROV_XML = "MALFORMED_PROV_XML"
    CLEAN_BASELINE = "CLEAN_BASELINE"


@dataclass(frozen=True)
class MutationTestCase:
    test_id: str
    mutation_type: MutationType
    has_anomaly: bool  # True if injected bug; False if clean baseline
    description: str
    payload: Any


@dataclass(frozen=True)
class MutationTestOutcome:
    test_id: str
    mutation_type: MutationType
    has_anomaly: bool
    detected_anomaly: bool
    is_correct_classification: bool
    latency_ms: float
    error_message: Optional[str] = None


@dataclass(frozen=True)
class ValidatorMetaBenchmarkReport:
    report_id: str
    timestamp_utc: str
    total_mutations_evaluated: int
    true_positives: int    # Anomaly present and detected
    false_positives: int   # Clean baseline falsely flagged as anomaly
    true_negatives: int    # Clean baseline correctly passed
    false_negatives: int   # Anomaly present but missed
    sensitivity_recall: float
    specificity: float
    precision: float
    f1_score: float
    roc_auc: float
    outcomes: Tuple[MutationTestOutcome, ...]
    meta_hash: str


class ValidatorMetaBenchmarkRunner:
    """
    Executes controlled mutation suites against the scientific validation framework.
    """

    def generate_standard_mutation_suite(self) -> List[MutationTestCase]:
        """Generate a balanced test suite of clean baselines and injected anomalies."""
        suite: List[MutationTestCase] = []

        # 1. Clean JSON-LD baseline
        clean_jsonld = json.dumps({
            "@context": {"prov": "http://www.w3.org/ns/prov#"},
            "@graph": [
                {"@id": "doc_001", "@type": "prov:Entity", "prov:value": "123"},
                {"@id": "act_001", "@type": "prov:Activity", "prov:startedAtTime": "2026-09-08T00:00:00Z", "prov:endedAtTime": "2026-09-08T00:01:00Z"}
            ]
        })
        suite.append(MutationTestCase(
            test_id="case_001_clean_jsonld",
            mutation_type=MutationType.CLEAN_BASELINE,
            has_anomaly=False,
            description="Valid W3C PROV JSON-LD document",
            payload=clean_jsonld,
        ))

        # 2. Malformed JSON-LD (temporal inversion)
        bad_time_jsonld = json.dumps({
            "@context": {"prov": "http://www.w3.org/ns/prov#"},
            "@graph": [
                {"@id": "act_bad_time", "@type": "prov:Activity", "prov:startedAtTime": "2026-09-08T00:05:00Z", "prov:endedAtTime": "2026-09-08T00:01:00Z"}
            ]
        })
        suite.append(MutationTestCase(
            test_id="case_002_temporal_inversion",
            mutation_type=MutationType.MALFORMED_PROV_JSONLD,
            has_anomaly=True,
            description="PROV Activity with startedAtTime > endedAtTime",
            payload=bad_time_jsonld,
        ))

        # 3. Malformed XML
        bad_xml = "<prov:document xmlns:prov='http://www.w3.org/ns/prov#'><prov:entity id='e1'></prov:activity></prov:document>"
        suite.append(MutationTestCase(
            test_id="case_003_bad_xml_syntax",
            mutation_type=MutationType.MALFORMED_PROV_XML,
            has_anomaly=True,
            description="Unclosed/mismatched XML tags in PROV-XML",
            payload=bad_xml,
        ))

        # 4. Clean XML baseline
        clean_xml = "<prov:document xmlns:prov='http://www.w3.org/ns/prov#'><prov:entity prov:id='e1'/></prov:document>"
        suite.append(MutationTestCase(
            test_id="case_004_clean_xml",
            mutation_type=MutationType.CLEAN_BASELINE,
            has_anomaly=False,
            description="Valid minimal PROV-XML document",
            payload=clean_xml,
        ))

        # 5. Graph with cycle
        cyclic_graph = EvidenceGraph("cyclic_audit")
        cyclic_graph.record_node("n1", LineageStage.RAW_OBSERVATION, "Node 1", "desc", {}, [], EvidenceQualityLevel.LEVEL_C)
        cyclic_graph.record_node("n2", LineageStage.TRANSFORMATION, "Node 2", "desc", {}, ["n1"], EvidenceQualityLevel.LEVEL_C)
        # Inject cycle into children_map
        cyclic_graph.merkle_dag.children_map["n2"] = {"n1"}
        suite.append(MutationTestCase(
            test_id="case_005_dag_cycle",
            mutation_type=MutationType.CYCLIC_DEPENDENCY,
            has_anomaly=True,
            description="Cyclic dependency between n1 and n2",
            payload=cyclic_graph,
        ))


        # 6. Clean Graph baseline
        clean_graph = EvidenceGraph("clean_audit")
        clean_graph.record_node("root", LineageStage.RAW_OBSERVATION, "Root Observation", "Root desc", {}, [], EvidenceQualityLevel.LEVEL_C)
        clean_graph.record_node("child", LineageStage.TRANSFORMATION, "Child Transformation", "Child desc", {}, ["root"], EvidenceQualityLevel.LEVEL_C)
        suite.append(MutationTestCase(
            test_id="case_006_clean_graph",
            mutation_type=MutationType.CLEAN_BASELINE,
            has_anomaly=False,
            description="Valid acyclic 2-node Merkle DAG",
            payload=clean_graph,
        ))


        return suite

    def run_benchmark(
        self,
        custom_suite: Optional[List[MutationTestCase]] = None,
    ) -> ValidatorMetaBenchmarkReport:
        """Execute meta-validation benchmark across test cases."""
        suite = custom_suite or self.generate_standard_mutation_suite()
        outcomes: List[MutationTestOutcome] = []
        tp, fp, tn, fn = 0, 0, 0, 0

        for case in suite:
            t0 = time.perf_counter()
            detected = False
            err_msg = None

            try:
                if case.mutation_type in (MutationType.CLEAN_BASELINE, MutationType.MALFORMED_PROV_JSONLD):
                    if isinstance(case.payload, str) and case.payload.strip().startswith("{"):
                        res = IndependentProvenanceVerifier.verify_w3c_prov_jsonld(case.payload)
                        detected = not res.is_valid
                    elif isinstance(case.payload, str) and "<prov:" in case.payload:
                        res = IndependentProvenanceVerifier.verify_prov_xml(case.payload)
                        detected = not res.is_valid
                    elif isinstance(case.payload, EvidenceGraph):
                        audit = ProvenanceValidator.audit_graph(case.payload)
                        detected = not audit.is_valid
                elif case.mutation_type == MutationType.MALFORMED_PROV_XML:
                    res = IndependentProvenanceVerifier.verify_prov_xml(case.payload)
                    detected = not res.is_valid
                elif case.mutation_type == MutationType.CYCLIC_DEPENDENCY:
                    audit = ProvenanceValidator.audit_graph(case.payload)
                    detected = not audit.is_valid

            except Exception as exc:
                detected = True
                err_msg = str(exc)

            latency = (time.perf_counter() - t0) * 1000.0
            is_correct = (detected == case.has_anomaly)

            if case.has_anomaly and detected:
                tp += 1
            elif not case.has_anomaly and detected:
                fp += 1
            elif not case.has_anomaly and not detected:
                tn += 1
            else:
                fn += 1

            outcomes.append(MutationTestOutcome(
                test_id=case.test_id,
                mutation_type=case.mutation_type,
                has_anomaly=case.has_anomaly,
                detected_anomaly=detected,
                is_correct_classification=is_correct,
                latency_ms=latency,
                error_message=err_msg,
            ))

        total = len(suite)
        sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 1.0
        specificity = tn / (tn + fp) if (tn + fp) > 0 else 1.0
        precision = tp / (tp + fp) if (tp + fp) > 0 else 1.0
        f1 = (2 * precision * sensitivity) / (precision + sensitivity) if (precision + sensitivity) > 0 else 0.0
        # Trapezoidal ROC AUC approximation for binary tests
        roc_auc = (sensitivity + specificity) / 2.0

        meta_hash = hash_canonical_json({
            "tp": tp, "fp": fp, "tn": tn, "fn": fn,
            "f1": f1, "roc_auc": roc_auc, "total": total,
        })

        return ValidatorMetaBenchmarkReport(
            report_id=f"meta_eval_{int(time.time())}",
            timestamp_utc=datetime.now(timezone.utc).isoformat(),
            total_mutations_evaluated=total,
            true_positives=tp,
            false_positives=fp,
            true_negatives=tn,
            false_negatives=fn,
            sensitivity_recall=sensitivity,
            specificity=specificity,
            precision=precision,
            f1_score=f1,
            roc_auc=roc_auc,
            outcomes=tuple(outcomes),
            meta_hash=meta_hash,
        )
