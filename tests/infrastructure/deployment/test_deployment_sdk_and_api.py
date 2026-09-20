"""Tests for Unified DeploymentSDK and FastAPI REST API Endpoints."""

import pytest
from app.infrastructure.deployment import DeploymentSDK, get_deployment_sdk
from app.infrastructure.deployment.api.deployment_routes import (
    list_deployments,
    trigger_deployment,
    get_deployment,
    rollback_deployment,
    list_releases,
    create_release,
    list_pipelines,
    run_pipeline,
    list_artifacts,
    promote_artifact,
    create_or_enable_feature,
    DeploymentCreateRequest,
    RollbackTriggerRequest,
    ReleaseCreateRequest,
    PipelineRunRequest,
    PromoteRequest,
    FeatureFlagCreateRequest,
)


def test_deployment_sdk_end_to_end_flow() -> None:
    sdk = DeploymentSDK()

    # 1. CI Pipeline execution
    pipe_run = sdk.run_pipeline("docutask-worker-ci", "commit-abcdef123456")
    assert pipe_run.status.value == "passed"

    # 2. Register and sign artifact
    art = sdk.artifact_registry.register_artifact(
        name="docutask-worker",
        version="2.1.0",
        artifact_type=sdk.artifact_registry.signer.__class__.__name__ and "container_image",  # container_image
        commit_sha="commit-abcdef123456",
        auto_sign=True,
    )
    assert art.artifact_id is not None

    # 3. Create release
    rel = sdk.create_release(
        version="2.1.0",
        components_changed=["worker"],
        artifact_ids=[art.artifact_id],
        changelog="New worker version",
    )
    assert rel.release_id is not None

    # 4. Deploy
    dep = sdk.deploy(
        service_name="docutask-worker",
        target_environment="prod",
        target_version="2.1.0",
        release_id=rel.release_id,
    )
    assert dep.status.value == "completed"
    assert sdk.verify(dep.deployment_id) is True

    # 5. Rollback
    rca = sdk.rollback(dep.deployment_id, reason="Testing SDK rollback API")
    assert rca.report_id is not None


def test_deployment_fastapi_routes() -> None:
    sdk = get_deployment_sdk()

    # 1. Trigger deployment
    dep_req = DeploymentCreateRequest(
        service_name="api-gateway",
        target_environment="staging",
        target_version="1.0.1",
    )
    dep_resp = trigger_deployment(dep_req)
    dep_id = dep_resp["deployment_id"]
    assert dep_resp["status"] == "completed"

    # 2. Get deployment
    get_resp = get_deployment(dep_id)
    assert get_resp["deployment_id"] == dep_id

    # 3. List deployments
    list_resp = list_deployments()
    assert list_resp["deployments_count"] >= 1

    # 4. Rollback route
    rb_req = RollbackTriggerRequest(reason="API test rollback")
    rb_resp = rollback_deployment(dep_id, rb_req)
    assert rb_resp["report_id"] is not None

    # 5. Create release route
    rel_req = ReleaseCreateRequest(
        version="3.0.0",
        components_changed=["all"],
        artifact_ids=["art-test"],
        changelog="Major 3.0.0 update",
    )
    rel_resp = create_release(rel_req)
    assert rel_resp["version"] == "3.0.0"

    # 6. Pipeline run route
    pr_req = PipelineRunRequest(pipeline_name="gateway-ci", commit_sha="commit-1234")
    pr_resp = run_pipeline(pr_req)
    assert pr_resp["status"] == "passed"

    # 7. Features route
    feat_req = FeatureFlagCreateRequest(flag_key="new_checkout_ui", percentage=50.0)
    feat_resp = create_or_enable_feature(feat_req)
    assert feat_resp["flag_key"] == "new_checkout_ui"
