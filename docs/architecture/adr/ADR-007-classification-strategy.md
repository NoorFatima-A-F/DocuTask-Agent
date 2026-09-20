# ADR-007: Classification Strategy

## Status
Accepted

## Context
Enterprise data must be protected according to its inherent sensitivity. Automated classification is necessary to prevent sensitive PII, healthcare records, financial details, or confidential legal documents from being exposed to unauthorized users or external AI models.

## Decision
1. Establish a 5-tier classification hierarchy: `PUBLIC`, `INTERNAL`, `CONFIDENTIAL`, `RESTRICTED`, and `HIGHLY_RESTRICTED`.
2. Implement `DataClassificationEngine` combining regex detectors, heuristic pattern matchers, and rule sets to identify sensitive categories (`PII`, `FINANCIAL`, `HEALTHCARE`, `LEGAL`, `CREDENTIALS`).
3. Attach confidence scores, evidence snippets, and detection methods to every classification event.

## Consequences
- **Positive**: Automated zero-trust classification applied at ingestion before data is indexed or passed to LLMs.
- **Trade-off**: Requires periodic updates to regex and keyword catalogs to maintain high recall.
