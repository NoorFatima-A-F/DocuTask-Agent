import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
export const RuntimeProvenanceGraphView = () => {
    const [selectedNode, setSelectedNode] = useState('node-val-check');
    const provenanceNodes = [
        {
            id: 'node-raw-doc',
            type: 'INPUT',
            label: 'Raw PDF Document #8891',
            digest: 'c7e12f00a8918231bbd93172ca0913ef451',
            details: '4-page multi-table commercial invoice uploaded at 18:22:09 UTC.',
            parents: [],
            children: ['node-plan-dec'],
        },
        {
            id: 'node-plan-dec',
            type: 'PLAN',
            label: 'Planner Trajectory (Flash + Parallelism=3)',
            digest: '8891dec0001a4f98b12e3914a87c53d0e91',
            details: 'Evaluated 3 candidates; selected flash-p3 with 0.892 utility.',
            parents: ['node-raw-doc'],
            children: ['node-ocr-tool'],
        },
        {
            id: 'node-ocr-tool',
            type: 'TOOL',
            label: 'Adaptive OCR Execution (Tesseract V5)',
            digest: 'ocr001trace99102fae89bb3c17820aedfa',
            details: 'Extracted 142 tokens and 28 bounding boxes in 124.5ms.',
            parents: ['node-plan-dec'],
            children: ['node-val-check'],
        },
        {
            id: 'node-val-check',
            type: 'VALIDATION',
            label: 'Rule & Invariant Reconciliation',
            digest: 'val001pass7721d4e9102fae89bb3c1782',
            details: 'Verified Subtotal + Tax == Total with p=0.0001 confidence.',
            parents: ['node-ocr-tool'],
            children: ['node-out-json'],
        },
        {
            id: 'node-out-json',
            type: 'OUTPUT',
            label: 'Certified Extraction JSON',
            digest: 'f81d4fae7dec11d0a76500a0c91e6bf6012',
            details: 'Stored in content-addressable registry with SHA-256 seal.',
            parents: ['node-val-check'],
            children: [],
        },
    ];
    const activeNode = provenanceNodes.find((n) => n.id === selectedNode) || provenanceNodes[0];
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Runtime Provenance DAG" }), _jsx(Badge, { variant: "success", size: "sm", children: "Acyclic & Grounded" })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "End-to-end data lineage graph proving how every output token directly originates from raw document inputs and verified tool steps." })] }), _jsxs("div", { className: "flex items-center gap-2", children: [_jsxs(Badge, { variant: "outline", size: "md", children: ["Lineage Nodes: ", provenanceNodes.length] }), _jsx(Badge, { variant: "intelligence", size: "md", children: "Zero Dangling References" })] })] }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-3 gap-6", children: [_jsx("div", { className: "lg:col-span-2 space-y-4", children: _jsxs(Card, { className: "p-6 space-y-6", children: [_jsx("div", { className: "text-xs font-semibold uppercase tracking-wider text-muted-foreground", children: "Lineage DAG Flow" }), _jsx("div", { className: "flex flex-col space-y-3", children: provenanceNodes.map((node, idx) => {
                                        const isSelected = node.id === selectedNode;
                                        return (_jsxs("div", { className: "space-y-2", children: [_jsxs("div", { className: `p-4 rounded-lg border cursor-pointer transition-all ${isSelected
                                                        ? 'border-primary ring-2 ring-primary/30 bg-primary/10'
                                                        : 'border-border/60 hover:border-border bg-card'}`, onClick: () => setSelectedNode(node.id), children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsxs("span", { className: "font-mono text-xs font-bold text-muted-foreground", children: ["#", idx + 1] }), _jsx("span", { className: "text-sm font-semibold text-foreground", children: node.label })] }), _jsx(Badge, { variant: node.type === 'OUTPUT' ? 'success' : node.type === 'INPUT' ? 'info' : 'outline', size: "sm", children: node.type })] }), _jsx("div", { className: "mt-2 text-xs text-muted-foreground", children: node.details }), _jsxs("div", { className: "mt-2 font-mono text-[10px] text-foreground/70", children: ["Digest: ", node.digest] })] }), idx < provenanceNodes.length - 1 && (_jsx("div", { className: "flex justify-center text-muted-foreground", children: _jsx("span", { className: "text-sm", children: "\u2193" }) }))] }, node.id));
                                    }) })] }) }), _jsx("div", { className: "space-y-4", children: _jsxs(Card, { className: "p-6 space-y-4", children: [_jsx("div", { className: "text-xs font-semibold uppercase tracking-wider text-muted-foreground", children: "Node Details" }), _jsxs("div", { className: "space-y-3", children: [_jsxs("div", { children: [_jsx("div", { className: "text-xs text-muted-foreground", children: "Node ID" }), _jsx("div", { className: "font-mono text-sm font-bold text-foreground", children: activeNode.id })] }), _jsxs("div", { children: [_jsx("div", { className: "text-xs text-muted-foreground", children: "Node Type" }), _jsx(Badge, { variant: "intelligence", size: "sm", className: "mt-1", children: activeNode.type })] }), _jsxs("div", { children: [_jsx("div", { className: "text-xs text-muted-foreground", children: "Cryptographic Digest" }), _jsx("div", { className: "font-mono text-xs text-foreground/90 break-all p-2 bg-muted/30 rounded border border-border/40 mt-1", children: activeNode.digest })] }), _jsxs("div", { children: [_jsx("div", { className: "text-xs text-muted-foreground", children: "Direct Ancestors (Parents)" }), _jsx("div", { className: "flex flex-wrap gap-1 mt-1", children: activeNode.parents.length > 0 ? (activeNode.parents.map((p) => _jsx(Badge, { variant: "outline", size: "sm", children: p }, p))) : (_jsx("span", { className: "text-xs text-muted-foreground", children: "Root Input (None)" })) })] }), _jsxs("div", { children: [_jsx("div", { className: "text-xs text-muted-foreground", children: "Direct Descendants (Children)" }), _jsx("div", { className: "flex flex-wrap gap-1 mt-1", children: activeNode.children.length > 0 ? (activeNode.children.map((c) => _jsx(Badge, { variant: "outline", size: "sm", children: c }, c))) : (_jsx("span", { className: "text-xs text-muted-foreground", children: "Terminal Output (Leaf)" })) })] })] })] }) })] })] }));
};
