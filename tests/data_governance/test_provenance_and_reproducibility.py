"""Test Provenance Engine and Output Reproducibility Verification."""

from app.data_governance.provenance.source import ProvenanceSourceRecord
from app.data_governance.provenance.transformations import ProvenanceTransformationRecord
from app.data_governance.provenance.history import ProvenanceHistoryEngine


def test_provenance_source_and_transformations():
    """Verify source checksum validation and transformation provenance chains."""
    engine = ProvenanceHistoryEngine()
    asset_id = "asset_ai_summary_88"

    # 1. Record Source
    source = ProvenanceSourceRecord(
        source_id="src_origin_1",
        asset_id=asset_id,
        original_uri="s3://documents/quarterly_report.pdf",
        source_type="FILE_UPLOAD",
        checksum_sha256="5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
        uploaded_by="user_cfo",
        organization_id="org_enterprise",
    )
    engine.record_source(source)

    # Content integrity check
    assert source.verify_content("password") is True
    assert source.verify_content("wrong_content") is False

    # 2. Record AI Transformation
    transform = ProvenanceTransformationRecord(
        transformation_id="trans_ai_1",
        asset_id=asset_id,
        step_name="AI_Executive_Summary",
        input_artifacts=[{"asset_id": "asset_raw_report", "version": "1"}],
        output_artifacts=[{"asset_id": asset_id, "version": "1"}],
        model_version="gemini-2.5-flash@v1.0",
        prompt_version="prompt_exec_summary@v2.1",
        parameters={"temperature": 0.2, "max_tokens": 1000},
        actor_id="agent_cfo_assistant",
    )
    engine.record_transformation(transform)

    # 3. Verify Reproducibility
    reproducibility = engine.verify_reproducibility(asset_id)
    assert reproducibility["is_reproducible"] is True
    assert reproducibility["has_source_record"] is True
    assert reproducibility["transformation_steps_count"] == 1
    assert reproducibility["all_models_specified"] is True
