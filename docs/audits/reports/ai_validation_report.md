# Enterprise AI Validation & Metric Report

## Executive Summary
- **Total Documents Evaluated**: 5
- **Average Field Accuracy**: **100.0%**
- **Average F1 Score**: **100.0%**
- **Regression Status**: **NONE** (Delta: +5.0%)

## Evidence Records Matrix

| Artifact ID | Model / Provider | Total Fields | Correct | Accuracy | F1 Score | Status | Evidence Path |
|-------------|------------------|--------------|---------|----------|----------|--------|---------------|
| `gold_inv_001` | `gemini-1.5-flash` | 7 | 7 | **100.0%** | 100.0% | `PASS` | [`val_7f_100acc.json`](docs\audits\evidence\val_7f_100acc.json) |
| `gold_rcp_001` | `gemini-1.5-flash` | 6 | 6 | **100.0%** | 100.0% | `PASS` | [`val_6f_100acc.json`](docs\audits\evidence\val_6f_100acc.json) |
| `gold_ctr_001` | `gemini-1.5-flash` | 6 | 6 | **100.0%** | 100.0% | `PASS` | [`val_6f_100acc.json`](docs\audits\evidence\val_6f_100acc.json) |
| `gold_pas_001` | `gemini-1.5-flash` | 6 | 6 | **100.0%** | 100.0% | `PASS` | [`val_6f_100acc.json`](docs\audits\evidence\val_6f_100acc.json) |
| `gold_med_001` | `gemini-1.5-flash` | 5 | 5 | **100.0%** | 100.0% | `PASS` | [`val_5f_100acc.json`](docs\audits\evidence\val_5f_100acc.json) |

## Regression Baseline Comparison
- **Baseline Version**: `v1.0_baseline` (95.0%)
- **Current Version**: `v1.1_candidate` (100.0%)
- **Quality Severity**: `NONE`
