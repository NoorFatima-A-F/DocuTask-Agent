import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { TrustIndicator } from '../../components/ui/TrustIndicator';
export const ConfidenceJourneyPanel = () => {
    const journeyMilestones = [
        {
            percentage: 41,
            delta: '+41%',
            reason: 'Raw Objective Ingested & Entity Model Structured',
            agent: 'Coordinator Agent',
            time: '09:15:00',
            trust: 'OBSERVED',
        },
        {
            percentage: 56,
            delta: '+15%',
            reason: 'Memory Recall of 18 Prior Thermal Invoices',
            agent: 'Memory Agent',
            time: '09:15:05',
            trust: 'VERIFIED',
        },
        {
            percentage: 74,
            delta: '+18%',
            reason: 'Ground Truth SROIE Annotation Matching (n=53)',
            agent: 'Evidence Agent',
            time: '09:15:10',
            trust: 'EMPIRICAL',
        },
        {
            percentage: 83,
            delta: '+9%',
            reason: 'Closed-Loop Bayesian Hyperparameter Convergence (x*=0.6800)',
            agent: 'Execution Agent',
            time: '09:22:40',
            trust: 'EMPIRICAL',
        },
        {
            percentage: 90,
            delta: '+7%',
            reason: '10-Fold Holdout Cross-Validation & Zero Regression Check',
            agent: 'Reflection Agent',
            time: '09:22:43',
            trust: 'VERIFIED',
        },
        {
            percentage: 97.2,
            delta: '+7.2%',
            reason: 'Statistical Power Verified (Power=0.84 >= 0.80, p=0.0012)',
            agent: 'Statistics Agent',
            time: '09:22:45',
            trust: 'VERIFIED',
        },
    ];
    return (_jsxs("div", { className: "w-full flex flex-col h-[700px] rounded-2xl bg-[#0F172A]/90 border border-[#1E293B] shadow-2xl overflow-hidden", children: [_jsxs(CardHeader, { className: "flex flex-row items-center justify-between py-4 px-6 border-b border-[#1E293B] bg-[#131D35]/50", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx(Badge, { variant: "intelligence", size: "sm", children: "CONFIDENCE TRAJECTORY" }), _jsx("span", { className: "text-xs text-[#94A3B8] font-mono", children: "Empirical Delta Attribution" })] }), _jsx(CardTitle, { className: "mt-1 text-base font-bold text-[#F8FAFC]", children: "The Confidence Journey (41% \u2794 97.2%)" })] }), _jsx("div", { className: "text-xs font-mono text-[#00D2FF] bg-[#0A0F1D] px-3.5 py-1.5 rounded-lg border border-cyan-500/30 font-bold", children: "Target Exceeded: +2.2% above SLA" })] }), _jsxs(CardContent, { className: "flex-1 overflow-y-auto p-6 space-y-6", children: [_jsx("p", { className: "text-xs text-[#94A3B8] leading-relaxed", children: "Every confidence increment is backed by an observable mathematical or empirical event rather than arbitrary progression:" }), _jsx("div", { className: "relative border-l-2 border-cyan-500/40 ml-4 pl-6 space-y-6", children: journeyMilestones.map((m, idx) => (_jsxs("div", { className: "relative group", children: [_jsxs("div", { className: `absolute -left-[35px] top-1.5 h-6 w-6 rounded-full flex items-center justify-center text-[10px] font-mono font-bold ring-4 ring-[#0F172A] ${idx === journeyMilestones.length - 1
                                        ? 'bg-gradient-to-tr from-[#0066FF] to-[#00D2FF] text-white shadow-[0_0_12px_rgba(0,210,255,0.8)] animate-pulse'
                                        : 'bg-emerald-500 text-slate-900'}`, children: [Math.round(m.percentage), "%"] }), _jsxs("div", { className: "p-4 rounded-xl bg-[#131D35] border border-[#1E293B] group-hover:border-cyan-500/40 transition-all space-y-2", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center justify-between gap-2", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsxs("span", { className: "text-sm font-bold font-mono text-[#00D2FF]", children: [m.percentage, "%"] }), _jsxs("span", { className: "text-xs font-mono text-[#10B981] font-bold", children: ["(", m.delta, ")"] }), _jsx(Badge, { variant: "intelligence", size: "sm", children: m.agent })] }), _jsxs("div", { className: "flex items-center gap-3", children: [_jsx(TrustIndicator, { state: m.trust }), _jsxs("span", { className: "text-xs font-mono text-[#64748B]", children: [m.time, " UTC"] })] })] }), _jsx("p", { className: "text-xs text-[#F8FAFC] font-medium leading-relaxed", children: m.reason })] })] }, m.reason))) })] })] }));
};
