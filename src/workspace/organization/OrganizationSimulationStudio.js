import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { Boxes, RotateCw, Sparkles, AlertTriangle, } from 'lucide-react';
import { organizationPlatformApiClient } from '../../services/organizationPlatformApiClient';
export const OrganizationSimulationStudio = () => {
    const [reports, setReports] = useState([]);
    const [loading, setLoading] = useState(true);
    const [simulating, setSimulating] = useState(false);
    const [selectedReport, setSelectedReport] = useState(null);
    const loadReports = async () => {
        try {
            setLoading(true);
            const data = await organizationPlatformApiClient.getSimulations();
            setReports(data);
            if (data.length > 0 && !selectedReport) {
                setSelectedReport(data[0] || null);
            }
        }
        catch (err) {
            console.error('Failed to load simulations:', err);
        }
        finally {
            setLoading(false);
        }
    };
    useEffect(() => {
        loadReports();
    }, []);
    const handleRunSimulation = async () => {
        try {
            setSimulating(true);
            const rep = await organizationPlatformApiClient.runSimulation(100);
            await loadReports();
            setSelectedReport(rep);
        }
        catch (err) {
            console.error('Error running organizational simulation:', err);
        }
        finally {
            setSimulating(false);
        }
    };
    return (_jsxs("div", { className: "space-y-6 p-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-border pb-4", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2 bg-primary/10 rounded-lg text-primary", children: _jsx(Boxes, { className: "w-6 h-6" }) }), _jsxs("div", { children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Digital Twin Organization Simulator" }), _jsx("p", { className: "text-sm text-muted-foreground", children: "Synthetic Enterprise Sandbox, Stress Testing, Chaos Fault Injections & Resilience Certification" })] })] }), _jsxs("div", { className: "flex items-center gap-3", children: [_jsx(Button, { variant: "outline", onClick: loadReports, disabled: loading, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RotateCw, { className: `w-4 h-4 ${loading ? 'animate-spin' : ''}` }), "Refresh"] }) }), _jsx(Button, { variant: "intelligence", onClick: handleRunSimulation, disabled: simulating, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(Sparkles, { className: "w-4 h-4" }), simulating ? 'Simulating 100 Twins...' : 'Run 100-Twin Stress Test'] }) })] })] }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-3 gap-6", children: [_jsxs("div", { className: "space-y-4", children: [_jsxs("h2", { className: "text-sm font-semibold", children: ["Simulation Runs (", reports.length, ")"] }), _jsx("div", { className: "space-y-3", children: reports.map((r) => (_jsx(Card, { onClick: () => setSelectedReport(r), className: `border cursor-pointer transition-all ${selectedReport?.report_id === r.report_id
                                        ? 'border-primary bg-primary/5 shadow-sm'
                                        : 'border-border hover:bg-muted/30'}`, children: _jsxs(CardContent, { className: "p-4 space-y-2", children: [_jsxs("div", { className: "flex justify-between items-start", children: [_jsx("span", { className: "font-semibold text-sm line-clamp-1", children: r.scenario_name }), _jsxs(Badge, { variant: r.success_rate >= 0.95 ? 'success' : 'warning', children: [(r.success_rate * 100).toFixed(0), "% Pass"] })] }), _jsxs("div", { className: "flex justify-between text-xs text-muted-foreground pt-1", children: [_jsxs("span", { children: ["Runs: ", r.runs_completed] }), _jsxs("span", { children: ["Resilience: ", (r.resilience_score * 100).toFixed(0), "%"] })] })] }) }, r.report_id))) })] }), _jsx("div", { className: "lg:col-span-2 space-y-6", children: selectedReport ? (_jsxs(Card, { className: "border-border shadow-sm", children: [_jsxs(CardHeader, { className: "flex flex-row items-center justify-between pb-3", children: [_jsxs("div", { children: [_jsx(CardTitle, { className: "text-lg", children: selectedReport.scenario_name }), _jsx("p", { className: "text-xs text-muted-foreground font-mono mt-0.5", children: selectedReport.report_id })] }), _jsx(Badge, { variant: "success", children: selectedReport.simulation_type })] }), _jsxs(CardContent, { className: "space-y-4", children: [_jsxs("div", { className: "grid grid-cols-2 md:grid-cols-4 gap-3", children: [_jsxs("div", { className: "p-3 bg-muted/40 border border-border rounded-lg text-center", children: [_jsx("div", { className: "text-xs text-muted-foreground", children: "Success Rate" }), _jsxs("div", { className: "text-xl font-bold text-emerald-500 mt-0.5", children: [(selectedReport.success_rate * 100).toFixed(1), "%"] })] }), _jsxs("div", { className: "p-3 bg-muted/40 border border-border rounded-lg text-center", children: [_jsx("div", { className: "text-xs text-muted-foreground", children: "Mean ROI" }), _jsxs("div", { className: "text-xl font-bold text-primary mt-0.5", children: [selectedReport.mean_roi_multiplier, "x"] })] }), _jsxs("div", { className: "p-3 bg-muted/40 border border-border rounded-lg text-center", children: [_jsx("div", { className: "text-xs text-muted-foreground", children: "p95 Latency" }), _jsxs("div", { className: "text-xl font-bold mt-0.5", children: [selectedReport.p95_latency_ms, " ms"] })] }), _jsxs("div", { className: "p-3 bg-muted/40 border border-border rounded-lg text-center", children: [_jsx("div", { className: "text-xs text-muted-foreground", children: "Resilience Score" }), _jsxs("div", { className: "text-xl font-bold text-purple-500 mt-0.5", children: [(selectedReport.resilience_score * 100).toFixed(0), "%"] })] })] }), _jsxs("div", { className: "space-y-2", children: [_jsxs("h3", { className: "text-sm font-semibold flex items-center gap-2", children: [_jsx(AlertTriangle, { className: "w-4 h-4 text-amber-500" }), "Tested Chaos Stress Conditions"] }), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-3 gap-2 text-xs", children: [_jsxs("div", { className: "p-2.5 bg-card border border-border rounded-lg", children: [_jsx("span", { className: "font-semibold text-foreground", children: "GPU Driver Failures" }), _jsx("p", { className: "text-muted-foreground mt-0.5", children: "Instant worker failover to CPU backup nodes." })] }), _jsxs("div", { className: "p-2.5 bg-card border border-border rounded-lg", children: [_jsx("span", { className: "font-semibold text-foreground", children: "Workload 3x Surge" }), _jsx("p", { className: "text-muted-foreground mt-0.5", children: "Dynamic DAG horizontal worker autoscaling." })] }), _jsxs("div", { className: "p-2.5 bg-card border border-border rounded-lg", children: [_jsx("span", { className: "font-semibold text-foreground", children: "Agent Deadlock Resolution" }), _jsx("p", { className: "text-muted-foreground mt-0.5", children: "Nash arbitration triggers within 120ms." })] })] })] })] })] })) : (_jsx(Card, { className: "border-border shadow-sm p-8 text-center text-muted-foreground", children: "Select a simulation report to inspect digital twin telemetry." })) })] })] }));
};
