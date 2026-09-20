import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { AlertTriangle, CheckCircle2, Clock, RefreshCw, Zap } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
export const IncidentManagementCenter = ({ missionId = 'cluster-primary-master', }) => {
    const [incidents] = useState([
        {
            id: 'inc-9b2f1a',
            title: 'Worker Thread Crash in Local Tesseract Cluster',
            subsystem: 'WORKERS',
            severity: 'MEDIUM',
            detectedAt: '10:14:02 UTC',
            status: 'RESOLVED',
            healingAction: 'WORKER_RESTART',
            mttrMs: 145,
            impactCost: '$0.00',
        },
        {
            id: 'inc-3e7c8d',
            title: 'Model Rate Limit Spike on Gemini 1.5 Pro',
            subsystem: 'API',
            severity: 'HIGH',
            detectedAt: '09:42:15 UTC',
            status: 'RESOLVED',
            healingAction: 'FALLBACK_MODEL_ENGAGE',
            mttrMs: 82,
            impactCost: '$0.00',
        },
        {
            id: 'inc-1a4f0e',
            title: 'Vector Cache Index Eviction Anomaly',
            subsystem: 'MEMORY',
            severity: 'LOW',
            detectedAt: '08:12:30 UTC',
            status: 'RESOLVED',
            healingAction: 'MEMORY_REPAIR',
            mttrMs: 65,
            impactCost: '$0.00',
        },
    ]);
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("div", { children: [_jsxs("h2", { className: "text-xl font-bold text-slate-100 flex items-center gap-2", children: [_jsx(AlertTriangle, { className: "w-5 h-5 text-amber-400" }), "Autonomous Incident Intelligence & Management Center"] }), _jsxs("p", { className: "text-sm text-slate-400", children: ["Real-time incident detection, correlation clustering, severity classification, and automated healing resolution for: ", _jsx("code", { className: "text-amber-300 font-mono text-xs", children: missionId })] })] }), _jsxs("div", { className: "flex items-center gap-3", children: [_jsx(Badge, { variant: "success", size: "md", children: "Active Incidents: 0" }), _jsxs("button", { className: "flex items-center gap-1.5 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium rounded-lg border border-slate-700", children: [_jsx(RefreshCw, { className: "w-3.5 h-3.5" }), "Sync Incident Stream"] })] })] }), _jsx("div", { className: "space-y-4 font-mono", children: incidents.map((inc) => (_jsx(Card, { className: "p-5 bg-slate-900 border-slate-800 hover:border-slate-700 transition-all", children: _jsxs("div", { className: "flex items-start justify-between", children: [_jsxs("div", { className: "space-y-1.5", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-xs text-slate-400", children: inc.id }), _jsx(Badge, { variant: inc.severity === 'HIGH' ? 'error' : inc.severity === 'MEDIUM' ? 'warning' : 'default', size: "sm", children: inc.severity }), _jsx("span", { className: "text-xs text-indigo-400 font-bold", children: inc.subsystem })] }), _jsx("h3", { className: "text-sm font-bold text-slate-100", children: inc.title }), _jsxs("div", { className: "flex items-center gap-4 text-xs text-slate-400 pt-1", children: [_jsxs("span", { className: "flex items-center gap-1", children: [_jsx(Clock, { className: "w-3.5 h-3.5 text-slate-500" }), "Detected: ", inc.detectedAt] }), _jsxs("span", { className: "flex items-center gap-1 text-emerald-400", children: [_jsx(Zap, { className: "w-3.5 h-3.5" }), "Healed: ", inc.healingAction, " (", inc.mttrMs, "ms)"] })] })] }), _jsxs("div", { className: "text-right space-y-1", children: [_jsxs(Badge, { variant: "success", size: "sm", className: "gap-1", children: [_jsx(CheckCircle2, { className: "w-3 h-3" }), inc.status] }), _jsxs("span", { className: "text-xs text-slate-400 block font-bold", children: ["Loss: ", inc.impactCost] })] })] }) }, inc.id))) })] }));
};
