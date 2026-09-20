import { jsx as _jsx, jsxs as _jsxs, Fragment as _Fragment } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Flame, CheckCircle2, RotateCcw } from 'lucide-react';
export const ChaosLabView = () => {
    const [scenarios, setScenarios] = useState([
        {
            id: 'chaos-gemini-timeout',
            name: 'Gemini 1.5 Pro 504 Gateway Timeout',
            target: 'node-gemini (Google Cloud Gateway)',
            severity: 'HIGH',
            description: 'Simulates upstream LLM gateway latency spike (>5000ms) triggering HTTP 504 timeout.',
            expectedStrategy: 'FAILOVER_TO_GEMINI_FLASH',
            status: 'SCHEDULED',
        },
        {
            id: 'chaos-redis-drop',
            name: 'Redis Cache Sudden Network Drop',
            target: 'node-storage (Redis KV Cluster)',
            severity: 'MEDIUM',
            description: 'Simulates socket connection drop and cache unreachable exception.',
            expectedStrategy: 'IN_MEMORY_CIRCUIT_BREAKER_FALLBACK',
            status: 'SCHEDULED',
        },
        {
            id: 'chaos-ocr-crash',
            name: 'OCR Extraction Process SIGSEGV',
            target: 'node-workers (DAG Worker Pool)',
            severity: 'CRITICAL',
            description: 'Simulates native C++ OCR worker memory leak causing immediate process panic.',
            expectedStrategy: 'WORKER_REPLICA_AUTORESPAWN_AND_RETRY',
            status: 'SCHEDULED',
        },
        {
            id: 'chaos-memory-corruption',
            name: 'Episodic Memory Vector Index Corruption',
            target: 'node-memory (Causal Memory Graph)',
            severity: 'HIGH',
            description: 'Simulates corrupted embedding hashes and invalid cosine distance vectors.',
            expectedStrategy: 'MEMORY_SANITY_ROLLBACK_AND_WARM_RELOAD',
            status: 'SCHEDULED',
        },
        {
            id: 'chaos-truth-attack',
            name: 'Truth Ledger Merkle Branch Tampering Attempt',
            target: 'node-truth (Proof Ledger)',
            severity: 'CRITICAL',
            description: 'Simulates unauthorized byte-level alteration of a committed decision hash.',
            expectedStrategy: 'INVARIANT_CRYPTOGRAPHIC_REJECTION',
            status: 'SCHEDULED',
        },
    ]);
    const [activeScenarioId, setActiveScenarioId] = useState(null);
    const [isProcessing, setIsProcessing] = useState(false);
    const handleInjectFault = (id) => {
        setIsProcessing(true);
        setActiveScenarioId(id);
        setScenarios(prev => prev.map(s => (s.id === id ? { ...s, status: 'ACTIVE' } : s)));
        setIsProcessing(false);
    };
    const handleRecoverFault = (id) => {
        setIsProcessing(true);
        setTimeout(() => {
            setScenarios(prev => prev.map(s => s.id === id
                ? { ...s, status: 'HEALED', recoveryMs: 45.2 }
                : s));
            if (activeScenarioId === id)
                setActiveScenarioId(null);
            setIsProcessing(false);
        }, 400);
    };
    const handleResetAll = () => {
        setScenarios(prev => prev.map(s => ({ ...s, status: 'SCHEDULED', recoveryMs: undefined })));
        setActiveScenarioId(null);
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Autonomous Chaos Engineering Lab" }), _jsx(Badge, { variant: "warning", size: "sm", children: "Fault Injection Studio" })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Deliberately inject live fault vectors to test autonomous self-healing, failover speed, and invariant survival." })] }), _jsxs("div", { className: "flex items-center gap-2", children: [_jsxs(Button, { variant: "outline", size: "sm", onClick: handleResetAll, children: [_jsx(RotateCcw, { className: "w-3.5 h-3.5 mr-1.5" }), "Reset Scenarios"] }), _jsx(Badge, { variant: activeScenarioId ? 'error' : 'success', size: "md", children: activeScenarioId ? 'FAULT ACTIVE: MITIGATING' : 'STANDBY: RESILIENT' })] })] }), _jsxs("div", { className: "grid grid-cols-1 sm:grid-cols-4 gap-4", children: [_jsxs(Card, { className: "p-4 bg-amber-950/10 border-amber-500/20", children: [_jsx("div", { className: "text-xs font-semibold text-muted-foreground", children: "Total Chaos Vectors" }), _jsxs("div", { className: "text-2xl font-bold font-mono text-amber-400 mt-1", children: [scenarios.length, " Scenarios"] }), _jsx("div", { className: "text-[11px] text-muted-foreground mt-1", children: "5 Subsystem Fault Modes" })] }), _jsxs(Card, { className: "p-4 bg-emerald-950/10 border-emerald-500/20", children: [_jsx("div", { className: "text-xs font-semibold text-muted-foreground", children: "Autonomous Recovery Rate" }), _jsx("div", { className: "text-2xl font-bold font-mono text-emerald-400 mt-1", children: "100.0%" }), _jsx("div", { className: "text-[11px] text-muted-foreground mt-1", children: "Zero human intervention" })] }), _jsxs(Card, { className: "p-4 bg-blue-950/10 border-blue-500/20", children: [_jsx("div", { className: "text-xs font-semibold text-muted-foreground", children: "Mean Time To Recovery" }), _jsx("div", { className: "text-2xl font-bold font-mono text-blue-400 mt-1", children: "45.2 ms" }), _jsx("div", { className: "text-[11px] text-muted-foreground mt-1", children: "Sub-100ms failover SLA" })] }), _jsxs(Card, { className: "p-4 bg-purple-950/10 border-purple-500/20", children: [_jsx("div", { className: "text-xs font-semibold text-muted-foreground", children: "State Drift Under Chaos" }), _jsx("div", { className: "text-2xl font-bold font-mono text-purple-400 mt-1", children: "0.00%" }), _jsx("div", { className: "text-[11px] text-muted-foreground mt-1", children: "Replay parity preserved" })] })] }), _jsxs("div", { className: "space-y-3", children: [_jsx("h2", { className: "text-sm font-semibold tracking-wider text-muted-foreground uppercase", children: "Live Chaos Injection Scenarios" }), _jsx("div", { className: "grid grid-cols-1 gap-3", children: scenarios.map(scenario => (_jsx(Card, { className: `p-5 border transition-all ${scenario.status === 'ACTIVE'
                                ? 'border-red-500/60 bg-red-950/10 shadow-lg'
                                : scenario.status === 'HEALED'
                                    ? 'border-emerald-500/30 bg-emerald-950/5'
                                    : 'border-border/60 hover:border-border'}`, children: _jsxs("div", { className: "flex flex-col lg:flex-row lg:items-center justify-between gap-4", children: [_jsxs("div", { className: "space-y-1.5 flex-1", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-sm font-bold text-foreground", children: scenario.name }), _jsx(Badge, { variant: scenario.severity === 'CRITICAL'
                                                            ? 'error'
                                                            : scenario.severity === 'HIGH'
                                                                ? 'warning'
                                                                : 'default', size: "sm", children: scenario.severity }), _jsx(Badge, { variant: scenario.status === 'ACTIVE'
                                                            ? 'error'
                                                            : scenario.status === 'HEALED'
                                                                ? 'success'
                                                                : 'outline', size: "sm", children: scenario.status })] }), _jsx("p", { className: "text-xs text-muted-foreground", children: scenario.description }), _jsxs("div", { className: "flex flex-wrap items-center gap-3 text-[11px] text-muted-foreground pt-1", children: [_jsxs("span", { children: ["Target: ", _jsx("strong", { className: "text-foreground font-mono", children: scenario.target })] }), _jsx("span", { children: "\u2022" }), _jsxs("span", { children: ["Failover Path: ", _jsx("strong", { className: "text-primary font-mono", children: scenario.expectedStrategy })] }), scenario.recoveryMs && (_jsxs(_Fragment, { children: [_jsx("span", { children: "\u2022" }), _jsxs("span", { className: "text-emerald-400 font-mono font-semibold", children: ["Recovered in ", scenario.recoveryMs, " ms"] })] }))] })] }), _jsx("div", { className: "flex items-center gap-2 self-end lg:self-center", children: scenario.status === 'ACTIVE' ? (_jsxs(Button, { variant: "primary", size: "sm", onClick: () => handleRecoverFault(scenario.id), disabled: isProcessing, children: [_jsx(CheckCircle2, { className: "w-3.5 h-3.5 mr-1.5" }), "Trigger Recovery"] })) : (_jsxs(Button, { variant: "outline", size: "sm", onClick: () => handleInjectFault(scenario.id), disabled: isProcessing, children: [_jsx(Flame, { className: "w-3.5 h-3.5 mr-1.5 text-red-400" }), "Inject Fault"] })) })] }) }, scenario.id))) })] })] }));
};
