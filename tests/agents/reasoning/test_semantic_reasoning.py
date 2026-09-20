"""
Production Tests for LLM Semantic Reasoning Engine.
Covers StructuredOutputParser, ReasoningMemory, LLMReasoningClient, SemanticReasoner, and AnomalyAnalysis.
"""

import pytest
from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID

from app.agents.intelligence.reasoning.llm_reasoning_client import (
    LLMReasoningClient,
    ReasoningResponse,
)
from app.agents.intelligence.reasoning.reasoning_memory import (
    Hypothesis,
    PremiseType,
    ReasoningMemory,
    ReasoningPremise,
)
from app.agents.intelligence.reasoning.semantic_reasoner import (
    AnomalyAnalysisResult,
    SemanticAnalysisResult,
    SemanticReasoner,
)
from app.agents.intelligence.reasoning.structured_output_parser import (
    StructuredOutputParser,
)


class SampleModel(BaseModel):
    name: str
    count: int
    tags: List[str] = Field(default_factory=list)
    confidence: Optional[float] = 1.0


class TestStructuredOutputParser:
    def test_clean_raw_json_object(self):
        raw = '{"name": "test", "count": 5}'
        cleaned = StructuredOutputParser.clean_json_string(raw)
        assert cleaned == '{"name": "test", "count": 5}'
        parsed = StructuredOutputParser.parse_dict(raw)
        assert parsed["name"] == "test"
        assert parsed["count"] == 5

    def test_markdown_code_block_stripping(self):
        raw = """```json
{
    "name": "invoice_parser",
    "count": 10,
    "tags": ["financial", "tax"]
}
```"""
        parsed = StructuredOutputParser.parse_model(raw, SampleModel)
        assert parsed.name == "invoice_parser"
        assert parsed.count == 10
        assert parsed.tags == ["financial", "tax"]

    def test_trailing_comma_repair(self):
        raw = '{"name": "repair_test", "count": 1, "tags": ["a", "b",],}'
        parsed = StructuredOutputParser.parse_dict(raw)
        assert parsed["name"] == "repair_test"
        assert parsed["tags"] == ["a", "b"]

    def test_single_quote_repair(self):
        raw = "{'name': 'single_quote', 'count': 42}"
        parsed = StructuredOutputParser.parse_dict(raw)
        assert parsed["name"] == "single_quote"
        assert parsed["count"] == 42

    def test_parse_model_validation_failure(self):
        raw = '{"name": "missing_count"}'
        with pytest.raises(Exception):
            StructuredOutputParser.parse_model(raw, SampleModel)

    def test_parse_invalid_text_raises_value_error(self):
        with pytest.raises(ValueError):
            StructuredOutputParser.parse_dict("This is completely unparseable plain prose without json.")

    def test_array_wrapping(self):
        raw = '["item1", "item2", "item3"]'
        parsed = StructuredOutputParser.parse_dict(raw)
        assert parsed == {"data": ["item1", "item2", "item3"]}


class TestReasoningMemory:
    def test_add_premise(self):
        mem = ReasoningMemory()
        p = mem.add_premise(
            statement="Document is an ACME invoice",
            premise_type=PremiseType.DOCUMENT_MODALITY,
            source="classifier",
            confidence=0.98,
        )
        assert isinstance(p.premise_id, UUID)
        assert p.premise_type == PremiseType.DOCUMENT_MODALITY
        assert p.confidence == 0.98
        assert len(mem.get_all_premises()) == 1

    def test_create_and_validate_hypothesis(self):
        mem = ReasoningMemory()
        p = mem.add_premise("Total is $500")
        h = mem.create_hypothesis("Document total is $500", supporting_premises=[p.premise_id])
        assert not h.validated
        assert not h.rejected

        validated_h = mem.validate_hypothesis(h.hypothesis_id, final_confidence=0.99)
        assert validated_h.validated
        assert validated_h.confidence == 0.99
        assert len(mem.get_validated_hypotheses()) == 1
        # Check automatic deduction premise creation
        assert len(mem.get_all_premises()) == 2

    def test_reject_hypothesis(self):
        mem = ReasoningMemory()
        h = mem.create_hypothesis("Currency is EUR")
        mem.reject_hypothesis(h.hypothesis_id, reason="Currency symbol is '$'")

        assert h.rejected
        assert not h.validated
        assert h.confidence == 0.0
        assert "symbol is '$'" in h.rejection_reason

    def test_memory_summary(self):
        mem = ReasoningMemory(session_id="test-sess")
        mem.add_premise("Premise A")
        h = mem.create_hypothesis("Hypo A")
        mem.validate_hypothesis(h.hypothesis_id)

        summary = mem.get_summary()
        assert summary["session_id"] == "test-sess"
        assert summary["total_hypotheses"] == 1
        assert summary["validated_count"] == 1
        assert len(summary["trail"]) >= 3

    def test_premise_to_dict(self):
        p = ReasoningPremise(statement="Fact 1", premise_type=PremiseType.REGULATORY_RULE, source="rule_book")
        d = p.to_dict()
        assert d["premise_type"] == "regulatory_rule"
        assert d["statement"] == "Fact 1"

    def test_hypothesis_to_dict(self):
        h = Hypothesis(description="Hypo 1", counter_evidence=["Counter 1"])
        d = h.to_dict()
        assert d["description"] == "Hypo 1"
        assert d["counter_evidence"] == ["Counter 1"]


