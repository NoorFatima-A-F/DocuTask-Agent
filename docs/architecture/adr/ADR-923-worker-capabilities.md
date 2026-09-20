# ADR-923: Worker Capability Indexing and Dynamic Discovery

## Status
Accepted

## Context
Diverse workloads require specialized worker hardware and software runtimes (e.g., CUDA GPU, OCR runtimes, high memory, HIPAA compliance). Hardcoding worker types to specific workloads limits operational flexibility.

## Decision
Implement `WorkerCapabilityRegistry` allowing workers to dynamically advertise standardized capabilities (e.g., `document.ocr`, `gpu.a100`, `workflow.execute`, `compliance.hipaa`). Support exact, group, and optional capability scoring.

## Consequences
- Decouples task definitions from physical worker types.
- Enables granular capability matching and optional optimization bonus scoring.
