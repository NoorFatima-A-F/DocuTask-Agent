# ADR-607: Fine-Grained Evidence & Citation Strategy

## Status
Accepted

## Context
AI hallucinations and ungrounded statements undermine trust in enterprise automation. Users and compliance auditors must be able to click on any assertion made by an agent and view the exact document, page number, and paragraph that justified that statement.

## Decision
We implement the `CitationEngine` and `ContextBuilder`. Every piece of evidence delivered to an LLM context is wrapped with a formal `Citation` record specifying document ID, version number, page number, chunk ID, and exact snippet text. Responses can be scored for factual grounding against the cited snippets.

## Consequences
- Every AI response is auditable with direct source attribution.
- Enables hallucination detection and automated grounding score calculation.
