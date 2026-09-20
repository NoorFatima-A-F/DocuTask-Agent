"""
Unit and integration tests for Phase V5 — Enterprise Document Intelligence & AI Extraction Verification Program.
"""

import os
import json
import pytest
from app.document_intelligence_verification import (
    BoundingBox,
    DocumentCategory,
    PerturbationType,
    DatasetVerifier,
    IngestionVerifier,
    ClassificationVerifier,
    OcrVerifier,
    LayoutVerifier,
    ExtractionVerifier,
    SchemaVerifier,
    RepairVerifier,
    GroundingVerifier,
    CalibrationVerifier,
    BusinessRulesVerifier,
    MultilingualVerifier,
    RobustnessVerifier,
    PipelineVerifier,
    SecurityVerifier,
    PerformanceVerifier,
    RegressionVerifier,
    ReadinessVerifier,
    DocumentIntelligenceScorer,
    EvidenceGenerator,
    VerificationStatus,
    SectionId,
)


def test_bounding_box_iou():
    box1 = BoundingBox(x_min=0.0, y_min=0.0, x_max=2.0, y_max=2.0)
    box2 = BoundingBox(x_min=1.0, y_min=1.0, x_max=3.0, y_max=3.0)
    # Area box1 = 4, Area box2 = 4, Inter area = 1, Union area = 4 + 4 - 1 = 7
    iou = box1.iou(box2)
    assert round(iou, 4) == round(1.0 / 7.0, 4)

    # Identical box
    assert box1.iou(box1) == 1.0


def test_section_a_datasets():
    v = DatasetVerifier()
    res = v.verify_all()
    assert res.section_id == SectionId.SECTION_A_DATASET
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4
    assert all(a.passed for a in res.assertions)


def test_section_b_ingestion():
    v = IngestionVerifier()
    res = v.verify_all()
    assert res.section_id == SectionId.SECTION_B_INGESTION
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_section_c_classification():
    v = ClassificationVerifier()
    res = v.verify_all()
    assert res.section_id == SectionId.SECTION_C_CLASSIFICATION
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_section_d_ocr():
    v = OcrVerifier()
    res = v.verify_all()
    assert res.section_id == SectionId.SECTION_D_OCR
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_section_e_layout():
    v = LayoutVerifier()
    res = v.verify_all()
    assert res.section_id == SectionId.SECTION_E_LAYOUT
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_section_f_extraction():
    v = ExtractionVerifier()
    res = v.verify_all()
    assert res.section_id == SectionId.SECTION_F_EXTRACTION
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_section_g_schema():
    v = SchemaVerifier()
    res = v.verify_all()
    assert res.section_id == SectionId.SECTION_G_SCHEMA
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_section_h_repair():
    v = RepairVerifier()
    res = v.verify_all()
    assert res.section_id == SectionId.SECTION_H_REPAIR
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_section_i_grounding():
    v = GroundingVerifier()
    res = v.verify_all()
    assert res.section_id == SectionId.SECTION_I_GROUNDING
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_section_j_calibration():
    v = CalibrationVerifier()
    res = v.verify_all()
    assert res.section_id == SectionId.SECTION_J_CALIBRATION
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_section_k_business_rules():
    v = BusinessRulesVerifier()
    res = v.verify_all()
    assert res.section_id == SectionId.SECTION_K_BUSINESS_RULES
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_section_l_multilingual():
    v = MultilingualVerifier()
    res = v.verify_all()
    assert res.section_id == SectionId.SECTION_L_MULTILINGUAL
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_section_m_robustness():
    v = RobustnessVerifier()
    res = v.verify_all()
    assert res.section_id == SectionId.SECTION_M_ROBUSTNESS
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_section_n_pipeline():
    v = PipelineVerifier()
    res = v.verify_all()
    assert res.section_id == SectionId.SECTION_N_PIPELINE
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_section_o_security():
    v = SecurityVerifier()
    res = v.verify_all()
    assert res.section_id == SectionId.SECTION_O_SECURITY
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_section_p_performance():
    v = PerformanceVerifier()
    res = v.verify_all()
    assert res.section_id == SectionId.SECTION_P_PERFORMANCE
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_section_q_regression():
    v = RegressionVerifier()
    res = v.verify_all()
    assert res.section_id == SectionId.SECTION_Q_REGRESSION
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_section_r_readiness():
    v = ReadinessVerifier()
    res = v.verify_all()
    assert res.section_id == SectionId.SECTION_R_READINESS
    assert res.status == VerificationStatus.PASSED
    assert res.score == 100.0
    assert len(res.assertions) == 4


def test_document_intelligence_scorer_and_scorecard():
    verifiers = [
        DatasetVerifier(),
        IngestionVerifier(),
        ClassificationVerifier(),
        OcrVerifier(),
        LayoutVerifier(),
        ExtractionVerifier(),
        SchemaVerifier(),
        RepairVerifier(),
        GroundingVerifier(),
        CalibrationVerifier(),
        BusinessRulesVerifier(),
        MultilingualVerifier(),
        RobustnessVerifier(),
        PipelineVerifier(),
        SecurityVerifier(),
        PerformanceVerifier(),
        RegressionVerifier(),
        ReadinessVerifier(),
    ]
    results = {v.verify_all().section_id.value: v.verify_all() for v in verifiers}
    scorer = DocumentIntelligenceScorer()
    scorecard = scorer.calculate_scorecard(results)

    assert scorecard.composite_score == 100.0
    assert scorecard.grade == "A+"
    assert scorecard.production_ready is True
    assert scorecard.total_assertions == 72
    assert scorecard.passed_assertions == 72
    assert len(scorecard.dimensions) == 15
    assert len(scorecard.sections) == 18


def test_evidence_export_and_manifest(tmp_path):
    output_dir = str(tmp_path / "doc_intel_evidence")
    docs_dir = str(tmp_path / "docs")

    verifiers = [DatasetVerifier(), IngestionVerifier(), OcrVerifier()]
    results = {v.verify_all().section_id.value: v.verify_all() for v in verifiers}
    scorer = DocumentIntelligenceScorer()
    scorecard = scorer.calculate_scorecard(results)

    exporter = EvidenceGenerator(output_dir=output_dir, docs_dir=docs_dir)
    summary = exporter.export_all(scorecard)

    assert os.path.exists(summary["manifest_path"])
    assert os.path.exists(summary["report_path"])

    with open(summary["manifest_path"], "r", encoding="utf-8") as f:
        manifest = json.load(f)
    assert manifest["composite_score"] == 100.0
    assert manifest["production_ready"] is True
    assert len(manifest["files"]) > 0
