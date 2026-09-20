import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Compass, RefreshCw, AlertTriangle, } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { BusinessApiClient } from '../../services/businessApiClient';
export const ProcessDiscoveryExplorer = () => {
    const [discovered, setDiscovered] = useState([]);
    const [loading, setLoading] = useState(true);
    const loadData = async () => {
        try {
            setLoading(true);
            const res = await BusinessApiClient.getDiscovery();
            setDiscovered(res);
        }
        catch (err) {
            console.error('Failed to load discovered processes:', err);
        }
        finally {
            setLoading(false);
        }
    };
    useEffect(() => {
        loadData();
    }, []);
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/60 p-6 rounded-2xl border border-slate-800 backdrop-blur-md", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2 bg-indigo-500/10 rounded-xl border border-indigo-500/20 text-indigo-400", children: _jsx(Compass, { className: "w-6 h-6" }) }), _jsxs("div", { children: [_jsx("h1", { className: "text-2xl font-bold text-white", children: "Process Mining & Discovery Explorer" }), _jsx("p", { className: "text-sm text-slate-400", children: "Autonomous reconstruction of actual organizational workflows from ERP telemetry & audit logs" })] })] }), _jsx(Button, { variant: "outline", onClick: loadData, disabled: loading, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RefreshCw, { className: `w-4 h-4 ${loading ? 'animate-spin' : ''}` }), "Refresh Mined Data"] }) })] }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-6", children: discovered.map((d) => (_jsxs(Card, { className: "p-6 bg-slate-900/40 border-slate-800 space-y-4", children: [_jsxs("div", { className: "flex justify-between items-start", children: [_jsxs("div", { children: [_jsx("h2", { className: "text-base font-bold text-white", children: d.name }), _jsxs("span", { className: "text-xs text-slate-400 font-mono", children: ["ID: ", d.discovered_id] })] }), _jsxs(Badge, { variant: "intelligence", children: [d.variants_count, " Path Variants"] })] }), _jsxs("div", { className: "grid grid-cols-3 gap-3 text-xs font-mono", children: [_jsxs("div", { className: "p-3 bg-slate-800/40 rounded-lg border border-slate-700/60", children: [_jsx("span", { className: "text-slate-400 block text-[11px]", children: "Frequency" }), _jsxs("span", { className: "text-white font-bold text-sm", children: [d.frequency.toLocaleString(), " runs"] })] }), _jsxs("div", { className: "p-3 bg-slate-800/40 rounded-lg border border-slate-700/60", children: [_jsx("span", { className: "text-slate-400 block text-[11px]", children: "Mean Duration" }), _jsxs("span", { className: "text-indigo-300 font-bold text-sm", children: [(d.mean_duration_sec / 60).toFixed(0), " mins"] })] }), _jsxs("div", { className: "p-3 bg-slate-800/40 rounded-lg border border-slate-700/60", children: [_jsx("span", { className: "text-slate-400 block text-[11px]", children: "Conformance" }), _jsxs("span", { className: "text-emerald-400 font-bold text-sm", children: [(d.compliance_score * 100).toFixed(0), "%"] })] })] }), _jsxs("div", { className: "space-y-2 pt-2 border-t border-slate-800", children: [_jsxs("span", { className: "text-xs font-semibold text-slate-300 flex items-center gap-1.5", children: [_jsx(AlertTriangle, { className: "w-3.5 h-3.5 text-amber-400" }), "Discovered Bottleneck Steps"] }), _jsx("div", { className: "flex flex-wrap gap-1.5", children: d.bottleneck_steps.map((b, idx) => (_jsx("span", { className: "px-2.5 py-1 bg-amber-950/40 border border-amber-800/40 text-amber-300 rounded font-mono text-[11px]", children: b }, idx))) })] })] }, d.discovered_id))) })] }));
};
