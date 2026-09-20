import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Users, Search, Clock, Zap, DollarSign, } from 'lucide-react';
export const AgentRegistryExplorer = () => {
    const [searchTerm, setSearchTerm] = useState('');
    const [selectedRole, setSelectedRole] = useState('ALL');
    const [selectedAgent, setSelectedAgent] = useState(null);
    const agents = [
        {
            id: 'agent-exec-01',
            name: 'Executive Director Alpha',
            role: 'EXECUTIVE',
            state: 'AVAILABLE',
            reputation: 0.992,
            latencyMs: 120,
            costPerSec: 0.08,
            capabilities: ['mission_orchestration', 'goal_alignment', 'strategic_planning'],
            tools: ['mission_decomposer', 'resource_allocator'],
            tasksCompleted: 142,
        },
        {
            id: 'agent-plan-01',
            name: 'Lead DAG Planner',
            role: 'PLANNER',
            state: 'EXECUTING',
            reputation: 0.985,
            latencyMs: 180,
            costPerSec: 0.06,
            capabilities: ['dag_scheduling', 'critical_path_analysis', 'dependency_resolution'],
            tools: ['dag_mutator', 'scheduler_engine'],
            tasksCompleted: 310,
        },
        {
            id: 'agent-coord-01',
            name: 'Swarm Coordinator',
            role: 'COORDINATOR',
            state: 'AVAILABLE',
            reputation: 0.978,
            latencyMs: 150,
            costPerSec: 0.05,
            capabilities: ['task_routing', 'agent_synchronization', 'market_auctioning'],
            tools: ['task_broker', 'auction_manager'],
            tasksCompleted: 480,
        },
        {
            id: 'agent-spec-ocr',
            name: 'Vision & OCR Specialist',
            role: 'SPECIALIST',
            state: 'EXECUTING',
            reputation: 0.988,
            latencyMs: 310,
            costPerSec: 0.04,
            capabilities: ['ocr_extraction', 'table_parsing', 'layout_detection', 'tokenization'],
            tools: ['tesseract_engine', 'vision_transformer'],
            tasksCompleted: 1250,
        },
        {
            id: 'agent-val-sec',
            name: 'Cryptographic Security Validator',
            role: 'VALIDATOR',
            state: 'VOTING',
            reputation: 0.995,
            latencyMs: 90,
            costPerSec: 0.03,
            capabilities: ['security_verification', 'cryptographic_audit', 'schema_validation'],
            tools: ['sha256_verifier', 'policy_evaluator'],
            tasksCompleted: 890,
        },
        {
            id: 'agent-res-opt',
            name: 'Resource & Token Governor',
            role: 'RESOURCE',
            state: 'AVAILABLE',
            reputation: 0.965,
            latencyMs: 80,
            costPerSec: 0.02,
            capabilities: ['budget_management', 'token_quota_control', 'rate_limiting'],
            tools: ['cost_calculator', 'load_balancer'],
            tasksCompleted: 620,
        },
    ];
    const filteredAgents = agents.filter(a => {
        const matchesSearch = a.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
            a.id.toLowerCase().includes(searchTerm.toLowerCase()) ||
            a.capabilities.some(c => c.toLowerCase().includes(searchTerm.toLowerCase()));
        const matchesRole = selectedRole === 'ALL' || a.role === selectedRole;
        return matchesSearch && matchesRole;
    });
    return (_jsxs("div", { className: "space-y-6", children: [_jsx("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: _jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Agent Registry Explorer" }), _jsxs(Badge, { variant: "intelligence", size: "sm", children: [filteredAgents.length, " Agents Listed"] })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Dynamic catalog of autonomous agent profiles, capabilities, permissions, and lifecycle telemetry." })] }) }), _jsxs("div", { className: "flex flex-col sm:flex-row gap-3", children: [_jsxs("div", { className: "relative flex-1", children: [_jsx(Search, { className: "w-4 h-4 absolute left-3 top-3 text-muted-foreground" }), _jsx("input", { type: "text", placeholder: "Search by agent name, ID, or semantic capability (e.g. ocr_extraction)...", value: searchTerm, onChange: e => setSearchTerm(e.target.value), className: "w-full pl-9 pr-4 py-2 text-xs rounded-md bg-background border border-border/60 focus:outline-none focus:ring-1 focus:ring-primary" })] }), _jsxs("select", { value: selectedRole, onChange: e => setSelectedRole(e.target.value), className: "text-xs px-3 py-2 rounded-md bg-background border border-border/60 focus:outline-none focus:ring-1 focus:ring-primary", children: [_jsx("option", { value: "ALL", children: "All Roles" }), _jsx("option", { value: "EXECUTIVE", children: "Executive" }), _jsx("option", { value: "PLANNER", children: "Planner" }), _jsx("option", { value: "COORDINATOR", children: "Coordinator" }), _jsx("option", { value: "SPECIALIST", children: "Specialist" }), _jsx("option", { value: "VALIDATOR", children: "Validator" }), _jsx("option", { value: "RESOURCE", children: "Resource" })] })] }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-3 gap-6", children: [_jsx("div", { className: "lg:col-span-2 space-y-3", children: filteredAgents.map(a => (_jsxs(Card, { onClick: () => setSelectedAgent(a), className: `p-4 cursor-pointer transition-all border ${selectedAgent?.id === a.id
                                ? 'border-primary ring-1 ring-primary bg-primary/5'
                                : 'border-border/60 hover:border-border'}`, children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center justify-between gap-2", children: [_jsxs("div", { className: "flex items-center gap-2.5", children: [_jsx("div", { className: "p-2 rounded-lg bg-muted/40 border border-border/40", children: _jsx(Users, { className: "w-4 h-4 text-primary" }) }), _jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "font-semibold text-sm", children: a.name }), _jsx(Badge, { variant: "outline", size: "sm", children: a.role })] }), _jsx("span", { className: "text-[11px] font-mono text-muted-foreground", children: a.id })] })] }), _jsxs("div", { className: "flex items-center gap-3", children: [_jsx(Badge, { variant: a.state === 'AVAILABLE'
                                                        ? 'success'
                                                        : a.state === 'EXECUTING'
                                                            ? 'info'
                                                            : a.state === 'VOTING'
                                                                ? 'warning'
                                                                : 'default', size: "sm", children: a.state }), _jsxs("span", { className: "text-xs font-mono font-bold text-emerald-400", children: [(a.reputation * 100).toFixed(1), "% Rep"] })] })] }), _jsx("div", { className: "flex flex-wrap gap-1.5 mt-3", children: a.capabilities.map(cap => (_jsx("span", { className: "text-[10px] font-mono px-2 py-0.5 rounded bg-muted/30 border border-border/30 text-muted-foreground", children: cap }, cap))) })] }, a.id))) }), _jsx("div", { children: selectedAgent ? (_jsxs(Card, { className: "p-5 border-border/60 sticky top-4 space-y-4", children: [_jsxs("div", { className: "flex items-center justify-between border-b border-border/40 pb-3", children: [_jsxs("div", { children: [_jsx("h3", { className: "font-bold text-sm", children: selectedAgent.name }), _jsx("span", { className: "text-[11px] font-mono text-muted-foreground", children: selectedAgent.id })] }), _jsx(Badge, { variant: "success", size: "sm", children: "HEALTHY" })] }), _jsxs("div", { className: "grid grid-cols-2 gap-3", children: [_jsxs("div", { className: "p-2.5 rounded bg-muted/20 border border-border/30", children: [_jsxs("span", { className: "text-[11px] text-muted-foreground flex items-center gap-1", children: [_jsx(Clock, { className: "w-3 h-3 text-blue-400" }), " Avg Latency"] }), _jsxs("div", { className: "text-sm font-bold font-mono text-blue-400 mt-1", children: [selectedAgent.latencyMs, " ms"] })] }), _jsxs("div", { className: "p-2.5 rounded bg-muted/20 border border-border/30", children: [_jsxs("span", { className: "text-[11px] text-muted-foreground flex items-center gap-1", children: [_jsx(DollarSign, { className: "w-3 h-3 text-emerald-400" }), " Compute Cost"] }), _jsxs("div", { className: "text-sm font-bold font-mono text-emerald-400 mt-1", children: ["$", selectedAgent.costPerSec, "/s"] })] })] }), _jsxs("div", { children: [_jsx("span", { className: "text-xs font-semibold text-muted-foreground block mb-2", children: "Equipped Tools" }), _jsx("div", { className: "space-y-1.5", children: selectedAgent.tools.map(t => (_jsxs("div", { className: "flex items-center gap-2 p-2 rounded bg-muted/10 border border-border/20 text-xs font-mono", children: [_jsx(Zap, { className: "w-3 h-3 text-primary" }), t] }, t))) })] }), _jsxs("div", { children: [_jsx("span", { className: "text-xs font-semibold text-muted-foreground block mb-1", children: "Total Verified Tasks" }), _jsxs("div", { className: "text-lg font-bold font-mono text-primary", children: [selectedAgent.tasksCompleted, " Executions"] })] }), _jsx(Button, { variant: "outline", size: "sm", className: "w-full", children: "Inspect Complete Audit Trace" })] })) : (_jsxs(Card, { className: "p-8 border-border/40 text-center text-muted-foreground", children: [_jsx(Users, { className: "w-8 h-8 mx-auto mb-2 opacity-40" }), _jsx("p", { className: "text-xs", children: "Select an agent profile from the directory to inspect runtime telemetry and tool bindings." })] })) })] })] }));
};
