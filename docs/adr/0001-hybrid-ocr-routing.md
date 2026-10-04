# ADR 0001: Hybrid OCR Routing with Confidence Fallbacks

## Status
Accepted

## Context
High-resolution enterprise PDFs contain mixed layouts: digital text, scanned tables, and handwritten signatures. A single OCR or LLM vision pass is either too slow or too expensive for high throughput production workloads.

## Decision
Implement a tiered, multi-stage routing mechanism:
1. Attempt native text extraction via PyMuPDF (`fitz`).
2. If text density < 15% or confidence score < 0.85, route to the OCR pipeline (Tesseract / EasyOCR).
3. Complex layouts, dense tabular structures, and low-confidence visual regions route to the Multimodal Vision LLM (Gemini 1.5 Flash / Claude) for structured schema extraction.

## Consequences
- **Positive:** Reduces token consumption and LLM inference costs by ~68% on native digital PDFs while maintaining >99% extraction accuracy.
- **Negative:** Requires local OCR runtime binaries in the Docker container and increases cold-start image size by ~85MB.
