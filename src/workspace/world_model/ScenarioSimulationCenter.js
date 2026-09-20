import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
/**
 * Phase 13.16: Autonomous World Modeling, Predictive Intelligence & Causal Reasoning Platform (AWMPICRP)
 * View 7: Scenario Simulation Center
 */
import { useEffect, useState } from 'react';
import { Sparkles, RefreshCw, Play, } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { WorldModelApiClient } from '../../services/worldModelApiClient';
export const ScenarioSimulationCenter = () => {
    const [branches, setBranches] = useState([]);
    const [loading, setLoading] = useState(true);
    const [simulating, setSimulating] = useState(false);
    const [selectedBranch, setSelectedBranch] = useState(null);
    const fetchScenarios = async () => {
        setLoading(true);
        try {
            const res = await WorldModelApiClient.getScenarios();
            setBranches(res.branches || []);
            if (res.branches && res.branches.length > 0 && !selectedBranch) {
                setSelectedBranch(res.branches[0] || null);
            }
        }
        catch (err) {
            console.error('Error fetching scenarios:', err);
        }
        finally {
            setLoading(false);
        }
    };
    useEffect(() => {
        fetchScenarios();
    }, []);
    const handleRunSim = async () => {
        setSimulating(true);
        try {
            await WorldModelApiClient.simulateScenarios({
                base_snapshot_id: 'snap-01',
                time_horizon_seconds: 86400,
            });
            await fetchScenarios();
        }
        catch (err) {
            console.error('Error simulating scenarios:', err);
        }
        finally {
            setSimulating(false);
        }
    };
    const getBranchBadge = (type) => {
        switch (type) {
            case 'best_case':
                return _jsx(Badge, { variant: "success", children: "Best Case" });
            case 'worst_case':
                return _jsx(Badge, { variant: "error", children: "Worst Case" });
            case 'black_swan':
                return _jsx(Badge, { variant: "warning", children: "Black Swan" });
            default:
                return _jsx(Badge, { variant: "intelligence", children: "Expected Case" });
        }
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/80 border border-blue-500/30 rounded-xl p-6", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2.5 bg-blue-500/10 border border-blue-500/30 rounded-lg text-blue-400", children: _jsx(Sparkles, { className: "w-6 h-6" }) }), _jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold text-white tracking-tight", children: "Scenario Simulation Center" }), _jsx(Badge, { variant: "intelligence", children: "Monte Carlo Branches" })] }), _jsx("p", { className: "text-sm text-slate-400", children: "Generates stochastic multi-branch futures: Baseline, Best Case, Worst Case, Expected, and Black Swan outlier conditions." })] })] }), _jsxs("div", { className: "flex items-center gap-3", children: [_jsx(Button, { variant: "outline", onClick: fetchScenarios, disabled: loading, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RefreshCw, { className: `w-4 h-4 ${loading ? 'animate-spin' : ''}` }), "Refresh"] }) }), _jsx(Button, { variant: "intelligence", onClick: handleRunSim, disabled: simulating, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(Play, { className: "w-4 h-4" }), simulating ? 'Simulating...' : 'Run Monte Carlo'] }) })] })] }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-3 gap-6", children: [_jsxs("div", { className: "space-y-3", children: [_jsxs("h3", { className: "text-xs font-semibold uppercase text-slate-400 tracking-wider", children: ["Simulated Branches (", branches.length, ")"] }), _jsx("div", { className: "space-y-2.5", children: branches.map((b) => {
                                    const isSelected = selectedBranch?.branch_id === b.branch_id;
                                    return (_jsxs("div", { onClick: () => setSelectedBranch(b), className: `p-4 rounded-lg border cursor-pointer transition-all ${isSelected
                                            ? 'bg-blue-950/40 border-blue-500/60 shadow-lg'
                                            : 'bg-slate-900/60 border-slate-800 hover:border-slate-700'}`, children: [_jsxs("div", { className: "flex items-center justify-between mb-2", children: [_jsx("span", { className: "text-xs font-mono text-blue-400", children: b.branch_id }), getBranchBadge(b.branch_type)] }), _jsxs("div", { className: "flex items-center justify-between text-xs text-slate-400", children: [_jsxs("span", { children: ["Probability: ", _jsxs("strong", { className: "text-white", children: [Math.round((b.probability || 0.6) * 100), "%"] })] }), _jsxs("span", { children: ["Divergence: ", _jsx("strong", { className: "text-cyan-400", children: b.state_divergence_delta })] })] })] }, b.branch_id));
                                }) })] }), _jsx("div", { className: "lg:col-span-2", children: selectedBranch ? (_jsxs(Card, { className: "bg-slate-900/80 border-slate-800 p-6 space-y-5", children: [_jsxs("div", { className: "flex items-start justify-between", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-xs font-mono text-blue-400 bg-blue-950/60 px-2 py-0.5 rounded border border-blue-500/30", children: selectedBranch.branch_id }), getBranchBadge(selectedBranch.branch_type)] }), _jsxs("h2", { className: "text-xl font-bold text-white mt-1", children: [selectedBranch.branch_type.toUpperCase().replace('_', ' '), " SCENARIO TRAJECTORY"] })] }), _jsxs("div", { className: "text-right", children: [_jsx("div", { className: "text-xs text-slate-400", children: "Branch Probability" }), _jsxs("div", { className: "text-2xl font-bold text-blue-400", children: [Math.round((selectedBranch.probability || 0.65) * 100), "%"] })] })] }), _jsxs("div", { className: "space-y-2", children: [_jsx("div", { className: "text-xs font-semibold text-slate-300 uppercase tracking-wider", children: "Critical Projected Events" }), _jsx("div", { className: "space-y-1.5", children: (selectedBranch.critical_events || []).map((evt, idx) => (_jsxs("div", { className: "p-2.5 bg-slate-950/80 rounded border border-slate-800 flex items-center gap-2 text-xs text-slate-200", children: [_jsx("span", { className: "text-blue-400 font-bold", children: "\u2022" }), _jsx("span", { children: evt })] }, idx))) })] }), _jsxs("div", { className: "space-y-2", children: [_jsx("div", { className: "text-xs font-semibold text-slate-300 uppercase tracking-wider", children: "Projected World State Variables" }), _jsx("pre", { className: "p-3 bg-slate-950/80 rounded border border-slate-800 font-mono text-xs text-cyan-300 whitespace-pre-wrap overflow-x-auto", children: JSON.stringify(selectedBranch.projected_state || {}, null, 2) })] })] })) : (_jsx(Card, { className: "bg-slate-900/40 border-slate-800 p-12 text-center text-slate-500", children: "Select a scenario branch to inspect its projection." })) })] })] }));
};
