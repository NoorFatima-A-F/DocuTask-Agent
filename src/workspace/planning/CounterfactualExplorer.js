import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
/**
 * Counterfactual Reasoning & Sensitivity Explorer Component.
 * Enables interactive parameter tuning, What-If counterfactual queries, and real-time tipping point analysis.
 */
import { useState, useEffect } from 'react';
import { PlanningApiClient } from '../../services/planningApiClient';
export const CounterfactualExplorerView = ({ missionId = 'mission_active_001', }) => {
    const [weights, setWeights] = useState({
        w_accuracy: 0.40,
        w_latency: 0.20,
        w_cost: 0.20,
        w_risk: 0.10,
        w_memory: 0.05,
        w_satisfaction: 0.05,
    });
    const [explanation, setExplanation] = useState(null);
    const [loading, setLoading] = useState(false);
    useEffect(() => {
        runWhatIf();
    }, [weights]);
    const runWhatIf = async () => {
        setLoading(true);
        try {
            const res = await PlanningApiClient.queryCounterfactual(missionId, 'WHAT_IF_WEIGHT_CHANGED', weights);
            setExplanation(res);
        }
        catch (err) {
            console.error('Failed to query counterfactuals', err);
        }
        finally {
            setLoading(false);
        }
    };
    const applyPreset = (name) => {
        if (name === 'AUDIT') {
            setWeights({ w_accuracy: 0.70, w_latency: 0.10, w_cost: 0.10, w_risk: 0.05, w_memory: 0.025, w_satisfaction: 0.025 });
        }
        else if (name === 'TURBO') {
            setWeights({ w_accuracy: 0.20, w_latency: 0.60, w_cost: 0.10, w_risk: 0.05, w_memory: 0.025, w_satisfaction: 0.025 });
        }
        else if (name === 'FRUGAL') {
            setWeights({ w_accuracy: 0.20, w_latency: 0.10, w_cost: 0.60, w_risk: 0.05, w_memory: 0.025, w_satisfaction: 0.025 });
        }
        else {
            setWeights({ w_accuracy: 0.40, w_latency: 0.20, w_cost: 0.20, w_risk: 0.10, w_memory: 0.05, w_satisfaction: 0.05 });
        }
    };
    return (_jsxs("div", { className: "bg-slate-900 border border-slate-800 rounded-xl p-6 text-slate-100 shadow-2xl space-y-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between border-b border-slate-800 pb-4 gap-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center space-x-3", children: [_jsx("span", { className: "px-2.5 py-1 text-xs font-bold uppercase tracking-wider bg-purple-500/20 text-purple-400 border border-purple-500/30 rounded-md", children: "Sensitivity & What-If Engine" }), _jsxs("span", { className: "text-xs text-slate-400 font-mono", children: ["Mission: ", missionId] }), loading && (_jsx("span", { className: "text-xs text-indigo-400 animate-pulse", children: "Calculating sensitivity..." }))] }), _jsx("h2", { className: "text-xl font-bold text-white mt-1", children: "Counterfactual Explainability Explorer" }), _jsx("p", { className: "text-sm text-slate-400", children: "Dynamically adjust utility weights to observe decision boundaries, ranking inversions, and tipping points." })] }), _jsxs("div", { className: "flex flex-wrap gap-2", children: [_jsx("button", { onClick: () => applyPreset('DEFAULT'), className: "px-2.5 py-1 bg-slate-800 hover:bg-slate-700 text-xs font-medium rounded border border-slate-700 transition", children: "Pareto Balanced" }), _jsx("button", { onClick: () => applyPreset('AUDIT'), className: "px-2.5 py-1 bg-indigo-900/50 hover:bg-indigo-800/60 text-indigo-300 text-xs font-medium rounded border border-indigo-700/50 transition", children: "Deep Audit (Accuracy)" }), _jsx("button", { onClick: () => applyPreset('TURBO'), className: "px-2.5 py-1 bg-cyan-900/50 hover:bg-cyan-800/60 text-cyan-300 text-xs font-medium rounded border border-cyan-700/50 transition", children: "Realtime SLA (Turbo)" }), _jsx("button", { onClick: () => applyPreset('FRUGAL'), className: "px-2.5 py-1 bg-emerald-900/50 hover:bg-emerald-800/60 text-emerald-300 text-xs font-medium rounded border border-emerald-700/50 transition", children: "Bulk Frugal (Cost)" })] })] }), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-4 gap-4 bg-slate-950/50 p-4 rounded-lg border border-slate-800", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex justify-between text-xs mb-1", children: [_jsx("span", { className: "text-slate-400", children: "Accuracy Weight (w_acc)" }), _jsx("span", { className: "font-mono text-emerald-400 font-bold", children: weights.w_accuracy.toFixed(2) })] }), _jsx("input", { type: "range", min: "0", max: "1", step: "0.05", value: weights.w_accuracy, onChange: (e) => setWeights({ ...weights, w_accuracy: parseFloat(e.target.value) }), className: "w-full accent-emerald-500 cursor-pointer" })] }), _jsxs("div", { children: [_jsxs("div", { className: "flex justify-between text-xs mb-1", children: [_jsx("span", { className: "text-slate-400", children: "Latency Penalty (w_lat)" }), _jsx("span", { className: "font-mono text-rose-400 font-bold", children: weights.w_latency.toFixed(2) })] }), _jsx("input", { type: "range", min: "0", max: "1", step: "0.05", value: weights.w_latency, onChange: (e) => setWeights({ ...weights, w_latency: parseFloat(e.target.value) }), className: "w-full accent-rose-500 cursor-pointer" })] }), _jsxs("div", { children: [_jsxs("div", { className: "flex justify-between text-xs mb-1", children: [_jsx("span", { className: "text-slate-400", children: "Cost Penalty (w_cost)" }), _jsx("span", { className: "font-mono text-amber-400 font-bold", children: weights.w_cost.toFixed(2) })] }), _jsx("input", { type: "range", min: "0", max: "1", step: "0.05", value: weights.w_cost, onChange: (e) => setWeights({ ...weights, w_cost: parseFloat(e.target.value) }), className: "w-full accent-amber-500 cursor-pointer" })] }), _jsxs("div", { children: [_jsxs("div", { className: "flex justify-between text-xs mb-1", children: [_jsx("span", { className: "text-slate-400", children: "Risk Penalty (w_risk)" }), _jsx("span", { className: "font-mono text-purple-400 font-bold", children: weights.w_risk.toFixed(2) })] }), _jsx("input", { type: "range", min: "0", max: "1", step: "0.05", value: weights.w_risk, onChange: (e) => setWeights({ ...weights, w_risk: parseFloat(e.target.value) }), className: "w-full accent-purple-500 cursor-pointer" })] })] }), explanation && (_jsxs("div", { className: "grid grid-cols-1 md:grid-cols-3 gap-4", children: [_jsxs("div", { className: "md:col-span-1 bg-gradient-to-br from-indigo-950/40 to-slate-900 border border-indigo-500/30 rounded-lg p-4 flex flex-col justify-between", children: [_jsxs("div", { children: [_jsx("span", { className: "text-[10px] uppercase font-bold text-indigo-400 tracking-wider block", children: "Counterfactual Winner" }), _jsx("h3", { className: "text-lg font-bold text-white mt-1", children: explanation.alternative_ranking?.[0]?.name || 'Strategy Delta' }), _jsx("p", { className: "text-xs text-slate-300 mt-2 leading-relaxed", children: explanation.summary_explanation })] }), explanation.tipping_point && (_jsxs("div", { className: "mt-4 pt-3 border-t border-indigo-900/50 bg-indigo-950/30 -mx-4 -mb-4 p-3 rounded-b-lg", children: [_jsx("span", { className: "text-[10px] font-bold text-amber-400 uppercase tracking-wider block mb-0.5", children: "Analytical Tipping Point" }), _jsx("span", { className: "text-xs text-slate-300 font-mono block", children: explanation.tipping_point.condition })] }))] }), _jsxs("div", { className: "md:col-span-2 bg-slate-950/60 border border-slate-800 rounded-lg p-4", children: [_jsx("h4", { className: "text-xs font-bold uppercase tracking-wider text-slate-400 mb-3", children: "Recalculated Strategy Order" }), _jsx("div", { className: "space-y-2 font-mono text-xs", children: explanation.alternative_ranking?.map((rankItem, idx) => (_jsxs("div", { className: `flex items-center justify-between p-2 rounded border ${idx === 0
                                        ? 'bg-emerald-950/30 border-emerald-500/40 text-emerald-200'
                                        : 'bg-slate-900/60 border-slate-800 text-slate-300'}`, children: [_jsxs("div", { className: "flex items-center space-x-2", children: [_jsxs("span", { className: "font-bold w-4", children: [idx + 1, "."] }), _jsx("span", { className: "font-sans font-medium", children: rankItem.name }), _jsxs("span", { className: "text-[10px] text-slate-500", children: ["(", rankItem.archetype, ")"] })] }), _jsxs("div", { className: "font-bold", children: ["U = ", rankItem.new_utility.toFixed(4)] })] }, rankItem.strategy_id))) })] })] }))] }));
};
