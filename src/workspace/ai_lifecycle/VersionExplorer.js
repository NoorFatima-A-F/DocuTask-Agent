import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { AILifecycleApiClient } from '../../services/aiLifecycleApiClient';
import { GitCommit, RotateCcw, Check, Sparkles, RefreshCw } from 'lucide-react';
export const VersionExplorer = () => {
    const [versions, setVersions] = useState([]);
    const [activeVersion, setActiveVersion] = useState(null);
    const [loading, setLoading] = useState(true);
    const [rollbackSuccess, setRollbackSuccess] = useState(false);
    useEffect(() => {
        const load = async () => {
            setLoading(true);
            const list = await AILifecycleApiClient.listVersions('agt_acme_invoice_reconciler');
            setVersions(list);
            if (list.length > 0 && list[0])
                setActiveVersion(list[0]);
            setLoading(false);
        };
        load();
    }, []);
    const handleRollback = async (tag) => {
        await AILifecycleApiClient.rollbackVersion('agt_acme_invoice_reconciler', tag);
        setRollbackSuccess(true);
        setTimeout(() => setRollbackSuccess(false), 3000);
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsx("div", { className: "flex items-center justify-between", children: _jsxs("div", { children: [_jsxs("h1", { className: "text-2xl font-bold text-white flex items-center gap-3", children: [_jsx(GitCommit, { className: "w-7 h-7 text-indigo-400" }), "Agent Version Control System (AVCS)"] }), _jsx("p", { className: "text-sm text-slate-400 mt-1", children: "Git-like immutable version history, prompt diffs, accuracy metrics, and instant rollback." })] }) }), loading ? (_jsxs("div", { className: "p-12 text-center text-slate-400", children: [_jsx(RefreshCw, { className: "w-6 h-6 animate-spin mx-auto mb-2" }), " Loading Version History..."] })) : (_jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-3 gap-6", children: [_jsxs(Card, { className: "bg-slate-900/80 border-slate-800 lg:col-span-1", children: [_jsx(CardHeader, { children: _jsxs(CardTitle, { className: "text-base text-white", children: ["Semantic Releases (", versions.length, ")"] }) }), _jsx(CardContent, { className: "space-y-3", children: versions.map((v) => (_jsxs("div", { onClick: () => setActiveVersion(v), className: `p-3 rounded-lg border cursor-pointer transition ${activeVersion?.version_id === v.version_id
                                        ? 'bg-indigo-950/40 border-indigo-500'
                                        : 'bg-slate-800/50 border-slate-700/60 hover:border-slate-600'}`, children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("span", { className: "text-sm font-bold text-white font-mono", children: ["v", v.version_tag] }), _jsxs(Badge, { variant: "success", children: [(v.accuracy_score * 100).toFixed(0), "% Acc"] })] }), _jsx("p", { className: "text-xs text-slate-400 mt-1 truncate", children: v.changelog }), _jsx("span", { className: "text-[10px] text-slate-500 mt-2 block font-mono", children: v.model_family })] }, v.version_id))) })] }), _jsxs(Card, { className: "bg-slate-900/80 border-slate-800 lg:col-span-2", children: [_jsx(CardHeader, { children: _jsxs("div", { className: "flex items-center justify-between", children: [_jsxs(CardTitle, { className: "text-base text-white flex items-center gap-2", children: [_jsx(Sparkles, { className: "w-4 h-4 text-indigo-400" }), " Version v", activeVersion?.version_tag, " Configuration"] }), _jsx(Button, { variant: "outline", onClick: () => activeVersion && handleRollback(activeVersion.version_tag), children: _jsxs("span", { className: "flex items-center gap-1.5 text-xs", children: [rollbackSuccess ? _jsx(Check, { className: "w-3.5 h-3.5 text-emerald-400" }) : _jsx(RotateCcw, { className: "w-3.5 h-3.5" }), "Rollback to v", activeVersion?.version_tag] }) })] }) }), _jsxs(CardContent, { className: "space-y-4", children: [_jsxs("div", { children: [_jsx("label", { className: "text-xs text-slate-400 font-semibold block mb-1", children: "System Prompt Directive" }), _jsx("div", { className: "p-3 bg-slate-950 rounded border border-slate-800 text-xs font-mono text-slate-200", children: activeVersion?.system_prompt })] }), _jsxs("div", { className: "grid grid-cols-2 gap-3", children: [_jsxs("div", { className: "p-3 bg-slate-800/40 rounded border border-slate-700/50 text-xs", children: [_jsx("span", { className: "text-slate-400 block text-[10px]", children: "Bound Tools" }), _jsx("span", { className: "text-slate-200 font-mono mt-1 block", children: activeVersion?.tools.join(', ') || 'None' })] }), _jsxs("div", { className: "p-3 bg-slate-800/40 rounded border border-slate-700/50 text-xs", children: [_jsx("span", { className: "text-slate-400 block text-[10px]", children: "Execution Unit Cost" }), _jsxs("span", { className: "text-emerald-400 font-bold mt-1 block font-mono", children: ["$", activeVersion?.cost_per_execution_usd, " USD"] })] })] })] })] })] }))] }));
};
