# ADR-833: Multi-Dimensional Evidence Artifacts & Evidence Bundles

## Status
Accepted

## Context
Compliance audits and internal security investigations require concrete proof beyond single-line log entries. Teams must produce model cards, prompt templates, lineage graphs, evaluation metrics, and approval records tied directly to specific execution runs.

## Decision
We implemented an Evidence Management System under `app/audit/evidence/`:
1. **Evidence Taxonomy (`EvidenceType`)**:
   - `AI_EVIDENCE`: Model registry snapshots, prompt versions, grounding confidence scores, evaluation metrics.
   - `DATA_EVIDENCE`: Source document checksums, lineage graphs, schema migration deltas.
   - `GOVERNANCE_EVIDENCE`: Policy rule snapshots, approval records, risk assessments.
   - `EXECUTION_EVIDENCE`: DAG execution traces, tool parameter snapshots, error stacks.
   - `SAFETY_EVIDENCE`: Safety gateway scan results, injection blocks, PII redaction reports.
2. **Evidence Bundles (`create_evidence_bundle()`)**: Packages correlated audit events, evidence artifacts, and policy snapshots into a self-contained, digitally signed package with a cryptographically signed manifest hash.

## Consequences
### Positive
- One-click generation of comprehensive, tamper-evident audit packages for regulators and customers.
- Direct association between raw inputs, AI inferences, governance checks, and resulting artifacts.
