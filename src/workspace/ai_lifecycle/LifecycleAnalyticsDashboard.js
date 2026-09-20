import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { AILifecycleApiClient } from '../../services/aiLifecycleApiClient';
import { BarChart3, TrendingUp, DollarSign, Clock, RefreshCw } from 'lucide-react';
export const LifecycleAnalyticsDashboard = () => {
    const [analytics, setAnalytics] = useState(null);
    const [loading, setLoading] = useState(true);
    useEffect(() => {
        const load = async () => {
            setLoading(true);
            const data = await AILifecycleApiClient.getAnalytics('agt_acme_invoice_reconciler');
            setAnalytics(data);
            setLoading(false);
        };
        load();
    }, []);
    if (loading || !analytics) {
        return (_jsxs("div", { className: "p-12 text-center text-slate-400", children: [_jsx(RefreshCw, { className: "w-6 h-6 animate-spin mx-auto mb-2" }), " Loading Analytics..."] }));
    }
    return (_jsxs("div", { className: "space-y-6", children: [_jsx("div", { className: "flex items-center justify-between", children: _jsxs("div", { children: [_jsxs("h1", { className: "text-2xl font-bold text-white flex items-center gap-3", children: [_jsx(BarChart3, { className: "w-7 h-7 text-indigo-400" }), "AI Application Business ROI & Fleet Analytics"] }), _jsx("p", { className: "text-sm text-slate-400 mt-1", children: "Quantified financial ROI in USD, developer hours saved, adoption metrics, and success rates." })] }) }), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-3 gap-4", children: [_jsx(Card, { className: "bg-slate-900/80 border-slate-800", children: _jsxs(CardContent, { className: "p-4 flex items-center gap-4", children: [_jsx("div", { className: "p-3 bg-emerald-950/60 text-emerald-400 rounded-lg", children: _jsx(DollarSign, { className: "w-6 h-6" }) }), _jsxs("div", { children: [_jsx("span", { className: "text-xs text-slate-400 block", children: "Automation ROI" }), _jsxs("span", { className: "text-2xl font-bold text-white", children: ["$", analytics.automation_roi_usd.toLocaleString()] })] })] }) }), _jsx(Card, { className: "bg-slate-900/80 border-slate-800", children: _jsxs(CardContent, { className: "p-4 flex items-center gap-4", children: [_jsx("div", { className: "p-3 bg-indigo-950/60 text-indigo-400 rounded-lg", children: _jsx(Clock, { className: "w-6 h-6" }) }), _jsxs("div", { children: [_jsx("span", { className: "text-xs text-slate-400 block", children: "Developer Hours Saved" }), _jsxs("span", { className: "text-2xl font-bold text-white", children: [analytics.developer_hours_saved, " Hours"] })] })] }) }), _jsx(Card, { className: "bg-slate-900/80 border-slate-800", children: _jsxs(CardContent, { className: "p-4 flex items-center gap-4", children: [_jsx("div", { className: "p-3 bg-cyan-950/60 text-cyan-400 rounded-lg", children: _jsx(TrendingUp, { className: "w-6 h-6" }) }), _jsxs("div", { children: [_jsx("span", { className: "text-xs text-slate-400 block", children: "Enterprise Adoption" }), _jsxs("span", { className: "text-2xl font-bold text-cyan-400", children: [analytics.adoption_score, "%"] })] })] }) })] }), _jsxs(Card, { className: "bg-slate-900/80 border-slate-800", children: [_jsx(CardHeader, { children: _jsx(CardTitle, { className: "text-base text-white", children: "Execution Reliability Breakdown" }) }), _jsx(CardContent, { className: "space-y-3", children: _jsxs("div", { className: "p-4 bg-slate-800/40 rounded border border-slate-700/50 flex items-center justify-between", children: [_jsxs("span", { className: "text-sm text-slate-300", children: ["Total Executions: ", analytics.total_executions.toLocaleString()] }), _jsxs(Badge, { variant: "success", children: ["Success Rate: ", analytics.success_rate_pct, "%"] })] }) })] })] }));
};
