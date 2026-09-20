import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { Cpu, RotateCw, Sparkles, Zap, HardDrive, DollarSign, PieChart, } from 'lucide-react';
import { organizationPlatformApiClient } from '../../services/organizationPlatformApiClient';
export const ResourceOptimizationCenter = () => {
    const [pool, setPool] = useState(null);
    const [plan, setPlan] = useState(null);
    const [loading, setLoading] = useState(true);
    const [optimizing, setOptimizing] = useState(false);
    const loadResources = async () => {
        try {
            setLoading(true);
            const data = await organizationPlatformApiClient.getResources();
            setPool(data.pool);
            setPlan(data.allocation_plan);
        }
        catch (err) {
            console.error('Failed to load resources:', err);
        }
        finally {
            setLoading(false);
        }
    };
    useEffect(() => {
        loadResources();
    }, []);
    const handleOptimize = async () => {
        try {
            setOptimizing(true);
            const newPlan = await organizationPlatformApiClient.optimizeResources('COST_EFFICIENCY');
            setPlan(newPlan);
            await loadResources();
        }
        catch (err) {
            console.error('Error optimizing resources:', err);
        }
        finally {
            setOptimizing(false);
        }
    };
    return (_jsxs("div", { className: "space-y-6 p-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-border pb-4", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2 bg-primary/10 rounded-lg text-primary", children: _jsx(Cpu, { className: "w-6 h-6" }) }), _jsxs("div", { children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Resource Allocation Intelligence" }), _jsx("p", { className: "text-sm text-muted-foreground", children: "Multi-Tenant Compute Slots, Token Quota Distribution, Memory Footprints & Pareto Budget Optimization" })] })] }), _jsxs("div", { className: "flex items-center gap-3", children: [_jsx(Button, { variant: "outline", onClick: loadResources, disabled: loading, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RotateCw, { className: `w-4 h-4 ${loading ? 'animate-spin' : ''}` }), "Refresh"] }) }), _jsx(Button, { variant: "intelligence", onClick: handleOptimize, disabled: optimizing, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(Sparkles, { className: "w-4 h-4" }), optimizing ? 'Solving Simplex...' : 'Run Pareto Optimization'] }) })] })] }), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-4 gap-4", children: [_jsx(Card, { className: "border-border shadow-sm", children: _jsxs(CardContent, { className: "p-4 space-y-2", children: [_jsxs("div", { className: "flex justify-between items-center text-xs text-muted-foreground", children: [_jsx("span", { children: "Compute Slots" }), _jsx(Cpu, { className: "w-4 h-4 text-primary" })] }), _jsxs("div", { className: "text-2xl font-bold", children: [pool?.compute_slots_used ?? 38, " / ", pool?.compute_slots_total ?? 64] }), _jsx("div", { className: "w-full bg-muted rounded-full h-1.5 overflow-hidden", children: _jsx("div", { className: "bg-primary h-full rounded-full", style: { width: `${((pool?.compute_slots_used ?? 38) / (pool?.compute_slots_total ?? 64)) * 100}%` } }) })] }) }), _jsx(Card, { className: "border-border shadow-sm", children: _jsxs(CardContent, { className: "p-4 space-y-2", children: [_jsxs("div", { className: "flex justify-between items-center text-xs text-muted-foreground", children: [_jsx("span", { children: "Monthly Tokens" }), _jsx(Zap, { className: "w-4 h-4 text-amber-500" })] }), _jsxs("div", { className: "text-2xl font-bold", children: [pool ? `${(pool.tokens_consumed / 1_000_000).toFixed(1)}M` : '54.2M', " /", ' ', pool ? `${(pool.token_budget_monthly / 1_000_000).toFixed(0)}M` : '150M'] }), _jsx("div", { className: "w-full bg-muted rounded-full h-1.5 overflow-hidden", children: _jsx("div", { className: "bg-amber-500 h-full rounded-full", style: { width: `${((pool?.tokens_consumed ?? 54.2) / (pool?.token_budget_monthly ?? 150)) * 100}%` } }) })] }) }), _jsx(Card, { className: "border-border shadow-sm", children: _jsxs(CardContent, { className: "p-4 space-y-2", children: [_jsxs("div", { className: "flex justify-between items-center text-xs text-muted-foreground", children: [_jsx("span", { children: "Vector Memory (GB)" }), _jsx(HardDrive, { className: "w-4 h-4 text-emerald-500" })] }), _jsxs("div", { className: "text-2xl font-bold", children: [pool?.memory_gb_used ?? 210.5, " / ", pool?.memory_gb_total ?? 512, " GB"] }), _jsx("div", { className: "w-full bg-muted rounded-full h-1.5 overflow-hidden", children: _jsx("div", { className: "bg-emerald-500 h-full rounded-full", style: { width: `${((pool?.memory_gb_used ?? 210.5) / (pool?.memory_gb_total ?? 512)) * 100}%` } }) })] }) }), _jsx(Card, { className: "border-border shadow-sm", children: _jsxs(CardContent, { className: "p-4 space-y-2", children: [_jsxs("div", { className: "flex justify-between items-center text-xs text-muted-foreground", children: [_jsx("span", { children: "Monthly Budget" }), _jsx(DollarSign, { className: "w-4 h-4 text-blue-500" })] }), _jsxs("div", { className: "text-2xl font-bold", children: ["$", pool?.dollar_budget_spent_usd.toLocaleString() ?? '16,800', " / $", pool?.dollar_budget_total_usd.toLocaleString() ?? '50,000'] }), _jsx("div", { className: "w-full bg-muted rounded-full h-1.5 overflow-hidden", children: _jsx("div", { className: "bg-blue-500 h-full rounded-full", style: { width: `${((pool?.dollar_budget_spent_usd ?? 16800) / (pool?.dollar_budget_total_usd ?? 50000)) * 100}%` } }) })] }) })] }), _jsxs(Card, { className: "border-border shadow-sm", children: [_jsxs(CardHeader, { className: "flex flex-row items-center justify-between pb-3", children: [_jsxs(CardTitle, { className: "text-base flex items-center gap-2", children: [_jsx(PieChart, { className: "w-4 h-4 text-primary" }), "Department Quota Allocations"] }), _jsxs(Badge, { variant: "success", children: ["PARETO OPTIMAL (", (plan?.overall_efficiency_score ?? 0.95) * 100, "%)"] })] }), _jsx(CardContent, { children: _jsx("div", { className: "overflow-x-auto", children: _jsxs("table", { className: "w-full text-sm", children: [_jsx("thead", { children: _jsxs("tr", { className: "border-b border-border text-left text-muted-foreground", children: [_jsx("th", { className: "pb-2 font-medium", children: "Department" }), _jsx("th", { className: "pb-2 font-medium", children: "Compute Slots" }), _jsx("th", { className: "pb-2 font-medium", children: "Token Quota / Mo" }), _jsx("th", { className: "pb-2 font-medium", children: "Memory" }), _jsx("th", { className: "pb-2 font-medium", children: "Budget Share" }), _jsx("th", { className: "pb-2 font-medium", children: "Priority Weight" })] }) }), _jsx("tbody", { className: "divide-y divide-border/60", children: plan?.quotas.map((q) => (_jsxs("tr", { className: "hover:bg-muted/30 transition-colors", children: [_jsx("td", { className: "py-3 font-semibold", children: q.department_name }), _jsxs("td", { className: "py-3 font-mono text-primary font-medium", children: [q.compute_slots, " slots"] }), _jsxs("td", { className: "py-3 text-muted-foreground font-mono", children: [(q.token_quota_monthly / 1_000_000).toFixed(0), "M tokens"] }), _jsxs("td", { className: "py-3 font-mono", children: [q.memory_gb, " GB"] }), _jsxs("td", { className: "py-3 font-semibold", children: ["$", q.budget_allocated_usd.toLocaleString()] }), _jsxs("td", { className: "py-3 font-mono", children: [q.priority_weight, "x"] })] }, q.department_id))) })] }) }) })] })] }));
};
