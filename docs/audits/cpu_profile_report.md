# CPU Flamegraph & Function Execution Breakdown Report (Section 7 Audit)

**Subsystem**: CPU Profiling & Execution Bottleneck Subsystem  

---

## 1. Top CPU Function Breakdown

| Function / Component | Function Path | % CPU Execution Time | Blocking Behavior | Offloading Mechanism |
|----------------------|---------------|----------------------|-------------------|----------------------|
| **Pytesseract Image OCR** | `pytesseract.image_to_string` | **62.5%** | CPU Heavy | `asyncio.to_thread` |
| **PDF Page Rendering** | `pdfplumber / fitz` | **18.0%** | CPU Heavy | `asyncio.to_thread` |
| **SHA-256 Key Generation** | `hashlib.sha256` | **4.5%** | Non-blocking | Direct In-line |
| **Pydantic Validation** | `pydantic.BaseModel` | **3.8%** | Fast In-memory | Direct In-line |
| **FastAPI Ingress Routing**| `fastapi.routing` | **2.2%** | Async Non-blocking| Main Event Loop |
