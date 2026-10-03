# ADR-843: Review Evidence Package & Explainable Decision Design

## Status
Accepted

## Context
Human reviewers forced to inspect raw JSON logs or disconnected database records make uninformed decisions, introducing human error into AI workflows. Trustworthy oversight requires structured, transparent evidence packages that present the full reasoning chain, grounding citations, model provenance, and safety evaluations.

## Decision
We implemented the `ReviewEvidencePackage` architecture under `app/oversight/reviews/`:
1. **Explainable Context**: Bundles proposed AI output, natural language explanation, chain-of-thought summary, and key risk/confidence scores.
2. **Grounding & Provenance**: Attaches source document citations, bounding locations, confidence metrics, prompt IDs, and model versions.
3. **Policy & Safety Context**: Explicitly lists triggered governance policies, safety sandbox evaluations, and flags, enabling rapid, informed human deliberation.

## Consequences
### Positive
- Transparent, auditable context provided to reviewers.
- Accelerated review turnaround times and reduced operational errors.
- Satisfies EU AI Act Article 14 transparency requirements.

### Negative / Trade-offs
- Evidence aggregation requires additional serialization and payload storage.
