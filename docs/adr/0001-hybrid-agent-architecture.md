# ADR 0001: Hybrid Deterministic/Agentic Processing Pipeline

## Status
Accepted

## Context
Document processing requires both high-accuracy OCR extraction and flexible intent categorization. Pure LLM processing is too expensive and hallucination-prone for raw text, while pure regex OCR fails on diverse layouts.

## Decision
We decouple raw text extraction into deterministic services (`src/services/ocr`) and constrain the LLM agent (`src/agents`) strictly to structured schema conforming and task routing via Pydantic output validation.

## Consequences
- Fast, low-cost processing for standard document layouts.
- Agent non-determinism is isolated and monitored via the offline evaluation harness (`evals/`).