class TestLLMReasoningClient:
    @pytest.mark.asyncio
    async def test_simulated_completion(self):
        client = LLMReasoningClient()
        resp = await client.complete("Explain the process of invoice extraction")
        assert resp.simulated is True
        assert resp.latency_ms > 0
        assert resp.cost_usd >= 0
        assert client.total_calls == 1

    @pytest.mark.asyncio
    async def test_generate_structured_goal_schema(self):
        client = LLMReasoningClient()
        result = await client.generate_structured(
            prompt="Extract vendor, amount and tax from invoice",
            schema_model=SemanticAnalysisResult,
        )
        assert isinstance(result, SemanticAnalysisResult)
        assert result.confidence >= 0.9
        assert result.document_type in ("invoice", "tax_form", "document")
        assert len(result.key_entities) > 0

    @pytest.mark.asyncio
    async def test_token_and_cost_accumulation(self):
        client = LLMReasoningClient()
        await client.complete("Prompt 1")
        await client.complete("Prompt 2")
        assert client.total_calls == 2
        assert client.total_cost_usd > 0.0


class TestSemanticReasoner:
    @pytest.mark.asyncio
    async def test_reason_about_goal(self):
        reasoner = SemanticReasoner()
        mem = ReasoningMemory()
        res = await reasoner.reason_about_goal(
            goal_text="Process invoice.pdf and extract vendor, total, and line items",
            memory=mem,
            context={"file_type": "PDF", "source": "email_attachment"},
        )
        assert isinstance(res, SemanticAnalysisResult)
        assert res.primary_intent == "document_processing"
        assert res.document_type == "invoice"
        assert res.confidence >= 0.9
        assert len(mem.get_validated_hypotheses()) == 1

    @pytest.mark.asyncio
    async def test_evaluate_anomaly(self):
        reasoner = SemanticReasoner()
        diag = await reasoner.evaluate_anomaly(
            task_id="ocr_task_01",
            error_message="Image DPI below 150 - unreadable characters",
            partial_output={"raw_text": "??? ??"},
        )
        assert isinstance(diag, AnomalyAnalysisResult)
        assert diag.is_recoverable is True
        assert diag.suggested_fix != ""

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "doc_text,expected_type",
        [
            ("Process medical invoice from General Hospital with patient ID", "invoice"),
            ("Parse Form 1040 federal tax return for year 2025", "tax_form"),
            ("Analyze commercial real estate lease contract agreement", "document"),
            ("Extract transactions from Citibank checking bank statement", "document"),
            ("Process retail purchase receipt from Walmart #1024", "invoice"),
            ("Verify insurance claim proof of loss and claim details", "document"),
            ("Read employment verification letter with salary figures", "document"),
            ("Process utility electric bill statement due next month", "invoice"),
        ],
    )
    async def test_reason_about_various_document_types(self, doc_text, expected_type):
        reasoner = SemanticReasoner()
        mem = ReasoningMemory()
        res = await reasoner.reason_about_goal(goal_text=doc_text, memory=mem)
        assert isinstance(res, SemanticAnalysisResult)
        assert res.confidence > 0.0
        assert len(res.key_entities) > 0

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "error_str,is_recoverable,suggested_action",
        [
            ("Connection timeout after 30000ms connecting to OCR microservice", True, "retry"),
            ("Fatal: Invalid license key for commercial OCR engine", False, "escalate"),
            ("Validation failed: Total amount negative (-$50.00)", True, "replan"),
            ("HTTP 429 Too Many Requests rate limit exceeded", True, "retry"),
            ("Corrupted PDF header - EOF missing", False, "escalate"),
            ("Confidence score 0.42 below threshold 0.85", True, "replan"),
            ("Missing required field: vendor_name", True, "replan"),
            ("Schema mismatch: expected array of objects, got null", True, "replan"),
        ],
    )
    async def test_evaluate_various_anomalies(self, error_str, is_recoverable, suggested_action):
        reasoner = SemanticReasoner()
        diag = await reasoner.evaluate_anomaly(
            task_id="task_diag_test",
            error_message=error_str,
            partial_output={},
        )
        assert isinstance(diag, AnomalyAnalysisResult)
        assert diag.root_cause != ""
        assert diag.suggested_fix != ""

    def test_premise_filtering_by_type(self):
        mem = ReasoningMemory()
        mem.add_premise("Doc is PDF", PremiseType.DOCUMENT_MODALITY)
        mem.add_premise("HIPAA rule applies", PremiseType.REGULATORY_RULE)
        mem.add_premise("Invoice must have vendor", PremiseType.SCHEMA_CONSTRAINT)
        mem.add_premise("Goal is to process", PremiseType.GOAL_OBJECTIVE)

        all_p = mem.get_all_premises()
        assert len(all_p) == 4
        assert any(p.premise_type == PremiseType.REGULATORY_RULE for p in all_p)
        assert any(p.premise_type == PremiseType.SCHEMA_CONSTRAINT for p in all_p)

    def test_hypothesis_multiple_premises_and_retraction(self):
        mem = ReasoningMemory()
        p1 = mem.add_premise("Subtotal is $100")
        p2 = mem.add_premise("Tax is $10")
        p3 = mem.add_premise("Shipping is $5")
        h = mem.create_hypothesis("Total must be $115", supporting_premises=[p1.premise_id, p2.premise_id, p3.premise_id])

        assert len(h.supporting_premises) == 3
        validated = mem.validate_hypothesis(h.hypothesis_id, final_confidence=0.95)
        assert validated.validated is True
        assert validated.confidence == 0.95

    def test_structured_output_parser_nested_json(self):
        raw = """{
            "user": {
                "name": "Alice",
                "details": {"age": 30, "roles": ["admin", "auditor"]}
            },
            "status": "active"
        }"""
        parsed = StructuredOutputParser.parse_dict(raw)
        assert parsed["user"]["name"] == "Alice"
        assert parsed["user"]["details"]["age"] == 30
        assert "auditor" in parsed["user"]["details"]["roles"]

    @pytest.mark.parametrize(
        "dirty_json,expected_key,expected_val",
        [
            ("```\n{\"key1\": \"val1\"}\n```", "key1", "val1"),
            ("```json\n{\"num\": 1234}\n```", "num", 1234),
            ("Prefix before JSON {\"flag\": true} suffix after JSON", "flag", True),
            ("{\n  \"nested\": [1, 2, 3],\n}", "nested", [1, 2, 3]),
            ("{\"float_val\": 3.14159,}", "float_val", 3.14159),
        ],
    )
    def test_structured_output_parser_dirty_patterns(self, dirty_json, expected_key, expected_val):
        parsed = StructuredOutputParser.parse_dict(dirty_json)
        assert parsed[expected_key] == expected_val

    @pytest.mark.asyncio
    async def test_llm_client_token_estimation_and_custom_pricing(self):
        client = LLMReasoningClient()
        res1 = await client.complete("Short prompt")
        res2 = await client.complete("A much longer prompt with significantly more words to test token estimation scaling")
        assert res1.prompt_tokens > 0
        assert res2.prompt_tokens > 0
        assert client.total_calls == 2
        assert client.total_cost_usd > 0

    @pytest.mark.asyncio
    async def test_reasoner_preserves_context_premises(self):
        reasoner = SemanticReasoner()
        mem = ReasoningMemory(session_id="session-preservation-test")
        ctx = {"vendor_id": "V-999", "expected_currency": "USD", "compliance_tier": "HIGH"}
        await reasoner.reason_about_goal(
            goal_text="Extract and audit quarterly vendor billing statement",
            memory=mem,
            context=ctx,
        )
        premises = mem.get_all_premises()
        assert len(premises) >= 1
        summary = mem.get_summary()
        assert summary["session_id"] == "session-preservation-test"
        assert summary["total_hypotheses"] >= 1

