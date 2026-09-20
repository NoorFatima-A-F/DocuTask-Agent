import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
export const EvidenceExplorerView = () => {
    const [selectedNode, setSelectedNode] = useState('ev-node-001');
    const evidenceNodes = [
        {
            id: 'ev-node-001',
            type: 'PLANNER_DECISION',
            agent: 'docutask-chief-planner',
            timestamp: '2026-09-10T18:22:10.142Z',
            hash: 'a8f3b20c91e847ad3ef0192a83c7482910fae12089bb3c17820aedfa9102bc45',
            parentHash: 'genesis_root_00000000000000000000000000000000000000000000000000000000',
            status: 'VERIFIED',
            inputs: { document_id: 'doc-inv-8891', pages: 4, sla_bound_ms: 1500, quality_target: 0.98 },
            outputs: { selected_model: 'gemini-2.5-flash', parallelism: 3, strategy: 'two_phase_ocr_extract' },
            metrics: { predicted_latency_ms: 380.0, predicted_cost_usd: 0.0018, confidence: 0.985 },
            proof: {
                algorithm: 'SHA-256+Ed25519-Sim',
                signature: 'sig_a8f3b20c91e847ad3ef0192a83c7482910fae12089bb3c17820aedfa',
                publicKey: 'pub_docutask_root_key_2026_a8f3',
                nonce: 819204,
            },
        },
        {
            id: 'ev-node-002',
            type: 'TOOL_EXECUTION',
            agent: 'docutask-ocr-worker-01',
            timestamp: '2026-09-10T18:22:10.522Z',
            hash: 'd4e9102fae89bb3c17820aedfa9102bc45a8f3b20c91e847ad3ef0192a83c748',
            parentHash: 'a8f3b20c91e847ad3ef0192a83c7482910fae12089bb3c17820aedfa9102bc45',
            status: 'VERIFIED',
            inputs: { region: 'header_block_bbox', binarization: 'otsu_adaptive', engine: 'tesseract_v5_enhanced' },
            outputs: { tokens_extracted: 142, skew_angle_deg: 0.4, raw_text: 'INVOICE #INV-2026-9921 TOTAL: $4,850.00' },
            metrics: { ocr_latency_ms: 124.5, token_cost_usd: 0.00042, energy_joules: 0.22 },
            proof: {
                algorithm: 'SHA-256+Ed25519-Sim',
                signature: 'sig_d4e9102fae89bb3c17820aedfa9102bc45a8f3b20c91e847ad3ef0192a',
                publicKey: 'pub_docutask_root_key_2026_d4e9',
                nonce: 492011,
            },
        },
        {
            id: 'ev-node-003',
            type: 'VALIDATION_CHECK',
            agent: 'docutask-qa-department',
            timestamp: '2026-09-10T18:22:10.680Z',
            hash: '7c3f810dae99120bc45a8f3b20c91e847ad3ef0192a83c748d4e9102fae89bb3c',
            parentHash: 'd4e9102fae89bb3c17820aedfa9102bc45a8f3b20c91e847ad3ef0192a83c748',
            status: 'VERIFIED',
            inputs: { line_items_sum: 4850.0, extracted_total: 4850.0, tolerance_usd: 0.01 },
            outputs: { invariant_reconciled: true, p_value: 0.0001, status: 'RECONCILED' },
            metrics: { check_latency_ms: 18.2, accuracy_score: 1.0 },
            proof: {
                algorithm: 'SHA-256+Ed25519-Sim',
                signature: 'sig_7c3f810dae99120bc45a8f3b20c91e847ad3ef0192a83c748d4e9102f',
                publicKey: 'pub_docutask_root_key_2026_7c3f',
                nonce: 192837,
            },
        },
        {
            id: 'ev-node-004',
            type: 'REFLECTION_MUTATION',
            agent: 'docutask-governance-council',
            timestamp: '2026-09-10T18:22:11.050Z',
            hash: '3b20c91e847ad3ef0192a83c748d4e9102fae89bb3c7c3f810dae99120bc45a8f',
            parentHash: '7c3f810dae99120bc45a8f3b20c91e847ad3ef0192a83c748d4e9102fae89bb3c',
            status: 'VERIFIED',
            inputs: { policy: 'ocr_deskew_threshold', observed_drift: '0.4 deg angle on rotated invoice headers' },
            outputs: { action: 'ADAPT_PREFILTER_POLICY', new_threshold_deg: 0.25, governance_vote: 'UNANIMOUS_APPROVED' },
            metrics: { expected_accuracy_lift: 0.038, policy_entropy_delta: -0.12 },
            proof: {
                algorithm: 'SHA-256+Ed25519-Sim',
                signature: 'sig_3b20c91e847ad3ef0192a83c748d4e9102fae89bb3c7c3f810dae99120b',
                publicKey: 'pub_docutask_root_key_2026_3b20',
                nonce: 663910,
            },
        },
    ];
    const activeNode = evidenceNodes.find((n) => n.id === selectedNode) || evidenceNodes[0];
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Execution Evidence Explorer" }), _jsx(Badge, { variant: "success", size: "sm", children: "Merkle Root Attested" })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Immutable cryptographic hash chains and Merkle DAG linking every planner decision, tool call, validation step, and policy mutation." })] }), _jsxs("div", { className: "flex items-center gap-2", children: [_jsx(Badge, { variant: "outline", size: "md", children: "SHA-256 + Ed25519" }), _jsx(Badge, { variant: "intelligence", size: "md", children: "DAG Depth: 4 Layers" })] })] }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-3 gap-6", children: [_jsxs("div", { className: "space-y-3", children: [_jsxs("div", { className: "text-xs font-semibold uppercase tracking-wider text-muted-foreground", children: ["Evidence Chain (", evidenceNodes.length, " Nodes)"] }), evidenceNodes.map((node) => {
                                const isSelected = node.id === selectedNode;
                                return (_jsxs(Card, { className: `p-4 cursor-pointer transition-all ${isSelected ? 'border-primary ring-1 ring-primary/40 bg-primary/5' : 'hover:border-border/80'}`, onClick: () => setSelectedNode(node.id), children: [_jsxs("div", { className: "flex items-start justify-between", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "font-mono text-xs font-bold text-foreground", children: node.id }), _jsx(Badge, { variant: node.status === 'VERIFIED' ? 'success' : 'warning', size: "sm", children: node.status })] }), _jsx("div", { className: "text-xs font-medium text-muted-foreground mt-1", children: node.type })] }), _jsx("span", { className: "text-[10px] font-mono text-muted-foreground", children: node.timestamp.split('T')[1]?.replace('Z', '') })] }), _jsxs("div", { className: "mt-3 font-mono text-[11px] text-muted-foreground truncate", children: [_jsx("span", { className: "text-foreground/70", children: "Hash: " }), node.hash.slice(0, 16), "...", node.hash.slice(-8)] })] }, node.id));
                            })] }), _jsx("div", { className: "lg:col-span-2 space-y-6", children: _jsxs(Card, { className: "p-6 space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-border/40 pb-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h2", { className: "text-lg font-bold", children: activeNode.id }), _jsx(Badge, { variant: "intelligence", size: "sm", children: activeNode.type })] }), _jsxs("div", { className: "text-xs text-muted-foreground mt-1", children: ["Source Agent: ", _jsx("span", { className: "font-mono text-foreground", children: activeNode.agent })] })] }), _jsxs("div", { className: "text-right", children: [_jsx("div", { className: "text-xs text-muted-foreground", children: "Timestamp (UTC)" }), _jsx("div", { className: "font-mono text-xs text-foreground", children: activeNode.timestamp })] })] }), _jsxs("div", { className: "bg-muted/30 rounded-lg p-4 border border-border/40 space-y-2", children: [_jsxs("div", { className: "text-xs font-semibold text-foreground flex items-center justify-between", children: [_jsx("span", { children: "Cryptographic Proof & Signature" }), _jsx("span", { className: "text-emerald-400 font-mono text-[11px]", children: "\u2713 Nonce & Signature Verified" })] }), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-2 text-xs font-mono", children: [_jsxs("div", { children: [_jsx("span", { className: "text-muted-foreground", children: "Digest: " }), _jsx("span", { className: "text-foreground/90 break-all", children: activeNode.hash })] }), _jsxs("div", { children: [_jsx("span", { className: "text-muted-foreground", children: "Parent Hash: " }), _jsxs("span", { className: "text-foreground/90 break-all", children: [activeNode.parentHash.slice(0, 24), "..."] })] }), _jsxs("div", { children: [_jsx("span", { className: "text-muted-foreground", children: "Signature: " }), _jsx("span", { className: "text-foreground/90 break-all", children: activeNode.proof.signature })] }), _jsxs("div", { children: [_jsx("span", { className: "text-muted-foreground", children: "Public Key: " }), _jsx("span", { className: "text-foreground/90", children: activeNode.proof.publicKey })] })] })] }), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-4", children: [_jsxs("div", { className: "space-y-2", children: [_jsx("div", { className: "text-xs font-semibold uppercase tracking-wider text-muted-foreground", children: "Verified Inputs" }), _jsx("pre", { className: "p-3 bg-muted/40 rounded border border-border/40 font-mono text-xs overflow-x-auto", children: JSON.stringify(activeNode.inputs, null, 2) })] }), _jsxs("div", { className: "space-y-2", children: [_jsx("div", { className: "text-xs font-semibold uppercase tracking-wider text-muted-foreground", children: "Verified Outputs" }), _jsx("pre", { className: "p-3 bg-muted/40 rounded border border-border/40 font-mono text-xs overflow-x-auto", children: JSON.stringify(activeNode.outputs, null, 2) })] })] }), _jsxs("div", { className: "space-y-2", children: [_jsx("div", { className: "text-xs font-semibold uppercase tracking-wider text-muted-foreground", children: "Runtime Telemetry Metrics" }), _jsx("div", { className: "grid grid-cols-3 gap-3", children: Object.entries(activeNode.metrics).map(([key, val]) => (_jsxs("div", { className: "p-3 bg-card border border-border/40 rounded", children: [_jsx("div", { className: "text-[11px] text-muted-foreground capitalize", children: key.replace(/_/g, ' ') }), _jsx("div", { className: "text-sm font-bold font-mono text-foreground mt-1", children: typeof val === 'number' ? (val < 1 && val > 0 ? val.toFixed(4) : val.toLocaleString()) : String(val) })] }, key))) })] })] }) })] })] }));
};
