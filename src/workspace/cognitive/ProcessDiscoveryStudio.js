import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import React, { useState, useEffect } from 'react';
import { TrendingUp, RefreshCw, ArrowRight } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { cognitiveApiClient } from '../../services/cognitiveApiClient';
export const ProcessDiscoveryStudio = () => {
    const [processes, setProcesses] = useState([]);
    const loadData = async () => {
        const data = await cognitiveApiClient.listDiscoveredProcesses();
        setProcesses(data);
    };
    useEffect(() => {
        loadData();
    }, []);
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex justify-between items-center", children: [_jsxs("div", { children: [_jsxs("h1", { className: "text-2xl font-bold text-slate-100 flex items-center gap-2", children: [_jsx(TrendingUp, { className: "w-7 h-7 text-emerald-400" }), "Autonomous Process Discovery & Mining Studio"] }), _jsx("p", { className: "text-slate-400 text-sm mt-1", children: "Reconstructs end-to-end workflows from execution traces, measuring cycle times and isolating bottlenecks." })] }), _jsx(Button, { variant: "outline", onClick: loadData, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RefreshCw, { className: "w-4 h-4" }), "Refresh"] }) })] }), _jsx("div", { className: "space-y-4", children: processes.map((proc) => (_jsxs(Card, { className: "p-5 bg-slate-900/60 border-slate-800 space-y-4", children: [_jsxs("div", { className: "flex justify-between items-start", children: [_jsxs("div", { children: [_jsx("h3", { className: "text-lg font-semibold text-slate-200", children: proc.process_name }), _jsxs("p", { className: "text-xs text-slate-400", children: ["Observed Executions: ", proc.observed_executions_count, " | Avg Cycle Time: ", proc.avg_cycle_time_seconds, "s"] })] }), _jsxs(Badge, { variant: "success", children: ["Opportunity Score: ", (proc.automation_opportunity_score * 100).toFixed(0), "%"] })] }), _jsxs("div", { children: [_jsx("h4", { className: "text-xs font-semibold text-slate-400 uppercase mb-2", children: "Reconstructed Execution Path" }), _jsx("div", { className: "flex flex-wrap gap-2 items-center", children: proc.reconstructed_steps.map((step, i) => (_jsxs(React.Fragment, { children: [_jsx("span", { className: "px-2.5 py-1.5 rounded bg-slate-800 text-xs font-medium text-slate-200 border border-slate-700", children: step }), i < proc.reconstructed_steps.length - 1 && (_jsx(ArrowRight, { className: "w-3.5 h-3.5 text-slate-500" }))] }, i))) })] }), _jsxs("div", { className: "p-3 rounded-lg bg-amber-950/20 border border-amber-500/30 space-y-1", children: [_jsx("span", { className: "text-xs font-semibold text-amber-300", children: "Detected Process Bottlenecks:" }), proc.bottlenecks.map((b, idx) => (_jsx("p", { className: "text-xs text-slate-300", children: b }, idx)))] })] }, proc.id))) })] }));
};
