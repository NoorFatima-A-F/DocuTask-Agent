import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Rocket, RotateCcw, RefreshCw, Activity, Clock, } from 'lucide-react';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { EvolutionPlatformApiClient } from '../../services/evolutionPlatformApiClient';
export const DeploymentControlCenter = () => {
    const [deployments, setDeployments] = useState([]);
    const [loading, setLoading] = useState(true);
    const [actionLoading, setActionLoading] = useState(null);
    useEffect(() => {
        loadDeployments();
    }, []);
    const loadDeployments = async () => {
        setLoading(true);
        try {
            const data = await EvolutionPlatformApiClient.listDeployments();
            setDeployments(data);
        }
        catch (err) {
            console.error('Failed to load deployments:', err);
        }
        finally {
            setLoading(false);
        }
    };
    const handleAdvanceTraffic = async (deploymentId, targetPct) => {
        setActionLoading(deploymentId);
        try {
            const updated = await EvolutionPlatformApiClient.advanceCanary(deploymentId, targetPct);
            setDeployments((prev) => prev.map((d) => (d.deployment_id === deploymentId ? updated : d)));
        }
        catch (err) {
            console.error('Failed to advance canary:', err);
        }
        finally {
            setActionLoading(null);
        }
    };
    const handleRollback = async (deploymentId) => {
        setActionLoading(deploymentId);
        try {
            const updated = await EvolutionPlatformApiClient.rollbackDeployment(deploymentId, 'Manual operator rollback');
            setDeployments((prev) => prev.map((d) => (d.deployment_id === deploymentId ? updated : d)));
        }
        catch (err) {
            console.error('Failed to rollback:', err);
        }
        finally {
            setActionLoading(null);
        }
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "bg-gradient-to-r from-slate-900 via-slate-900 to-slate-950 border border-slate-800 rounded-2xl p-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-4 shadow-xl", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2.5 bg-emerald-500/10 border border-emerald-500/20 rounded-xl", children: _jsx(Rocket, { className: "w-6 h-6 text-emerald-400" }) }), _jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-xl font-bold text-slate-100", children: "Progressive Canary & Blue/Green Deployment" }), _jsx(Badge, { variant: "success", size: "sm", children: "Automated Rollback Safeguard" })] }), _jsx("p", { className: "text-sm text-slate-400 mt-0.5", children: "Control progressive canary rollout percentages with real-time SLA circuit-breakers and instant rollback capability." })] })] }), _jsx("div", { className: "flex items-center gap-3", children: _jsx(Button, { variant: "outline", onClick: loadDeployments, disabled: loading, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RefreshCw, { className: `w-4 h-4 ${loading ? 'animate-spin' : ''}` }), "Refresh"] }) }) })] }), _jsx("div", { className: "space-y-5", children: deployments.map((dep) => (_jsxs("div", { className: "bg-slate-900/80 border border-slate-800 rounded-xl p-6 space-y-5 shadow-lg", children: [_jsxs("div", { className: "flex flex-col md:flex-row md:items-center justify-between gap-3 pb-4 border-b border-slate-800", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("h2", { className: "text-lg font-bold text-slate-100 font-mono", children: dep.deployment_id }), _jsx(Badge, { variant: dep.deployment_state === 'PROMOTED'
                                                        ? 'success'
                                                        : dep.deployment_state === 'ROLLED_BACK'
                                                            ? 'error'
                                                            : 'intelligence', size: "sm", children: dep.deployment_state })] }), _jsxs("span", { className: "text-xs text-slate-400 font-mono mt-1 block", children: ["Target Version: ", _jsx("span", { className: "text-slate-200 font-semibold", children: dep.target_version }), " \u2022 Mutation: ", dep.mutation_id] })] }), dep.deployment_state !== 'ROLLED_BACK' && (_jsx("div", { className: "flex items-center gap-2", children: _jsx(Button, { variant: "danger", size: "sm", onClick: () => handleRollback(dep.deployment_id), disabled: actionLoading === dep.deployment_id, children: _jsxs("span", { className: "flex items-center gap-1.5", children: [_jsx(RotateCcw, { className: "w-3.5 h-3.5" }), "Emergency Rollback"] }) }) }))] }), _jsxs("div", { className: "space-y-2", children: [_jsxs("div", { className: "flex items-center justify-between text-xs font-mono text-slate-300", children: [_jsx("span", { children: "Canary Traffic Routing" }), _jsxs("span", { className: "font-bold text-emerald-400", children: [dep.canary_traffic_pct.toFixed(0), "% Production Load"] })] }), _jsx("div", { className: "w-full bg-slate-950 h-3 rounded-full border border-slate-800 overflow-hidden", children: _jsx("div", { className: "bg-emerald-400 h-full rounded-full transition-all duration-500", style: { width: `${dep.canary_traffic_pct}%` } }) }), dep.deployment_state !== 'ROLLED_BACK' && dep.canary_traffic_pct < 100 && (_jsxs("div", { className: "flex items-center gap-2 pt-2", children: [_jsx(Button, { variant: "outline", size: "sm", onClick: () => handleAdvanceTraffic(dep.deployment_id, 25), disabled: actionLoading === dep.deployment_id, children: "Promote to 25%" }), _jsx(Button, { variant: "outline", size: "sm", onClick: () => handleAdvanceTraffic(dep.deployment_id, 50), disabled: actionLoading === dep.deployment_id, children: "Promote to 50%" }), _jsx(Button, { variant: "intelligence", size: "sm", onClick: () => handleAdvanceTraffic(dep.deployment_id, 100), disabled: actionLoading === dep.deployment_id, children: "Full 100% Blue/Green Promotion" })] }))] }), _jsxs("div", { className: "grid grid-cols-1 sm:grid-cols-3 gap-4 font-mono text-xs", children: [_jsxs("div", { className: "p-3 bg-slate-950/80 border border-slate-800 rounded-lg space-y-1", children: [_jsx("div", { className: "flex items-center justify-between text-slate-400", children: _jsxs("span", { className: "flex items-center gap-1.5", children: [_jsx(Clock, { className: "w-3.5 h-3.5 text-indigo-400" }), "Live P95 Latency"] }) }), _jsxs("div", { className: "text-base font-bold text-indigo-300", children: [dep.live_p95_latency_ms.toFixed(1), "ms"] }), _jsxs("div", { className: "text-[10px] text-slate-500", children: ["Threshold: ", dep.auto_rollback_latency_threshold_ms, "ms"] })] }), _jsxs("div", { className: "p-3 bg-slate-950/80 border border-slate-800 rounded-lg space-y-1", children: [_jsx("div", { className: "flex items-center justify-between text-slate-400", children: _jsxs("span", { className: "flex items-center gap-1.5", children: [_jsx(Activity, { className: "w-3.5 h-3.5 text-emerald-400" }), "Live Error Rate"] }) }), _jsxs("div", { className: "text-base font-bold text-emerald-300", children: [(dep.live_error_rate * 100).toFixed(3), "%"] }), _jsxs("div", { className: "text-[10px] text-slate-500", children: ["Threshold: ", (dep.auto_rollback_error_threshold * 100).toFixed(1), "%"] })] }), _jsxs("div", { className: "p-3 bg-slate-950/80 border border-slate-800 rounded-lg space-y-1", children: [_jsx("div", { className: "text-slate-400", children: "Rollback Snapshot Link" }), _jsx("div", { className: "text-xs font-semibold text-purple-400 truncate", children: dep.rollback_snapshot_id || 'snap_prod_v13_12' }), _jsx("div", { className: "text-[10px] text-slate-500", children: "Circuit-breaker armed" })] })] })] }, dep.deployment_id))) })] }));
};
