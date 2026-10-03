"""Tests for Prompt Governance Developer SDK, Decorators, and FastAPI Endpoints (Phase 8D)."""

from app.prompts.sdk.client import PromptGovernanceSDK
from app.prompts.sdk.decorators import governed_prompt
from app.prompts.evaluation.datasets import PromptEvaluationDataset
from app.prompts.api.routes import (
    create_prompt,
    get_prompt,
    transition_lifecycle,
    render_prompt,
)
from app.prompts.api.schemas import (
    PromptCreateRequestDTO,
    PromptLifecycleTransitionRequestDTO,
    PromptRenderRequestDTO,
)


def test_prompt_governance_sdk_end_to_end():
    sdk = PromptGovernanceSDK()

    # 1. Create prompt
    prompt, v1 = sdk.create_prompt(
        prompt_id="invoice_extractor",
        name="Invoice Extractor",
        organization_id="org_sdk",
        owner="lead_dev@enterprise.com",
        initial_template="Extract vendor from: {{ doc_text }}",
        variables=["doc_text"],
    )

    # 2. Evaluate prompt
    dataset = PromptEvaluationDataset(
        dataset_id="ds_eval_1",
        name="Invoice Dataset",
        organization_id="org_sdk",
    )
    dataset.add_case(variables={"doc_text": "Acme Corp"}, expected_output="Acme Corp")
    metrics = sdk.evaluate_version(
        prompt_id="invoice_extractor",
        version_id=v1.version_id,
        organization_id="org_sdk",
        dataset=dataset,
        inference_fn=lambda prompt_text: "Acme Corp",
    )
    assert metrics.accuracy_score == 1.0

    # 3. Submit and approve
    sdk.submit_and_approve("invoice_extractor", v1.version_id, "org_sdk")

    # 4. Deploy to Production
    sdk.deploy("invoice_extractor", v1.version_id, "org_sdk")

    # 5. Execute governed prompt
    res = sdk.execute_governed_prompt(
        prompt_id="invoice_extractor",
        organization_id="org_sdk",
        variables={"doc_text": "Acme Corp"},
        model_executor=lambda rendered: f"Extracted from '{rendered}'",
    )
    assert res.is_success is True
    assert "Acme Corp" in res.rendered_prompt

    # 6. Verify telemetry recorded
    summary = sdk.analytics.get_prompt_summary("invoice_extractor", "org_sdk")
    assert summary.total_invocations == 1


def test_governed_prompt_decorator():
    sdk = PromptGovernanceSDK()

    prompt, v1 = sdk.create_prompt(
        prompt_id="greet_user",
        name="Greet User",
        organization_id="org_dec",
        owner="dev@test.com",
        initial_template="Hello {{ user_name }}! Welcome to DocuTask.",
        variables=["user_name"],
    )
    sdk.submit_and_approve("greet_user", v1.version_id, "org_dec")
    sdk.deploy("greet_user", v1.version_id, "org_dec")

    @governed_prompt(prompt_id="greet_user", sdk=sdk, organization_id="org_dec")
    def run_llm(rendered_prompt: str):
        return f"LLM Output for: {rendered_prompt}"

    res = run_llm(user_name="Alice")
    assert res.is_success is True
    assert "Hello Alice!" in res.rendered_prompt


def test_fastapi_prompt_governance_endpoints():
    # 1. Create prompt
    create_req = PromptCreateRequestDTO(
        prompt_id="api_prompt_1",
        name="API Prompt Test",
        owner="api_user@test.com",
        initial_template="Analyze {{ query }}",
        variables=["query"],
    )
    create_res = create_prompt(create_req, organization_id="org_api")
    assert create_res.prompt_id == "api_prompt_1"

    # 2. Get prompt
    get_res = get_prompt("api_prompt_1", organization_id="org_api")
    assert get_res.name == "API Prompt Test"

    # 3. Transition lifecycle to VALIDATION
    trans_req = PromptLifecycleTransitionRequestDTO(
        target_state="VALIDATION",
        actor="qa@test.com",
        reason="Ready for validation",
    )
    trans_res = transition_lifecycle("api_prompt_1", trans_req, organization_id="org_api")
    assert trans_res.to_state.value == "VALIDATION"

    # 4. Render prompt using explicit version
    render_req = PromptRenderRequestDTO(
        version_id=create_res.active_version_id,
        variables={"query": "Financial Quarter 3"},
    )
    render_res = render_prompt("api_prompt_1", render_req, organization_id="org_api")
    assert "Financial Quarter 3" in render_res["rendered_text"]
