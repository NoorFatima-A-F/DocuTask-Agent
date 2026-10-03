"""Unit tests for Deployment REST API endpoints."""
from app.deployment.api.routes import (
    approve_promotion,
    create_deployment,
    create_flag,
    create_release,
    evaluate_flag,
    execute_rollback,
    list_deployments,
    list_releases,
    request_promotion,
)
from app.deployment.api.schemas import (
    ApprovePromotionSchema,
    CreateDeploymentRequest,
    CreateFlagRequest,
    CreateReleaseRequest,
    EvaluateFlagRequest,
    RequestPromotionSchema,
    RollbackRequest,
)


def test_api_release_and_deployment_workflow():
    # 1. Create release
    rel_req = CreateReleaseRequest(
        version="4.0.0",
        name="API Test Release",
        commit_sha="api-commit-sha",
        artifact_ids=["art-api-01"],
    )
    rel_res = create_release(rel_req)
    assert rel_res.version == "4.0.0"
    assert rel_res.status == "PUBLISHED"

    # List releases
    rels = list_releases()
    assert any(r.release_id == rel_res.release_id for r in rels)

    # 2. Create deployment
    dep_req = CreateDeploymentRequest(
        release_id=rel_res.release_id,
        target_environment="dev",
        strategy="ROLLING",
        replicas=2,
    )
    dep_res = create_deployment(dep_req)
    assert dep_res.status == "ACTIVE"
    assert dep_res.replicas == 2

    # List deployments
    deps = list_deployments(environment="dev")
    assert len(deps) >= 1

    # 3. Rollback
    rb_req = RollbackRequest(
        deployment_id=dep_res.deployment_id,
        reason="API test rollback",
    )
    rb_res = execute_rollback(rb_req)
    assert rb_res.success is True
    assert rb_res.failed_deployment_id == dep_res.deployment_id


def test_api_promotion_and_flags():
    # 1. Create flag
    flag_req = CreateFlagRequest(
        key="api_experimental_flag",
        name="API Exp Flag",
        enabled=True,
    )
    flag_res = create_flag(flag_req)
    assert flag_res["key"] == "api_experimental_flag"

    # 2. Evaluate flag
    eval_req = EvaluateFlagRequest(key="api_experimental_flag", environment="prod")
    eval_res = evaluate_flag(eval_req)
    assert eval_res.enabled is True

    # 3. Request promotion
    prom_req = RequestPromotionSchema(
        release_id="rel-prom-01",
        target_env="staging",
        source_env="testing",
    )
    prom_res = request_promotion(prom_req)
    assert prom_res.status == "PENDING_APPROVAL"

    # 4. Approve promotion
    appr_req = ApprovePromotionSchema(role="qa_lead", approver="qa_lead_user")
    appr_res = approve_promotion(prom_res.promotion_id, appr_req)
    assert "qa_lead" in appr_res.approved_roles
