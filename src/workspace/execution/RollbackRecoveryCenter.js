import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { Undo2, RotateCw, } from 'lucide-react';
import { executionPlatformApiClient } from '../../services/executionPlatformApiClient';
export const RollbackRecoveryCenter = () => {
    const [rollbacks, setRollbacks] = useState([]);
    const [loading, setLoading] = useState(true);
    const loadRollbacks = async () => {
        try {
            setLoading(true);
            const res = await executionPlatformApiClient.listRollbacks();
            setRollbacks(res.rollbacks || []);
        }
        catch (err) {
            console.error('Failed to load rollbacks:', err);
        }
        finally {
            setLoading(false);
        }
    };
    useEffect(() => {
        loadRollbacks();
    }, []);
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-slate-900/60 p-6 rounded-2xl border border-slate-800", children: [_jsxs("div", { children: [_jsxs("h1", { className: "text-xl font-bold text-white flex items-center gap-2", children: [_jsx(Undo2, { className: "w-5 h-5 text-rose-400" }), "Saga Rollback & Checkpoint Recovery Center"] }), _jsx("p", { className: "text-slate-400 text-sm mt-1", children: "Automated compensating transaction dispatcher, LIFO inverse execution & zero-residue cleanup" })] }), _jsx(Button, { variant: "outline", onClick: loadRollbacks, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RotateCw, { className: "w-4 h-4" }), "Refresh"] }) })] }), _jsxs(Card, { className: "bg-slate-900/60 border-slate-800", children: [_jsx(CardHeader, { children: _jsxs(CardTitle, { className: "text-base text-white", children: ["Compensating Rollback Sessions (", rollbacks.length, ")"] }) }), _jsx(CardContent, { children: loading && rollbacks.length === 0 ? (_jsx("div", { className: "py-8 text-center text-xs text-slate-500", children: "Loading rollbacks..." })) : rollbacks.length === 0 ? (_jsx("div", { className: "py-12 text-center text-sm text-slate-500", children: "No rollback events recorded. All production execution pipelines have completed with clean invariants." })) : (_jsx("div", { className: "space-y-4", children: rollbacks.map((rb) => (_jsxs("div", { className: "p-4 bg-slate-950 border border-slate-800 rounded-xl space-y-3", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-2", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-sm font-bold text-white", children: rb.trigger_reason }), _jsx(Badge, { variant: rb.status === 'completed' ? 'success' : 'error', children: rb.status.toUpperCase() })] }), _jsxs("p", { className: "text-xs text-slate-400 font-mono mt-1", children: ["Rollback ID: ", rb.rollback_id, " \u2022 Mission: ", rb.mission_id] })] }), _jsxs("span", { className: "text-xs text-slate-400", children: [rb.completed_compensations, " / ", rb.steps_to_compensate.length, " Inverses Executed"] })] }), _jsx("div", { className: "pl-4 border-l-2 border-rose-800/60 space-y-2", children: rb.steps_to_compensate.map((step) => (_jsxs("div", { className: "p-2.5 bg-slate-900/80 rounded-lg border border-slate-800 flex items-center justify-between text-xs", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx(Undo2, { className: "w-3.5 h-3.5 text-rose-400" }), _jsxs("span", { className: "text-slate-200", children: ["Undoing: ", _jsx("span", { className: "font-mono text-purple-300", children: step.original_step_id })] }), _jsx("span", { className: "text-slate-500", children: "via" }), _jsx("span", { className: "font-mono text-slate-400", children: step.compensation_tool_id })] }), _jsx(Badge, { variant: "success", children: step.status })] }, step.compensation_id))) })] }, rb.rollback_id))) })) })] })] }));
};
