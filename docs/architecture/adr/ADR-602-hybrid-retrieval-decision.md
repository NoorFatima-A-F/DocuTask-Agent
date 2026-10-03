# ADR-602: Hybrid Retrieval & Multi-Factor Reciprocal Rank Fusion

## Status
Accepted

## Context
Relying solely on dense vector search causes failures for exact entity lookups, SKU numbers, contract clauses, and specific numerical IDs. Conversely, pure keyword search fails on semantic paraphrasing and conceptual inquiries.

## Decision
We implement a hybrid retrieval architecture combining:
1. Lexical BM25 keyword matching for exact terms and code identifiers.
2. Dense vector similarity for conceptual and semantic queries.
3. Reciprocal Rank Fusion (RRF) to merge candidate result lists without requiring ad-hoc score normalization:
$$RRF(d) = \sum_{m \in M} \frac{1}{k + r_m(d)}$$
4. Multi-factor reranking incorporating semantic similarity, keyword density, document authority, content freshness decay, and trust scores.

## Consequences
- Significantly higher retrieval recall and precision across both technical and business queries.
- Transparent score attribution for auditing ranking decisions.
