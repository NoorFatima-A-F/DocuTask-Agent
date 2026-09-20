import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
/**
 * Planner Self-Evaluation & Calibration Card Component.
 * Displays predicted vs actual execution metrics, calibration scores, and automated feedback tuning loops.
 */
import { useState, useEffect } from 'react';
import { PlanningApiClient } from '../../services/planningApiClient';
export const PlannerCalibrationCardView = ({ missionId = 'mission_active_001', }) => {
    const [metric, setMetric] = useState(null);
    const [loading, setLoading] = useState(true);
    useEffect(() => {
        loadCalibration();
    }, [missionId]);
    const loadCalibration = async () => {
        setLoading(true);
        try {
            const data = await PlanningApiClient.evaluateMission(missionId, 1920.0, 0.0039, 0.99);
            setMetric(data);
        }
        catch (err) {
            console.error('Failed to load calibration', err);
        }
        finally {
            setLoading(false);
        }
    };
    if (loading || !metric) {
        return (_jsxs("div", { className: "flex items-center justify-center p-8 text-slate-400", children: [_jsx("div", { className: "animate-spin rounded-full h-6 w-6 border-b-2 border-indigo-500 mr-2" }), _jsx("span", { children: "Calculating Calibration Errors..." })] }));
    }
    const comp = metric.comparison;
    return (_jsxs("div", { className: "bg-slate-900 border border-slate-800 rounded-xl p-6 text-slate-100 shadow-2xl space-y-5", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between border-b border-slate-800 pb-3 gap-3", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center space-x-2", children: [_jsx("span", { className: "px-2 py-0.5 text-[10px] font-bold uppercase tracking-wider bg-indigo-500/20 text-indigo-400 border border-indigo-500/30 rounded", children: "Self-Evaluation Loop" }), _jsxs("span", { className: "text-xs text-slate-400 font-mono", children: ["Mission: ", metric.mission_id] })] }), _jsx("h3", { className: "text-lg font-bold text-white mt-1", children: "Planner Calibration & Drift Analysis" })] }), _jsxs("div", { className: "bg-emerald-950/40 border border-emerald-500/40 px-3 py-1.5 rounded-lg text-right", children: [_jsx("span", { className: "text-[10px] uppercase text-emerald-300 font-semibold block", children: "Model Calibration" }), _jsxs("span", { className: "text-sm font-bold text-emerald-400 font-mono", children: [(metric.overall_calibration_score * 100).toFixed(1), "%"] })] })] }), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-3 gap-3 text-xs font-mono", children: [_jsxs("div", { className: "bg-slate-950/60 p-3 rounded-lg border border-slate-800", children: [_jsx("span", { className: "text-slate-400 block text-[10px] uppercase", children: "Execution Latency" }), _jsxs("div", { className: "flex justify-between mt-1 text-slate-200", children: [_jsxs("span", { children: ["Pred: ", comp.predicted_latency_ms.toFixed(0), "ms"] }), _jsxs("span", { children: ["Act: ", comp.actual_latency_ms.toFixed(0), "ms"] })] }), _jsxs("div", { className: "text-emerald-400 text-[11px] mt-1", children: ["Delta: ", comp.latency_delta_ms > 0 ? `+${comp.latency_delta_ms.toFixed(0)}ms` : `${comp.latency_delta_ms.toFixed(0)}ms`, " (err: ", comp.latency_error_pct.toFixed(1), "%)"] })] }), _jsxs("div", { className: "bg-slate-950/60 p-3 rounded-lg border border-slate-800", children: [_jsx("span", { className: "text-slate-400 block text-[10px] uppercase", children: "Cost Consumption" }), _jsxs("div", { className: "flex justify-between mt-1 text-slate-200", children: [_jsxs("span", { children: ["Pred: $", comp.predicted_cost_usd.toFixed(4)] }), _jsxs("span", { children: ["Act: $", comp.actual_cost_usd.toFixed(4)] })] }), _jsxs("div", { className: "text-emerald-400 text-[11px] mt-1", children: ["Delta: $", comp.cost_delta_usd.toFixed(4), " (err: ", comp.cost_error_pct.toFixed(1), "%)"] })] }), _jsxs("div", { className: "bg-slate-950/60 p-3 rounded-lg border border-slate-800", children: [_jsx("span", { className: "text-slate-400 block text-[10px] uppercase", children: "Validation Accuracy" }), _jsxs("div", { className: "flex justify-between mt-1 text-slate-200", children: [_jsxs("span", { children: ["Pred: ", (comp.predicted_accuracy * 100).toFixed(1), "%"] }), _jsxs("span", { children: ["Act: ", (comp.actual_accuracy * 100).toFixed(1), "%"] })] }), _jsxs("div", { className: "text-emerald-400 text-[11px] mt-1", children: ["Gain: +", (comp.accuracy_delta * 100).toFixed(2), "%"] })] })] }), _jsxs("div", { className: "bg-slate-950/40 p-3.5 rounded-lg border border-slate-800/80 space-y-2 text-xs", children: [_jsx("div", { className: "font-bold text-slate-300 uppercase tracking-wider text-[11px]", children: "Root Cause & Automated Tuning" }), _jsx("div", { className: "text-slate-400", children: metric.root_causes.map((rc, i) => (_jsxs("p", { className: "font-sans leading-relaxed text-slate-300", children: ["\u2022 ", rc] }, i))) }), Object.keys(metric.tuning_recommendations).length > 0 && (_jsx("div", { className: "pt-2 border-t border-slate-800/60 font-mono text-[11px] text-indigo-300", children: Object.entries(metric.tuning_recommendations).map(([k, v]) => (_jsxs("div", { className: "flex space-x-2", children: [_jsxs("span", { className: "text-slate-500 uppercase", children: [k, ":"] }), _jsx("span", { children: v })] }, k))) }))] })] }));
};
