# ADR-008: Lineage Graph Design

## Status
Accepted

## Context
Understanding how data transforms across workflows, agent swarms, connector plugins, and AI models requires end-to-end directed lineage tracking.

## Decision
1. Implement `LineageGraphEngine` representing data transformations as a directed acyclic graph (DAG).
2. Lineage nodes encompass `DATASET`, `DOCUMENT`, `WORKFLOW`, `TASK`, `AGENT`, `CONNECTOR`, `MODEL`, `PROMPT`, `USER`, and `SYSTEM`.
3. Lineage edges represent explicit relationships: `CREATED`, `READ`, `WRITTEN`, `TRANSFORMED`, `DERIVED_FROM`, `USED_BY`, `GENERATED_BY`, and `APPROVED_BY`.
4. Provide recursive upstream lineage (origin root cause) and downstream lineage (impact radius) traversal.

## Consequences
- **Positive**: Complete visibility into what transformed data, which models participated, and what artifacts were produced.
- **Trade-off**: High-frequency fine-grained graph recording requires efficient node indexing.
