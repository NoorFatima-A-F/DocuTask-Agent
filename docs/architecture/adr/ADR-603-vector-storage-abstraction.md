# ADR-603: Vector Storage & Embedding Provider Abstraction

## Status
Accepted

## Context
Tying the platform directly to a specific vector database (e.g. Pinecone, Qdrant, pgvector) or a single proprietary embedding API (e.g. OpenAI, Cohere) creates vendor lock-in, infrastructure inflexibility, and test execution friction.

## Decision
We decouple vector storage and vector generation into two pluggable abstractions:
1. `EmbeddingProvider`: Unified interface for vector embedding generation with support for Gemini, OpenAI, local Sentence Transformers, and deterministic offline hash embeddings.
2. `VectorStoreInterface`: Interface providing insert, batch insert, k-NN similarity search, partition filtering, and deletion, implemented via `InMemoryVectorStore` (development/testing) and adapters for `pgvector`, `Qdrant`, and `Milvus` (production).

## Consequences
- Fast, self-contained, zero-dependency testing in CI environments.
- Freedom to switch embedding models or vector backends without refactoring retrieval pipelines.
