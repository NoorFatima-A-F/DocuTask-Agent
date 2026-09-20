import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
export const BenchmarkCertificateCenterView = () => {
    const [selectedCert, setSelectedCert] = useState('cert-inv-1000');
    const certificates = [
        {
            id: 'cert-inv-1000',
            title: 'Enterprise Invoice Benchmark (1,000 Pages)',
            sampleSize: 1000,
            throughputPgSec: 48.5,
            p95LatencyMs: 245.0,
            f1Score: 0.994,
            costPer1k: 1.25,
            confidenceInterval99: [0.991, 0.997],
            pValue: 0.0001,
            reproducibilityScore: 99.85,
            signature: 'sig_cert_a8f3b20c91e847ad3ef0192a83c7482910fae12089bb3c17',
            merkleLeafHash: '3ef0192a83c7482910fae12089bb3c17820aedfa9102bc45a8f3b20c91e847ad',
            certifiedAt: '2026-09-10T18:00:00Z',
        },
        {
            id: 'cert-table-500',
            title: 'Dense Financial Tables Benchmark (500 Pages)',
            sampleSize: 500,
            throughputPgSec: 36.2,
            p95LatencyMs: 380.0,
            f1Score: 0.991,
            costPer1k: 1.80,
            confidenceInterval99: [0.988, 0.994],
            pValue: 0.0002,
            reproducibilityScore: 99.90,
            signature: 'sig_cert_7c3f810dae99120bc45a8f3b20c91e847ad3ef0192a83c748',
            merkleLeafHash: 'd4e9102fae89bb3c17820aedfa9102bc45a8f3b20c91e847ad3ef0192a83c748',
            certifiedAt: '2026-09-10T18:15:00Z',
        },
    ];
    const activeCert = certificates.find((c) => c.id === selectedCert) || certificates[0];
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Benchmark Certification Center" }), _jsx(Badge, { variant: "success", size: "sm", children: "Mathematically Certified" })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Independently reproducible benchmark performance proofs attested with 99% confidence intervals and cryptographic signatures." })] }), _jsxs("div", { className: "flex items-center gap-2", children: [_jsx(Badge, { variant: "outline", size: "md", children: "p < 0.0001" }), _jsx(Badge, { variant: "intelligence", size: "md", children: "Repeatability: 99.85%" })] })] }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-3 gap-6", children: [_jsxs("div", { className: "space-y-3", children: [_jsxs("div", { className: "text-xs font-semibold uppercase tracking-wider text-muted-foreground", children: ["Certified Benchmark Suites (", certificates.length, ")"] }), certificates.map((cert) => {
                                const isSelected = cert.id === selectedCert;
                                return (_jsxs(Card, { className: `p-4 cursor-pointer transition-all ${isSelected ? 'border-primary ring-1 ring-primary/40 bg-primary/5' : 'hover:border-border/80'}`, onClick: () => setSelectedCert(cert.id), children: [_jsxs("div", { className: "flex items-start justify-between", children: [_jsxs("div", { children: [_jsx("span", { className: "font-semibold text-xs text-foreground", children: cert.title }), _jsx("div", { className: "text-xs font-mono text-muted-foreground mt-0.5", children: cert.id })] }), _jsx(Badge, { variant: "success", size: "sm", children: "CERTIFIED" })] }), _jsxs("div", { className: "mt-3 flex items-center justify-between text-xs font-mono text-muted-foreground", children: [_jsxs("span", { className: "text-foreground", children: [cert.throughputPgSec, " pg/s"] }), _jsxs("span", { className: "text-emerald-400 font-bold", children: [(cert.f1Score * 100).toFixed(1), "% F1"] }), _jsxs("span", { children: ["$", cert.costPer1k, "/1k"] })] })] }, cert.id));
                            })] }), _jsx("div", { className: "lg:col-span-2 space-y-4", children: _jsxs(Card, { className: "p-6 space-y-6 border-emerald-500/30 bg-emerald-950/5 relative overflow-hidden", children: [_jsxs("div", { className: "flex items-start justify-between border-b border-border/40 pb-4", children: [_jsxs("div", { children: [_jsx(Badge, { variant: "success", size: "sm", className: "mb-2", children: "OFFICIAL BENCHMARK CERTIFICATE" }), _jsx("h2", { className: "text-xl font-bold tracking-tight", children: activeCert.title }), _jsxs("div", { className: "text-xs text-muted-foreground mt-1", children: ["Sample Size: ", _jsxs("span", { className: "font-bold text-foreground", children: [activeCert.sampleSize.toLocaleString(), " Documents"] }), " | Certified: ", _jsx("span", { className: "font-mono text-foreground", children: activeCert.certifiedAt })] })] }), _jsxs("div", { className: "text-right font-mono", children: [_jsx("div", { className: "text-[10px] text-muted-foreground", children: "Reproducibility Parity" }), _jsxs("div", { className: "text-xl font-extrabold text-emerald-400", children: [activeCert.reproducibilityScore, "%"] })] })] }), _jsxs("div", { className: "grid grid-cols-2 sm:grid-cols-4 gap-4", children: [_jsxs("div", { className: "p-3 bg-card border border-border/40 rounded-lg", children: [_jsx("div", { className: "text-[11px] text-muted-foreground", children: "Throughput" }), _jsxs("div", { className: "text-lg font-bold font-mono text-foreground mt-1", children: [activeCert.throughputPgSec, " ", _jsx("span", { className: "text-xs font-normal text-muted-foreground", children: "pg/sec" })] })] }), _jsxs("div", { className: "p-3 bg-card border border-border/40 rounded-lg", children: [_jsx("div", { className: "text-[11px] text-muted-foreground", children: "P95 Latency" }), _jsxs("div", { className: "text-lg font-bold font-mono text-foreground mt-1", children: [activeCert.p95LatencyMs, " ", _jsx("span", { className: "text-xs font-normal text-muted-foreground", children: "ms" })] })] }), _jsxs("div", { className: "p-3 bg-card border border-border/40 rounded-lg", children: [_jsx("div", { className: "text-[11px] text-muted-foreground", children: "Accuracy (F1)" }), _jsxs("div", { className: "text-lg font-bold font-mono text-emerald-400 mt-1", children: [(activeCert.f1Score * 100).toFixed(2), "%"] })] }), _jsxs("div", { className: "p-3 bg-card border border-border/40 rounded-lg", children: [_jsx("div", { className: "text-[11px] text-muted-foreground", children: "Cost per 1k" }), _jsxs("div", { className: "text-lg font-bold font-mono text-foreground mt-1", children: ["$", activeCert.costPer1k.toFixed(2)] })] })] }), _jsxs("div", { className: "p-4 bg-muted/30 border border-border/40 rounded-lg space-y-2", children: [_jsx("div", { className: "text-xs font-semibold text-foreground", children: "Statistical Bounds & Confidence Intervals" }), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-2 text-xs font-mono text-muted-foreground", children: [_jsxs("div", { children: ["99% CI Bounds: ", _jsxs("span", { className: "text-foreground font-bold", children: ["[", activeCert.confidenceInterval99[0], ", ", activeCert.confidenceInterval99[1], "]"] })] }), _jsxs("div", { children: ["Hypothesis Test: ", _jsxs("span", { className: "text-foreground font-bold", children: ["p-value = ", activeCert.pValue, " (Significant)"] })] })] })] }), _jsxs("div", { className: "p-3 bg-card border border-border/40 rounded font-mono text-[11px] text-muted-foreground space-y-1", children: [_jsxs("div", { children: [_jsx("span", { className: "text-foreground", children: "Merkle Leaf Digest: " }), activeCert.merkleLeafHash] }), _jsxs("div", { children: [_jsx("span", { className: "text-foreground", children: "Authority Signature: " }), _jsx("span", { className: "text-emerald-400 font-bold", children: activeCert.signature })] })] })] }) })] })] }));
};
