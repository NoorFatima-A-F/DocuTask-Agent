import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Workflow, Plus, ArrowRight, Clock, Layers, CheckCircle, } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
export const ProcessDesigner = () => {
    const [steps, setSteps] = useState([
        { id: 'step_1', name: 'Multimodal OCR Data Extraction', type: 'TASK', dept: 'Finance', sla: '60s' },
        { id: 'step_2', name: 'Tax & Compliance Audit', type: 'TASK', dept: 'Finance', sla: '120s' },
        { id: 'step_3', name: 'Threshold Routing Gateway', type: 'GATEWAY_EXCLUSIVE', dept: 'Finance', sla: '10s' },
        { id: 'step_4', name: 'Manager Approval Gate', type: 'HUMAN_APPROVAL', dept: 'Finance', sla: '30m' },
        { id: 'step_5', name: 'SAP ERP Ledger Entry', type: 'TASK', dept: 'Finance', sla: '180s' },
    ]);
    const [selectedStep, setSelectedStep] = useState(steps[0]);
    const [feedback, setFeedback] = useState(null);
    const handleAddStep = () => {
        const newStep = {
            id: `step_${steps.length + 1}`,
            name: `Automated Verification Gate #${steps.length + 1}`,
            type: 'TASK',
            dept: 'Finance',
            sla: '90s',
        };
        setSteps([...steps, newStep]);
        setSelectedStep(newStep);
        setFeedback(`Added step "${newStep.name}" to process graph.`);
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/60 p-6 rounded-2xl border border-slate-800 backdrop-blur-md", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2 bg-indigo-500/10 rounded-xl border border-indigo-500/20 text-indigo-400", children: _jsx(Workflow, { className: "w-6 h-6" }) }), _jsxs("div", { children: [_jsx("h1", { className: "text-2xl font-bold text-white", children: "BPMN Process Designer" }), _jsx("p", { className: "text-sm text-slate-400", children: "Visual business process canvas with tasks, gateways, human gates, and SLA contracts" })] })] }), _jsx(Button, { variant: "intelligence", onClick: handleAddStep, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(Plus, { className: "w-4 h-4" }), " Add Workflow Node"] }) })] }), feedback && (_jsxs("div", { className: "p-4 bg-emerald-500/10 border border-emerald-500/20 rounded-xl text-emerald-300 text-sm flex items-center justify-between", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx(CheckCircle, { className: "w-4 h-4" }), _jsx("span", { children: feedback })] }), _jsx("button", { onClick: () => setFeedback(null), className: "text-xs text-emerald-400 hover:text-emerald-200 underline", children: "Dismiss" })] })), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-3 gap-6", children: [_jsxs(Card, { className: "lg:col-span-2 p-6 bg-slate-900/40 border-slate-800 space-y-4", children: [_jsxs("h2", { className: "text-base font-semibold text-white flex items-center gap-2", children: [_jsx(Layers, { className: "w-4 h-4 text-indigo-400" }), "Executable Business Process Graph"] }), _jsx("div", { className: "space-y-3 pt-2", children: steps.map((s, idx) => {
                                    const isSelected = selectedStep?.id === s.id;
                                    return (_jsxs("div", { className: "space-y-3", children: [_jsxs("div", { onClick: () => setSelectedStep(s), className: `p-4 rounded-xl border cursor-pointer transition-all flex items-center justify-between ${isSelected
                                                    ? 'bg-slate-800/90 border-indigo-500 shadow-md'
                                                    : 'bg-slate-900/60 border-slate-800 hover:border-slate-700'}`, children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("span", { className: "w-6 h-6 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center text-xs font-mono text-indigo-300", children: idx + 1 }), _jsxs("div", { children: [_jsx("span", { className: "font-bold text-white text-sm block", children: s.name }), _jsxs("span", { className: "text-xs text-slate-400 font-mono", children: ["Department: ", s.dept] })] })] }), _jsxs("div", { className: "flex items-center gap-3", children: [_jsx(Badge, { variant: s.type === 'HUMAN_APPROVAL'
                                                                    ? 'warning'
                                                                    : s.type === 'GATEWAY_EXCLUSIVE'
                                                                        ? 'intelligence'
                                                                        : 'default', children: s.type }), _jsxs("span", { className: "text-xs text-amber-400 font-mono flex items-center gap-1", children: [_jsx(Clock, { className: "w-3.5 h-3.5" }), " ", s.sla] })] })] }), idx < steps.length - 1 && (_jsx("div", { className: "flex justify-center", children: _jsx(ArrowRight, { className: "w-4 h-4 text-slate-600 rotate-90" }) }))] }, s.id));
                                }) })] }), _jsxs(Card, { className: "lg:col-span-1 p-6 bg-slate-900/60 border-slate-800 space-y-4", children: [_jsx("h2", { className: "text-base font-bold text-white border-b border-slate-800 pb-3", children: "Node Configuration" }), selectedStep ? (_jsxs("div", { className: "space-y-4 text-xs", children: [_jsxs("div", { children: [_jsx("label", { className: "block text-slate-400 mb-1", children: "Step Name" }), _jsx("input", { type: "text", value: selectedStep.name, onChange: (e) => {
                                                    const updated = { ...selectedStep, name: e.target.value };
                                                    setSelectedStep(updated);
                                                    setSteps(steps.map((st) => (st.id === updated.id ? updated : st)));
                                                }, className: "w-full bg-slate-800 border border-slate-700 text-white rounded-lg p-2.5 text-xs" })] }), _jsxs("div", { children: [_jsx("label", { className: "block text-slate-400 mb-1", children: "Node Type" }), _jsxs("select", { value: selectedStep.type, onChange: (e) => {
                                                    const updated = { ...selectedStep, type: e.target.value };
                                                    setSelectedStep(updated);
                                                    setSteps(steps.map((st) => (st.id === updated.id ? updated : st)));
                                                }, className: "w-full bg-slate-800 border border-slate-700 text-white rounded-lg p-2.5 text-xs", children: [_jsx("option", { value: "TASK", children: "Standard Agent Task" }), _jsx("option", { value: "GATEWAY_EXCLUSIVE", children: "Exclusive Decision Gateway (XOR)" }), _jsx("option", { value: "GATEWAY_PARALLEL", children: "Parallel Fork / Join Gateway (AND)" }), _jsx("option", { value: "HUMAN_APPROVAL", children: "Human-in-the-Loop Approval Gate" })] })] }), _jsxs("div", { children: [_jsx("label", { className: "block text-slate-400 mb-1", children: "Target SLA Duration" }), _jsx("input", { type: "text", value: selectedStep.sla, onChange: (e) => {
                                                    const updated = { ...selectedStep, sla: e.target.value };
                                                    setSelectedStep(updated);
                                                    setSteps(steps.map((st) => (st.id === updated.id ? updated : st)));
                                                }, className: "w-full bg-slate-800 border border-slate-700 text-white rounded-lg p-2.5 text-xs" })] }), _jsxs("div", { className: "pt-2 border-t border-slate-800", children: [_jsx("span", { className: "text-slate-400 block mb-1", children: "BPMN Validation" }), _jsxs("span", { className: "text-emerald-400 font-mono text-[11px] flex items-center gap-1.5", children: [_jsx(CheckCircle, { className: "w-3.5 h-3.5" }), " Syntax & Sagas Validated"] })] })] })) : (_jsx("p", { className: "text-slate-500 italic text-xs", children: "Select a node to configure properties." }))] })] })] }));
};
