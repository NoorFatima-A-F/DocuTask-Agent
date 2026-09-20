import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { FileCheck, Play, Layers, } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
export const DecisionRulesStudio = () => {
    const [testAmount, setTestAmount] = useState(45000);
    const [testTier, setTestTier] = useState('TIER_1');
    const [evaluatedAction, setEvaluatedAction] = useState('ROUTE_MANAGER_APPROVAL');
    const handleEvaluate = () => {
        if (testAmount < 1000 && testTier === 'TIER_1') {
            setEvaluatedAction('AUTO_APPROVE (Micro-invoice Policy)');
        }
        else if (testAmount >= 50000) {
            setEvaluatedAction('ROUTE_CFO_APPROVAL (Executive Threshold)');
        }
        else {
            setEvaluatedAction('ROUTE_MANAGER_APPROVAL (Standard Review)');
        }
    };
    const rules = [
        { id: 'rule_1', name: 'Micro Invoice Auto-Approval', condition: 'amount < $1,000 & Tier-1', action: 'AUTO_APPROVE', priority: 1 },
        { id: 'rule_2', name: 'Standard Manager Review', condition: '$1,000 <= amount < $50,000', action: 'ROUTE_MANAGER_APPROVAL', priority: 2 },
        { id: 'rule_3', name: 'Executive CFO Sign-off', condition: 'amount >= $50,000', action: 'ROUTE_CFO_APPROVAL', priority: 3 },
    ];
    return (_jsxs("div", { className: "space-y-6", children: [_jsx("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/60 p-6 rounded-2xl border border-slate-800 backdrop-blur-md", children: _jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2 bg-indigo-500/10 rounded-xl border border-indigo-500/20 text-indigo-400", children: _jsx(FileCheck, { className: "w-6 h-6" }) }), _jsxs("div", { children: [_jsx("h1", { className: "text-2xl font-bold text-white", children: "Enterprise Decision Rules Studio" }), _jsx("p", { className: "text-sm text-slate-400", children: "DMN-style decision tables, conditional routing rules, and financial approval thresholds" })] })] }) }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-3 gap-6", children: [_jsxs(Card, { className: "lg:col-span-2 p-6 bg-slate-900/40 border-slate-800 space-y-4", children: [_jsxs("h2", { className: "text-base font-semibold text-white flex items-center gap-2", children: [_jsx(Layers, { className: "w-4 h-4 text-indigo-400" }), "Decision Table: Invoice Financial Approval Policy"] }), _jsx("div", { className: "overflow-x-auto", children: _jsxs("table", { className: "w-full text-left text-xs font-mono text-slate-300", children: [_jsx("thead", { className: "bg-slate-800/60 uppercase text-slate-400 border-b border-slate-700", children: _jsxs("tr", { children: [_jsx("th", { className: "py-3 px-4", children: "Priority" }), _jsx("th", { className: "py-3 px-4", children: "Rule Name" }), _jsx("th", { className: "py-3 px-4", children: "Condition Expression" }), _jsx("th", { className: "py-3 px-4", children: "Action Decision" })] }) }), _jsx("tbody", { className: "divide-y divide-slate-800/60", children: rules.map((r) => (_jsxs("tr", { className: "hover:bg-slate-800/30", children: [_jsxs("td", { className: "py-3 px-4 text-indigo-400 font-bold", children: ["#", r.priority] }), _jsx("td", { className: "py-3 px-4 font-sans font-medium text-white", children: r.name }), _jsx("td", { className: "py-3 px-4 text-slate-300", children: r.condition }), _jsx("td", { className: "py-3 px-4", children: _jsx(Badge, { variant: "intelligence", children: r.action }) })] }, r.id))) })] }) })] }), _jsxs(Card, { className: "lg:col-span-1 p-6 bg-slate-900/60 border-slate-800 space-y-4", children: [_jsx("h2", { className: "text-base font-bold text-white border-b border-slate-800 pb-3", children: "Interactive Policy Sandbox" }), _jsxs("div", { className: "space-y-3 text-xs", children: [_jsxs("div", { children: [_jsx("label", { className: "block text-slate-400 mb-1", children: "Invoice Amount ($)" }), _jsx("input", { type: "number", value: testAmount, onChange: (e) => setTestAmount(Number(e.target.value)), className: "w-full bg-slate-800 border border-slate-700 text-white rounded-lg p-2.5 text-xs" })] }), _jsxs("div", { children: [_jsx("label", { className: "block text-slate-400 mb-1", children: "Vendor Tier" }), _jsxs("select", { value: testTier, onChange: (e) => setTestTier(e.target.value), className: "w-full bg-slate-800 border border-slate-700 text-white rounded-lg p-2.5 text-xs", children: [_jsx("option", { value: "TIER_1", children: "Tier 1 (Strategic Partner)" }), _jsx("option", { value: "TIER_2", children: "Tier 2 (Standard Vendor)" }), _jsx("option", { value: "TIER_3", children: "Tier 3 (New / High Risk)" })] })] }), _jsx(Button, { variant: "intelligence", className: "w-full", onClick: handleEvaluate, children: _jsxs("span", { className: "flex items-center justify-center gap-2", children: [_jsx(Play, { className: "w-4 h-4" }), " Evaluate Decision"] }) }), _jsxs("div", { className: "pt-3 border-t border-slate-800", children: [_jsx("span", { className: "text-slate-400 block mb-1", children: "Evaluated Action:" }), _jsx("div", { className: "p-3 bg-slate-800/60 rounded-xl border border-indigo-500/40 font-mono text-emerald-300 font-bold text-xs", children: evaluatedAction })] })] })] })] })] }));
};
