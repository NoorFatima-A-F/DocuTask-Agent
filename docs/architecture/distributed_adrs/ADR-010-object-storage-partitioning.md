# ADR-010: Date-Partitioned Blob Object Storage Strategy

**Status**: **ACCEPTED**  
**Date**: 2026-08-19  

## 1. Context & Problem Statement
Prevent single-directory filesystem degradation when storing millions of document files.

## 2. Decision Outcome
Partition object storage by date: `storage/uploads/YYYY/MM/DD/{document_id}/original.pdf`.

## 3. Consequences
- **Positive**: Direct $O(1)$ file path lookups; zero directory listing performance penalties.
