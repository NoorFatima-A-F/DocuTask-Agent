# Evaluation dataset sources

All 36 documents in `evals/dataset/` are **synthetic**. They were produced by
`python evals/generate.py` (fixed seed `20261108`), which writes for each document:

| File | Content |
|---|---|
| `document.png` | The page rendered with Pillow's default font (what OCR reads in live mode) |
| `text.txt` | The exact text that was rendered |
| `truth.json` | Ground-truth field values used for scoring |

| Type | Count | Notes |
|---|---:|---|
| invoice | 12 | 2-4 line items, tax 0-20%, USD/EUR/GBP, mixed date formats (ISO, "August 19, 2026", dd/mm/yyyy) |
| receipt | 12 | 2-5 items, 7% tax, cash/credit/debit |
| utility_bill | 12 | account number, service address, kWh usage, amount due |

- Company, store, customer and street names are invented; no real people, companies or documents
  are used, and no third-party data is included.
- Line items, subtotals, tax and totals are arithmetically consistent.
- Limitations: clean single-page renders with one font. They do not represent scans, photos,
  handwriting, multi-page PDFs, tables with borders or non-English documents. Results on this set
  are an upper bound for real-world documents.
- `dd/mm/yyyy` dates are deliberately included; they are ambiguous for parsers that assume
  month-first and exercise the date grounding.

Regenerate with `python evals/generate.py`; the output is byte-for-byte reproducible for a given
Pillow version.
