"""Test Data Governance SDK Facade and REST API Router."""

import pytest
from app.data_governance.sdk.client import DataGovernanceSDK
from app.data_governance.registry.models import ClassificationLevel, AssetType
from app.data_governance.api.routes import create_data_governance_router, RegisterAssetRequest, ClassifyTextRequest


def test_data_governance_sdk_facade():
    """Verify SDK facade registration, classification, masking, and access tracking."""
    sdk = DataGovernanceSDK()

    asset = sdk.register(
        asset_id="asset_sdk_doc_1",
        organization_id="org_sdk",
        workspace_id="ws_sdk",
        name="Quarterly Summary.pdf",
        source="upload",
        owner_id="user_sdk_owner",
        classification=ClassificationLevel.INTERNAL,
    )
    assert asset.asset_id == "asset_sdk_doc_1"

    # Classify
    cls_res = sdk.classify("Confidential compensation records for engineering team.")
    assert cls_res.classification in (ClassificationLevel.RESTRICTED, ClassificationLevel.CONFIDENTIAL)

    # Mask
    masked = sdk.mask("Contact: ceo@startup.io")
    assert "c***@startup.io" in masked

    # Access
    event = sdk.record_access(asset.asset_id, "org_sdk", "user_sdk_owner")
    assert event.asset_id == asset.asset_id


def test_data_governance_api_endpoints_direct():
    """Verify FastAPI router functions directly without requiring httpx TestClient."""
    sdk = DataGovernanceSDK()
    router = create_data_governance_router(
        registry_service=sdk.registry,
        classifier_engine=sdk.classifier,
        lineage_graph=sdk.lineage.graph,
        provenance_engine=sdk.provenance,
        catalog=sdk.catalog,
    )

    # 1. Register Asset via router function
    reg_req = RegisterAssetRequest(
        asset_id="api_asset_1",
        organization_id="org_api",
        workspace_id="ws_api",
        name="API Invoice.pdf",
        asset_type=AssetType.DOCUMENT,
        source="api_sync",
        location_uri="s3://invoices/api.pdf",
        owner_id="user_api",
        responsible_team="Billing",
        department="Finance",
        creator_id="user_api",
        classification=ClassificationLevel.CONFIDENTIAL,
    )
    # Find route handlers
    routes_by_path = {r.path: r.endpoint for r in router.routes}

    register_fn = routes_by_path["/api/v1/data/assets"]
    res_reg = register_fn(reg_req)
    assert res_reg["status"] == "SUCCESS"
    assert res_reg["asset"].name == "API Invoice.pdf"

    # 2. Get Asset
    get_fn = routes_by_path["/api/v1/data/assets/{asset_id}"]
    res_get = get_fn(asset_id="api_asset_1", organization_id="org_api")
    assert res_get["asset"].asset_id == "api_asset_1"

    # 3. Classify Text
    classify_fn = routes_by_path["/api/v1/data/classify"]
    res_cls = classify_fn(ClassifyTextRequest(text="Confidential patient health MRN-998811"))
    assert res_cls["result"].classification is not None

    # 4. Search Catalog
    search_fn = routes_by_path["/api/v1/data/catalog/search"]
    res_search = search_fn(organization_id="org_api", q="Invoice")
    assert len(res_search["results"]) >= 1
