import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
/**
 * Phase 13.16: Autonomous World Modeling, Predictive Intelligence & Causal Reasoning Platform (AWMPICRP)
 * View 9: Predictive Intelligence Dashboard
 */
import { useEffect, useState } from 'react';
import { TrendingUp, RefreshCw, Activity, Zap, } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { WorldModelApiClient } from '../../services/worldModelApiClient';
export const PredictiveIntelligenceDashboard = () => {
    const [trajectories, setTrajectories] = useState([]);
    const [loading, setLoading] = useState(true);
    const [targetMetric, setTargetMetric] = useState('Enterprise Document Ingestion Throughput');
    const [predictedVal, setPredictedVal] = useState('14200');
    const [generating, setGenerating] = useState(false);
    const fetchForecasts = async () => {
        setLoading(true);
        try {
            const res = await WorldModelApiClient.getForecasts();
            setTrajectories(res.trajectories || []);
        }
        catch (err) {
            console.error('Error fetching forecasts:', err);
        }
        finally {
            setLoading(false);
        }
    };
    useEffect(() => {
        fetchForecasts();
    }, []);
    const handleGenerate = async (e) => {
        e.preventDefault();
        setGenerating(true);
        try {
            await WorldModelApiClient.generateForecast({
                target_metric: targetMetric,
                horizon: 'medium_term',
                horizon_seconds: 86400,
                include_causal_factors: true,
            });
            await fetchForecasts();
        }
        catch (err) {
            console.error('Error generating forecast:', err);
        }
        finally {
            setGenerating(false);
        }
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/80 border border-purple-500/30 rounded-xl p-6", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2.5 bg-purple-500/10 border border-purple-500/30 rounded-lg text-purple-400", children: _jsx(TrendingUp, { className: "w-6 h-6" }) }), _jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold text-white tracking-tight", children: "Predictive Intelligence Dashboard" }), _jsx(Badge, { variant: "intelligence", children: "95% Confidence Intervals" })] }), _jsx("p", { className: "text-sm text-slate-400", children: "Probabilistic multi-horizon forecasting for latency, spend, failure risk, and SLA breaches." })] })] }), _jsx("div", { className: "flex items-center gap-3", children: _jsx(Button, { variant: "outline", onClick: fetchForecasts, disabled: loading, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RefreshCw, { className: `w-4 h-4 ${loading ? 'animate-spin' : ''}` }), "Refresh"] }) }) })] }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-3 gap-6", children: [_jsxs("div", { className: "lg:col-span-2 space-y-4", children: [_jsxs("h3", { className: "text-base font-semibold text-white flex items-center gap-2", children: [_jsx(Activity, { className: "w-5 h-5 text-purple-400" }), "Active Forecast Trajectories"] }), _jsx("div", { className: "space-y-4", children: trajectories.map((traj) => (_jsxs(Card, { className: "bg-slate-900/60 border-slate-800 p-5 space-y-4 hover:border-purple-500/40 transition-all", children: [_jsxs("div", { className: "flex items-start justify-between", children: [_jsxs("div", { children: [_jsx("span", { className: "text-xs font-mono text-purple-400 bg-purple-950/60 px-2 py-0.5 rounded border border-purple-500/30", children: traj.trajectory_id }), _jsx("h4", { className: "text-base font-bold text-white mt-1", children: traj.target_metric })] }), _jsxs(Badge, { variant: "success", children: ["Confidence: ", Math.round((traj.confidence_score || 0.91) * 100), "%"] })] }), _jsxs("div", { className: "grid grid-cols-3 gap-3 text-center", children: [_jsxs("div", { className: "p-3 bg-slate-950/80 rounded border border-slate-800", children: [_jsx("span", { className: "text-slate-400 text-[10px] uppercase font-semibold block", children: "95% Lower Bound" }), _jsx("span", { className: "text-sm font-mono text-slate-300 font-bold", children: traj.lower_bound_95 })] }), _jsxs("div", { className: "p-3 bg-purple-950/40 rounded border border-purple-500/40", children: [_jsx("span", { className: "text-purple-300 text-[10px] uppercase font-semibold block", children: "Expected Value" }), _jsx("span", { className: "text-base font-mono text-purple-200 font-bold", children: traj.expected_value })] }), _jsxs("div", { className: "p-3 bg-slate-950/80 rounded border border-slate-800", children: [_jsx("span", { className: "text-slate-400 text-[10px] uppercase font-semibold block", children: "95% Upper Bound" }), _jsx("span", { className: "text-sm font-mono text-slate-300 font-bold", children: traj.upper_bound_95 })] })] }), _jsxs("div", { className: "text-xs text-slate-400", children: [_jsx("span", { className: "font-semibold text-slate-300 block mb-1", children: "Causal Drivers Identified:" }), _jsx("div", { className: "flex flex-wrap gap-2", children: (traj.causal_drivers || ['Diurnal load rhythm', 'Batch concurrency peak']).map((d, idx) => (_jsx("span", { className: "px-2.5 py-1 rounded bg-slate-800 border border-slate-700 text-slate-200", children: d }, idx))) })] })] }, traj.trajectory_id))) })] }), _jsxs(Card, { className: "bg-slate-900/60 border-slate-800 p-5 space-y-4", children: [_jsxs("h3", { className: "text-base font-semibold text-white flex items-center gap-2", children: [_jsx(Zap, { className: "w-5 h-5 text-purple-400" }), "Generate New Forecast"] }), _jsxs("form", { onSubmit: handleGenerate, className: "space-y-4 text-xs", children: [_jsxs("div", { children: [_jsx("label", { className: "block text-slate-300 font-semibold mb-1", children: "Target Metric" }), _jsx("input", { type: "text", required: true, value: targetMetric, onChange: (e) => setTargetMetric(e.target.value), className: "w-full bg-slate-800 border border-slate-700 rounded p-2 text-white text-xs" })] }), _jsxs("div", { children: [_jsx("label", { className: "block text-slate-300 font-semibold mb-1", children: "Estimated Value Base" }), _jsx("input", { type: "number", required: true, value: predictedVal, onChange: (e) => setPredictedVal(e.target.value), className: "w-full bg-slate-800 border border-slate-700 rounded p-2 text-white font-mono text-xs" })] }), _jsx(Button, { variant: "intelligence", type: "submit", disabled: generating, className: "w-full", children: _jsxs("span", { className: "flex items-center justify-center gap-2", children: [_jsx(TrendingUp, { className: "w-4 h-4" }), generating ? 'Forecasting...' : 'Compute Trajectory'] }) })] })] })] })] }));
};
