# Audit Framework Inventory & Component Specification (Section 1 Audit)

**Target System**: AI Document Processing Platform  
**Target Subsystem**: Validation Framework, Benchmark Runners & Evidence Engines (`app/validation/`)  

---

## 1. Audit Framework Component Inventory

| Component Name | File Path | Purpose | Inputs | Outputs | Failure Modes | Status |
|----------------|-----------|---------|--------|---------|---------------|--------|
| **Validation Runner CLI** | [app/validation/runner.py](file:///C:/Users/User/Desktop/ai_document_processing_platform/app/validation/runner.py) | CLI entry point for executing gold evaluations & audits | Command args | Execution logs, exit code | Arg parsing error | `[VERIFIED_BY_INSPECTION]` **✓ Active** |
| **Metrics Engine** | [app/validation/metrics.py](file:///C:/Users/User/Desktop/ai_document_processing_platform/app/validation/metrics.py) | Calculates Accuracy, Precision, Recall, F1, ECE, Brier | Raw extraction dicts | Metric scores (0.0-1.0) | Zero-division, key error | `[VERIFIED_BY_INSPECTION]` **✓ Active** |
| **Evidence Hash Logger** | [app/validation/evidence.py](file:///C:/Users/User/Desktop/ai_document_processing_platform/app/validation/evidence.py) | Generates SHA-256 evidence records & hash chains | Evaluation results | Evidence JSON / Hash | Disk I/O error | `[VERIFIED_BY_INSPECTION]` **✓ Active** |
| **Benchmark Reproducer** | [app/validation/benchmarks.py](file:///C:/Users/User/Desktop/ai_document_processing_platform/app/validation/benchmarks.py) | Runs latency benchmarks & measures percentiles | Concurrency params | Latency percentiles | Timing drift | `[VERIFIED_BY_INSPECTION]` **✓ Active** |
| **Report Generator** | [app/validation/reports.py](file:///C:/Users/User/Desktop/ai_document_processing_platform/app/validation/reports.py) | Generates Markdown & JSON audit reports | Evaluation metrics | Markdown files | Template error | `[VERIFIED_BY_INSPECTION]` **✓ Active** |
| **Security Attack Runner**| [app/validation/security/attack_runner.py](file:///C:/Users/User/Desktop/ai_document_processing_platform/app/validation/security/attack_runner.py) | Executes prompt injection & unicode attack suites | Attack payloads | Defense rate (%) | Exception swallow | `[VERIFIED_BY_INSPECTION]` **✓ Active** |
| **Production Chaos Engine**| [app/validation/production/chaos.py](file:///C:/Users/User/Desktop/ai_document_processing_platform/app/validation/production/chaos.py) | Injects fault conditions (429, 500, DB drop) | Fault config | System recovery time | Unhandled crash | `[VERIFIED_BY_INSPECTION]` **✓ Active** |
