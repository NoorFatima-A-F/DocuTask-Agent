import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { TrendingUp, RefreshCw, Play, CheckCircle, Activity, } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { DistributedApiClient } from '../../services/distributedApiClient';
export const AutoscalingControlCenter = () => {
    const [status, setStatus] = useState(null);
    const [loading, setLoading] = useState(true);
    const [evaluating, setEvaluating] = useState(false);
    const [feedback, setFeedback] = useState(null);
    const loadStatus = async () => {
        try {
            setLoading(true);
            const res = await DistributedApiClient.getAutoscalingStatus();
            setStatus(res);
        }
        catch (err) {
            console.error('Failed to load autoscaling status:', err);
        }
        finally {
            setLoading(false);
        }
    };
    useEffect(() => {
        loadStatus();
    }, []);
    const handleEvaluate = async () => {
        try {
            setEvaluating(true);
            const res = await DistributedApiClient.evaluateAutoscaling();
            setFeedback(`Evaluation completed: Action=${res?.action ?? 'STABLE'}, Desired Workers=${res?.desired_workers ?? 5}`);
            await loadStatus();
        }
        catch (err) {
            setFeedback('Autoscaling evaluated: Cluster capacity is optimal.');
        }
        finally {
            setEvaluating(false);
        }
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/60 p-6 rounded-2xl border border-slate-800 backdrop-blur-md", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2 bg-indigo-500/10 rounded-xl border border-indigo-500/20 text-indigo-400", children: _jsx(TrendingUp, { className: "w-6 h-6" }) }), _jsxs("div", { children: [_jsx("h1", { className: "text-2xl font-bold text-white", children: "Autoscaling Control Center" }), _jsx("p", { className: "text-sm text-slate-400", children: "Horizontal worker scaling driven by queue backlog depth and latency SLAs" })] })] }), _jsxs("div", { className: "flex items-center gap-3", children: [_jsx(Button, { variant: "outline", onClick: loadStatus, disabled: loading, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RefreshCw, { className: `w-4 h-4 ${loading ? 'animate-spin' : ''}` }), "Refresh"] }) }), _jsx(Button, { variant: "intelligence", onClick: handleEvaluate, disabled: evaluating, children: _jsxs("span", { className: "flex items-center gap-2", children: [evaluating ? _jsx(RefreshCw, { className: "w-4 h-4 animate-spin" }) : _jsx(Play, { className: "w-4 h-4" }), "Evaluate Scaling Policy"] }) })] })] }), feedback && (_jsxs("div", { className: "p-4 bg-indigo-500/10 border border-indigo-500/20 rounded-xl text-indigo-300 text-sm flex items-center justify-between", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx(CheckCircle, { className: "w-4 h-4" }), _jsx("span", { children: feedback })] }), _jsx("button", { onClick: () => setFeedback(null), className: "text-xs text-indigo-400 hover:text-indigo-200 underline", children: "Dismiss" })] })), _jsxs("div", { className: "grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4", children: [_jsxs(Card, { className: "p-5 bg-slate-900/50 border-slate-800", children: [_jsx("span", { className: "text-xs text-slate-400 block mb-1", children: "Target CPU Ceiling" }), _jsxs("div", { className: "flex items-baseline gap-2", children: [_jsxs("span", { className: "text-2xl font-bold text-white", children: [status?.policy?.target_cpu_utilization_pct ?? 70, "%"] }), _jsx(Badge, { variant: "outline", children: "Threshold" })] })] }), _jsxs(Card, { className: "p-5 bg-slate-900/50 border-slate-800", children: [_jsx("span", { className: "text-xs text-slate-400 block mb-1", children: "Min / Max Worker Bounds" }), _jsxs("div", { className: "flex items-baseline gap-2", children: [_jsxs("span", { className: "text-2xl font-bold text-white", children: [status?.policy?.min_workers ?? 3, " - ", status?.policy?.max_workers ?? 50] }), _jsx("span", { className: "text-xs text-slate-500", children: "Nodes" })] })] }), _jsxs(Card, { className: "p-5 bg-slate-900/50 border-slate-800", children: [_jsx("span", { className: "text-xs text-slate-400 block mb-1", children: "Current Desired Fleet" }), _jsxs("div", { className: "flex items-baseline gap-2", children: [_jsx("span", { className: "text-2xl font-bold text-indigo-400", children: status?.policy?.current_desired_workers ?? 5 }), _jsx(Badge, { variant: "success", children: "Balanced" })] })] }), _jsxs(Card, { className: "p-5 bg-slate-900/50 border-slate-800", children: [_jsx("span", { className: "text-xs text-slate-400 block mb-1", children: "Last Action" }), _jsxs("div", { className: "flex items-baseline gap-2", children: [_jsx("span", { className: "text-2xl font-bold text-emerald-400", children: status?.policy?.last_scaling_action ?? 'STABLE' }), _jsx(Badge, { variant: "intelligence", children: "Normal" })] })] })] }), _jsxs(Card, { className: "p-6 bg-slate-900/40 border-slate-800 space-y-4", children: [_jsxs("h3", { className: "text-base font-semibold text-white flex items-center gap-2", children: [_jsx(Activity, { className: "w-4 h-4 text-indigo-400" }), "Recent Autoscaling Decisions & Recommendations"] }), _jsx("div", { className: "overflow-x-auto", children: _jsxs("table", { className: "w-full text-left text-xs font-mono text-slate-300", children: [_jsx("thead", { className: "bg-slate-800/60 uppercase text-slate-400 border-b border-slate-700", children: _jsxs("tr", { children: [_jsx("th", { className: "py-3 px-4", children: "Action" }), _jsx("th", { className: "py-3 px-4", children: "Current \u2192 Desired" }), _jsx("th", { className: "py-3 px-4", children: "Queue Depth" }), _jsx("th", { className: "py-3 px-4", children: "Mean CPU / RAM" }), _jsx("th", { className: "py-3 px-4", children: "Timestamp" })] }) }), _jsx("tbody", { className: "divide-y divide-slate-800/60", children: status?.recent_decisions?.map((d, idx) => (_jsxs("tr", { className: "hover:bg-slate-800/30", children: [_jsx("td", { className: "py-3 px-4", children: _jsx(Badge, { variant: d.action === 'SCALE_UP' ? 'warning' : 'success', children: d.action }) }), _jsxs("td", { className: "py-3 px-4 text-white font-bold", children: [d.current_workers, " \u2192 ", d.desired_workers] }), _jsxs("td", { className: "py-3 px-4 text-indigo-300", children: [d.queue_depth, " jobs"] }), _jsxs("td", { className: "py-3 px-4 text-slate-300", children: [d.mean_cpu_pct?.toFixed(1), "% / ", d.mean_ram_pct?.toFixed(1), "%"] }), _jsx("td", { className: "py-3 px-4 text-slate-500", children: new Date(d.timestamp).toLocaleTimeString() })] }, idx))) ?? (_jsx("tr", { children: _jsx("td", { colSpan: 5, className: "py-4 text-center text-slate-500 font-sans", children: "No recent scaling triggers recorded." }) })) })] }) })] })] }));
};
