import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
export const OutcomeVerificationView = () => {
    const [selectedFilter, setSelectedFilter] = useState('ALL');
    const outcomes = [
        {
            id: 'OUT-2026-901',
            missionId: 'MIS-INV-8821',
            task: 'Structured Invoice Extraction',
            model: 'Gemini 2.5 Flash',
            predictedAcc: 0.965,
            observedAcc: 0.972,
            predictedLat: 480,
            observedLat: 462,
            predictedCost: 0.0018,
            observedCost: 0.00175,
            slaTargetMs: 1000,
            isSlaOk: true,
            timestamp: '1 min ago',
            status: 'VERIFIED',
        },
        {
            id: 'OUT-2026-902',
            missionId: 'MIS-TABLE-4412',
            task: 'Multi-Page Financial Table Extraction',
            model: 'Gemini 1.5 Pro',
            predictedAcc: 0.985,
            observedAcc: 0.988,
            predictedLat: 1850,
            observedLat: 1920,
            predictedCost: 0.0125,
            observedCost: 0.0131,
            slaTargetMs: 2500,
            isSlaOk: true,
            timestamp: '3 mins ago',
            status: 'VERIFIED',
        },
        {
            id: 'OUT-2026-903',
            missionId: 'MIS-SCAN-1099',
            task: 'Degraded Receipt OCR & Normalization',
            model: 'Gemini 2.5 Flash',
            predictedAcc: 0.920,
            observedAcc: 0.895,
            predictedLat: 550,
            observedLat: 1150,
            predictedCost: 0.0018,
            observedCost: 0.0036,
            slaTargetMs: 1000,
            isSlaOk: false,
            timestamp: '8 mins ago',
            status: 'SLA_BREACH',
        },
        {
            id: 'OUT-2026-904',
            missionId: 'MIS-KYC-0034',
            task: 'Identity Document Verification',
            model: 'Gemini Flash-Lite',
            predictedAcc: 0.940,
            observedAcc: 0.945,
            predictedLat: 220,
            observedLat: 210,
            predictedCost: 0.0004,
            observedCost: 0.00038,
            slaTargetMs: 800,
            isSlaOk: true,
            timestamp: '12 mins ago',
            status: 'VERIFIED',
        },
    ];
    const filteredOutcomes = outcomes.filter((o) => {
        if (selectedFilter === 'ALL')
            return true;
        return o.status === selectedFilter;
    });
    return (_jsxs("div", { className: "space-y-6", children: [_jsx("div", { className: "p-6 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-xl", children: _jsxs("div", { className: "flex flex-col md:flex-row items-start md:items-center justify-between gap-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-xl", children: "\uD83C\uDFAF" }), _jsx("h2", { className: "text-lg font-bold font-mono text-[#F8FAFC]", children: "Empirical Outcome Verification Engine" }), _jsx(Badge, { variant: "success", size: "sm", children: "ONLINE PAIRING ACTIVE" })] }), _jsx("p", { className: "text-sm font-mono text-[#94A3B8] mt-1", children: "Deterministic comparison of pre-execution planner predictions against post-execution ground-truth telemetry." })] }), _jsxs("div", { className: "flex items-center gap-2", children: [_jsxs("button", { onClick: () => setSelectedFilter('ALL'), className: `px-3 py-1.5 rounded-lg text-xs font-mono font-medium transition-all ${selectedFilter === 'ALL'
                                        ? 'bg-blue-600 text-white'
                                        : 'bg-[#1E293B] text-[#94A3B8] hover:bg-[#334155]'}`, children: ["All Runs (", outcomes.length, ")"] }), _jsx("button", { onClick: () => setSelectedFilter('SLA_BREACH'), className: `px-3 py-1.5 rounded-lg text-xs font-mono font-medium transition-all ${selectedFilter === 'SLA_BREACH'
                                        ? 'bg-rose-600 text-white'
                                        : 'bg-[#1E293B] text-[#94A3B8] hover:bg-[#334155]'}`, children: "SLA Breaches (1)" })] })] }) }), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-4 gap-4", children: [_jsxs(Card, { className: "p-4 bg-[#0F172A] border-[#1E293B]", children: [_jsx("div", { className: "text-xs font-mono text-[#94A3B8]", children: "Overall SLA Compliance" }), _jsx("div", { className: "text-2xl font-bold font-mono text-emerald-400 mt-1", children: "97.8%" }), _jsx("div", { className: "text-[11px] font-mono text-[#64748B] mt-1", children: "Target: \u2265 95.0%" })] }), _jsxs(Card, { className: "p-4 bg-[#0F172A] border-[#1E293B]", children: [_jsx("div", { className: "text-xs font-mono text-[#94A3B8]", children: "Mean Accuracy Error (MAE)" }), _jsx("div", { className: "text-2xl font-bold font-mono text-cyan-400 mt-1", children: "0.0142" }), _jsx("div", { className: "text-[11px] font-mono text-[#64748B] mt-1", children: "1.4% average residual" })] }), _jsxs(Card, { className: "p-4 bg-[#0F172A] border-[#1E293B]", children: [_jsx("div", { className: "text-xs font-mono text-[#94A3B8]", children: "Mean Latency Error" }), _jsx("div", { className: "text-2xl font-bold font-mono text-indigo-400 mt-1", children: "38.4 ms" }), _jsx("div", { className: "text-[11px] font-mono text-[#64748B] mt-1", children: "Within \u00B150ms band" })] }), _jsxs(Card, { className: "p-4 bg-[#0F172A] border-[#1E293B]", children: [_jsx("div", { className: "text-xs font-mono text-[#94A3B8]", children: "Cost Drift Tracking" }), _jsx("div", { className: "text-2xl font-bold font-mono text-emerald-400 mt-1", children: "-$0.00004" }), _jsx("div", { className: "text-[11px] font-mono text-[#64748B] mt-1", children: "Slight empirical surplus" })] })] }), _jsxs(Card, { className: "p-6 bg-[#0F172A] border-[#1E293B]", children: [_jsx("h3", { className: "text-sm font-bold font-mono text-[#F8FAFC] mb-4", children: "Recent Ground-Truth Verification Records" }), _jsx("div", { className: "overflow-x-auto", children: _jsxs("table", { className: "w-full text-left font-mono text-xs", children: [_jsx("thead", { children: _jsxs("tr", { className: "border-b border-[#1E293B] text-[#94A3B8]", children: [_jsx("th", { className: "pb-3", children: "Mission & Task" }), _jsx("th", { className: "pb-3", children: "Model" }), _jsx("th", { className: "pb-3", children: "Predicted vs Observed Acc" }), _jsx("th", { className: "pb-3", children: "Predicted vs Observed Latency" }), _jsx("th", { className: "pb-3", children: "Predicted vs Observed Cost" }), _jsx("th", { className: "pb-3", children: "SLA Status" })] }) }), _jsx("tbody", { className: "divide-y divide-[#1E293B]", children: filteredOutcomes.map((o) => {
                                        const accDiff = (o.observedAcc - o.predictedAcc) * 100;
                                        const latDiff = o.observedLat - o.predictedLat;
                                        return (_jsxs("tr", { className: "hover:bg-[#1E293B]/40 transition-colors", children: [_jsxs("td", { className: "py-3", children: [_jsx("div", { className: "font-bold text-[#F8FAFC]", children: o.missionId }), _jsx("div", { className: "text-[#64748B] text-[11px]", children: o.task })] }), _jsx("td", { className: "py-3 text-[#E2E8F0]", children: o.model }), _jsxs("td", { className: "py-3", children: [_jsxs("div", { className: "text-[#F8FAFC]", children: [(o.predictedAcc * 100).toFixed(1), "% \u2192 ", (o.observedAcc * 100).toFixed(1), "%"] }), _jsx("div", { className: `text-[11px] ${accDiff >= 0 ? 'text-emerald-400' : 'text-rose-400'}`, children: accDiff >= 0 ? `+${accDiff.toFixed(1)}%` : `${accDiff.toFixed(1)}%` })] }), _jsxs("td", { className: "py-3", children: [_jsxs("div", { className: "text-[#F8FAFC]", children: [o.predictedLat, "ms \u2192 ", o.observedLat, "ms"] }), _jsx("div", { className: `text-[11px] ${latDiff <= 0 ? 'text-emerald-400' : 'text-amber-400'}`, children: latDiff >= 0 ? `+${latDiff}ms` : `${latDiff}ms` })] }), _jsx("td", { className: "py-3", children: _jsxs("div", { className: "text-[#F8FAFC]", children: ["$", o.predictedCost.toFixed(4), " \u2192 $", o.observedCost.toFixed(4)] }) }), _jsx("td", { className: "py-3", children: _jsx(Badge, { variant: o.isSlaOk ? 'success' : 'error', size: "sm", children: o.isSlaOk ? 'COMPLIANT' : 'BREACH' }) })] }, o.id));
                                    }) })] }) })] })] }));
};
