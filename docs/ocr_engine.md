# Enterprise OCR Engine & Raw Text Extraction Pipeline

**Platform**: AI Document Processing Platform  
**Target Path**: `C:\Users\User\Desktop\ai_document_processing_platform`  
**Subsystem**: OCR & Text Extraction Engine (Prompt 4 Baseline)  

---

## 1. Executive Summary

The OCR & Text Extraction Subsystem provides a modular, provider-independent text extraction pipeline. It intelligently classifies documents (Digital PDF vs. Scanned PDF vs. Images vs. Plain Text), extracts native digital text directly with 100% confidence, falls back to OCR per page for scanned content, applies modular image preprocessing filters (grayscale, contrast enhancement, deskew), computes page and document-level confidence metrics, and persists structured extraction results.

---

## 2. OCR Architecture & Pipeline Sequence

```
 Client (POST /ocr/extract/{id})
               │
               ▼
      DocumentTypeDetector
               │
   ┌───────────┼───────────┐
   ▼           ▼           ▼
  TXT        Images       PDF
(Native)   (Tesseract)     │
                           ▼
                  pdfplumber Inspection
                     ┌─────┴─────┐
                     ▼           ▼
                Native Text   Scanned Page
                 (Direct)    (Render -> OCR)
                     │           │
                     └─────┬─────┘
                           │
                           ▼
           Compute Page Confidence Scores
                           │
                           ▼
      Persist Page Records to `extracted_texts` (DB)
                           │
                           ▼
      Return Aggregated DocumentContent (200 OK)
```

---

## 3. Provider Abstraction Model

Business logic interacts exclusively with the abstract class `OCRProvider`:

```python
class OCRProvider(ABC):
    @abstractmethod
    async def extract_text(self, image_bytes: bytes, language: str = "eng") -> str: ...
    @abstractmethod
    async def extract_page(self, image_bytes: bytes, page_number: int = 1, language: str = "eng") -> PageContent: ...
    @abstractmethod
    async def get_confidence(self, image_bytes: bytes, language: str = "eng") -> float: ...
    @abstractmethod
    async def detect_language(self, image_bytes: bytes) -> Optional[str]: ...
    @abstractmethod
    async def health_check(self) -> bool: ...
```

### Pluggable Provider Roadmap
- **`TesseractOCRProvider` (Active Baseline)**: Open-source OCR with Pillow image preprocessing.
- **Future Cloud Providers**: AWS Textract, Google Cloud Vision, Azure Document Intelligence, PaddleOCR, EasyOCR. Adding a new provider requires zero modifications to services or API routes.

---

## 4. Image Preprocessing Subsystem

The `ImagePreprocessor` applies modular image enhancements prior to OCR:
1. **Grayscale Conversion**: Eliminates color noise.
2. **Contrast Enhancement**: Accentuates text boundaries.
3. **Median Filtering**: Eliminates salt-and-pepper noise.
4. **Adaptive Thresholding / Binarization**: Converts to high-contrast binary for maximum optical recognition clarity.

---

## 5. Confidence Calculation Model

- **Page-Level Confidence**:
  - Digital native text: `1.0` (100% confidence).
  - OCR extracted text: Word-level mean confidence score computed from Tesseract dictionary metrics (\(0.0\) to \(1.0\)).
- **Document-Level Confidence**:
  - Computed as the arithmetic mean across all page confidence scores:
    $$\text{Average Confidence} = \frac{1}{N} \sum_{i=1}^{N} \text{Confidence}(\text{Page}_i)$$

---

## 6. Status Lifecycle

Document processing transitions through well-defined lifecycle states:
- `UPLOADED`: Ingested, awaiting extraction.
- `OCR_RUNNING`: Active text extraction in progress.
- `OCR_COMPLETED`: Text extracted and persisted to database.
- `OCR_FAILED`: Extraction failure recorded.

---

## 7. API Endpoints Reference

| Method | Endpoint | Description | Status Code | Auth |
|--------|----------|-------------|-------------|------|
| `POST` | `/api/v1/ocr/extract/{document_id}` | Trigger OCR / text extraction pipeline | 200 OK | Bearer JWT |
| `GET`  | `/api/v1/ocr/text/{document_id}` | Retrieve aggregated document extracted text | 200 OK | Bearer JWT |
| `GET`  | `/api/v1/ocr/pages/{document_id}` | Retrieve per-page extracted text breakdown | 200 OK | Bearer JWT |
| `GET`  | `/api/v1/ocr/status/{document_id}` | Retrieve extraction status and confidence metrics | 200 OK | Bearer JWT |
