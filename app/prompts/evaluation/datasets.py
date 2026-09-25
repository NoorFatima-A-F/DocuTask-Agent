"""Prompt Evaluation Dataset Domain Models (Phase 8D)."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class PromptBenchmarkCase(BaseModel):
    """Single test case within a prompt evaluation dataset."""
    case_id: str = Field(default_factory=lambda: f"tc_{uuid.uuid4().hex[:6]}")
    variables: Dict[str, Any] = Field(default_factory=dict)
    expected_output: Optional[Any] = None
    evaluation_criteria: str = "exact_or_semantic"
    tags: List[str] = Field(default_factory=list)


class PromptEvaluationDataset(BaseModel):
    """Governed evaluation dataset containing ground-truth test cases."""
    dataset_id: str
    name: str
    purpose: str = "Regression and quality evaluation"
    organization_id: str
    version: str = "1.0.0"
    owner: str = "ai-evals@enterprise.com"
    test_cases: List[PromptBenchmarkCase] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def add_case(
        self,
        variables: Dict[str, Any],
        expected_output: Optional[Any] = None,
        criteria: str = "exact_or_semantic",
    ) -> PromptBenchmarkCase:
        case = PromptBenchmarkCase(
            variables=variables,
            expected_output=expected_output,
            evaluation_criteria=criteria,
        )
        self.test_cases.append(case)
        return case
