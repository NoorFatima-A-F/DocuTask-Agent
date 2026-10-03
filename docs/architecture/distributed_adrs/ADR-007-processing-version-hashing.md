# ADR-007: Multi-Stage Processing Version Hashing

**Status**: **ACCEPTED**  
**Date**: 2026-08-19  

## 1. Context & Problem Statement
Auditing historical extraction reproducibility requires knowing exact OCR, prompt, model, and schema versions.

## 2. Decision Outcome
Compute composite version hash: `SHA256(ocr_ver + prompt_ver + model_ver + schema_ver)` stored on `DocumentJob` and `AIExtraction` entities.

## 3. Consequences
- **Positive**: 100% scientific reproducibility of historical extraction runs.
