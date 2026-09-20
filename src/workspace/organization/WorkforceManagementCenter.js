import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { Users, UserPlus, RotateCw, Sparkles, } from 'lucide-react';
import { organizationPlatformApiClient } from '../../services/organizationPlatformApiClient';
export const WorkforceManagementCenter = () => {
    const [agents, setAgents] = useState([]);
    const [loading, setLoading] = useState(true);
    const [rebalancing, setRebalancing] = useState(false);
    const [hiring, setHiring] = useState(false);
    const [newName, setNewName] = useState('');
    const [newRole, setNewRole] = useState('ENGINEERING_AGENT');
    const loadAgents = async () => {
        try {
            setLoading(true);
            const data = await organizationPlatformApiClient.getAgents();
            setAgents(data);
        }
        catch (err) {
            console.error('Failed to load agents:', err);
        }
        finally {
            setLoading(false);
        }
    };
    useEffect(() => {
        loadAgents();
    }, []);
    const handleRebalance = async () => {
        try {
            setRebalancing(true);
            await organizationPlatformApiClient.optimizeWorkforce();
            await loadAgents();
        }
        catch (err) {
            console.error('Error rebalancing workforce:', err);
        }
        finally {
            setRebalancing(false);
        }
    };
    const handleHire = async (e) => {
        e.preventDefault();
        if (!newName.trim())
            return;
        try {
            setHiring(true);
            await organizationPlatformApiClient.hireAgent(newName, newRole, 'dept_engineering_core', ['pipeline_execution']);
            setNewName('');
            await loadAgents();
        }
        catch (err) {
            console.error('Error hiring agent:', err);
        }
        finally {
            setHiring(false);
        }
    };
    return (_jsxs("div", { className: "space-y-6 p-6", children: [_jsxs("div", { className: "flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-border pb-4", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2 bg-primary/10 rounded-lg text-primary", children: _jsx(Users, { className: "w-6 h-6" }) }), _jsxs("div", { children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Autonomous Workforce Manager" }), _jsx("p", { className: "text-sm text-muted-foreground", children: "Agent Employee Registry, Skill Matrix Profiles, Dynamic Workload Balancing & Capability Upgrades" })] })] }), _jsxs("div", { className: "flex items-center gap-3", children: [_jsx(Button, { variant: "outline", onClick: loadAgents, disabled: loading, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(RotateCw, { className: `w-4 h-4 ${loading ? 'animate-spin' : ''}` }), "Refresh"] }) }), _jsx(Button, { variant: "intelligence", onClick: handleRebalance, disabled: rebalancing, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(Sparkles, { className: "w-4 h-4" }), rebalancing ? 'Rebalancing...' : 'Rebalance Workloads'] }) })] })] }), _jsxs(Card, { className: "border-border shadow-sm", children: [_jsx(CardHeader, { children: _jsxs(CardTitle, { className: "text-base flex items-center gap-2", children: [_jsx(UserPlus, { className: "w-4 h-4 text-primary" }), "Provision Specialized Agent Worker"] }) }), _jsx(CardContent, { children: _jsxs("form", { onSubmit: handleHire, className: "flex flex-col md:flex-row gap-4", children: [_jsx("input", { type: "text", value: newName, onChange: (e) => setNewName(e.target.value), placeholder: "e.g. Smart OCR Normalization Specialist", className: "flex-1 px-3.5 py-2 text-sm rounded-md border border-input bg-background focus:outline-none focus:ring-1 focus:ring-primary" }), _jsxs("select", { value: newRole, onChange: (e) => setNewRole(e.target.value), className: "px-3.5 py-2 text-sm rounded-md border border-input bg-background focus:outline-none focus:ring-1 focus:ring-primary", children: [_jsx("option", { value: "RESEARCH_AGENT", children: "RESEARCH_AGENT" }), _jsx("option", { value: "ENGINEERING_AGENT", children: "ENGINEERING_AGENT" }), _jsx("option", { value: "ANALYST_AGENT", children: "ANALYST_AGENT" }), _jsx("option", { value: "SECURITY_AGENT", children: "SECURITY_AGENT" }), _jsx("option", { value: "OPERATIONS_AGENT", children: "OPERATIONS_AGENT" })] }), _jsx(Button, { type: "submit", variant: "primary", disabled: hiring || !newName.trim(), children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(UserPlus, { className: "w-4 h-4" }), hiring ? 'Provisioning...' : 'Provision Agent'] }) })] }) })] }), _jsx("div", { className: "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4", children: agents.map((agent) => (_jsxs(Card, { className: "border-border shadow-sm hover:border-primary/50 transition-colors", children: [_jsx(CardHeader, { className: "pb-2", children: _jsxs("div", { className: "flex justify-between items-start", children: [_jsxs("div", { children: [_jsx(CardTitle, { className: "text-base", children: agent.name }), _jsx("span", { className: "text-xs text-muted-foreground font-mono", children: agent.agent_id })] }), _jsx(Badge, { variant: agent.status === 'ACTIVE' ? 'success' : agent.status === 'BUSY' ? 'warning' : 'outline', children: agent.status })] }) }), _jsxs(CardContent, { className: "space-y-3", children: [_jsxs("div", { className: "flex justify-between items-center text-xs", children: [_jsx(Badge, { variant: "intelligence", children: agent.role }), _jsxs("span", { className: "text-muted-foreground", children: ["Level ", agent.learning_level, " Specialist"] })] }), _jsxs("div", { className: "space-y-1", children: [_jsxs("div", { className: "flex justify-between text-xs", children: [_jsx("span", { className: "text-muted-foreground", children: "Workload:" }), _jsxs("span", { className: "font-semibold", children: [agent.current_workload_percent, "%"] })] }), _jsx("div", { className: "w-full bg-muted rounded-full h-1.5 overflow-hidden", children: _jsx("div", { className: `h-full rounded-full ${agent.current_workload_percent > 80
                                                    ? 'bg-red-500'
                                                    : agent.current_workload_percent > 50
                                                        ? 'bg-amber-500'
                                                        : 'bg-emerald-500'}`, style: { width: `${Math.min(100, agent.current_workload_percent)}%` } }) })] }), _jsxs("div", { className: "space-y-1", children: [_jsx("div", { className: "text-xs font-semibold text-muted-foreground", children: "Verified Skills:" }), _jsx("div", { className: "flex flex-wrap gap-1", children: agent.skills.map((s) => (_jsxs("span", { className: "px-2 py-0.5 rounded bg-muted/60 text-[11px] font-mono border border-border", children: [s.skill_name, " (", (s.proficiency_level * 100).toFixed(0), "%)"] }, s.skill_name))) })] }), _jsxs("div", { className: "grid grid-cols-2 gap-2 pt-2 border-t border-border/60 text-xs", children: [_jsxs("div", { children: [_jsx("span", { className: "text-muted-foreground", children: "Productivity:" }), _jsxs("span", { className: "font-semibold text-emerald-500 ml-1", children: [(agent.productivity_score * 100).toFixed(0), "%"] })] }), _jsxs("div", { children: [_jsx("span", { className: "text-muted-foreground", children: "Rate:" }), _jsxs("span", { className: "font-semibold ml-1", children: ["$", agent.hourly_cost_usd, "/hr"] })] })] })] })] }, agent.agent_id))) })] }));
};
