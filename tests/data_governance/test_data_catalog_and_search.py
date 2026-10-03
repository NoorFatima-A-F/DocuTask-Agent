"""Test Searchable Enterprise Data Catalog."""

from app.data_governance.registry.models import (
    AssetType,
    ClassificationLevel,
    DataOwnership,
)
from app.data_governance.registry.repository import DataAssetRepository
from app.data_governance.registry.service import DataGovernanceRegistryService
from app.data_governance.catalog.search import EnterpriseDataCatalog


def test_enterprise_data_catalog_faceted_search():
    """Verify faceted search across departments, classifications, and keywords."""
    repo = DataAssetRepository()
    service = DataGovernanceRegistryService(repository=repo)
    catalog = EnterpriseDataCatalog(repository=repo)
    org_id = "org_catalog_test"

    # Register assets
    service.register_asset(
        asset_id="doc_tax_2025",
        organization_id=org_id,
        workspace_id="ws_finance",
        name="2025 Corporate Tax Filings.pdf",
        asset_type=AssetType.DOCUMENT,
        source="tax_portal",
        location_uri="storage://finance/tax2025.pdf",
        owner=DataOwnership(owner_user_id="user_cpa", responsible_team="Tax", department="Finance"),
        creator_id="user_cpa",
        classification=ClassificationLevel.RESTRICTED,
        compliance_tags=["SOX", "TAX"],
    )

    service.register_asset(
        asset_id="doc_ai_prompt",
        organization_id=org_id,
        workspace_id="ws_eng",
        name="Customer Support System Prompt.txt",
        asset_type=AssetType.PROMPT,
        source="prompt_registry",
        location_uri="storage://prompts/support.txt",
        owner=DataOwnership(owner_user_id="user_dev", responsible_team="AI Core", department="Engineering"),
        creator_id="user_dev",
        classification=ClassificationLevel.INTERNAL,
    )

    catalog.index_all(org_id)

    # 1. Search by department
    fin_results = catalog.search(organization_id=org_id, department="Finance")
    assert len(fin_results) == 1
    assert fin_results[0].asset_id == "doc_tax_2025"

    # 2. Search by classification
    rest_results = catalog.search(organization_id=org_id, classification=ClassificationLevel.RESTRICTED)
    assert len(rest_results) == 1
    assert rest_results[0].name == "2025 Corporate Tax Filings.pdf"

    # 3. Search by keyword
    prompt_results = catalog.search(organization_id=org_id, query="Support")
    assert len(prompt_results) == 1
    assert prompt_results[0].asset_id == "doc_ai_prompt"
