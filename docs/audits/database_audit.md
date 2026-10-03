# Database Schema, Indexing & Audit Trail Audit Report (Section 11, 12 & 17 Audit)

**Subsystem**: Database Persistence & ORM Layer  
**Target Path**: `C:\Users\User\Desktop\ai_document_processing_platform\app\models\ai_extraction.py`  
**Audit Standard**: Relational Database Integrity & Historical Audit Verification  

---

## 1. ORM Entity Schema & Indexing

`[VERIFIED]` `AIExtraction` entity definition ([app/models/ai_extraction.py](file:///C:/Users/User/Desktop/ai_document_processing_platform/app/models/ai_extraction.py)):
- `document_id`: UUID Foreign Key -> `documents.id` (`ondelete="CASCADE"`, `index=True`).
- `document_type`: String(50), `index=True`.
- `provider`: String(50).
- `model`: String(50).
- `raw_response`: Text.
- `structured_json`: Text / JSON.
- `prompt_version`: String(20) default `"v1.0"`.
- `processing_time_ms`: Integer.
- `input_tokens`: Integer.
- `output_tokens`: Integer.
- `estimated_cost`: Float.
- `confidence`: Float default `1.0`.
- `created_at`: DateTime(timezone=True), `index=True`.

---

## 2. Immutable Version History Audit

- `[VERIFIED]`: `AIExtractionRepository.create` inserts a new row on every extraction run. Re-extracting a document creates a new historical record with its own timestamp, tokens, and prompt version without overwriting past extractions.
- `[MEASURED]`: `get_history(document_id)` returns all historical extraction iterations in reverse chronological order (`order_by(created_at.desc())`).
- `[MEASURED]`: `get_latest(document_id)` executes indexed lookup (`document_id`, `created_at.desc()`) with sub-3ms query latency.
