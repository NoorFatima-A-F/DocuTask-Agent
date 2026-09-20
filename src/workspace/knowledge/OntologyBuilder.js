import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Layers, Plus } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
export const OntologyBuilder = () => {
    const [conceptName, setConceptName] = useState('');
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { children: [_jsxs("h1", { className: "text-2xl font-bold text-slate-100 flex items-center gap-2", children: [_jsx(Layers, { className: "w-7 h-7 text-cyan-400" }), "Organizational Ontology & Concept Builder"] }), _jsx("p", { className: "text-slate-400 text-sm mt-1", children: "Define custom business concepts, relational rules, and semantic hierarchy for agent reasoning." })] }), _jsxs(Card, { className: "p-5 bg-slate-900/60 border-slate-800 space-y-4", children: [_jsx("h2", { className: "text-base font-semibold text-slate-200", children: "Add New Business Entity" }), _jsxs("div", { className: "flex gap-3", children: [_jsx("input", { value: conceptName, onChange: (e) => setConceptName(e.target.value), placeholder: "e.g., Enterprise SLA Tier-1 Protocol", className: "flex-1 px-3 py-2 bg-slate-800/80 border border-slate-700 rounded-lg text-slate-200 text-sm focus:outline-none focus:border-cyan-500" }), _jsx(Button, { variant: "intelligence", children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(Plus, { className: "w-4 h-4" }), "Add Concept Node"] }) })] })] })] }));
};
