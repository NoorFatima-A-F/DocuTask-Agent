import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { Server, RotateCw, Activity, } from 'lucide-react';
import { executionPlatformApiClient } from '../../services/executionPlatformApiClient';
export const ConnectorManagementCenter = () => {
    const [connectors, setConnectors] = useState([]);
    const [testingId, setTestingId] = useState(null);
    const [loading, setLoading] = useState(true);
    const loadConnectors = async () => {
        try {
            setLoading(true);
            const res = await executionPlatformApiClient.listConnectors();
            setConnectors(res.connectors || []);
        }
        catch (err) {
            console.error('Failed to load connectors:', err);
        }
        finally {
            setLoading(false);
        }
    };
    useEffect(() => {
        loadConnectors();
    }, []);
    const handleTestConnector = async (connectorId) => {
        try {
            setTestingId(connectorId);
            await executionPlatformApiClient.testConnector(connectorId);
            await loadConnectors();
        }
        catch (err) {
            console.error('Error testing connector:', err);
        }
        finally {
            setTestingId(null);
        }
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-slate-900/60 p-6 rounded-2xl border border-slate-800", children: [_jsxs("div", { children: [_jsxs("h1", { className: "text-xl font-bold text-white flex items-center gap-2", children: [_jsx(Server, { className: "w-5 h-5 text-emerald-400" }), "Universal Connector Framework & Gateway Hub"] }), _jsx("p", { className: "text-slate-400 text-sm mt-1", children: "Real-time connection pooling, round-trip latency probes, protocol adapters (REST, gRPC, DBs, Cloud SDKs)" })] }), _jsx(Button, { variant: "outline", onClick: loadConnectors, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RotateCw, { className: "w-4 h-4" }), "Refresh"] }) })] }), loading && connectors.length === 0 ? (_jsx("p", { className: "text-xs text-slate-500 py-8 text-center", children: "Loading connectors..." })) : (_jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4", children: connectors.map((c) => (_jsxs(Card, { className: "bg-slate-900/60 border-slate-800 flex flex-col justify-between", children: [_jsxs(CardHeader, { className: "pb-2", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx(Badge, { variant: "outline", className: "text-xs", children: c.category }), _jsxs(Badge, { variant: c.status === 'connected' ? 'success' : 'error', className: "flex items-center gap-1", children: [_jsx("span", { className: "w-1.5 h-1.5 rounded-full bg-emerald-400" }), c.status] })] }), _jsx(CardTitle, { className: "text-base text-white mt-2", children: c.name })] }), _jsxs(CardContent, { className: "space-y-4", children: [_jsxs("div", { className: "text-xs space-y-1.5 font-mono text-slate-400", children: [_jsxs("p", { className: "truncate", children: [_jsx("span", { className: "text-slate-500", children: "Endpoint:" }), " ", c.endpoint_url] }), _jsxs("p", { children: [_jsx("span", { className: "text-slate-500", children: "Protocol:" }), " ", c.protocol] }), _jsxs("p", { children: [_jsx("span", { className: "text-slate-500", children: "Latency:" }), " ", c.latency_ms, " ms"] }), _jsxs("p", { children: [_jsx("span", { className: "text-slate-500", children: "RPM:" }), " ", c.rpm_used, " / ", c.rate_limit_rpm] })] }), _jsxs("div", { className: "pt-2 border-t border-slate-800 flex items-center justify-between", children: [_jsxs("span", { className: "text-[11px] text-emerald-400 font-semibold", children: ["Health: ", (c.health_score * 100).toFixed(0), "%"] }), _jsx(Button, { variant: "outline", className: "text-xs", onClick: () => handleTestConnector(c.connector_id), disabled: testingId === c.connector_id, children: _jsxs("span", { className: "flex items-center gap-1.5", children: [_jsx(Activity, { className: "w-3.5 h-3.5 text-emerald-400" }), testingId === c.connector_id ? 'Probing...' : 'Probe Health'] }) })] })] })] }, c.connector_id))) }))] }));
};
