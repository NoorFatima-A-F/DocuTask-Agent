import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Target, RefreshCw } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { cognitiveApiClient } from '../../services/cognitiveApiClient';
export const DecisionIntelligenceExplorer = () => {
    const [decisions, setDecisions] = useState([]);
    const loadData = async () => {
        const data = await cognitiveApiClient.listDecisions();
        setDecisions(data);
    };
    useEffect(() => {
        loadData();
    }, []);
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex justify-between items-center", children: [_jsxs("div", { children: [_jsxs("h1", { className: "text-2xl font-bold text-slate-100 flex items-center gap-2", children: [_jsx(Target, { className: "w-7 h-7 text-indigo-400" }), "Enterprise Decision Intelligence Explorer"] }), _jsx("p", { className: "text-slate-400 text-sm mt-1", children: "Tracks autonomous decision objects, reasoning rationales, alternatives, and verifies expected vs. actual outcomes." })] }), _jsx(Button, { variant: "outline", onClick: loadData, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RefreshCw, { className: "w-4 h-4" }), "Refresh"] }) })] }), _jsx("div", { className: "space-y-4", children: decisions.map((dec) => (_jsxs(Card, { className: "p-5 bg-slate-900/60 border-slate-800 space-y-4", children: [_jsxs("div", { className: "flex justify-between items-start", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2 mb-1", children: [_jsxs(Badge, { variant: "outline", className: "text-indigo-400 border-indigo-500/30", children: ["Confidence: ", (dec.confidence_score * 100).toFixed(0), "%"] }), _jsx(Badge, { variant: dec.outcome_matched ? 'success' : 'warning', children: dec.outcome_matched ? 'Outcome Calibrated & Matched' : 'Pending Verification' })] }), _jsx("h3", { className: "text-lg font-semibold text-slate-200", children: dec.decision_topic })] }), _jsx("span", { className: "text-xs font-mono text-slate-400", children: dec.id })] }), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-4 text-xs", children: [_jsxs("div", { className: "p-3 bg-slate-800/40 rounded border border-slate-700/60 space-y-1", children: [_jsx("span", { className: "font-semibold text-slate-400 uppercase", children: "Chosen Action:" }), _jsx("p", { className: "text-slate-200 font-medium", children: dec.chosen_action }), _jsxs("p", { className: "text-slate-400 mt-2", children: ["Rationale: ", dec.reasoning_rationale] })] }), _jsxs("div", { className: "p-3 bg-slate-800/40 rounded border border-slate-700/60 space-y-1", children: [_jsx("span", { className: "font-semibold text-slate-400 uppercase", children: "Expected vs Actual:" }), _jsxs("p", { className: "text-emerald-400", children: ["Expected: ", JSON.stringify(dec.expected_outcome)] }), _jsxs("p", { className: "text-cyan-400", children: ["Actual: ", JSON.stringify(dec.actual_outcome || 'Observing live metrics...')] })] })] })] }, dec.id))) })] }));
};
