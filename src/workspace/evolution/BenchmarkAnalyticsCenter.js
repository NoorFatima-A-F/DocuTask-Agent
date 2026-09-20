import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { BarChart3, Play, RefreshCw, Clock, Zap, Target, } from 'lucide-react';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { EvolutionPlatformApiClient } from '../../services/evolutionPlatformApiClient';
export const BenchmarkAnalyticsCenter = () => {
    const [benchmarks, setBenchmarks] = useState([]);
    const [latestBenchmark, setLatestBenchmark] = useState(null);
    const [loading, setLoading] = useState(true);
    const [running, setRunning] = useState(false);
    useEffect(() => {
        loadBenchmarks();
    }, []);
    const loadBenchmarks = async () => {
        setLoading(true);
        try {
            const data = await EvolutionPlatformApiClient.listBenchmarks();
            setBenchmarks(data);
            if (data.length > 0) {
                const last = data[data.length - 1];
                if (last)
                    setLatestBenchmark(last);
            }
        }
        catch (err) {
            console.error('Failed to load benchmarks:', err);
        }
        finally {
            setLoading(false);
        }
    };
    const handleRunBenchmark = async () => {
        setRunning(true);
        try {
            const res = await EvolutionPlatformApiClient.runBenchmark({
                baseline_version: 'v13.12-prod',
                candidate_version: `v13.13-eval-${Math.random().toString(36).substring(2, 6)}`,
                test_case_count: 500,
            });
            setLatestBenchmark(res);
            setBenchmarks((prev) => [...prev, res]);
        }
        catch (err) {
            console.error('Benchmark error:', err);
        }
        finally {
            setRunning(false);
        }
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "bg-gradient-to-r from-slate-900 via-slate-900 to-slate-950 border border-slate-800 rounded-2xl p-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-4 shadow-xl", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2.5 bg-emerald-500/10 border border-emerald-500/20 rounded-xl", children: _jsx(BarChart3, { className: "w-6 h-6 text-emerald-400" }) }), _jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-xl font-bold text-slate-100", children: "Empirical Benchmark Analytics Center" }), _jsx(Badge, { variant: "success", size: "sm", children: "Side-by-Side Trials" })] }), _jsx("p", { className: "text-sm text-slate-400 mt-0.5", children: "Empirical side-by-side comparative testing across thousands of synthetic and production workloads." })] })] }), _jsxs("div", { className: "flex items-center gap-3", children: [_jsx(Button, { variant: "outline", onClick: loadBenchmarks, disabled: loading, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RefreshCw, { className: `w-4 h-4 ${loading ? 'animate-spin' : ''}` }), "Refresh"] }) }), _jsx(Button, { variant: "intelligence", onClick: handleRunBenchmark, disabled: running, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(Play, { className: `w-4 h-4 ${running ? 'animate-spin' : ''}` }), running ? 'Executing 500 Trials...' : 'Run Empirical Benchmark'] }) })] })] }), latestBenchmark && (_jsxs("div", { className: "bg-slate-900/80 border border-slate-800 rounded-xl p-6 space-y-5", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-3 pb-4 border-b border-slate-800", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsxs("h2", { className: "text-base font-bold text-slate-100", children: [latestBenchmark.baseline_version, " vs. ", latestBenchmark.candidate_version] }), _jsx(Badge, { variant: latestBenchmark.status === 'PASSED' ? 'success' : 'error', size: "sm", children: latestBenchmark.status })] }), _jsxs("span", { className: "text-xs text-slate-400 font-mono mt-0.5 block", children: [latestBenchmark.test_cases_run, " test cases evaluated \u2022 Safe: ", latestBenchmark.safety_compliance_score === 1.0 ? '100%' : 'Degraded'] })] }), _jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-xs text-slate-400", children: "Net Improvement:" }), _jsxs("span", { className: "text-xl font-bold text-emerald-400 font-mono", children: ["+", latestBenchmark.improvement_score_pct.toFixed(1), "%"] })] })] }), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-3 gap-4 font-mono", children: [_jsxs("div", { className: "bg-slate-950/80 border border-slate-800 rounded-lg p-4 space-y-2", children: [_jsxs("div", { className: "flex items-center justify-between text-xs text-slate-400", children: [_jsxs("span", { className: "flex items-center gap-1.5", children: [_jsx(Clock, { className: "w-4 h-4 text-indigo-400" }), "P95 Latency"] }), _jsxs("span", { className: "text-emerald-400 font-bold", children: ["-", (((latestBenchmark.baseline_latency_p95 - latestBenchmark.candidate_latency_p95) / latestBenchmark.baseline_latency_p95) * 100).toFixed(1), "%"] })] }), _jsxs("div", { className: "flex items-baseline justify-between pt-1", children: [_jsxs("div", { className: "text-xs text-slate-500", children: ["Base: ", _jsxs("span", { className: "text-slate-300", children: [latestBenchmark.baseline_latency_p95.toFixed(1), "ms"] })] }), _jsxs("div", { className: "text-sm font-bold text-indigo-300", children: ["Cand: ", latestBenchmark.candidate_latency_p95.toFixed(1), "ms"] })] })] }), _jsxs("div", { className: "bg-slate-950/80 border border-slate-800 rounded-lg p-4 space-y-2", children: [_jsxs("div", { className: "flex items-center justify-between text-xs text-slate-400", children: [_jsxs("span", { className: "flex items-center gap-1.5", children: [_jsx(Zap, { className: "w-4 h-4 text-amber-400" }), "Token Cost / Task"] }), _jsxs("span", { className: "text-emerald-400 font-bold", children: ["-", (((latestBenchmark.baseline_token_cost - latestBenchmark.candidate_token_cost) / latestBenchmark.baseline_token_cost) * 100).toFixed(1), "%"] })] }), _jsxs("div", { className: "flex items-baseline justify-between pt-1", children: [_jsxs("div", { className: "text-xs text-slate-500", children: ["Base: ", _jsxs("span", { className: "text-slate-300", children: ["$", latestBenchmark.baseline_token_cost.toFixed(4)] })] }), _jsxs("div", { className: "text-sm font-bold text-amber-300", children: ["Cand: $", latestBenchmark.candidate_token_cost.toFixed(4)] })] })] }), _jsxs("div", { className: "bg-slate-950/80 border border-slate-800 rounded-lg p-4 space-y-2", children: [_jsxs("div", { className: "flex items-center justify-between text-xs text-slate-400", children: [_jsxs("span", { className: "flex items-center gap-1.5", children: [_jsx(Target, { className: "w-4 h-4 text-emerald-400" }), "Accuracy"] }), _jsxs("span", { className: "text-emerald-400 font-bold", children: ["+", (((latestBenchmark.candidate_accuracy - latestBenchmark.baseline_accuracy) / latestBenchmark.baseline_accuracy) * 100).toFixed(2), "%"] })] }), _jsxs("div", { className: "flex items-baseline justify-between pt-1", children: [_jsxs("div", { className: "text-xs text-slate-500", children: ["Base: ", _jsxs("span", { className: "text-slate-300", children: [(latestBenchmark.baseline_accuracy * 100).toFixed(1), "%"] })] }), _jsxs("div", { className: "text-sm font-bold text-emerald-300", children: ["Cand: ", (latestBenchmark.candidate_accuracy * 100).toFixed(1), "%"] })] })] })] })] })), _jsxs("div", { className: "bg-slate-900/80 border border-slate-800 rounded-xl p-6 space-y-4", children: [_jsx("h2", { className: "text-base font-semibold text-slate-100", children: "Benchmark Trial History" }), _jsx("div", { className: "overflow-x-auto", children: _jsxs("table", { className: "w-full text-left text-xs text-slate-300 font-mono", children: [_jsx("thead", { className: "bg-slate-950/60 text-slate-400 border-b border-slate-800 uppercase tracking-wider", children: _jsxs("tr", { children: [_jsx("th", { className: "py-2.5 px-3", children: "Trial ID" }), _jsx("th", { className: "py-2.5 px-3", children: "Baseline" }), _jsx("th", { className: "py-2.5 px-3", children: "Candidate" }), _jsx("th", { className: "py-2.5 px-3", children: "P95 \u0394" }), _jsx("th", { className: "py-2.5 px-3", children: "Cost \u0394" }), _jsx("th", { className: "py-2.5 px-3", children: "Net Score" }), _jsx("th", { className: "py-2.5 px-3", children: "Status" })] }) }), _jsx("tbody", { className: "divide-y divide-slate-800/60", children: benchmarks.slice().reverse().map((b) => (_jsxs("tr", { className: "hover:bg-slate-800/30 transition-colors", children: [_jsx("td", { className: "py-2.5 px-3 font-semibold text-slate-300", children: b.comparison_id }), _jsx("td", { className: "py-2.5 px-3 text-slate-400", children: b.baseline_version }), _jsx("td", { className: "py-2.5 px-3 text-indigo-300", children: b.candidate_version }), _jsxs("td", { className: "py-2.5 px-3 text-emerald-400", children: ["-", (((b.baseline_latency_p95 - b.candidate_latency_p95) / b.baseline_latency_p95) * 100).toFixed(1), "%"] }), _jsxs("td", { className: "py-2.5 px-3 text-emerald-400", children: ["-", (((b.baseline_token_cost - b.candidate_token_cost) / b.baseline_token_cost) * 100).toFixed(1), "%"] }), _jsxs("td", { className: "py-2.5 px-3 font-bold text-emerald-400", children: ["+", b.improvement_score_pct.toFixed(1), "%"] }), _jsx("td", { className: "py-2.5 px-3", children: _jsx(Badge, { variant: b.status === 'PASSED' ? 'success' : 'error', size: "sm", children: b.status }) })] }, b.comparison_id))) })] }) })] })] }));
};
