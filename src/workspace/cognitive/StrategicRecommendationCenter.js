import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Sparkles, RefreshCw } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { cognitiveApiClient } from '../../services/cognitiveApiClient';
export const StrategicRecommendationCenter = () => {
    const [recommendations, setRecommendations] = useState([]);
    const loadData = async () => {
        const data = await cognitiveApiClient.getRecommendations();
        setRecommendations(data);
    };
    useEffect(() => {
        loadData();
    }, []);
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex justify-between items-center", children: [_jsxs("div", { children: [_jsxs("h1", { className: "text-2xl font-bold text-slate-100 flex items-center gap-2", children: [_jsx(Sparkles, { className: "w-7 h-7 text-indigo-400" }), "Executive Strategic Recommendation Center"] }), _jsx("p", { className: "text-slate-400 text-sm mt-1", children: "Synthesizes weekly executive recommendations on Automation, Risk Prevention, Model Upgrades, and Budgeting." })] }), _jsx(Button, { variant: "outline", onClick: loadData, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RefreshCw, { className: "w-4 h-4" }), "Refresh"] }) })] }), _jsx("div", { className: "space-y-4", children: recommendations.map((rec) => (_jsxs(Card, { className: "p-5 bg-slate-900/60 border-slate-800 space-y-3", children: [_jsxs("div", { className: "flex justify-between items-start", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx(Badge, { variant: "outline", className: "text-indigo-400 border-indigo-500/30", children: rec.category }), _jsxs(Badge, { variant: rec.urgency === 'HIGH' ? 'warning' : 'info', children: [rec.urgency, " Urgency"] })] }), _jsx("span", { className: "text-xs font-mono text-slate-500", children: rec.id })] }), _jsx("h3", { className: "text-base font-semibold text-slate-100", children: rec.title }), _jsx("p", { className: "text-xs text-slate-300 bg-slate-800/40 p-3 rounded border border-slate-700/50", children: rec.description }), _jsx("div", { className: "pt-2 border-t border-slate-800 flex justify-between items-center text-xs text-emerald-400 font-mono", children: _jsxs("span", { children: ["Projected Impact: ", rec.projected_business_impact] }) })] }, rec.id))) })] }));
};
