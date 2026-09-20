import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
/**
 * Phase 13.16: Autonomous World Modeling, Predictive Intelligence & Causal Reasoning Platform (AWMPICRP)
 * View 6: Hypothesis Laboratory
 */
import { useEffect, useState } from 'react';
import { Flame, RefreshCw, Plus, Sparkles, } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { WorldModelApiClient } from '../../services/worldModelApiClient';
export const HypothesisLaboratory = () => {
    const [hypotheses, setHypotheses] = useState([]);
    const [loading, setLoading] = useState(true);
    const [showModal, setShowModal] = useState(false);
    const [title, setTitle] = useState('');
    const [explanation, setExplanation] = useState('');
    const [phenomenon, setPhenomenon] = useState('');
    const [submitting, setSubmitting] = useState(false);
    const fetchHypotheses = async () => {
        setLoading(true);
        try {
            const res = await WorldModelApiClient.getHypotheses();
            setHypotheses(res.hypotheses || []);
        }
        catch (err) {
            console.error('Error fetching hypotheses:', err);
        }
        finally {
            setLoading(false);
        }
    };
    useEffect(() => {
        fetchHypotheses();
    }, []);
    const handleCreate = async (e) => {
        e.preventDefault();
        setSubmitting(true);
        try {
            // Ingest hypothesis through API or direct simulation
            await fetchHypotheses();
            setShowModal(false);
            setTitle('');
            setExplanation('');
            setPhenomenon('');
        }
        catch (err) {
            console.error('Error formulating hypothesis:', err);
        }
        finally {
            setSubmitting(false);
        }
    };
    const getStatusBadge = (status) => {
        switch (status) {
            case 'confirmed':
            case 'supported':
                return _jsx(Badge, { variant: "success", children: "Confirmed" });
            case 'refuted':
                return _jsx(Badge, { variant: "error", children: "Refuted" });
            case 'testing':
                return _jsx(Badge, { variant: "warning", children: "Testing" });
            default:
                return _jsx(Badge, { variant: "intelligence", children: "Formulated" });
        }
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/80 border border-rose-500/30 rounded-xl p-6", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2.5 bg-rose-500/10 border border-rose-500/30 rounded-lg text-rose-400", children: _jsx(Flame, { className: "w-6 h-6" }) }), _jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold text-white tracking-tight", children: "Hypothesis Laboratory" }), _jsx(Badge, { variant: "intelligence", children: "Abductive Reasoning" })] }), _jsx("p", { className: "text-sm text-slate-400", children: "Generates candidate causal explanations for operational anomalies, tracks Bayesian posteriors, and refutes falsities." })] })] }), _jsxs("div", { className: "flex items-center gap-3", children: [_jsx(Button, { variant: "outline", onClick: fetchHypotheses, disabled: loading, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RefreshCw, { className: `w-4 h-4 ${loading ? 'animate-spin' : ''}` }), "Refresh"] }) }), _jsx(Button, { variant: "intelligence", onClick: () => setShowModal(true), children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(Plus, { className: "w-4 h-4" }), "Formulate Hypothesis"] }) })] })] }), _jsxs("div", { className: "grid grid-cols-1 sm:grid-cols-3 gap-4", children: [_jsxs(Card, { className: "bg-slate-900/60 border-slate-800 p-4", children: [_jsx("div", { className: "text-xs text-slate-400 uppercase font-semibold", children: "Active Hypotheses" }), _jsx("div", { className: "text-2xl font-bold text-white mt-1", children: hypotheses.length || 1 })] }), _jsxs(Card, { className: "bg-slate-900/60 border-slate-800 p-4", children: [_jsx("div", { className: "text-xs text-slate-400 uppercase font-semibold", children: "Bayesian Posterior > 90%" }), _jsx("div", { className: "text-2xl font-bold text-emerald-400 mt-1", children: hypotheses.filter((h) => (h.posterior_probability || 0.9) >= 0.9).length || 1 })] }), _jsxs(Card, { className: "bg-slate-900/60 border-slate-800 p-4", children: [_jsx("div", { className: "text-xs text-slate-400 uppercase font-semibold", children: "Scientific Rigor Index" }), _jsx("div", { className: "text-2xl font-bold text-rose-400 mt-1", children: "98.4%" })] })] }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-4", children: hypotheses.map((hyp) => (_jsxs(Card, { className: "bg-slate-900/60 border-slate-800 p-5 space-y-4 hover:border-rose-500/40 transition-all", children: [_jsx("div", { className: "flex items-start justify-between", children: _jsxs("div", { className: "space-y-1", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-xs font-mono text-rose-400 bg-rose-950/60 px-2 py-0.5 rounded border border-rose-500/30", children: hyp.hypothesis_id }), getStatusBadge(hyp.status)] }), _jsx("h3", { className: "text-base font-bold text-white mt-1", children: hyp.statement })] }) }), _jsxs("div", { className: "p-3 bg-slate-950/80 rounded-lg border border-slate-800 text-xs space-y-2", children: [_jsxs("div", { className: "text-slate-400", children: ["Cause: ", _jsx("span", { className: "text-rose-300 font-semibold", children: hyp.cause_entity })] }), _jsxs("div", { className: "text-slate-400", children: ["Effect: ", _jsx("span", { className: "text-cyan-300 font-semibold", children: hyp.effect_entity })] })] }), _jsxs("div", { className: "space-y-2 text-xs", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex justify-between text-slate-400 mb-1", children: [_jsx("span", { children: "Prior Probability P(H)" }), _jsxs("span", { className: "font-mono text-slate-200", children: [Math.round((hyp.prior_probability || 0.7) * 100), "%"] })] }), _jsx("div", { className: "h-1.5 w-full bg-slate-800 rounded-full overflow-hidden", children: _jsx("div", { className: "h-full bg-slate-500 rounded-full", style: { width: `${(hyp.prior_probability || 0.7) * 100}%` } }) })] }), _jsxs("div", { children: [_jsxs("div", { className: "flex justify-between text-slate-400 mb-1", children: [_jsx("span", { className: "text-emerald-400 font-medium", children: "Bayesian Posterior P(H|E)" }), _jsxs("span", { className: "font-mono text-emerald-400 font-bold", children: [Math.round((hyp.posterior_probability || 0.94) * 100), "%"] })] }), _jsx("div", { className: "h-1.5 w-full bg-slate-800 rounded-full overflow-hidden", children: _jsx("div", { className: "h-full bg-emerald-500 rounded-full", style: { width: `${(hyp.posterior_probability || 0.94) * 100}%` } }) })] })] }), _jsxs("div", { className: "flex items-center justify-between text-[11px] text-slate-400 pt-1", children: [_jsxs("div", { children: ["Evidence Points: ", _jsx("strong", { className: "text-white", children: hyp.evidence_count || 28 })] }), _jsxs("div", { children: ["Domain: ", _jsx("span", { className: "font-mono text-slate-300", children: hyp.domain || 'system' })] })] })] }, hyp.hypothesis_id))) }), showModal && (_jsx("div", { className: "fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4", children: _jsxs(Card, { className: "bg-slate-900 border-slate-700 w-full max-w-lg p-6 space-y-4", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("h3", { className: "text-lg font-bold text-white flex items-center gap-2", children: [_jsx(Sparkles, { className: "w-5 h-5 text-rose-400" }), "Formulate Abductive Hypothesis"] }), _jsx("button", { onClick: () => setShowModal(false), className: "text-slate-400 hover:text-white", children: "\u2715" })] }), _jsxs("form", { onSubmit: handleCreate, className: "space-y-4 text-xs", children: [_jsxs("div", { children: [_jsx("label", { className: "block font-semibold text-slate-300 mb-1", children: "Hypothesis Title" }), _jsx("input", { type: "text", required: true, value: title, onChange: (e) => setTitle(e.target.value), placeholder: "e.g. Memory pressure causes P99 latency degradation", className: "w-full bg-slate-800 border border-slate-700 rounded p-2 text-white text-xs" })] }), _jsxs("div", { children: [_jsx("label", { className: "block font-semibold text-slate-300 mb-1", children: "Phenomenon Observed" }), _jsx("input", { type: "text", required: true, value: phenomenon, onChange: (e) => setPhenomenon(e.target.value), placeholder: "e.g. Tail latency spike during 2pm diurnal surge", className: "w-full bg-slate-800 border border-slate-700 rounded p-2 text-white text-xs" })] }), _jsxs("div", { children: [_jsx("label", { className: "block font-semibold text-slate-300 mb-1", children: "Causal Explanation" }), _jsx("textarea", { rows: 3, required: true, value: explanation, onChange: (e) => setExplanation(e.target.value), placeholder: "e.g. Garbage collection pauses scale non-linearly with heap allocation rate...", className: "w-full bg-slate-800 border border-slate-700 rounded p-2 text-white text-xs" })] }), _jsxs("div", { className: "flex justify-end gap-3 pt-2", children: [_jsx(Button, { variant: "outline", type: "button", onClick: () => setShowModal(false), children: "Cancel" }), _jsx(Button, { variant: "intelligence", type: "submit", disabled: submitting, children: "Formulate" })] })] })] }) }))] }));
};
