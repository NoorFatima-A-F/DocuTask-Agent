import { jsx as _jsx, jsxs as _jsxs, Fragment as _Fragment } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { Zap, Search, RotateCw, } from 'lucide-react';
import { executionPlatformApiClient } from '../../services/executionPlatformApiClient';
export const ToolRegistryExplorer = () => {
    const [tools, setTools] = useState([]);
    const [selectedTool, setSelectedTool] = useState(null);
    const [categoryFilter, setCategoryFilter] = useState('');
    const [searchQuery, setSearchQuery] = useState('');
    const [loading, setLoading] = useState(true);
    const loadTools = async () => {
        try {
            setLoading(true);
            const res = await executionPlatformApiClient.listTools({
                category: categoryFilter || undefined,
                search: searchQuery || undefined,
            });
            setTools(res.tools || []);
            if (res.tools && res.tools.length > 0 && !selectedTool) {
                setSelectedTool(res.tools[0] || null);
            }
        }
        catch (err) {
            console.error('Failed to load tools:', err);
        }
        finally {
            setLoading(false);
        }
    };
    useEffect(() => {
        loadTools();
    }, [categoryFilter]);
    const handleSearchSubmit = (e) => {
        e.preventDefault();
        loadTools();
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-slate-900/60 p-6 rounded-2xl border border-slate-800", children: [_jsxs("div", { children: [_jsxs("h1", { className: "text-xl font-bold text-white flex items-center gap-2", children: [_jsx(Zap, { className: "w-5 h-5 text-amber-400" }), "Universal Tool Registry & Capability Taxonomy"] }), _jsx("p", { className: "text-slate-400 text-sm mt-1", children: "Dynamic discovery, JSON Schema contract validation, latency tracking & compensation bindings" })] }), _jsx(Button, { variant: "outline", onClick: loadTools, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RotateCw, { className: "w-4 h-4" }), "Refresh"] }) })] }), _jsxs("div", { className: "flex flex-col md:flex-row gap-3", children: [_jsxs("form", { onSubmit: handleSearchSubmit, className: "flex-1 flex gap-2", children: [_jsxs("div", { className: "relative flex-1", children: [_jsx(Search, { className: "w-4 h-4 text-slate-500 absolute left-3 top-3" }), _jsx("input", { type: "text", className: "w-full bg-slate-900 border border-slate-800 rounded-lg pl-9 pr-4 py-2 text-white text-sm focus:outline-none focus:border-purple-500", placeholder: "Search tools by name, tag or description...", value: searchQuery, onChange: (e) => setSearchQuery(e.target.value) })] }), _jsx(Button, { variant: "secondary", onClick: loadTools, children: "Search" })] }), _jsxs("select", { className: "bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-300 focus:outline-none focus:border-purple-500", value: categoryFilter, onChange: (e) => setCategoryFilter(e.target.value), children: [_jsx("option", { value: "", children: "All Categories" }), _jsx("option", { value: "code_repository", children: "Code Repositories (GitHub)" }), _jsx("option", { value: "communication", children: "Communication (Slack)" }), _jsx("option", { value: "infrastructure", children: "Infrastructure (K8s)" }), _jsx("option", { value: "cloud", children: "Cloud (AWS/GCP)" }), _jsx("option", { value: "database", children: "Database (PostgreSQL)" }), _jsx("option", { value: "payment_finance", children: "Payment & Finance (Stripe)" }), _jsx("option", { value: "browser_vision", children: "Browser Vision (Playwright)" })] })] }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-3 gap-6", children: [_jsxs(Card, { className: "lg:col-span-1 bg-slate-900/60 border-slate-800", children: [_jsx(CardHeader, { children: _jsxs(CardTitle, { className: "text-sm font-semibold text-white", children: ["Registered Tools (", tools.length, ")"] }) }), _jsx(CardContent, { className: "space-y-2 max-h-[600px] overflow-y-auto", children: loading && tools.length === 0 ? (_jsx("p", { className: "text-xs text-slate-500 py-4 text-center", children: "Loading tools..." })) : tools.map((t) => (_jsxs("div", { onClick: () => setSelectedTool(t), className: `p-3 rounded-lg border cursor-pointer transition-all ${selectedTool?.tool_id === t.tool_id
                                        ? 'bg-purple-950/40 border-purple-600'
                                        : 'bg-slate-800/40 border-slate-800 hover:border-slate-700'}`, children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-xs font-semibold text-white truncate max-w-[180px]", children: t.name }), _jsx(Badge, { variant: "outline", children: t.tool_type })] }), _jsxs("div", { className: "flex items-center justify-between mt-2 text-[11px] text-slate-400", children: [_jsxs("span", { className: "text-amber-400", children: ["Health: ", (t.health_score * 100).toFixed(0), "%"] }), _jsxs("span", { children: [t.average_latency_ms, "ms avg"] })] })] }, t.tool_id))) })] }), _jsxs(Card, { className: "lg:col-span-2 bg-slate-900/60 border-slate-800", children: [_jsx(CardHeader, { children: _jsxs("div", { className: "flex items-center justify-between", children: [_jsx(CardTitle, { className: "text-base text-white", children: selectedTool ? selectedTool.name : 'Select a Tool' }), selectedTool && (_jsxs(Badge, { variant: selectedTool.risk_level === 'low'
                                                ? 'success'
                                                : selectedTool.risk_level === 'medium'
                                                    ? 'warning'
                                                    : 'error', children: [selectedTool.risk_level.toUpperCase(), " RISK"] }))] }) }), _jsx(CardContent, { className: "space-y-6", children: selectedTool && (_jsxs(_Fragment, { children: [_jsx("p", { className: "text-sm text-slate-300", children: selectedTool.description }), _jsxs("div", { className: "grid grid-cols-2 sm:grid-cols-4 gap-3 p-3 bg-slate-950/60 rounded-lg border border-slate-800 text-xs", children: [_jsxs("div", { children: [_jsx("span", { className: "text-slate-500 block", children: "Rate Limit" }), _jsxs("span", { className: "text-slate-200 font-mono", children: [selectedTool.rate_limit_per_min, " req/min"] })] }), _jsxs("div", { children: [_jsx("span", { className: "text-slate-500 block", children: "Timeout" }), _jsxs("span", { className: "text-slate-200 font-mono", children: [selectedTool.timeout_seconds, "s"] })] }), _jsxs("div", { children: [_jsx("span", { className: "text-slate-500 block", children: "Total Calls" }), _jsx("span", { className: "text-slate-200 font-mono", children: selectedTool.total_calls })] }), _jsxs("div", { children: [_jsx("span", { className: "text-slate-500 block", children: "Compensation Tool" }), _jsx("span", { className: "text-purple-300 font-mono truncate block", children: selectedTool.compensation_tool_id || 'None' })] })] }), _jsxs("div", { children: [_jsx("h4", { className: "text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2", children: "Input Parameters Specification" }), _jsx("div", { className: "border border-slate-800 rounded-lg overflow-hidden", children: _jsxs("table", { className: "w-full text-left text-xs", children: [_jsx("thead", { className: "bg-slate-950 text-slate-400", children: _jsxs("tr", { children: [_jsx("th", { className: "p-2.5", children: "Parameter" }), _jsx("th", { className: "p-2.5", children: "Type" }), _jsx("th", { className: "p-2.5", children: "Required" }), _jsx("th", { className: "p-2.5", children: "Description" })] }) }), _jsx("tbody", { className: "divide-y divide-slate-800 text-slate-300", children: selectedTool.parameters.map((p) => (_jsxs("tr", { className: "hover:bg-slate-800/30", children: [_jsx("td", { className: "p-2.5 font-mono text-purple-300", children: p.name }), _jsx("td", { className: "p-2.5 font-mono text-slate-400", children: p.param_type }), _jsx("td", { className: "p-2.5", children: p.required ? (_jsx("span", { className: "text-red-400", children: "Yes" })) : (_jsx("span", { className: "text-slate-500", children: "No" })) }), _jsx("td", { className: "p-2.5 text-slate-400", children: p.description })] }, p.name))) })] }) })] })] })) })] })] })] }));
};
