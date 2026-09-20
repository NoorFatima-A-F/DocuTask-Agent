import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
/**
 * Phase 13.16: Autonomous World Modeling, Predictive Intelligence & Causal Reasoning Platform (AWMPICRP)
 * View 12: World Evolution Timeline & Event Stream
 */
import { useEffect, useState } from 'react';
import { Clock, RefreshCw, Activity, Sparkles, Zap, Brain, GitBranch, Flame, } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { WorldModelApiClient } from '../../services/worldModelApiClient';
export const WorldEvolutionTimeline = () => {
    const [events, setEvents] = useState([]);
    const [memories, setMemories] = useState([]);
    const [loading, setLoading] = useState(true);
    const fetchData = async () => {
        setLoading(true);
        try {
            const [evRes, memRes] = await Promise.all([
                WorldModelApiClient.getEvents(50),
                WorldModelApiClient.getMemoryRecords(),
            ]);
            setEvents(evRes.events || []);
            setMemories(memRes.records || []);
        }
        catch (err) {
            console.error('Error fetching evolution timeline data:', err);
        }
        finally {
            setLoading(false);
        }
    };
    useEffect(() => {
        fetchData();
    }, []);
    const getEventIcon = (type) => {
        if (type.includes('knowledge'))
            return Brain;
        if (type.includes('causal'))
            return GitBranch;
        if (type.includes('hypothesis'))
            return Flame;
        if (type.includes('scenario') || type.includes('counterfactual'))
            return Sparkles;
        return Zap;
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/80 border border-emerald-500/30 rounded-xl p-6", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2.5 bg-emerald-500/10 border border-emerald-500/30 rounded-lg text-emerald-400", children: _jsx(Clock, { className: "w-6 h-6" }) }), _jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold text-white tracking-tight", children: "World Evolution Timeline" }), _jsx(Badge, { variant: "intelligence", children: "Memory Consolidation & Audit" })] }), _jsx("p", { className: "text-sm text-slate-400", children: "Audit trail of continuous world updates, cognitive learning cycles, and multi-tier memory retention." })] })] }), _jsx("div", { className: "flex items-center gap-3", children: _jsx(Button, { variant: "outline", onClick: fetchData, disabled: loading, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RefreshCw, { className: `w-4 h-4 ${loading ? 'animate-spin' : ''}` }), "Refresh"] }) }) })] }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-3 gap-6", children: [_jsxs("div", { className: "lg:col-span-2 space-y-4", children: [_jsxs("h3", { className: "text-base font-semibold text-white flex items-center gap-2", children: [_jsx(Activity, { className: "w-5 h-5 text-emerald-400" }), "Live World Model Event Stream (", events.length, ")"] }), _jsx("div", { className: "space-y-3", children: events.map((evt) => {
                                    const Icon = getEventIcon(evt.event_type);
                                    return (_jsxs("div", { className: "p-4 bg-slate-900/60 rounded-lg border border-slate-800 space-y-2 hover:border-slate-700 transition-all text-xs", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("div", { className: "p-1.5 bg-slate-800 rounded text-emerald-400", children: _jsx(Icon, { className: "w-4 h-4" }) }), _jsx("span", { className: "font-mono text-emerald-400 font-semibold", children: evt.event_type })] }), _jsx("span", { className: "text-[11px] text-slate-400", children: new Date(evt.timestamp || Date.now()).toLocaleTimeString() })] }), _jsx("pre", { className: "p-2.5 bg-slate-950/80 rounded border border-slate-800/80 font-mono text-[11px] text-slate-300 whitespace-pre-wrap overflow-x-auto", children: JSON.stringify(evt.payload || {}, null, 2) })] }, evt.event_id));
                                }) })] }), _jsxs("div", { className: "space-y-4", children: [_jsxs("h3", { className: "text-base font-semibold text-white flex items-center gap-2", children: [_jsx(Brain, { className: "w-5 h-5 text-purple-400" }), "Consolidated Cognitive Memory"] }), _jsx("div", { className: "space-y-3", children: memories.map((mem) => (_jsxs(Card, { className: "bg-slate-900/60 border-slate-800 p-4 space-y-2.5", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx(Badge, { variant: "intelligence", children: mem.tier }), _jsxs("span", { className: "text-[10px] text-slate-400 font-mono", children: ["Importance: ", Math.round((mem.importance_score || 0.9) * 100), "%"] })] }), _jsx("div", { className: "text-xs font-semibold text-slate-200", children: mem.content?.concept || mem.content?.lesson || JSON.stringify(mem.content) }), _jsxs("div", { className: "flex items-center justify-between text-[11px] text-slate-400 pt-1", children: [_jsxs("span", { children: ["Access Count: ", _jsx("strong", { className: "text-white", children: mem.access_count || 1 })] }), _jsx("div", { className: "flex gap-1", children: (mem.associations || ['world_model']).slice(0, 3).map((a, i) => (_jsx("span", { className: "px-1.5 py-0.5 rounded bg-slate-800 text-[10px] text-slate-300", children: a }, i))) })] })] }, mem.record_id))) })] })] })] }));
};
