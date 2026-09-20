import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { ShieldCheck, Play, RotateCw, Activity, Zap, CheckCircle2, Workflow, Server, Layers, Terminal, } from 'lucide-react';
import { executionPlatformApiClient } from '../../services/executionPlatformApiClient';
export const ExecutionExecutiveDashboard = () => {
    const [overview, setOverview] = useState(null);
    const [recentMissions, setRecentMissions] = useState([]);
    const [loading, setLoading] = useState(true);
    const [executingQuickGoal, setExecutingQuickGoal] = useState(false);
    const loadData = async () => {
        try {
            setLoading(true);
            const [ov, mList] = await Promise.all([
                executionPlatformApiClient.getOverview(),
                executionPlatformApiClient.listMissions(),
            ]);
            setOverview(ov);
            setRecentMissions(mList.missions || []);
        }
        catch (err) {
            console.error('Failed to load execution overview:', err);
        }
        finally {
            setLoading(false);
        }
    };
    useEffect(() => {
        loadData();
    }, []);
    const handleQuickExecute = async (goal) => {
        try {
            setExecutingQuickGoal(true);
            await executionPlatformApiClient.executeGoal({
                goal,
                dry_run: false,
                initiated_by: 'Executive Director Console',
            });
            await loadData();
        }
        catch (err) {
            console.error('Execution goal error:', err);
        }
        finally {
            setExecutingQuickGoal(false);
        }
    };
    if (loading && !overview) {
        return (_jsx("div", { className: "flex items-center justify-center h-96", children: _jsxs("div", { className: "flex flex-col items-center gap-4", children: [_jsx(RotateCw, { className: "w-8 h-8 animate-spin text-purple-500" }), _jsx("p", { className: "text-gray-400", children: "Loading Execution Platform Telemetry..." })] }) }));
    }
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-gradient-to-r from-slate-900 via-purple-950 to-slate-900 p-6 rounded-2xl border border-purple-800/40 shadow-xl", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("h1", { className: "text-2xl font-bold text-white tracking-wide", children: "Autonomous Real-World Execution Platform" }), _jsx(Badge, { variant: "intelligence", children: "Phase 13.15 ARWE-UTOCOP" })] }), _jsx("p", { className: "text-purple-200/80 text-sm mt-1", children: "Universal Tool Orchestration, Cyber-Physical Operations, Digital Twin Sandboxing & Cryptographic Ledgers" })] }), _jsxs("div", { className: "flex items-center gap-3", children: [_jsx(Button, { variant: "outline", onClick: loadData, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RotateCw, { className: "w-4 h-4" }), "Refresh"] }) }), _jsx(Button, { variant: "intelligence", onClick: () => handleQuickExecute('Deploy autonomous hotfix to canary and verify'), disabled: executingQuickGoal, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(Play, { className: "w-4 h-4" }), executingQuickGoal ? 'Executing Mission...' : 'Execute Hotfix Mission'] }) })] })] }), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4", children: [_jsxs(Card, { className: "bg-slate-900/60 border-slate-800 backdrop-blur", children: [_jsxs(CardHeader, { className: "flex flex-row items-center justify-between pb-2", children: [_jsx(CardTitle, { className: "text-sm font-medium text-slate-400", children: "Active Connectors" }), _jsx(Server, { className: "w-4 h-4 text-emerald-400" })] }), _jsxs(CardContent, { children: [_jsxs("div", { className: "text-2xl font-bold text-white", children: [overview?.connected_count || 0, " / ", overview?.total_connectors || 0] }), _jsxs("p", { className: "text-xs text-emerald-400 mt-1 flex items-center gap-1", children: [_jsx(CheckCircle2, { className: "w-3 h-3" }), " All external gateways healthy"] })] })] }), _jsxs(Card, { className: "bg-slate-900/60 border-slate-800 backdrop-blur", children: [_jsxs(CardHeader, { className: "flex flex-row items-center justify-between pb-2", children: [_jsx(CardTitle, { className: "text-sm font-medium text-slate-400", children: "Registered Tools" }), _jsx(Zap, { className: "w-4 h-4 text-amber-400" })] }), _jsxs(CardContent, { children: [_jsx("div", { className: "text-2xl font-bold text-white", children: overview?.total_tools || 0 }), _jsx("p", { className: "text-xs text-slate-400 mt-1", children: "Across 8 taxonomy categories" })] })] }), _jsxs(Card, { className: "bg-slate-900/60 border-slate-800 backdrop-blur", children: [_jsxs(CardHeader, { className: "flex flex-row items-center justify-between pb-2", children: [_jsx(CardTitle, { className: "text-sm font-medium text-slate-400", children: "Total Missions Run" }), _jsx(Workflow, { className: "w-4 h-4 text-purple-400" })] }), _jsxs(CardContent, { children: [_jsx("div", { className: "text-2xl font-bold text-white", children: overview?.total_missions || 0 }), _jsxs("p", { className: "text-xs text-purple-400 mt-1", children: [overview?.completed_missions || 0, " completed successfully"] })] })] }), _jsxs(Card, { className: "bg-slate-900/60 border-slate-800 backdrop-blur", children: [_jsxs(CardHeader, { className: "flex flex-row items-center justify-between pb-2", children: [_jsx(CardTitle, { className: "text-sm font-medium text-slate-400", children: "Cryptographic Audit Ledger" }), _jsx(ShieldCheck, { className: "w-4 h-4 text-cyan-400" })] }), _jsxs(CardContent, { children: [_jsx("div", { className: "text-2xl font-bold text-cyan-400", children: overview?.audit_ledger_integrity ? '100% Valid' : 'Degraded' }), _jsx("p", { className: "text-xs text-slate-400 mt-1", children: "SHA-256 Chained Integrity" })] })] })] }), _jsxs(Card, { className: "bg-slate-900/70 border-slate-800", children: [_jsx(CardHeader, { children: _jsxs(CardTitle, { className: "text-base text-white flex items-center gap-2", children: [_jsx(Layers, { className: "w-5 h-5 text-purple-400" }), "Core Autonomous Execution Invariant Pipeline"] }) }), _jsx(CardContent, { children: _jsx("div", { className: "flex flex-wrap items-center gap-2 text-xs font-mono", children: [
                                'Goal Ingestion',
                                'CPM Planning',
                                'Tool Selection',
                                'Capability Check',
                                'Credential Vault',
                                'Policy Gate',
                                'Risk Scoring',
                                'Simulation Sandbox',
                                'Execution Dispatch',
                                'Verification Cert',
                                'Saga Rollback',
                                'Audit Chain',
                            ].map((step, idx) => (_jsxs("div", { className: "flex items-center gap-2", children: [_jsxs("span", { className: "px-3 py-1.5 rounded-lg bg-purple-950/60 border border-purple-700/50 text-purple-200", children: [idx + 1, ". ", step] }), idx < 11 && _jsx("span", { className: "text-slate-600 font-bold", children: "\u2192" })] }, step))) }) })] }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-3 gap-6", children: [_jsxs(Card, { className: "lg:col-span-1 bg-slate-900/60 border-slate-800", children: [_jsx(CardHeader, { children: _jsxs(CardTitle, { className: "text-base text-white flex items-center gap-2", children: [_jsx(Terminal, { className: "w-4 h-4 text-purple-400" }), "Direct Goal Dispatcher"] }) }), _jsxs(CardContent, { className: "space-y-3", children: [_jsx("p", { className: "text-xs text-slate-400", children: "Trigger autonomous missions with automatic Critical Path DAG compilation and safety simulation:" }), _jsxs("div", { className: "space-y-2", children: [_jsx(Button, { variant: "outline", className: "w-full justify-start text-xs text-left", onClick: () => handleQuickExecute('Deploy autonomous hotfix to canary and verify'), disabled: executingQuickGoal, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(Play, { className: "w-3.5 h-3.5 text-purple-400" }), "K8s Canary Hotfix & Slack Broadcast"] }) }), _jsx(Button, { variant: "outline", className: "w-full justify-start text-xs text-left", onClick: () => handleQuickExecute('Issue monthly customer invoice and store S3 receipt'), disabled: executingQuickGoal, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(Play, { className: "w-3.5 h-3.5 text-emerald-400" }), "Stripe Customer Invoicing & S3 Vault"] }) }), _jsx(Button, { variant: "outline", className: "w-full justify-start text-xs text-left", onClick: () => handleQuickExecute('Scrape portal status table and persist to DB'), disabled: executingQuickGoal, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(Play, { className: "w-3.5 h-3.5 text-cyan-400" }), "Playwright Web Scrape & SQL Store"] }) })] })] })] }), _jsxs(Card, { className: "lg:col-span-2 bg-slate-900/60 border-slate-800", children: [_jsx(CardHeader, { children: _jsxs(CardTitle, { className: "text-base text-white flex items-center gap-2", children: [_jsx(Activity, { className: "w-4 h-4 text-emerald-400" }), "Recent Mission Executions"] }) }), _jsx(CardContent, { children: recentMissions.length === 0 ? (_jsx("div", { className: "text-center py-8 text-slate-500 text-sm", children: "No recent missions found. Launch a mission above to observe real-time telemetry." })) : (_jsx("div", { className: "space-y-3", children: recentMissions.slice(0, 4).map((m) => (_jsxs("div", { className: "p-3 bg-slate-800/40 border border-slate-700/50 rounded-lg flex items-center justify-between", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-sm font-semibold text-white", children: m.goal }), _jsx(Badge, { variant: m.status === 'completed'
                                                                    ? 'success'
                                                                    : m.status === 'executing'
                                                                        ? 'intelligence'
                                                                        : 'warning', children: m.status })] }), _jsxs("p", { className: "text-xs text-slate-400 mt-1", children: ["ID: ", m.mission_id, " \u2022 Steps: ", m.steps.length, " \u2022 Duration: ", m.total_execution_time_ms, "ms"] })] }), _jsxs(Badge, { variant: "outline", children: [m.risk_level, " risk"] })] }, m.mission_id))) })) })] })] })] }));
};
