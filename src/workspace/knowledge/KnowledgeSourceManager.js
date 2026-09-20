import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Database, RefreshCw } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { knowledgeApiClient } from '../../services/knowledgeApiClient';
export const KnowledgeSourceManager = () => {
    const [sources, setSources] = useState([]);
    const [syncingId, setSyncingId] = useState(null);
    const loadSources = async () => {
        const data = await knowledgeApiClient.listSources();
        setSources(data);
    };
    useEffect(() => {
        loadSources();
    }, []);
    const handleSync = async (srcId) => {
        setSyncingId(srcId);
        try {
            await fetch(`/api/v1/knowledge/sources/${srcId}/sync?tenant_id=default-tenant`, { method: 'POST' });
            await loadSources();
        }
        finally {
            setSyncingId(null);
        }
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsx("div", { className: "flex justify-between items-center", children: _jsxs("div", { children: [_jsxs("h1", { className: "text-2xl font-bold text-slate-100 flex items-center gap-2", children: [_jsx(Database, { className: "w-7 h-7 text-indigo-400" }), "Enterprise Data Source & Connector Manager"] }), _jsx("p", { className: "text-slate-400 text-sm mt-1", children: "Manage real-time sync connectors for Google Drive, Confluence, SharePoint, Slack, Jira, and Salesforce." })] }) }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-4", children: sources.map((src) => (_jsxs(Card, { className: "p-5 bg-slate-900/60 border-slate-800 flex flex-col justify-between", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex justify-between items-start mb-2", children: [_jsx(Badge, { variant: "outline", className: "text-indigo-400 border-indigo-500/30 font-mono", children: src.source_type }), _jsx(Badge, { variant: src.health_status === 'HEALTHY' ? 'success' : 'warning', children: src.health_status })] }), _jsx("h3", { className: "text-lg font-semibold text-slate-200 mb-1", children: src.name }), _jsxs("p", { className: "text-xs text-slate-400 mb-4 font-mono", children: ["Sync Cron: ", src.sync_schedule, " | Synced Assets: ", src.total_assets_synced] })] }), _jsxs("div", { className: "pt-3 border-t border-slate-800 flex justify-between items-center", children: [_jsxs("span", { className: "text-xs text-slate-400", children: ["Status: ", src.is_active ? 'Active Auto-Sync' : 'Paused'] }), _jsx(Button, { variant: "intelligence", size: "sm", onClick: () => handleSync(src.id), disabled: syncingId === src.id, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RefreshCw, { className: `w-3.5 h-3.5 ${syncingId === src.id ? 'animate-spin' : ''}` }), syncingId === src.id ? 'Syncing...' : 'Trigger Sync'] }) })] })] }, src.id))) })] }));
};
