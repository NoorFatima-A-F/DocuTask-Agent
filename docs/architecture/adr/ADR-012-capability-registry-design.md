# Architecture Decision Record: ADR-012

## Title
Decoupled Capability Registry for Dynamic Platform Feature Discovery

## Status
**ACCEPTED** (2026-03-24)

## Context
Code that performs hardcoded checks like `if ocr_module_installed:` or direct imports of specific connector implementations introduces brittle coupling. Business workflows should request capabilities (`document.ocr`, `ai.embedding`, `tool_calling`, `storage`) rather than concrete class implementations.

## Decision
We implement a centralized **CapabilityRegistry**. Modules and plugins advertise capabilities with semantic versioning and attribute descriptors. Consumers query `has_capability("document.ocr")` and discover active providers dynamically.

## Consequences
### Positive
- Zero direct coupling between workflow orchestration and specific vendor integrations.
- Enables dynamic runtime swapping of capability providers (e.g., cloud OCR vs local OCR).
### Negative / Trade-Offs
- Capability naming conventions must be standardized across platform domains.
