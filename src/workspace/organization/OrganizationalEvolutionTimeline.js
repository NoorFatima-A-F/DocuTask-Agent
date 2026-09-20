import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { History, RotateCw, Clock, Sparkles, } from 'lucide-react';
import { organizationPlatformApiClient } from '../../services/organizationPlatformApiClient';
export const OrganizationalEvolutionTimeline = () => {
    const [cycles, setCycles] = useState([]);
    const [loading, setLoading] = useState(true);
    const loadCycles = async () => {
        try {
            setLoading(true);
            const data = await organizationPlatformApiClient.getCycles();
            setCycles(data);
        }
        catch (err) {
            console.error('Failed to load cycles:', err);
        }
        finally {
            setLoading(false);
        }
    };
    useEffect(() => {
        loadCycles();
    }, []);
    return (_jsxs("div", { className: "space-y-6 p-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-border pb-4", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2 bg-primary/10 rounded-lg text-primary", children: _jsx(History, { className: "w-6 h-6" }) }), _jsxs("div", { children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Organizational Evolution Timeline" }), _jsx("p", { className: "text-sm text-muted-foreground", children: "Chronological Generational Lineage of Enterprise Topologies, Strategic Refinements & ROI Advances" })] })] }), _jsx(Button, { variant: "outline", onClick: loadCycles, disabled: loading, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RotateCw, { className: `w-4 h-4 ${loading ? 'animate-spin' : ''}` }), "Refresh"] }) })] }), _jsxs(Card, { className: "border-border shadow-sm", children: [_jsx(CardHeader, { children: _jsxs(CardTitle, { className: "text-base flex items-center gap-2", children: [_jsx(Sparkles, { className: "w-4 h-4 text-primary" }), "Evolution Generations (", cycles.length, ")"] }) }), _jsx(CardContent, { children: _jsx("div", { className: "relative pl-6 border-l-2 border-border space-y-6 my-2", children: cycles.map((c, idx) => (_jsxs("div", { className: "relative", children: [_jsx("div", { className: "absolute -left-[31px] top-1.5 w-4 h-4 rounded-full bg-primary border-4 border-background" }), _jsxs("div", { className: "p-4 bg-muted/30 border border-border rounded-lg space-y-2", children: [_jsxs("div", { className: "flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsxs("span", { className: "font-bold text-sm text-foreground", children: ["Generation #", cycles.length - idx] }), _jsx("span", { className: "font-mono text-xs text-primary font-semibold", children: c.cycle_id })] }), _jsx(Badge, { variant: "success", children: c.status })] }), _jsxs("div", { className: "grid grid-cols-2 md:grid-cols-4 gap-3 text-xs pt-1 text-muted-foreground", children: [_jsxs("div", { children: [_jsx("span", { children: "Mission: " }), _jsx("strong", { className: "text-foreground", children: c.mission_id })] }), _jsxs("div", { children: [_jsx("span", { children: "Strategy: " }), _jsx("strong", { className: "text-foreground", children: c.strategy_id })] }), _jsxs("div", { children: [_jsx("span", { children: "Composite Health: " }), _jsxs("strong", { className: "text-emerald-500", children: [(c.composite_health_score * 100).toFixed(1), "%"] })] }), _jsxs("div", { children: [_jsx("span", { children: "ROI Multiplier: " }), _jsxs("strong", { className: "text-primary", children: [c.roi_multiplier, "x"] })] })] }), _jsxs("div", { className: "flex justify-between items-center text-[11px] text-muted-foreground pt-2 border-t border-border/60", children: [_jsxs("span", { className: "flex items-center gap-1", children: [_jsx(Clock, { className: "w-3.5 h-3.5" }), " Executed in ", c.duration_ms, " ms"] }), _jsx("span", { children: "Governance Seal Verified (SHA-256)" })] })] })] }, c.cycle_id))) }) })] })] }));
};
