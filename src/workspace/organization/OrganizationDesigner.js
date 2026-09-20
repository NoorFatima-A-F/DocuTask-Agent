import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { Network, RotateCw, Sparkles, Users, } from 'lucide-react';
import { organizationPlatformApiClient } from '../../services/organizationPlatformApiClient';
export const OrganizationDesigner = () => {
    const [org, setOrg] = useState(null);
    const [loading, setLoading] = useState(true);
    const [restructuring, setRestructuring] = useState(false);
    const [selectedDept, setSelectedDept] = useState(null);
    const loadStructure = async () => {
        try {
            setLoading(true);
            const data = await organizationPlatformApiClient.getStructure();
            setOrg(data);
            if (data.departments.length > 0 && !selectedDept) {
                setSelectedDept(data.departments[0] || null);
            }
        }
        catch (err) {
            console.error('Failed to load organization structure:', err);
        }
        finally {
            setLoading(false);
        }
    };
    useEffect(() => {
        loadStructure();
    }, []);
    const handleRestructure = async () => {
        try {
            setRestructuring(true);
            const res = await fetch('/api/v1/organization/restructure?org_id=org_enterprise_root', {
                method: 'POST',
            });
            const data = await res.json();
            setOrg(data);
        }
        catch (err) {
            console.error('Error restructuring organization:', err);
        }
        finally {
            setRestructuring(false);
        }
    };
    return (_jsxs("div", { className: "space-y-6 p-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-border pb-4", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2 bg-primary/10 rounded-lg text-primary", children: _jsx(Network, { className: "w-6 h-6" }) }), _jsxs("div", { children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "AI Organization Designer" }), _jsx("p", { className: "text-sm text-muted-foreground", children: "Dynamic Department Structuring, Autonomous Team Formation & Span-of-Control Optimization" })] })] }), _jsxs("div", { className: "flex items-center gap-3", children: [_jsx(Button, { variant: "outline", onClick: loadStructure, disabled: loading, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RotateCw, { className: `w-4 h-4 ${loading ? 'animate-spin' : ''}` }), "Refresh"] }) }), _jsx(Button, { variant: "intelligence", onClick: handleRestructure, disabled: restructuring, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(Sparkles, { className: "w-4 h-4" }), restructuring ? 'Optimizing...' : 'Re-Optimize Hierarchy'] }) })] })] }), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-4 gap-4", children: [_jsx(Card, { className: "border-border shadow-sm", children: _jsxs(CardContent, { className: "p-4", children: [_jsx("div", { className: "text-xs text-muted-foreground", children: "Operational Efficiency" }), _jsx("div", { className: "text-2xl font-bold text-emerald-500 mt-1", children: org ? `${(org.operational_efficiency * 100).toFixed(1)}%` : '95.0%' }), _jsx("p", { className: "text-xs text-muted-foreground mt-0.5", children: "Redundancy eliminated" })] }) }), _jsx(Card, { className: "border-border shadow-sm", children: _jsxs(CardContent, { className: "p-4", children: [_jsx("div", { className: "text-xs text-muted-foreground", children: "Span of Control" }), _jsx("div", { className: "text-2xl font-bold text-primary mt-1", children: org ? org.span_of_control : 3.8 }), _jsx("p", { className: "text-xs text-muted-foreground mt-0.5", children: "Average teams per head" })] }) }), _jsx(Card, { className: "border-border shadow-sm", children: _jsxs(CardContent, { className: "p-4", children: [_jsx("div", { className: "text-xs text-muted-foreground", children: "Departments Formed" }), _jsx("div", { className: "text-2xl font-bold mt-1", children: org?.departments.length ?? 3 }), _jsx("p", { className: "text-xs text-muted-foreground mt-0.5", children: "Active specialized units" })] }) }), _jsx(Card, { className: "border-border shadow-sm", children: _jsxs(CardContent, { className: "p-4", children: [_jsx("div", { className: "text-xs text-muted-foreground", children: "Executive Board" }), _jsx("div", { className: "text-2xl font-bold text-purple-500 mt-1", children: org?.executive_board.length ?? 3 }), _jsx("p", { className: "text-xs text-muted-foreground mt-0.5", children: "CEO, CTO & CFO agents" })] }) })] }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-3 gap-6", children: [_jsxs("div", { className: "space-y-4", children: [_jsx("h2", { className: "text-sm font-semibold", children: "Active Departments" }), _jsx("div", { className: "space-y-3", children: org?.departments.map((d) => (_jsx(Card, { onClick: () => setSelectedDept(d), className: `border cursor-pointer transition-all ${selectedDept?.department_id === d.department_id
                                        ? 'border-primary bg-primary/5 shadow-sm'
                                        : 'border-border hover:bg-muted/30'}`, children: _jsxs(CardContent, { className: "p-4 space-y-2", children: [_jsxs("div", { className: "flex justify-between items-start", children: [_jsx("span", { className: "font-semibold text-sm", children: d.name }), _jsx(Badge, { variant: "outline", children: d.head_role })] }), _jsxs("div", { className: "flex items-center justify-between text-xs text-muted-foreground pt-1", children: [_jsxs("span", { children: ["Teams: ", d.teams.length] }), _jsxs("span", { className: "text-emerald-500 font-medium", children: ["Health: ", (d.health_score * 100).toFixed(0), "%"] })] })] }) }, d.department_id))) })] }), _jsx("div", { className: "lg:col-span-2 space-y-6", children: selectedDept ? (_jsxs(Card, { className: "border-border shadow-sm", children: [_jsxs(CardHeader, { className: "flex flex-row items-center justify-between pb-3", children: [_jsxs("div", { children: [_jsx(CardTitle, { className: "text-lg", children: selectedDept.name }), _jsxs("p", { className: "text-xs text-muted-foreground mt-0.5", children: ["Lead: ", _jsx("span", { className: "font-mono text-primary", children: selectedDept.head_role })] })] }), _jsxs("div", { className: "text-right text-xs", children: [_jsx("div", { className: "text-muted-foreground", children: "Budget Allocated:" }), _jsxs("div", { className: "font-semibold text-sm", children: ["$", selectedDept.budget_allocated_usd.toLocaleString()] })] })] }), _jsxs(CardContent, { className: "space-y-4", children: [_jsxs("div", { children: [_jsx("h3", { className: "text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-2", children: "Department Capabilities" }), _jsx("div", { className: "flex flex-wrap gap-1.5", children: selectedDept.capabilities.map((cap) => (_jsx(Badge, { variant: "intelligence", children: cap }, cap))) })] }), _jsxs("div", { children: [_jsxs("h3", { className: "text-sm font-semibold mb-2 flex items-center gap-2", children: [_jsx(Users, { className: "w-4 h-4 text-primary" }), "Autonomous Teams (", selectedDept.teams.length, ")"] }), _jsx("div", { className: "space-y-3", children: selectedDept.teams.map((t) => (_jsxs("div", { className: "p-3 bg-muted/30 border border-border rounded-lg space-y-2 text-xs", children: [_jsxs("div", { className: "flex justify-between items-center", children: [_jsx("span", { className: "font-semibold text-sm text-foreground", children: t.name }), _jsxs("span", { className: "text-emerald-500 font-medium", children: ["Productivity: ", (t.productivity_score * 100).toFixed(0), "%"] })] }), _jsx("p", { className: "text-muted-foreground", children: t.mission_scope }), _jsxs("div", { className: "flex items-center gap-4 text-muted-foreground pt-1 border-t border-border/60", children: [_jsxs("span", { children: ["Team Lead: ", _jsx("strong", { className: "text-foreground", children: t.lead_role })] }), _jsxs("span", { children: ["Active Tasks: ", _jsx("strong", { className: "text-foreground", children: t.active_task_count })] }), _jsxs("span", { children: ["Workers: ", _jsx("strong", { className: "text-foreground", children: t.member_agent_ids.length })] })] })] }, t.team_id))) })] })] })] })) : (_jsx(Card, { className: "border-border shadow-sm p-8 text-center text-muted-foreground", children: "Select a department to view autonomous teams and capability assignments." })) })] })] }));
};
