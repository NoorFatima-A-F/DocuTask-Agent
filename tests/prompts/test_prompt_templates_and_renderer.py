"""Tests for Prompt Template Engine, Variable Validation, and Rendering (Phase 8D)."""

import pytest
from app.prompts.templates.variables import PromptVariableDefinition, VariableType
from app.prompts.templates.renderer import PromptTemplateRenderer
from app.prompts.templates.engine import PromptTemplateEngine


def test_variable_validation():
    v_str = PromptVariableDefinition(name="department", var_type=VariableType.STRING, required=True)
    assert v_str.validate_value("Finance") == "Finance"

    with pytest.raises(ValueError, match="Required variable 'department' was not provided"):
        v_str.validate_value(None)

    v_num = PromptVariableDefinition(name="threshold", var_type=VariableType.NUMBER, default_value=100.0)
    assert v_num.validate_value(None) == 100.0
    assert v_num.validate_value("250.5") == 250.5

    v_bool = PromptVariableDefinition(name="strict_mode", var_type=VariableType.BOOLEAN)
    assert v_bool.validate_value("yes") is True
    assert v_bool.validate_value(False) is False


def test_template_rendering_variables_and_conditionals():
    template = """
You are an AI assistant for {{ department }}.
{% if include_policy %}
Follow strict policy rules: {{ policy_name }}
{% endif %}
Analyze document:
{{ document_text }}
"""
    # 1. Render without conditional
    res1 = PromptTemplateRenderer.render(
        template=template,
        variables={"department": "Accounting", "document_text": "Invoice #123", "include_policy": False},
    )
    assert "Accounting" in res1
    assert "Invoice #123" in res1
    assert "Follow strict policy rules" not in res1

    # 2. Render with conditional
    res2 = PromptTemplateRenderer.render(
        template=template,
        variables={
            "department": "Accounting",
            "document_text": "Invoice #123",
            "include_policy": True,
            "policy_name": "SOX-2026",
        },
    )
    assert "Follow strict policy rules: SOX-2026" in res2


def test_template_engine_partials_and_composition():
    engine = PromptTemplateEngine()
    engine.register_partial("footer", "End of prompt instructions. Return JSON only.")

    template = "Extract invoice.\n{{> footer }}"
    rendered = engine.render(template)
    assert "Return JSON only." in rendered

    # Composition
    composed = engine.compose_templates(
        base_template="You are an enterprise AI assistant.",
        department_rules="Do not disclose customer phone numbers.",
        task_instructions="Extract the billing address.",
    )
    assert "enterprise AI assistant" in composed
    assert "Do not disclose customer phone numbers" in composed
    assert "Extract the billing address" in composed
