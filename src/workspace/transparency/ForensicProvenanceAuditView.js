import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
export const ForensicProvenanceAuditView = () => {
    const provenanceSteps = [
        {
            step: 1,
            stage: 'RAW_DOCUMENT_INGESTION',
            description: 'Raw PDF page 1 ingested (300 DPI, SHA-256: 9f82ab...)',
            actor: 'DocumentIngestionWorker',
            timestamp: '16:00:00.120',
            artifact: 'page_1.png (2480x3508)',
        },
        {
            step: 2,
            stage: 'OCR_BOUNDING_BOX',
            description: 'Optical bounding box [x:1840, y:3120, w:240, h:48] -> "$1,420.50"',
            actor: 'LayoutLMOCRWorker',
            timestamp: '16:00:00.310',
            artifact: 'Confidence: 0.985',
        },
        {
            step: 3,
            stage: 'LLM_STRUCTURED_EXTRACTION',
            description: 'Structured parsing routed to Gemini 2.5 Flash -> 1420.50 USD',
            actor: 'LLMReasoningWorker',
            timestamp: '16:00:00.740',
            artifact: 'Field Confidence: 0.965',
        },
        {
            step: 4,
            stage: 'INVARIANT_VALIDATION',
            description: 'Subtotal ($1,300.00) + Tax ($120.50) == Total ($1,420.50) arithmetic verification',
            actor: 'InvariantValidationWorker',
            timestamp: '16:00:00.790',
            artifact: 'Status: 100% VALIDATED',
        },
        {
            step: 5,
            stage: 'CRYPTOGRAPHIC_SIGN_COMMIT',
            description: 'Persisted to Postgres + ED25519 signature manifest generated',
            actor: 'AuditSecurityWorker',
            timestamp: '16:00:00.825',
            artifact: 'Signature: ED25519_SIG_8F3A20B1',
        },
    ];
    return (_jsxs("div", { className: "space-y-6", children: [_jsx("div", { className: "p-6 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-xl", children: _jsx("div", { className: "flex flex-col md:flex-row items-start md:items-center justify-between gap-4", children: _jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-xl", children: "\uD83D\uDD2C" }), _jsx("h2", { className: "text-lg font-bold font-mono text-[#F8FAFC]", children: "Forensic Field Provenance & Cryptographic Lineage" }), _jsx(Badge, { variant: "success", size: "sm", children: "TAMPER-PROOF MERKLE CHAIN" })] }), _jsx("p", { className: "text-sm font-mono text-[#94A3B8] mt-1", children: "End-to-end auditability tracing any extracted field back to pixel coordinates, OCR tokens, LLM responses, and database commits." })] }) }) }), _jsxs(Card, { className: "p-6 bg-[#0F172A] border-[#1E293B]", children: [_jsxs("div", { className: "flex items-center justify-between pb-4 border-b border-[#1E293B]", children: [_jsxs("div", { children: [_jsx("span", { className: "text-xs font-mono text-cyan-400 font-bold", children: "FIELD LINEAGE TRACE:" }), _jsx("h3", { className: "text-base font-bold font-mono text-[#F8FAFC]", children: "invoice_total_amount \u2192 $1,420.50 USD" }), _jsx("div", { className: "text-xs font-mono text-[#64748B] mt-0.5", children: "Document: DOC-INV-2026 \u2022 Status: Cryptographically Sealed" })] }), _jsx(Badge, { variant: "success", size: "md", children: "100% TRACEABLE" })] }), _jsx("div", { className: "space-y-4 mt-6", children: provenanceSteps.map((s) => (_jsx("div", { className: "p-4 rounded-xl bg-[#020617] border border-[#1E293B]", children: _jsxs("div", { className: "flex flex-col md:flex-row items-start md:items-center justify-between gap-2", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("span", { className: "w-6 h-6 rounded-full bg-cyan-950 border border-cyan-500/50 flex items-center justify-center text-xs font-mono font-bold text-cyan-300", children: s.step }), _jsxs("div", { children: [_jsx("h4", { className: "text-xs font-bold font-mono text-[#F8FAFC]", children: s.stage }), _jsx("p", { className: "text-xs font-mono text-[#94A3B8] mt-0.5", children: s.description })] })] }), _jsxs("div", { className: "text-right font-mono text-xs", children: [_jsx("div", { className: "text-[#64748B] text-[11px]", children: s.timestamp }), _jsx("div", { className: "text-emerald-400 font-bold mt-0.5", children: s.artifact })] })] }) }, s.step))) })] })] }));
};
