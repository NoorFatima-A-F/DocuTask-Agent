# ADR-821: Enterprise AI Safety Runtime & Gateway Architecture

## Status
Accepted

## Context
DocuTask Agent operates autonomous multi-agent workflows processing sensitive documents, executing database queries, and utilizing foundation models across multiple organizations. Unchecked AI operations introduce severe risks including direct/indirect prompt injection, confidential data leakage, toxic content generation, and hallucinations. A unified runtime defense layer is required to enforce strict safety boundaries before, during, and after AI inference without duplicating existing governance control planes.

## Decision
We implemented the Enterprise AI Safety & Responsible AI Runtime Platform (EAS-RARP) under `app/safety/`.
1. **Safety Pipeline**: A multi-stage evaluation pipeline coordinating:
   - Pre-Execution: Input length, character validity, prompt injection detection, multi-strategy jailbreak detection, and automated PII masking/redaction.
   - In-Execution: Tool calling sandbox enforcement, danger tier RBAC, and parameter sanitization.
   - Post-Execution: Output toxicity screening, system prompt and secret leakage detection, factuality checking, and knowledge chunk grounding verification.
2. **Context Model**: Every safety evaluation operates over an immutable `SafetyContext` capturing tenant ID, model metadata, prompt variables, tool parameters, data sensitivity, and source trust tiers.
3. **Decisions & Actions**: Standardized `SafetyDecision` responses yielding `ALLOW`, `ALLOW_WITH_AUDIT`, `MODIFY`, `REDACT`, `REQUIRE_HUMAN`, `ESCALATE`, or `BLOCK`.

## Consequences
### Positive
- Defense-in-depth safety enforcement protecting all AI inference endpoints and agents.
- Clear separation between static governance policies and active runtime safety enforcement.
- Real-time event publishing and automated incident tracking.

### Negative / Trade-offs
- Slight latency overhead (typically < 15ms) for regex and rule-based evaluation prior to LLM calls.
