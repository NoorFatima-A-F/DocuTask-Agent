import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { SaaSApiClient } from '../../services/saasApiClient';
import { Radio, CheckCircle2, Activity, RefreshCw } from 'lucide-react';
export const IntegrationHub = () => {
    const [connectors, setConnectors] = useState([]);
    const [testResults, setTestResults] = useState({});
    const [loading, setLoading] = useState(true);
    useEffect(() => {
        const load = async () => {
            setLoading(true);
            const list = await SaaSApiClient.listIntegrations('tenant_acme_corp');
            setConnectors(list);
            setLoading(false);
        };
        load();
    }, []);
    const handleTest = async (connectorId) => {
        setTestResults((prev) => ({ ...prev, [connectorId]: 'TESTING...' }));
        const res = await SaaSApiClient.testConnector(connectorId);
        setTestResults((prev) => ({ ...prev, [connectorId]: `${res.status} (${res.latency_ms}ms)` }));
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsx("div", { className: "flex items-center justify-between", children: _jsxs("div", { children: [_jsxs("h1", { className: "text-2xl font-bold text-white flex items-center gap-3", children: [_jsx(Radio, { className: "w-7 h-7 text-indigo-400" }), "Enterprise Integration Hub"] }), _jsx("p", { className: "text-sm text-slate-400 mt-1", children: "Connect autonomous agent meshes to Google Drive, Teams, Slack, SAP, Salesforce, Jira, and GitHub." })] }) }), loading ? (_jsxs("div", { className: "p-12 text-center text-slate-400", children: [_jsx(RefreshCw, { className: "w-6 h-6 animate-spin mx-auto mb-2" }), " Loading Connectors..."] })) : (_jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 gap-6", children: connectors.map((c) => {
                    const testStatus = testResults[c.connector_id];
                    return (_jsxs(Card, { className: "bg-slate-900/80 border-slate-800", children: [_jsx(CardHeader, { children: _jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("div", { children: [_jsx(CardTitle, { className: "text-lg text-white", children: c.name }), _jsx("span", { className: "text-xs font-mono text-slate-400", children: c.connector_type })] }), _jsx(Badge, { variant: c.status === 'CONNECTED' ? 'success' : 'error', children: c.status })] }) }), _jsxs(CardContent, { className: "space-y-4", children: [_jsxs("div", { className: "text-xs text-slate-400 space-y-1 bg-slate-800/40 p-3 rounded", children: [_jsxs("div", { children: ["Auth Type: ", _jsx("span", { className: "text-slate-200 font-mono", children: c.auth_type })] }), _jsxs("div", { children: ["Last Synced: ", _jsx("span", { className: "text-slate-200", children: new Date(c.last_synced_at).toLocaleTimeString() })] }), _jsxs("div", { children: ["Connected Workspaces: ", _jsx("span", { className: "text-indigo-400 font-mono", children: c.connected_workspaces.join(', ') })] })] }), _jsxs("div", { className: "flex items-center justify-between pt-2", children: [testStatus && (_jsxs("span", { className: "text-xs font-mono text-emerald-400 flex items-center gap-1", children: [_jsx(CheckCircle2, { className: "w-3.5 h-3.5" }), " ", testStatus] })), !testStatus && _jsx("span", { className: "text-xs text-slate-500", children: "Ready for ping test" }), _jsx(Button, { variant: "outline", onClick: () => handleTest(c.connector_id), children: _jsxs("span", { className: "flex items-center gap-1.5 text-xs", children: [_jsx(Activity, { className: "w-3.5 h-3.5" }), " Test Link"] }) })] })] })] }, c.connector_id));
                }) }))] }));
};
