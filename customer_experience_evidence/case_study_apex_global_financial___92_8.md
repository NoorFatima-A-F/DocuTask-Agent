# Enterprise Case Study: Apex Global Financial Services

## Client Profile
* **Industry**: Financial Services & Asset Management
* **Scale**: 125,000 invoices/year across 45 countries
* **Legacy Stack**: Manual PDF data entry, legacy regex scripts, disparate spreadsheets

## The Business Challenge
Prior to adopting DocuTask Agent, Apex Financial's accounts payable department required 22 full-time analysts performing manual 3-way document matching between purchase orders, invoices, and receipts. The legacy regex OCR scripts frequently failed whenever vendor layouts shifted, leading to invoice backlogs exceeding 21 days and over $120,000 in missed early-payment discounts.

## The Autonomous AI Solution
Apex deployed DocuTask Agent as their core document intelligence operating system:
1. **Zero-Configuration Email Ingestion**: Automatically captures invoices from AP mailboxes via OAuth2 Microsoft Graph.
2. **Multimodal Grounded Extraction**: Maps tables and non-standard layouts with 99.1% character precision.
3. **Deterministic 3-Way PO Matching**: Verifies line-item quantities and vendor tax IDs directly against NetSuite.
4. **Human-in-the-Loop Fast-Track**: High-confidence (>95%) items are approved instantly; edge cases present visual bounding-box citations for single-click review.

## Quantified Business Outcomes
* **$2,280,000 Net Annual Savings**: Cost per invoice reduced from $35.00 to $0.025.
* **91.5% Straight-Through Processing (STP)**: 9 out of 10 invoices clear end-to-end without human touching.
* **4.2x Net Annual ROI**: Complete infrastructure investment recouped in 1.4 months.
