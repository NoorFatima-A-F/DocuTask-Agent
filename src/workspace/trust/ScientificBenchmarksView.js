import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
export const ScientificBenchmarksView = () => {
    const benchmarks = [
        {
            id: 'bench_inv_1000',
            name: 'Standard Enterprise Invoices 1,000-Doc Corpus',
            dataset: 'CorpDoc-Invoice-1K',
            fingerprint: '0x1a2b...9c0d',
            size: 1000,
            seed: 42,
            accuracy: 0.994,
            latencyP50: 820.0,
            costPer1k: '$7.80',
            repeatability: '99.95%',
            evidence: '0x8f2ac31b4e5d6a7b',
        },
        {
            id: 'bench_con_500',
            name: 'Commercial Master Services Agreements 500-Doc Corpus',
            dataset: 'LegalCorp-MSA-500',
            fingerprint: '0x2b3c...0d1e',
            size: 500,
            seed: 1337,
            accuracy: 0.985,
            latencyP50: 1950.0,
            costPer1k: '$32.00',
            repeatability: '99.88%',
            evidence: '0x3c7eb44a1d9e2f8c',
        },
        {
            id: 'bench_med_250',
            name: 'Clinical Trial Patient Intake Forms 250-Doc Corpus',
            dataset: 'HealthSecure-Intake-250',
            fingerprint: '0x3c4d...1e2f',
            size: 250,
            seed: 999,
            accuracy: 0.988,
            latencyP50: 1600.0,
            costPer1k: '$24.50',
            repeatability: '99.91%',
            evidence: '0x991afe820b4c7d6e',
        },
    ];
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Scientific Benchmark Registry" }), _jsx(Badge, { variant: "intelligence", size: "sm", children: "Pillar 5" })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Independently reproducible benchmark datasets with frozen RNG seeds, environment captures, and 10-run repeatability verification." })] }), _jsx("div", { className: "flex items-center gap-2", children: _jsx(Badge, { variant: "success", size: "md", children: "Repeatability: >99.8% Certified" }) })] }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-3 gap-4", children: benchmarks.map((b) => (_jsxs(Card, { className: "p-5 flex flex-col justify-between", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center justify-between mb-2", children: [_jsx("span", { className: "font-mono text-xs text-primary font-semibold", children: b.id }), _jsxs(Badge, { variant: "outline", size: "sm", className: "font-mono", children: ["Seed: ", b.seed] })] }), _jsx("h3", { className: "text-sm font-semibold text-foreground mb-1", children: b.name }), _jsxs("div", { className: "text-xs text-muted-foreground mb-4", children: ["Dataset: ", _jsx("strong", { className: "text-foreground", children: b.dataset }), " (", b.size, " docs)"] }), _jsxs("div", { className: "grid grid-cols-2 gap-2 p-2.5 rounded bg-muted/20 border border-border/40 mb-4 text-center text-xs", children: [_jsxs("div", { children: [_jsx("div", { className: "text-[10px] text-muted-foreground", children: "Accuracy" }), _jsxs("div", { className: "font-mono font-bold text-emerald-400", children: [(b.accuracy * 100).toFixed(1), "%"] })] }), _jsxs("div", { children: [_jsx("div", { className: "text-[10px] text-muted-foreground", children: "P50 Latency" }), _jsxs("div", { className: "font-mono font-bold text-foreground", children: [b.latencyP50, " ms"] })] }), _jsxs("div", { children: [_jsx("div", { className: "text-[10px] text-muted-foreground", children: "Cost / 1k Docs" }), _jsx("div", { className: "font-mono font-bold text-foreground", children: b.costPer1k })] }), _jsxs("div", { children: [_jsx("div", { className: "text-[10px] text-muted-foreground", children: "Repeatability" }), _jsx("div", { className: "font-mono font-bold text-primary", children: b.repeatability })] })] })] }), _jsxs("div", { className: "border-t border-border/40 pt-3 flex items-center justify-between text-xs text-muted-foreground", children: [_jsxs("span", { className: "font-mono text-[11px]", children: ["Evidence: ", b.evidence] }), _jsx("button", { className: "text-primary hover:underline font-medium", children: "Re-Run Benchmark \u2192" })] })] }, b.id))) })] }));
};
