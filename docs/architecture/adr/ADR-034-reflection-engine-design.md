# ADR-034: Governed Reflection & Continuous Improvement Engine

## Status
Accepted

## Context
Continuous agent learning and self-correction are vital for enterprise autonomy. However, persisting raw, private chain-of-thought (CoT) traces poses security, privacy, and compliance risks. The platform requires structured reflection without exposing raw prompt internals.

## Decision
We implement `ReflectionEngine` generating structured `ReflectionReport`s:
- Execution Summary: Concise overview of what happened.
- Success Factors: Key positive factors enabling successful completion.
- Failure Factors: Root causes identified when errors occur.
- Improvement Suggestions: Actionable recommendations for future runs.
- Memory Update Recommendations: Key-value proposals for procedural and episodic memory consolidation.

Private chain-of-thought tokens are discarded post-execution; only structured reasoning summaries (`ReasoningSummary`) and reflection reports are retained.

## Consequences
- Protects sensitive reasoning data while preserving actionable learnings for future iterations.
- Automatically drives memory consolidation and procedural learning.
