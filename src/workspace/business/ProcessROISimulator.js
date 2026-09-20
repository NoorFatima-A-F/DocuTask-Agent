import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Calculator, Play, RefreshCw, } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { BusinessApiClient } from '../../services/businessApiClient';
export const ProcessROISimulator = () => {
    const [txCount, setTxCount] = useState(1000);
    const [running, setRunning] = useState(false);
    const [result, setResult] = useState(null);
    const handleSimulate = async () => {
        try {
            setRunning(true);
            const res = await BusinessApiClient.runSimulation({
                process_id: 'proc_invoice_enterprise_01',
                simulated_transactions_count: txCount,
            });
            setResult(res);
        }
        catch (err) {
            console.error('Failed to run simulation:', err);
        }
        finally {
            setRunning(false);
        }
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsx("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/60 p-6 rounded-2xl border border-slate-800 backdrop-blur-md", children: _jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2 bg-indigo-500/10 rounded-xl border border-indigo-500/20 text-indigo-400", children: _jsx(Calculator, { className: "w-6 h-6" }) }), _jsxs("div", { children: [_jsx("h1", { className: "text-2xl font-bold text-white", children: "What-If Process Simulation & ROI Forecaster" }), _jsx("p", { className: "text-sm text-slate-400", children: "Monte Carlo discrete-event simulation forecasting cost, cycle time, and ROI before production deployment" })] })] }) }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-3 gap-6", children: [_jsxs(Card, { className: "lg:col-span-1 p-6 bg-slate-900/60 border-slate-800 space-y-4", children: [_jsx("h2", { className: "text-base font-bold text-white border-b border-slate-800 pb-3", children: "Simulation Parameters" }), _jsxs("div", { className: "space-y-3 text-xs", children: [_jsxs("div", { children: [_jsx("label", { className: "block text-slate-400 mb-1", children: "Simulated Transaction Volume" }), _jsx("input", { type: "number", value: txCount, onChange: (e) => setTxCount(Number(e.target.value)), className: "w-full bg-slate-800 border border-slate-700 text-white rounded-lg p-2.5 text-xs" })] }), _jsxs("div", { children: [_jsx("label", { className: "block text-slate-400 mb-1", children: "Target Process Workflow" }), _jsxs("select", { className: "w-full bg-slate-800 border border-slate-700 text-white rounded-lg p-2.5 text-xs", children: [_jsx("option", { value: "proc_invoice_enterprise_01", children: "End-to-End Enterprise Invoicing" }), _jsx("option", { value: "proc_vendor_onboarding", children: "Global Vendor Onboarding" })] })] }), _jsx(Button, { variant: "intelligence", className: "w-full", onClick: handleSimulate, disabled: running, children: _jsxs("span", { className: "flex items-center justify-center gap-2", children: [running ? _jsx(RefreshCw, { className: "w-4 h-4 animate-spin" }) : _jsx(Play, { className: "w-4 h-4" }), "Run Monte Carlo Simulation"] }) })] })] }), _jsxs(Card, { className: "lg:col-span-2 p-6 bg-slate-900/40 border-slate-800 space-y-5", children: [_jsxs("div", { className: "flex justify-between items-center border-b border-slate-800 pb-3", children: [_jsx("h2", { className: "text-base font-semibold text-white", children: "Projected Business Impact & ROI" }), result && _jsxs(Badge, { variant: "success", children: ["Simulated (", txCount, " Transactions)"] })] }), result ? (_jsxs("div", { className: "space-y-4", children: [_jsxs("div", { className: "grid grid-cols-1 sm:grid-cols-3 gap-4", children: [_jsxs("div", { className: "p-4 bg-slate-800/40 rounded-xl border border-slate-700/60", children: [_jsx("span", { className: "text-slate-400 text-xs block mb-1", children: "Net Cost Savings" }), _jsxs("span", { className: "text-2xl font-bold text-emerald-400 font-mono", children: ["$", result.cost_reduction_usd.toLocaleString()] })] }), _jsxs("div", { className: "p-4 bg-slate-800/40 rounded-xl border border-slate-700/60", children: [_jsx("span", { className: "text-slate-400 text-xs block mb-1", children: "Cycle Time Reduction" }), _jsxs("span", { className: "text-2xl font-bold text-indigo-300 font-mono", children: [((result.baseline_cycle_time_sec - result.optimized_cycle_time_sec) / 60).toFixed(0), " mins"] })] }), _jsxs("div", { className: "p-4 bg-slate-800/40 rounded-xl border border-slate-700/60", children: [_jsx("span", { className: "text-slate-400 text-xs block mb-1", children: "Throughput Boost" }), _jsxs("span", { className: "text-2xl font-bold text-cyan-300 font-mono", children: ["+", result.throughput_increase_pct.toFixed(0), "%"] })] })] }), _jsxs("div", { className: "space-y-2 pt-2 border-t border-slate-800 text-xs font-mono text-slate-300", children: [_jsxs("div", { className: "flex justify-between", children: [_jsx("span", { className: "text-slate-400", children: "Baseline Legacy Process Cost:" }), _jsxs("span", { className: "text-white", children: ["$", result.baseline_cost_usd.toLocaleString()] })] }), _jsxs("div", { className: "flex justify-between", children: [_jsx("span", { className: "text-slate-400", children: "AI-Optimized Autonomous Cost:" }), _jsxs("span", { className: "text-emerald-400 font-bold", children: ["$", result.optimized_cost_usd.toLocaleString()] })] })] })] })) : (_jsx("p", { className: "text-slate-500 italic text-sm py-8 text-center", children: "Configure parameters and click \"Run Monte Carlo Simulation\" to forecast process ROI." }))] })] })] }));
};
