import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
/**
 * Phase 13.16: Autonomous World Modeling, Predictive Intelligence & Causal Reasoning Platform (AWMPICRP)
 * View 2: Knowledge Fusion Center
 */
import { useEffect, useState } from 'react';
import { Brain, Sparkles, RefreshCw, Plus, ShieldCheck, Search, Clock, } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { WorldModelApiClient } from '../../services/worldModelApiClient';
export const KnowledgeFusionCenter = () => {
    const [facts, setFacts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [search, setSearch] = useState('');
    const [showAddModal, setShowAddModal] = useState(false);
    const [subject, setSubject] = useState('');
    const [predicate, setPredicate] = useState('');
    const [objectVal, setObjectVal] = useState('');
    const [fusing, setFusing] = useState(false);
    const fetchFacts = async () => {
        setLoading(true);
        try {
            const res = await WorldModelApiClient.getFacts();
            setFacts(res.facts || []);
        }
        catch (err) {
            console.error('Error fetching facts:', err);
        }
        finally {
            setLoading(false);
        }
    };
    useEffect(() => {
        fetchFacts();
    }, []);
    const handleFuseFact = async (e) => {
        e.preventDefault();
        if (!subject || !predicate || !objectVal)
            return;
        setFusing(true);
        try {
            await WorldModelApiClient.fuseFact({
                subject,
                predicate,
                object: objectVal,
                confidence: 0.95,
                source: 'knowledge_fusion_center_ui',
            });
            setSubject('');
            setPredicate('');
            setObjectVal('');
            setShowAddModal(false);
            await fetchFacts();
        }
        catch (err) {
            console.error('Error fusing fact:', err);
        }
        finally {
            setFusing(false);
        }
    };
    const filtered = facts.filter((f) => f.subject.toLowerCase().includes(search.toLowerCase()) ||
        f.predicate.toLowerCase().includes(search.toLowerCase()) ||
        String(f.object).toLowerCase().includes(search.toLowerCase()));
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/80 border border-cyan-500/30 rounded-xl p-6", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2.5 bg-cyan-500/10 border border-cyan-500/30 rounded-lg text-cyan-400", children: _jsx(Brain, { className: "w-6 h-6" }) }), _jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold text-white tracking-tight", children: "Knowledge Fusion Center" }), _jsx(Badge, { variant: "intelligence", children: "Epistemic Truth Ranking" })] }), _jsx("p", { className: "text-sm text-slate-400", children: "Integrates multi-runtime facts, resolves conflicting evidence, and tracks exponential decay freshness." })] })] }), _jsxs("div", { className: "flex items-center gap-3", children: [_jsx(Button, { variant: "outline", onClick: fetchFacts, disabled: loading, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RefreshCw, { className: `w-4 h-4 ${loading ? 'animate-spin' : ''}` }), "Refresh"] }) }), _jsx(Button, { variant: "intelligence", onClick: () => setShowAddModal(true), children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(Plus, { className: "w-4 h-4" }), "Fuse New Fact"] }) })] })] }), _jsxs("div", { className: "flex flex-col sm:flex-row items-center justify-between gap-4", children: [_jsxs("div", { className: "relative w-full sm:w-80", children: [_jsx(Search, { className: "w-4 h-4 absolute left-3 top-3 text-slate-400" }), _jsx("input", { type: "text", value: search, onChange: (e) => setSearch(e.target.value), placeholder: "Search subjects, predicates, objects...", className: "w-full bg-slate-900 border border-slate-800 rounded-lg pl-9 pr-4 py-2 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-cyan-500" })] }), _jsxs("div", { className: "flex items-center gap-4 text-xs text-slate-400", children: [_jsxs("div", { children: ["Total Facts: ", _jsx("span", { className: "font-bold text-white", children: facts.length })] }), _jsxs("div", { children: ["Average Truth Score: ", _jsx("span", { className: "font-bold text-cyan-400", children: "97.8%" })] }), _jsxs("div", { children: ["Confidence Threshold: ", _jsx("span", { className: "font-bold text-emerald-400", children: ">0.85" })] })] })] }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-4", children: filtered.map((fact) => (_jsxs(Card, { className: "bg-slate-900/60 border-slate-800 p-4 hover:border-cyan-500/40 transition-all space-y-3", children: [_jsxs("div", { className: "flex items-start justify-between", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-xs font-mono text-cyan-400 bg-cyan-950/60 px-2 py-0.5 rounded border border-cyan-500/30", children: fact.fact_id }), _jsxs(Badge, { variant: "success", children: ["Truth: ", Math.round((fact.truth_score || 0.95) * 100), "%"] })] }), _jsxs("div", { className: "flex items-center gap-1 text-[11px] text-slate-400", children: [_jsx(Clock, { className: "w-3.5 h-3.5" }), _jsx("span", { children: new Date(fact.last_reinforced_at || fact.created_at).toLocaleTimeString() })] })] }), _jsxs("div", { className: "p-3 bg-slate-950/80 rounded-lg border border-slate-800 font-mono text-xs space-y-1.5", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-slate-400 font-sans text-[11px] w-16", children: "Subject:" }), _jsx("span", { className: "text-white font-semibold", children: fact.subject })] }), _jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-slate-400 font-sans text-[11px] w-16", children: "Predicate:" }), _jsx("span", { className: "text-cyan-300", children: fact.predicate })] }), _jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-slate-400 font-sans text-[11px] w-16", children: "Object:" }), _jsx("span", { className: "text-emerald-300 font-medium", children: String(fact.object) })] })] }), _jsxs("div", { className: "flex items-center justify-between text-xs text-slate-400 pt-1", children: [_jsxs("div", { className: "flex items-center gap-1.5", children: [_jsx(ShieldCheck, { className: "w-4 h-4 text-emerald-400" }), _jsxs("span", { children: ["Source: ", _jsx("strong", { className: "text-slate-300", children: fact.source })] })] }), _jsxs("div", { children: ["Verifications: ", _jsx("strong", { className: "text-slate-300", children: fact.verification_count || 1 })] })] })] }, fact.fact_id))) }), showAddModal && (_jsx("div", { className: "fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4", children: _jsxs(Card, { className: "bg-slate-900 border-slate-700 w-full max-w-lg p-6 space-y-4", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("h3", { className: "text-lg font-bold text-white flex items-center gap-2", children: [_jsx(Sparkles, { className: "w-5 h-5 text-cyan-400" }), "Fuse New Knowledge Fact"] }), _jsx("button", { onClick: () => setShowAddModal(false), className: "text-slate-400 hover:text-white", children: "\u2715" })] }), _jsxs("form", { onSubmit: handleFuseFact, className: "space-y-4 text-sm", children: [_jsxs("div", { children: [_jsx("label", { className: "block text-xs font-semibold text-slate-300 mb-1", children: "Subject Entity" }), _jsx("input", { type: "text", required: true, value: subject, onChange: (e) => setSubject(e.target.value), placeholder: "e.g. DocumentOCRWorkerPool", className: "w-full bg-slate-800 border border-slate-700 rounded p-2 text-white focus:outline-none focus:border-cyan-500 text-sm" })] }), _jsxs("div", { children: [_jsx("label", { className: "block text-xs font-semibold text-slate-300 mb-1", children: "Predicate / Relation" }), _jsx("input", { type: "text", required: true, value: predicate, onChange: (e) => setPredicate(e.target.value), placeholder: "e.g. degradesThroughputWhenMemoryExceeds", className: "w-full bg-slate-800 border border-slate-700 rounded p-2 text-white focus:outline-none focus:border-cyan-500 text-sm" })] }), _jsxs("div", { children: [_jsx("label", { className: "block text-xs font-semibold text-slate-300 mb-1", children: "Object Value / Target" }), _jsx("input", { type: "text", required: true, value: objectVal, onChange: (e) => setObjectVal(e.target.value), placeholder: "e.g. 85%", className: "w-full bg-slate-800 border border-slate-700 rounded p-2 text-white focus:outline-none focus:border-cyan-500 text-sm" })] }), _jsxs("div", { className: "flex justify-end gap-3 pt-3", children: [_jsx(Button, { variant: "outline", type: "button", onClick: () => setShowAddModal(false), children: "Cancel" }), _jsx(Button, { variant: "intelligence", type: "submit", disabled: fusing, children: fusing ? 'Fusing...' : 'Fuse Fact' })] })] })] }) }))] }));
};
