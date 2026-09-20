# AI Extraction Pipeline Architectural Specification

**Subsystem**: AI Extraction Engine  
**Path**: `C:\Users\User\Desktop\ai_document_processing_platform\app\ai\`  

---

## 1. Clean Architecture Layer Decoupling

The AI subsystem sits strictly above the OCR and Storage subsystems:

```
[API Layer]  app/api/v1/endpoints/ai.py
     │
[Service Layer]  app/services/ai_extraction_service.py
     │
[Abstraction Layer]  app/ai/base.py (LLMProvider)
     │
[Factory Layer]  app/ai/factory.py (LLMFactory)
     │
[Concrete Provider]  app/ai/providers/gemini.py (GeminiProvider)
```

---

## 2. Validation & Automatic Retry Strategy

If an LLM returns malformed JSON or fails Pydantic schema validation:
1. `AIValidator` catches the `ValidationError`.
2. Formats specific validation error detail messages.
3. `AIExtractionService` appends the error feedback to the prompt:
   ```
   CORRECTION REQUIRED: Your previous attempt failed validation with error: {error_details}.
   Please correct the JSON structure to strictly conform to the required schema.
   ```
4. Re-submits to the provider (up to 3 retries maximum).
5. If all retries fail, raises `AIRetryLimitExceededException` and transitions status to `EXTRACTION_FAILED`.
