import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
export const PlatformDiagnosticsView = () => {
    const diagnostics = {
        kernelStatus: 'OPERATIONAL',
        uptimeSeconds: 84920,
        activeThreads: 12,
        diContainerInstances: 18,
        capabilityProvidersOnline: 9,
        policyEvaluationsTotal: 1420,
        policyViolationCount: 0,
        sandboxEnclavesActive: 4,
        merkleDagIntegrity: '100.0% VERIFIED',
        gcLatencyMs: 0.8,
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Platform OS Diagnostics" }), _jsx(Badge, { variant: "success", size: "sm", children: "Kernel Healthy" })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Real-time kernel diagnostics, DI container resolutions, capability health radar, and sandbox telemetry." })] }), _jsxs(Badge, { variant: "outline", size: "md", children: ["Uptime: ", (diagnostics.uptimeSeconds / 3600).toFixed(1), " Hours"] })] }), _jsxs("div", { className: "grid grid-cols-2 sm:grid-cols-3 gap-4", children: [_jsxs(Card, { className: "p-4", children: [_jsx("div", { className: "text-xs text-muted-foreground", children: "Kernel Status" }), _jsx("div", { className: "text-lg font-bold font-mono text-emerald-400 mt-1", children: diagnostics.kernelStatus })] }), _jsxs(Card, { className: "p-4", children: [_jsx("div", { className: "text-xs text-muted-foreground", children: "DI Container Singletons" }), _jsx("div", { className: "text-lg font-bold font-mono text-foreground mt-1", children: diagnostics.diContainerInstances })] }), _jsxs(Card, { className: "p-4", children: [_jsx("div", { className: "text-xs text-muted-foreground", children: "Capability Providers" }), _jsxs("div", { className: "text-lg font-bold font-mono text-foreground mt-1", children: [diagnostics.capabilityProvidersOnline, " Online"] })] }), _jsxs(Card, { className: "p-4", children: [_jsx("div", { className: "text-xs text-muted-foreground", children: "Policy Evaluations" }), _jsx("div", { className: "text-lg font-bold font-mono text-foreground mt-1", children: diagnostics.policyEvaluationsTotal })] }), _jsxs(Card, { className: "p-4", children: [_jsx("div", { className: "text-xs text-muted-foreground", children: "Policy Violations" }), _jsx("div", { className: "text-lg font-bold font-mono text-emerald-400 mt-1", children: diagnostics.policyViolationCount })] }), _jsxs(Card, { className: "p-4", children: [_jsx("div", { className: "text-xs text-muted-foreground", children: "Merkle DAG Integrity" }), _jsx("div", { className: "text-lg font-bold font-mono text-emerald-400 mt-1", children: diagnostics.merkleDagIntegrity })] })] })] }));
};
