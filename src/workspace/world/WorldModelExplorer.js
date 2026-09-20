import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { Globe, Search, History, Lock, Clock, } from 'lucide-react';
export const WorldModelExplorer = () => {
    const [selectedType, setSelectedType] = useState('ALL');
    const [searchQuery, setSearchQuery] = useState('');
    const entities = [
        {
            id: 'agent-planner-01',
            type: 'AGENT',
            name: 'APDLE Live DAG Planner',
            healthScore: 0.99,
            status: 'OPTIMAL',
            attributes: { role: 'PLANNER', throughput_qps: 45, concurrency: 8 },
            updatedAt: '2026-09-12 10:15:00 UTC',
        },
        {
            id: 'agent-ocr-specialist-01',
            type: 'AGENT',
            name: 'Parallel Table Extraction Specialist',
            healthScore: 0.98,
            status: 'OPTIMAL',
            attributes: { role: 'SPECIALIST', batch_size: 16, accuracy: 0.995 },
            updatedAt: '2026-09-12 10:15:30 UTC',
        },
        {
            id: 'res-gpu-vram-01',
            type: 'RESOURCE',
            name: 'Host VRAM Allocation Pool',
            healthScore: 0.97,
            status: 'OPTIMAL',
            attributes: { total_vram_gb: 24, allocated_vram_gb: 11.6, free_vram_gb: 12.4 },
            updatedAt: '2026-09-12 10:16:00 UTC',
        },
        {
            id: 'infra-eventbus-01',
            type: 'INFRASTRUCTURE',
            name: 'Multicast EventBus Router',
            healthScore: 1.0,
            status: 'OPTIMAL',
            attributes: { events_per_sec: 12500, buffer_capacity_mb: 512, dropped_frames: 0 },
            updatedAt: '2026-09-12 10:16:15 UTC',
        },
        {
            id: 'pol-concurrency-quota-01',
            type: 'POLICY',
            name: 'Dynamic Concurrency Quota Policy',
            healthScore: 1.0,
            status: 'ACTIVE',
            attributes: { max_tasks_per_dag: 16, memory_threshold_pct: 60.0 },
            updatedAt: '2026-09-12 10:16:30 UTC',
        },
    ];
    const snapshots = [
        { id: 'wss-000003', sequence: 3, hash: '0x9e8a7b6c5d...110a', timestamp: '2026-09-12 10:15:00 UTC', entitiesCount: 18 },
        { id: 'wss-000002', sequence: 2, hash: '0x3c4d5e6f7a...882b', timestamp: '2026-09-12 09:45:00 UTC', entitiesCount: 16 },
        { id: 'wss-000001', sequence: 1, hash: '0x7a8b9c0d1e...554c', timestamp: '2026-09-12 09:15:00 UTC', entitiesCount: 14 },
    ];
    const filteredEntities = entities.filter((e) => {
        const matchesType = selectedType === 'ALL' || e.type === selectedType;
        const matchesSearch = e.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
            e.id.toLowerCase().includes(searchQuery.toLowerCase());
        return matchesType && matchesSearch;
    });
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "World Model Explorer" }), _jsx(Badge, { variant: "intelligence", size: "sm", hasDot: true, isPulsing: true, children: "GROUND TRUTH STATE" }), _jsx(Badge, { variant: "outline", size: "sm", children: "AWM-PSDTIP Phase 13.10" })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Complete enterprise state model across agents, tasks, resources, infrastructure, policies, capabilities, and historical time-travel reconstruction." })] }), _jsxs("div", { className: "flex items-center gap-2", children: [_jsxs(Button, { variant: "outline", size: "sm", children: [_jsx(History, { className: "w-3.5 h-3.5 mr-1.5" }), "Time-Travel Query"] }), _jsxs(Button, { variant: "intelligence", size: "sm", children: [_jsx(Globe, { className: "w-3.5 h-3.5 mr-1.5" }), "Create State Snapshot"] })] })] }), _jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center justify-between gap-4", children: [_jsx("div", { className: "flex items-center gap-2 overflow-x-auto pb-1 sm:pb-0", children: ['ALL', 'AGENT', 'RESOURCE', 'INFRASTRUCTURE', 'POLICY'].map((t) => (_jsx(Button, { variant: selectedType === t ? 'primary' : 'ghost', size: "sm", onClick: () => setSelectedType(t), children: t }, t))) }), _jsxs("div", { className: "relative w-full sm:w-64", children: [_jsx(Search, { className: "w-3.5 h-3.5 absolute left-2.5 top-2.5 text-muted-foreground" }), _jsx("input", { type: "text", value: searchQuery, onChange: (e) => setSearchQuery(e.target.value), placeholder: "Search entity or ID...", className: "w-full bg-secondary/50 text-xs rounded-md pl-8 pr-2 py-1.5 border border-border/40 focus:outline-none focus:border-primary" })] })] }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-12 gap-6", children: [_jsx("div", { className: "lg:col-span-8 space-y-4", children: filteredEntities.map((ent) => (_jsxs(Card, { className: "p-5 border-border/40 space-y-3 hover:border-purple-500/30 transition-colors", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center justify-between gap-2", children: [_jsxs("div", { className: "space-y-1", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-xs font-mono font-bold text-foreground", children: ent.id }), _jsx(Badge, { variant: "intelligence", size: "sm", children: ent.type }), _jsx(Badge, { variant: "success", size: "sm", children: ent.status })] }), _jsx("h3", { className: "text-sm font-semibold text-foreground", children: ent.name })] }), _jsxs("span", { className: "text-xs font-mono text-emerald-400 font-bold", children: ["Health: ", (ent.healthScore * 100).toFixed(1), "%"] })] }), _jsx("div", { className: "p-3 rounded bg-secondary/20 border border-border/30 text-xs font-mono text-muted-foreground grid grid-cols-1 sm:grid-cols-3 gap-2", children: Object.entries(ent.attributes).map(([k, v], idx) => (_jsxs("div", { className: "truncate", children: [_jsxs("span", { className: "text-foreground", children: [k, ":"] }), " ", String(v)] }, idx))) }), _jsxs("div", { className: "flex items-center justify-between text-[11px] text-muted-foreground pt-2 border-t border-border/30 font-mono", children: [_jsxs("span", { children: ["Updated: ", ent.updatedAt] }), _jsx("span", { className: "text-purple-400", children: "\u25CF Ground-Truth Synchronized" })] })] }, ent.id))) }), _jsxs("div", { className: "lg:col-span-4 space-y-3", children: [_jsx("h2", { className: "text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-2", children: "State Snapshots & Hash Tree" }), snapshots.map((s) => (_jsxs(Card, { className: "p-3.5 border-border/40 bg-secondary/10 space-y-2", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("span", { className: "text-xs font-mono font-bold text-foreground", children: ["Seq #", s.sequence, " (", s.id, ")"] }), _jsxs(Badge, { variant: "outline", size: "sm", children: [s.entitiesCount, " Entities"] })] }), _jsxs("div", { className: "flex items-center gap-1.5 text-[11px] font-mono text-purple-300", children: [_jsx(Lock, { className: "w-3 h-3 text-purple-400 flex-shrink-0" }), _jsx("span", { className: "truncate", children: s.hash })] }), _jsxs("div", { className: "text-[10px] text-muted-foreground font-mono flex items-center gap-1", children: [_jsx(Clock, { className: "w-3 h-3" }), _jsx("span", { children: s.timestamp })] })] }, s.id)))] })] })] }));
};
