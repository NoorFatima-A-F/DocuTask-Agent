import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { ShieldAlert, } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
export const SLAIntelligenceCenter = () => {
    const [slaItems] = useState([
        {
            id: 'sla_inv_gold',
            process: 'End-to-End Enterprise Invoice Processing',
            target: '2h 00m',
            elapsed: '45m 12s',
            riskScore: 0.12,
            status: 'HEALTHY',
            escalationRole: 'role_finance_director',
        },
        {
            id: 'sla_vendor_kyc',
            process: 'Global Vendor Onboarding & AML Clearance',
            target: '24h 00m',
            elapsed: '20h 30m',
            riskScore: 0.88,
            status: 'ELEVATED_RISK',
            escalationRole: 'role_compliance_officer',
        },
    ]);
    return (_jsxs("div", { className: "space-y-6", children: [_jsx("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/60 p-6 rounded-2xl border border-slate-800 backdrop-blur-md", children: _jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2 bg-indigo-500/10 rounded-xl border border-indigo-500/20 text-indigo-400", children: _jsx(ShieldAlert, { className: "w-6 h-6" }) }), _jsxs("div", { children: [_jsx("h1", { className: "text-2xl font-bold text-white", children: "SLA Intelligence & Breach Predictor" }), _jsx("p", { className: "text-sm text-slate-400", children: "Proactive hazard modeling, turnaround deadline countdowns, and automated role escalations" })] })] }) }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-6", children: slaItems.map((item) => (_jsxs(Card, { className: "p-6 bg-slate-900/40 border-slate-800 space-y-4", children: [_jsxs("div", { className: "flex justify-between items-start", children: [_jsxs("div", { children: [_jsx("h2", { className: "text-base font-bold text-white", children: item.process }), _jsxs("span", { className: "text-xs text-slate-400 font-mono", children: ["Contract: ", item.id] })] }), _jsx(Badge, { variant: item.status === 'HEALTHY' ? 'success' : 'warning', children: item.status })] }), _jsxs("div", { className: "grid grid-cols-2 gap-3 text-xs font-mono", children: [_jsxs("div", { className: "p-3 bg-slate-800/40 rounded-lg border border-slate-700/60", children: [_jsx("span", { className: "text-slate-400 block text-[11px]", children: "SLA Target" }), _jsx("span", { className: "text-white font-bold text-sm", children: item.target })] }), _jsxs("div", { className: "p-3 bg-slate-800/40 rounded-lg border border-slate-700/60", children: [_jsx("span", { className: "text-slate-400 block text-[11px]", children: "Current Elapsed" }), _jsx("span", { className: "text-indigo-300 font-bold text-sm", children: item.elapsed })] })] }), _jsxs("div", { children: [_jsxs("div", { className: "flex justify-between text-xs mb-1", children: [_jsx("span", { className: "text-slate-400", children: "Breach Hazard Probability" }), _jsxs("span", { className: "font-mono font-bold text-amber-400", children: [(item.riskScore * 100).toFixed(0), "%"] })] }), _jsx("div", { className: "w-full bg-slate-800 h-2 rounded-full overflow-hidden", children: _jsx("div", { className: `h-full rounded-full transition-all ${item.riskScore > 0.5 ? 'bg-amber-500' : 'bg-emerald-500'}`, style: { width: `${item.riskScore * 100}%` } }) })] }), _jsxs("div", { className: "pt-2 border-t border-slate-800 text-xs text-slate-400 flex justify-between items-center", children: [_jsx("span", { children: "Auto-Escalation Target:" }), _jsx("span", { className: "font-mono text-cyan-300", children: item.escalationRole })] })] }, item.id))) })] }));
};
