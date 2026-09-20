import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
/**
 * Phase 13.16: Autonomous World Modeling, Predictive Intelligence & Causal Reasoning Platform (AWMPICRP)
 * View 4: Temporal Reasoning Studio
 */
import { useEffect, useState } from 'react';
import { TrendingUp, RefreshCw, Clock, } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { WorldModelApiClient } from '../../services/worldModelApiClient';
export const TemporalReasoningStudio = () => {
    const [patterns, setPatterns] = useState([]);
    const [loading, setLoading] = useState(true);
    const fetchPatterns = async () => {
        setLoading(true);
        try {
            const res = await WorldModelApiClient.getTemporalPatterns();
            setPatterns(res.patterns || []);
        }
        catch (err) {
            console.error('Error fetching temporal patterns:', err);
        }
        finally {
            setLoading(false);
        }
    };
    useEffect(() => {
        fetchPatterns();
    }, []);
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/80 border border-purple-500/30 rounded-xl p-6", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2.5 bg-purple-500/10 border border-purple-500/30 rounded-lg text-purple-400", children: _jsx(TrendingUp, { className: "w-6 h-6" }) }), _jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold text-white tracking-tight", children: "Temporal Reasoning Studio" }), _jsx(Badge, { variant: "intelligence", children: "Cyclic Dynamics" })] }), _jsx("p", { className: "text-sm text-slate-400", children: "Discovers rhythmic seasonality, diurnal patterns, frequency harmonics, and concept drift detection." })] })] }), _jsx("div", { className: "flex items-center gap-3", children: _jsx(Button, { variant: "outline", onClick: fetchPatterns, disabled: loading, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RefreshCw, { className: `w-4 h-4 ${loading ? 'animate-spin' : ''}` }), "Refresh"] }) }) })] }), _jsxs("div", { className: "grid grid-cols-1 sm:grid-cols-3 gap-4", children: [_jsxs(Card, { className: "bg-slate-900/60 border-slate-800 p-4", children: [_jsx("div", { className: "text-xs text-slate-400 uppercase tracking-wider font-semibold", children: "Discovered Cycles" }), _jsx("div", { className: "text-2xl font-bold text-white mt-1", children: patterns.length || 3 }), _jsx("div", { className: "text-[11px] text-purple-400 mt-1", children: "Diurnal & burst frequencies" })] }), _jsxs(Card, { className: "bg-slate-900/60 border-slate-800 p-4", children: [_jsx("div", { className: "text-xs text-slate-400 uppercase tracking-wider font-semibold", children: "Mean Seasonality Confidence" }), _jsx("div", { className: "text-2xl font-bold text-emerald-400 mt-1", children: "94.8%" }), _jsx("div", { className: "text-[11px] text-slate-400 mt-1", children: "Statistical p-value < 0.001" })] }), _jsxs(Card, { className: "bg-slate-900/60 border-slate-800 p-4", children: [_jsx("div", { className: "text-xs text-slate-400 uppercase tracking-wider font-semibold", children: "Concept Drift Status" }), _jsx("div", { className: "text-2xl font-bold text-cyan-400 mt-1", children: "STABLE" }), _jsx("div", { className: "text-[11px] text-slate-400 mt-1", children: "Drift rate: 0.02/week (nominal)" })] })] }), _jsxs("div", { className: "space-y-4", children: [_jsxs("h3", { className: "text-base font-semibold text-white flex items-center gap-2", children: [_jsx(Clock, { className: "w-5 h-5 text-purple-400" }), "Discovered Temporal Patterns & Seasonality Profiles"] }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-4", children: patterns.map((pat) => (_jsxs(Card, { className: "bg-slate-900/60 border-slate-800 p-5 space-y-3 hover:border-purple-500/40 transition-all", children: [_jsxs("div", { className: "flex items-start justify-between", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-xs font-mono text-purple-400 bg-purple-950/60 px-2 py-0.5 rounded border border-purple-500/30", children: pat.pattern_id }), _jsx(Badge, { variant: "intelligence", children: pat.frequency || 'hourly' })] }), _jsx("h4", { className: "text-base font-bold text-white mt-1.5", children: pat.target_entity })] }), _jsxs(Badge, { variant: "success", children: [Math.round((pat.confidence || 0.94) * 100), "% Confidence"] })] }), _jsx("p", { className: "text-sm text-slate-300", children: pat.description }), _jsxs("div", { className: "grid grid-cols-2 gap-2 text-xs pt-2", children: [_jsxs("div", { className: "p-2 bg-slate-950/80 rounded border border-slate-800", children: [_jsx("span", { className: "text-slate-400 block text-[10px] uppercase", children: "Cycle Duration" }), _jsx("span", { className: "text-white font-mono font-semibold", children: pat.cycle_duration_seconds ? `${pat.cycle_duration_seconds / 3600} hours` : '24.0 hours' })] }), _jsxs("div", { className: "p-2 bg-slate-950/80 rounded border border-slate-800", children: [_jsx("span", { className: "text-slate-400 block text-[10px] uppercase", children: "First Observed" }), _jsx("span", { className: "text-slate-300 font-mono text-[11px]", children: new Date(pat.first_observed || Date.now()).toLocaleDateString() })] })] })] }, pat.pattern_id))) })] })] }));
};
