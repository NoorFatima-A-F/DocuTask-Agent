import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { AILifecycleApiClient } from '../../services/aiLifecycleApiClient';
import { Wrench, CheckCircle2, Sparkles, Code2, Bot, RefreshCw } from 'lucide-react';
export const AgentBuilder = () => {
    const [templates, setTemplates] = useState([]);
    const [selectedTemplate, setSelectedTemplate] = useState(null);
    const [form, setForm] = useState({
        name: '',
        slug: '',
        category: 'AUTOMATION',
        system_prompt: '',
        tools: 'tool_erp_lookup, tool_ocr_extract',
        owner_email: 'admin@acmecorp.com',
    });
    const [submitting, setSubmitting] = useState(false);
    const [releasedAgent, setReleasedAgent] = useState(null);
    useEffect(() => {
        const load = async () => {
            const list = await AILifecycleApiClient.listTemplates();
            setTemplates(list);
            if (list.length > 0 && list[0]) {
                applyTemplate(list[0]);
            }
        };
        load();
    }, []);
    const applyTemplate = (t) => {
        setSelectedTemplate(t);
        setForm({
            name: t.name,
            slug: t.name.toLowerCase().replace(/[^a-z0-9]+/g, '-'),
            category: t.category,
            system_prompt: t.default_prompt,
            tools: t.default_tools.join(', '),
            owner_email: 'admin@acmecorp.com',
        });
    };
    const handleBuildAndDeploy = async (e) => {
        e.preventDefault();
        setSubmitting(true);
        const toolsArray = form.tools.split(',').map((t) => t.trim()).filter(Boolean);
        const res = await fetch('/api/v1/ai-lifecycle/full-release', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                tenant_id: 'tenant_acme_corp',
                organization_id: 'org_acme_americas',
                workspace_id: 'ws_acme_invoicing',
                name: form.name,
                slug: form.slug,
                category: form.category,
                owner_id: 'usr_acme_admin',
                owner_email: form.owner_email,
                system_prompt: form.system_prompt,
                tools: toolsArray,
                connectors: ['conn_acme_sap'],
            }),
        });
        if (res.ok) {
            const data = await res.json();
            setReleasedAgent(data);
        }
        setSubmitting(false);
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsx("div", { className: "flex items-center justify-between", children: _jsxs("div", { children: [_jsxs("h1", { className: "text-2xl font-bold text-white flex items-center gap-3", children: [_jsx(Wrench, { className: "w-7 h-7 text-indigo-400" }), "AI Application Builder & Starter Studio"] }), _jsx("p", { className: "text-sm text-slate-400 mt-1", children: "Scaffold, configure prompts, bind tools, and trigger turnkey CI/CD release pipelines." })] }) }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-3 gap-4", children: templates.map((tmpl) => (_jsxs("div", { onClick: () => applyTemplate(tmpl), className: `p-4 rounded-xl border cursor-pointer transition ${selectedTemplate?.template_id === tmpl.template_id
                        ? 'bg-indigo-950/40 border-indigo-500 shadow-lg'
                        : 'bg-slate-900/80 border-slate-800 hover:border-slate-700'}`, children: [_jsxs("div", { className: "flex items-center justify-between mb-2", children: [_jsx(Badge, { variant: "intelligence", children: tmpl.category }), _jsx(Sparkles, { className: "w-4 h-4 text-indigo-400" })] }), _jsx("span", { className: "text-sm font-semibold text-white block", children: tmpl.name }), _jsx("p", { className: "text-xs text-slate-400 mt-1 line-clamp-2", children: tmpl.description })] }, tmpl.template_id))) }), _jsxs(Card, { className: "bg-slate-900/80 border-slate-800", children: [_jsx(CardHeader, { children: _jsxs(CardTitle, { className: "text-base text-white flex items-center gap-2", children: [_jsx(Code2, { className: "w-5 h-5 text-emerald-400" }), " Agent Configuration & CI/CD Release"] }) }), _jsxs(CardContent, { children: [_jsxs("form", { onSubmit: handleBuildAndDeploy, className: "space-y-4", children: [_jsxs("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-4", children: [_jsxs("div", { children: [_jsx("label", { className: "text-xs text-slate-300 font-medium block mb-1", children: "Application Name" }), _jsx("input", { type: "text", required: true, className: "w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded text-sm text-white focus:outline-none focus:border-indigo-500", value: form.name, onChange: (e) => setForm({ ...form, name: e.target.value }) })] }), _jsxs("div", { children: [_jsx("label", { className: "text-xs text-slate-300 font-medium block mb-1", children: "Category" }), _jsxs("select", { className: "w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded text-sm text-white focus:outline-none focus:border-indigo-500", value: form.category, onChange: (e) => setForm({ ...form, category: e.target.value }), children: [_jsx("option", { value: "FINANCIAL_AUDIT", children: "FINANCIAL_AUDIT" }), _jsx("option", { value: "COMPLIANCE", children: "COMPLIANCE" }), _jsx("option", { value: "LEGAL_ANALYSIS", children: "LEGAL_ANALYSIS" }), _jsx("option", { value: "AUTOMATION", children: "AUTOMATION" }), _jsx("option", { value: "EXTRACTION", children: "EXTRACTION" }), _jsx("option", { value: "RESEARCH", children: "RESEARCH" })] })] })] }), _jsxs("div", { children: [_jsx("label", { className: "text-xs text-slate-300 font-medium block mb-1", children: "System Prompt Directives" }), _jsx("textarea", { rows: 4, required: true, className: "w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded text-sm text-white font-mono focus:outline-none focus:border-indigo-500", value: form.system_prompt, onChange: (e) => setForm({ ...form, system_prompt: e.target.value }) })] }), _jsxs("div", { children: [_jsx("label", { className: "text-xs text-slate-300 font-medium block mb-1", children: "Bound Tools (Comma separated)" }), _jsx("input", { type: "text", className: "w-full px-3 py-2 bg-slate-800 border border-slate-700 rounded text-sm text-white font-mono", value: form.tools, onChange: (e) => setForm({ ...form, tools: e.target.value }) })] }), _jsx("div", { className: "flex justify-end pt-3 border-t border-slate-800", children: _jsx(Button, { variant: "intelligence", type: "submit", disabled: submitting, children: _jsxs("span", { className: "flex items-center gap-2", children: [submitting ? _jsx(RefreshCw, { className: "w-4 h-4 animate-spin" }) : _jsx(Bot, { className: "w-4 h-4" }), "Execute DevSecOps Release Pipeline"] }) }) })] }), releasedAgent && (_jsxs("div", { className: "mt-6 p-4 rounded-lg bg-emerald-950/30 border border-emerald-800/50 space-y-2", children: [_jsxs("div", { className: "flex items-center gap-2 text-emerald-400 font-bold text-sm", children: [_jsx(CheckCircle2, { className: "w-5 h-5" }), " Full Lifecycle Release Successful!"] }), _jsxs("div", { className: "text-xs text-slate-300 grid grid-cols-2 gap-2 font-mono", children: [_jsxs("div", { children: ["Agent ID: ", releasedAgent.agent.agent_id] }), _jsxs("div", { children: ["State: ", releasedAgent.agent.lifecycle_state] }), _jsxs("div", { children: ["Test Quality Score: ", releasedAgent.test_result.accuracy_score] }), _jsxs("div", { children: ["Security Score: ", releasedAgent.security_scan.security_score, "/100"] })] })] }))] })] })] }));
};
