import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { SaaSApiClient } from '../../services/saasApiClient';
import { LayoutGrid, FolderGit2, HardDrive, Users, RefreshCw } from 'lucide-react';
export const WorkspaceExplorer = () => {
    const [workspaces, setWorkspaces] = useState([]);
    const [projects, setProjects] = useState([]);
    const [loading, setLoading] = useState(true);
    useEffect(() => {
        const load = async () => {
            setLoading(true);
            const [ws, prj] = await Promise.all([
                SaaSApiClient.listWorkspaces('tenant_acme_corp'),
                SaaSApiClient.listProjects('tenant_acme_corp'),
            ]);
            setWorkspaces(ws);
            setProjects(prj);
            setLoading(false);
        };
        load();
    }, []);
    return (_jsxs("div", { className: "space-y-6", children: [_jsx("div", { className: "flex items-center justify-between", children: _jsxs("div", { children: [_jsxs("h1", { className: "text-2xl font-bold text-white flex items-center gap-3", children: [_jsx(LayoutGrid, { className: "w-7 h-7 text-indigo-400" }), "Workspaces & Project Namespaces"] }), _jsx("p", { className: "text-sm text-slate-400 mt-1", children: "Scoped team workspaces, agent allocations, storage quotas, and autonomous pipelines." })] }) }), loading ? (_jsxs("div", { className: "p-12 text-center text-slate-400", children: [_jsx(RefreshCw, { className: "w-6 h-6 animate-spin mx-auto mb-2" }), " Loading Workspaces..."] })) : (_jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-6", children: workspaces.map((ws) => {
                    const wsProjects = projects.filter((p) => p.workspace_id === ws.workspace_id);
                    return (_jsxs(Card, { className: "bg-slate-900/80 border-slate-800", children: [_jsx(CardHeader, { children: _jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("div", { children: [_jsx(CardTitle, { className: "text-lg text-white", children: ws.name }), _jsx("span", { className: "text-xs font-mono text-slate-400", children: ws.workspace_id })] }), _jsx(Badge, { variant: "intelligence", children: ws.slug })] }) }), _jsxs(CardContent, { className: "space-y-4", children: [_jsxs("div", { className: "grid grid-cols-2 gap-3 text-xs bg-slate-800/40 p-3 rounded", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx(Users, { className: "w-4 h-4 text-indigo-400" }), _jsxs("div", { children: [_jsx("span", { className: "text-slate-400 block text-[10px]", children: "Allocated Agents" }), _jsxs("span", { className: "font-bold text-white", children: [ws.allocated_agents_count, " Concurrency"] })] })] }), _jsxs("div", { className: "flex items-center gap-2", children: [_jsx(HardDrive, { className: "w-4 h-4 text-cyan-400" }), _jsxs("div", { children: [_jsx("span", { className: "text-slate-400 block text-[10px]", children: "Storage Quota" }), _jsxs("span", { className: "font-bold text-white", children: [ws.allocated_storage_gb, " GB"] })] })] })] }), _jsxs("div", { children: [_jsxs("span", { className: "text-xs font-semibold text-slate-400 uppercase tracking-wider block mb-2", children: ["Active Projects (", wsProjects.length, ")"] }), _jsxs("div", { className: "space-y-2", children: [wsProjects.map((p) => (_jsxs("div", { className: "p-3 bg-slate-800/60 rounded border border-slate-700/60 flex items-center justify-between", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx(FolderGit2, { className: "w-4 h-4 text-emerald-400" }), _jsxs("div", { children: [_jsx("span", { className: "text-sm font-medium text-slate-200 block", children: p.name }), _jsx("span", { className: "text-xs text-slate-400", children: p.description })] })] }), _jsxs(Badge, { variant: "success", className: "text-[10px]", children: [p.active_workflows_count, " Workflows"] })] }, p.project_id))), wsProjects.length === 0 && (_jsx("p", { className: "text-xs text-slate-500 italic", children: "No projects initialized yet." }))] })] })] })] }, ws.workspace_id));
                }) }))] }));
};
