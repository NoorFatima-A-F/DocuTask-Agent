import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { ShieldAlert, Sparkles, CheckCircle, } from 'lucide-react';
import { ApdlePlannerApiClient } from '../../services/apdlePlannerApiClient';
export const RecoveryGraphViewer = () => {
    const [injected, setInjected] = useState(false);
    const [loading, setLoading] = useState(false);
    const handleSimulateRecovery = async () => {
        setLoading(true);
        try {
            await ApdlePlannerApiClient.triggerReplan('default_mission', 'node_ocr_01', 'Low OCR Confidence Holdout Scan (0.38)');
            setInjected(true);
        }
        catch (e) {
            console.error('Recovery failed:', e);
        }
        finally {
            setLoading(false);
        }
    };
    return (_jsx("div", { className: "space-y-6 font-mono", children: _jsxs("div", { className: "bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-4", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-3", children: [_jsxs("div", { children: [_jsxs("h3", { className: "text-sm font-bold text-cyan-300 flex items-center gap-2", children: [_jsx(ShieldAlert, { className: "w-4 h-4 text-purple-400" }), "Autonomous Recovery DAG Subsystem"] }), _jsx("p", { className: "text-xs text-slate-400 mt-0.5", children: "Replaces blind retry loops with executable recovery DAG branches (Deskewing $\\to$ Schema Relaxation $\\to$ Re-validation)." })] }), _jsxs("button", { onClick: handleSimulateRecovery, disabled: loading, className: "flex items-center gap-1.5 px-3 py-1.5 bg-purple-950/60 hover:bg-purple-900/60 border border-purple-800 text-purple-300 rounded-lg text-xs font-mono transition-all disabled:opacity-50", children: [_jsx(Sparkles, { className: `w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}` }), "Inject Recovery Pipeline"] })] }), injected && (_jsxs("div", { className: "p-3 bg-emerald-950/40 border border-emerald-800/80 rounded-lg flex items-center gap-2 text-xs text-emerald-300", children: [_jsx(CheckCircle, { className: "w-4 h-4 text-emerald-400 shrink-0" }), _jsx("span", { children: "Recovery subgraph successfully injected! Generation incremented and wavefront re-evaluated." })] })), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-3 gap-4", children: [_jsxs("div", { className: "p-4 bg-slate-950/80 border border-red-800/60 rounded-xl space-y-2 text-xs", children: [_jsx("div", { className: "text-[10px] text-red-400 uppercase font-bold", children: "1. Failure Point" }), _jsx("div", { className: "text-sm font-bold text-slate-100", children: "Adaptive OCR Scan" }), _jsx("div", { className: "text-[11px] text-slate-400", children: "Low confidence scan (0.38 < 0.70 threshold)" }), _jsx("div", { className: "text-[10px] text-red-400 font-bold", children: "STATUS: FAILED / MUTATED" })] }), _jsxs("div", { className: "p-4 bg-slate-950/80 border border-purple-800/80 rounded-xl space-y-2 text-xs", children: [_jsx("div", { className: "text-[10px] text-purple-400 uppercase font-bold", children: "2. Injected Recovery Branch" }), _jsx("div", { className: "text-sm font-bold text-purple-200", children: "Image Contrast & Deskew Filter" }), _jsx("div", { className: "text-[11px] text-slate-400", children: "Pre-processes image raster before secondary OCR pass" }), _jsx("div", { className: "text-[10px] text-purple-400 font-bold", children: "STATUS: INJECTED & EXECUTING" })] }), _jsxs("div", { className: "p-4 bg-slate-950/80 border border-emerald-800/60 rounded-xl space-y-2 text-xs", children: [_jsx("div", { className: "text-[10px] text-emerald-400 uppercase font-bold", children: "3. Resume Target" }), _jsx("div", { className: "text-sm font-bold text-slate-100", children: "Table Line-Item Parsing" }), _jsx("div", { className: "text-[11px] text-slate-400", children: "Consumes recovered high-resolution OCR text" }), _jsx("div", { className: "text-[10px] text-emerald-400 font-bold", children: "STATUS: READY TO RESUME" })] })] })] }) }));
};
