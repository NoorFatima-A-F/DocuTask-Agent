import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { SaaSApiClient } from '../../services/saasApiClient';
import { Network, Building, FolderTree, MapPin, RefreshCw } from 'lucide-react';
export const OrganizationManager = () => {
    const [tree, setTree] = useState([]);
    const [loading, setLoading] = useState(true);
    useEffect(() => {
        const fetchTree = async () => {
            setLoading(true);
            const data = await SaaSApiClient.getOrganizationTree('tenant_acme_corp');
            setTree(data);
            setLoading(false);
        };
        fetchTree();
    }, []);
    const renderNode = (node, depth = 0) => (_jsxs("div", { className: "space-y-3", style: { marginLeft: `${depth * 24}px` }, children: [_jsxs("div", { className: "p-4 rounded-lg bg-slate-800/60 border border-slate-700 flex items-center justify-between", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx(Building, { className: "w-5 h-5 text-indigo-400" }), _jsxs("div", { children: [_jsx("span", { className: "text-sm font-semibold text-white block", children: node.name }), _jsxs("span", { className: "text-xs text-slate-400", children: [node.business_unit, " \u2022 ", node.organization_id] })] })] }), _jsxs("div", { className: "flex items-center gap-3", children: [_jsxs(Badge, { variant: "outline", className: "flex items-center gap-1 text-xs", children: [_jsx(MapPin, { className: "w-3 h-3" }), " ", node.country_code] }), _jsx(Badge, { variant: "info", children: "Org Node" })] })] }), node.children && node.children.map((child) => renderNode(child, depth + 1))] }, node.organization_id));
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("div", { children: [_jsxs("h1", { className: "text-2xl font-bold text-white flex items-center gap-3", children: [_jsx(Network, { className: "w-7 h-7 text-indigo-400" }), "Enterprise Organization Hierarchy"] }), _jsx("p", { className: "text-sm text-slate-400 mt-1", children: "Hierarchical multi-level structure: Tenant \u2192 Divisions \u2192 Business Units \u2192 Labs." })] }), _jsxs(Badge, { variant: "intelligence", className: "px-3 py-1", children: [_jsx(FolderTree, { className: "w-4 h-4 mr-1 inline" }), " Tree View"] })] }), _jsxs(Card, { className: "bg-slate-900/80 border-slate-800", children: [_jsx(CardHeader, { children: _jsx(CardTitle, { className: "text-base text-white", children: "Acme Corporation Global Division Tree" }) }), _jsx(CardContent, { className: "space-y-4", children: loading ? (_jsxs("div", { className: "p-8 text-center text-slate-400", children: [_jsx(RefreshCw, { className: "w-6 h-6 animate-spin mx-auto mb-2" }), " Loading hierarchy..."] })) : (tree.map((root) => renderNode(root))) })] })] }));
};
