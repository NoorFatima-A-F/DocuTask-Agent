import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Activity, ShieldCheck, Zap, Play, RotateCw, Clock, DollarSign, TrendingUp, } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { AIOperationsApiClient } from '../../services/aiOperationsApiClient';
export const AIOperationsExecutiveDashboard = () => {
    const [overview, setOverview] = useState(null);
    const [fleet, setFleet] = useState([]);
    const [loading, setLoading] = useState(true);
    const [runningCycle, setRunningCycle] = useState(false);
    const [cycleResult, setCycleResult] = useState(null);
    const loadData = async () => {
        try {
            setLoading(true);
            const [ov, fl] = await Promise.all([
                AIOperationsApiClient.getOverview(),
                AIOperationsApiClient.getFleetTelemetry(),
            ]);
            setOverview(ov);
            setFleet(fl);
        }
        catch (err) {
            console.error('Failed to load AI operations overview:', err);
        }
        finally {
            setLoading(false);
        }
    };
    useEffect(() => {
        loadData();
    }, []);
    const handleRunOperationsCycle = async () => {
        try {
            setRunningCycle(true);
            const res = await AIOperationsApiClient.runOperationsCycle('agent_chief_architect');
            setCycleResult(res);
            await loadData();
        }
        catch (err) {
            console.error('Failed to run operations cycle:', err);
        }
        finally {
            setRunningCycle(false);
        }
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 bg-slate-900/60 p-6 rounded-2xl border border-slate-800/80 backdrop-blur-md", children: [_jsx("div", { children: _jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2.5 bg-indigo-500/10 rounded-xl border border-indigo-500/20", children: _jsx(Activity, { className: "w-6 h-6 text-indigo-400" }) }), _jsxs("div", { children: [_jsx("h1", { className: "text-2xl font-bold text-white tracking-tight", children: "AI Operations Control Center" }), _jsx("p", { className: "text-sm text-slate-400", children: "Enterprise Agent Observability, Evaluation & Controlled Improvement" })] })] }) }), _jsxs("div", { className: "flex items-center gap-3", children: [_jsx(Button, { variant: "outline", onClick: loadData, disabled: loading, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RotateCw, { className: `w-4 h-4 ${loading ? 'animate-spin' : ''}` }), "Refresh"] }) }), _jsx(Button, { variant: "intelligence", onClick: handleRunOperationsCycle, disabled: runningCycle, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(Play, { className: `w-4 h-4 ${runningCycle ? 'animate-spin' : ''}` }), runningCycle ? 'Running Cycle...' : 'Execute Operations Cycle'] }) })] })] }), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4", children: [_jsxs(Card, { className: "p-5 bg-slate-900/40 border-slate-800", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-sm font-medium text-slate-400", children: "Fleet Health" }), _jsx(ShieldCheck, { className: "w-5 h-5 text-emerald-400" })] }), _jsxs("div", { className: "mt-2 flex items-baseline gap-2", children: [_jsxs("span", { className: "text-3xl font-bold text-white", children: [overview?.fleet_health_score ?? 100, "%"] }), _jsx(Badge, { variant: "success", children: "Optimal" })] }), _jsxs("p", { className: "mt-1 text-xs text-slate-500", children: [overview?.healthy_agents ?? 0, " Healthy / ", overview?.degraded_agents ?? 0, " Degraded"] })] }), _jsxs(Card, { className: "p-5 bg-slate-900/40 border-slate-800", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-sm font-medium text-slate-400", children: "Avg p95 Latency" }), _jsx(Clock, { className: "w-5 h-5 text-cyan-400" })] }), _jsxs("div", { className: "mt-2 flex items-baseline gap-2", children: [_jsx("span", { className: "text-3xl font-bold text-white", children: overview?.mean_fleet_latency_ms ?? 0 }), _jsx("span", { className: "text-xs text-slate-400", children: "ms" })] }), _jsxs("p", { className: "mt-1 text-xs text-slate-500", children: ["SLA compliance: ", overview?.sla_compliance_pct ?? 99.9, "%"] })] }), _jsxs(Card, { className: "p-5 bg-slate-900/40 border-slate-800", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-sm font-medium text-slate-400", children: "Total Tokens" }), _jsx(Zap, { className: "w-5 h-5 text-amber-400" })] }), _jsx("div", { className: "mt-2 flex items-baseline gap-2", children: _jsx("span", { className: "text-3xl font-bold text-white", children: (overview?.total_tokens_consumed ?? 0).toLocaleString() }) }), _jsxs("p", { className: "mt-1 text-xs text-slate-500", children: [overview?.total_invocations ?? 0, " total invocations"] })] }), _jsxs(Card, { className: "p-5 bg-slate-900/40 border-slate-800", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-sm font-medium text-slate-400", children: "Total Cost" }), _jsx(DollarSign, { className: "w-5 h-5 text-indigo-400" })] }), _jsxs("div", { className: "mt-2 flex items-baseline gap-2", children: [_jsxs("span", { className: "text-3xl font-bold text-white", children: ["$", overview?.total_cost_usd ?? 0.0] }), _jsx(Badge, { variant: "intelligence", children: "Controlled" })] }), _jsxs("p", { className: "mt-1 text-xs text-slate-500", children: ["Error rate: ", ((overview?.mean_fleet_error_rate ?? 0) * 100).toFixed(2), "%"] })] })] }), cycleResult && (_jsx(Card, { className: "p-5 bg-indigo-950/30 border-indigo-500/30", children: _jsxs("div", { className: "flex items-start justify-between", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2 bg-indigo-500/20 rounded-lg", children: _jsx(TrendingUp, { className: "w-5 h-5 text-indigo-400" }) }), _jsxs("div", { children: [_jsx("h3", { className: "text-sm font-semibold text-white", children: "Autonomous AI Operations Cycle Completed" }), _jsxs("p", { className: "text-xs text-slate-400 mt-0.5", children: ["Evaluated ", cycleResult.agent_id, " \u2022 Generated proposal: ", cycleResult.improvement_proposal?.proposal_id, " \u2022 Canary validated"] })] })] }), _jsx(Badge, { variant: "success", children: "Executed" })] }) })), _jsxs(Card, { className: "p-6 bg-slate-900/40 border-slate-800", children: [_jsxs("div", { className: "flex items-center justify-between mb-4", children: [_jsxs("div", { children: [_jsx("h2", { className: "text-lg font-semibold text-white", children: "Active Agent Fleet" }), _jsx("p", { className: "text-xs text-slate-400", children: "Real-time status, token throughput, and latency distribution" })] }), _jsxs(Badge, { variant: "outline", children: [fleet.length, " Agents Enrolled"] })] }), _jsx("div", { className: "overflow-x-auto", children: _jsxs("table", { className: "w-full text-left text-sm", children: [_jsx("thead", { children: _jsxs("tr", { className: "border-b border-slate-800 text-slate-400 text-xs uppercase tracking-wider", children: [_jsx("th", { className: "pb-3 font-medium", children: "Agent" }), _jsx("th", { className: "pb-3 font-medium", children: "Role" }), _jsx("th", { className: "pb-3 font-medium", children: "Status" }), _jsx("th", { className: "pb-3 font-medium", children: "Success Rate" }), _jsx("th", { className: "pb-3 font-medium", children: "p95 Latency" }), _jsx("th", { className: "pb-3 font-medium", children: "Tokens / Cost" }), _jsx("th", { className: "pb-3 font-medium", children: "Invocations" })] }) }), _jsx("tbody", { className: "divide-y divide-slate-800/60", children: fleet.map((agent) => (_jsxs("tr", { className: "hover:bg-slate-800/30 transition-colors", children: [_jsxs("td", { className: "py-3.5", children: [_jsxs("div", { className: "flex items-center gap-2.5", children: [_jsx("div", { className: "w-2 h-2 rounded-full bg-indigo-400" }), _jsx("span", { className: "font-medium text-white", children: agent.agent_name })] }), _jsx("span", { className: "text-xs text-slate-500 font-mono ml-4.5", children: agent.version })] }), _jsx("td", { className: "py-3.5 text-slate-300 text-xs", children: agent.role }), _jsx("td", { className: "py-3.5", children: _jsx(Badge, { variant: agent.health_status === 'HEALTHY'
                                                        ? 'success'
                                                        : agent.health_status === 'DEGRADED'
                                                            ? 'warning'
                                                            : 'error', children: agent.health_status }) }), _jsx("td", { className: "py-3.5", children: _jsxs("span", { className: "font-semibold text-slate-200", children: [(agent.success_rate * 100).toFixed(1), "%"] }) }), _jsxs("td", { className: "py-3.5 text-slate-300", children: [agent.p95_latency_ms, " ms"] }), _jsxs("td", { className: "py-3.5", children: [_jsxs("div", { className: "text-xs text-slate-200", children: [agent.total_tokens_consumed.toLocaleString(), " tok"] }), _jsxs("div", { className: "text-[11px] text-slate-500", children: ["$", agent.total_cost_usd] })] }), _jsx("td", { className: "py-3.5 text-slate-300", children: agent.total_invocations })] }, agent.agent_id))) })] }) })] })] }));
};
