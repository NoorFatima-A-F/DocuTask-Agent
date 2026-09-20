# Enterprise AI Extraction Engine & Structured Document Intelligence

**Platform**: AI Document Processing Platform  
**Target Path**: `C:\Users\User\Desktop\ai_document_processing_platform`  
**Subsystem**: AI Extraction Subsystem (Prompt 5 Baseline)  

---

## 1. Executive Summary

The AI Extraction Engine converts raw OCR document text into validated, schema-driven JSON data objects. It sits entirely on top of the frozen OCR, Storage, Authentication, and Database subsystems. Business logic is completely decoupled from concrete LLM vendors via the abstract interface `LLMProvider`.

---

## 2. Extraction Pipeline Sequence

```
 Client Request (POST /ai/extract/{document_id})
                        │
                        ▼
               AIExtractionService
                        │
                        ▼
             Retrieve Cached OCR Text
                        │
                        ▼
      LLMFactory (Get LLMProvider - e.g. Gemini)
                        │
                        ▼
           PromptBuilder & SchemaRegistry
                        │
                        ▼
           LLM JSON Generation Request
                        │
                        ▼
               Raw JSON Response
                        │
                        ▼
         AIValidator (Pydantic Schema Check)
            ┌───────────┴───────────┐
            ▼                       ▼
         Valid JSON              Failure
            │                       │
            │          Retry Loop (Max 3 Attempts with Corrective Feedback)
            │                       │
            └───────────┬───────────┘
                        │
                        ▼
   Persist AIExtraction Record (Audit History preserved)
                        │
                        ▼
  Update Document Status to EXTRACTION_COMPLETED
                        │
                        ▼
       Return ExtractionResponse (200 OK)
```

---

## 3. Status Lifecycle

Document status transitions:
- `UPLOADED` -> `OCR_RUNNING` -> `OCR_COMPLETED` -> `EXTRACTION_RUNNING` -> `EXTRACTION_COMPLETED` (or `EXTRACTION_FAILED`).

---

## 4. API Endpoints Reference

| Method | Endpoint | Description | Status Code | Auth |
|--------|----------|-------------|-------------|------|
| `POST` | `/api/v1/ai/extract/{document_id}` | Trigger structured AI extraction | 200 OK | Bearer JWT |
| `GET`  | `/api/v1/ai/result/{document_id}` | Retrieve latest extraction result | 200 OK | Bearer JWT |
| `GET`  | `/api/v1/ai/status/{document_id}` | Retrieve AI extraction status | 200 OK | Bearer JWT |
| `GET`  | `/api/v1/ai/history/{document_id}` | Retrieve historical extractions | 200 OK | Bearer JWT |
| `DELETE`| `/api/v1/ai/result/{document_id}` | Delete extraction result | 200 OK | Bearer JWT |
