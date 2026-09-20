import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { BarChart3, RefreshCw, } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { BusinessApiClient } from '../../services/businessApiClient';
export const KPIDashboard = () => {
    const [kpis, setKpis] = useState([]);
    const [loading, setLoading] = useState(true);
    const loadKpis = async () => {
        try {
            setLoading(true);
            const res = await BusinessApiClient.getKPIs();
            setKpis(res);
        }
        catch (err) {
            console.error('Failed to load KPIs:', err);
        }
        finally {
            setLoading(false);
        }
    };
    useEffect(() => {
        loadKpis();
    }, []);
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/60 p-6 rounded-2xl border border-slate-800 backdrop-blur-md", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2 bg-indigo-500/10 rounded-xl border border-indigo-500/20 text-indigo-400", children: _jsx(BarChart3, { className: "w-6 h-6" }) }), _jsxs("div", { children: [_jsx("h1", { className: "text-2xl font-bold text-white", children: "Enterprise KPI Scorecard" }), _jsx("p", { className: "text-sm text-slate-400", children: "Value accounting, turnaround velocity, unit processing economics & automation ROI" })] })] }), _jsx(Button, { variant: "outline", onClick: loadKpis, disabled: loading, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RefreshCw, { className: `w-4 h-4 ${loading ? 'animate-spin' : ''}` }), "Refresh"] }) })] }), _jsx("div", { className: "grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4", children: kpis.map((k) => (_jsxs(Card, { className: "p-5 bg-slate-900/40 border-slate-800 space-y-3", children: [_jsxs("div", { className: "flex justify-between items-start", children: [_jsx("span", { className: "text-xs text-slate-400 block font-medium", children: k.name }), _jsx(Badge, { variant: "success", children: k.trend })] }), _jsx("div", { className: "flex items-baseline gap-2", children: _jsx("span", { className: "text-2xl font-bold text-white font-mono", children: k.unit === 'USD' ? `$${k.current_value.toLocaleString()}` : `${k.current_value} ${k.unit}` }) }), _jsxs("div", { className: "pt-2 border-t border-slate-800/80 text-xs text-slate-400 flex justify-between", children: [_jsx("span", { children: "Legacy Benchmark:" }), _jsx("span", { className: "font-mono text-slate-300", children: k.unit === 'USD' ? `$${k.benchmark_value}` : `${k.benchmark_value} ${k.unit}` })] })] }, k.kpi_id))) })] }));
};
