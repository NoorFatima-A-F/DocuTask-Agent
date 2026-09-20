import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { GitFork, RotateCcw, CheckCircle2 } from 'lucide-react';
export const MissionTimeMachineView = () => {
    const [selectedStep, setSelectedStep] = useState(2);
    const [rewindMessage, setRewindMessage] = useState(null);
    const [forkMessage, setForkMessage] = useState(null);
    const checkpoints = [
        {
            step: 0,
            id: 'chk-01',
            time: '14:00:00 UTC',
            hash: 'a1b2c3d4e5f6001',
            health: 100.0,
            tasks: 1,
            memoryNodes: 12,
            cost: '$0.0000',
            summary: 'Mission initialized. PDF document chunks queued for ingestion.',
        },
        {
            step: 1,
            id: 'chk-02',
            time: '14:00:45 UTC',
            hash: 'a1b2c3d4e5f6002',
            health: 100.0,
            tasks: 4,
            memoryNodes: 28,
            cost: '$0.0012',
            summary: 'OCR extraction parallelized across 4 DAG workers.',
        },
        {
            step: 2,
            id: 'chk-03',
            time: '14:01:30 UTC',
            hash: 'a1b2c3d4e5f6003',
            health: 65.0,
            tasks: 4,
            memoryNodes: 35,
            cost: '$0.0025',
            summary: 'Gemini 504 Timeout injected. Incident declared. Flash failover active.',
        },
        {
            step: 3,
            id: 'chk-04',
            time: '14:02:20 UTC',
            hash: 'a1b2c3d4e5f6004',
            health: 100.0,
            tasks: 2,
            memoryNodes: 48,
            cost: '$0.0031',
            summary: 'Failover resolved. Invariant verification 100% passed. Mission finalized.',
        },
    ];
    const currentChk = (checkpoints.find(c => c.step === selectedStep) || checkpoints[0]);
    const handleRewind = () => {
        setForkMessage(null);
        setRewindMessage(`Restored mission execution state to Step ${currentChk.step} (${currentChk.id}). State hash verified.`);
    };
    const handleFork = () => {
        setRewindMessage(null);
        setForkMessage(`Forked counterfactual mission branch 'mission-fork-7b9a2c' starting from Step ${currentChk.step}.`);
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Runtime Time Machine & State Restoration" }), _jsx(Badge, { variant: "intelligence", size: "sm", children: "Deterministic Rewind" })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Explore past execution states, rewind mission context to any historical step, and fork counterfactual execution branches." })] }), _jsx("div", { className: "flex items-center gap-2", children: _jsx(Badge, { variant: "success", size: "md", children: "4 Checkpoints Available" }) })] }), _jsxs(Card, { className: "p-6 border-border/60 space-y-4", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "text-xs font-semibold text-muted-foreground uppercase", children: "Execution Scrub-Bar" }), _jsxs("span", { className: "text-xs font-mono text-primary font-bold", children: ["Current Point: Step ", selectedStep] })] }), _jsx("div", { className: "grid grid-cols-4 gap-2 pt-2", children: checkpoints.map(c => (_jsxs("button", { onClick: () => {
                                setSelectedStep(c.step);
                                setRewindMessage(null);
                                setForkMessage(null);
                            }, className: `p-3 rounded-lg border text-left transition-all ${selectedStep === c.step
                                ? 'border-primary bg-primary/10 shadow'
                                : 'border-border/40 bg-muted/20 hover:border-border'}`, children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("span", { className: "text-xs font-bold text-foreground", children: ["Step ", c.step] }), _jsxs(Badge, { variant: c.health < 100 ? 'warning' : 'success', size: "sm", children: [c.health, "%"] })] }), _jsx("div", { className: "text-[10px] text-muted-foreground font-mono mt-1", children: c.time })] }, c.step))) })] }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-3 gap-6", children: [_jsxs("div", { className: "lg:col-span-2 space-y-4", children: [_jsx("h2", { className: "text-sm font-semibold tracking-wider text-muted-foreground uppercase", children: "Historical State Payload" }), _jsxs(Card, { className: "p-5 border-border/60 space-y-4", children: [_jsxs("div", { className: "flex items-center justify-between border-b border-border/40 pb-3", children: [_jsxs("div", { children: [_jsxs("div", { className: "text-base font-bold text-foreground", children: ["Step ", currentChk.step, ": ", currentChk.summary] }), _jsxs("div", { className: "text-xs font-mono text-muted-foreground mt-0.5", children: ["State Hash: ", _jsx("strong", { className: "text-primary", children: currentChk.hash })] })] }), _jsx(Badge, { variant: "intelligence", size: "md", children: currentChk.id })] }), _jsxs("div", { className: "grid grid-cols-2 sm:grid-cols-4 gap-3 pt-1", children: [_jsxs("div", { className: "p-3 bg-muted/40 rounded border border-border/30 text-center", children: [_jsx("div", { className: "text-[10px] text-muted-foreground", children: "Twin Health" }), _jsxs("div", { className: "text-sm font-mono font-bold text-foreground mt-0.5", children: [currentChk.health, "%"] })] }), _jsxs("div", { className: "p-3 bg-muted/40 rounded border border-border/30 text-center", children: [_jsx("div", { className: "text-[10px] text-muted-foreground", children: "Active Tasks" }), _jsx("div", { className: "text-sm font-mono font-bold text-foreground mt-0.5", children: currentChk.tasks })] }), _jsxs("div", { className: "p-3 bg-muted/40 rounded border border-border/30 text-center", children: [_jsx("div", { className: "text-[10px] text-muted-foreground", children: "Memory Nodes" }), _jsx("div", { className: "text-sm font-mono font-bold text-foreground mt-0.5", children: currentChk.memoryNodes })] }), _jsxs("div", { className: "p-3 bg-muted/40 rounded border border-border/30 text-center", children: [_jsx("div", { className: "text-[10px] text-muted-foreground", children: "Cost Accumulated" }), _jsx("div", { className: "text-sm font-mono font-bold text-emerald-400 mt-0.5", children: currentChk.cost })] })] }), rewindMessage && (_jsxs("div", { className: "p-3 bg-emerald-950/10 rounded border border-emerald-500/20 text-xs text-emerald-400 font-mono flex items-center gap-2", children: [_jsx(CheckCircle2, { className: "w-4 h-4 text-emerald-400 shrink-0" }), _jsx("span", { children: rewindMessage })] })), forkMessage && (_jsxs("div", { className: "p-3 bg-blue-950/10 rounded border border-blue-500/20 text-xs text-blue-400 font-mono flex items-center gap-2", children: [_jsx(GitFork, { className: "w-4 h-4 text-blue-400 shrink-0" }), _jsx("span", { children: forkMessage })] }))] })] }), _jsxs("div", { className: "space-y-4", children: [_jsx("h2", { className: "text-sm font-semibold tracking-wider text-muted-foreground uppercase", children: "Time-Travel Actions" }), _jsxs(Card, { className: "p-5 border-border/60 space-y-3", children: [_jsxs(Button, { variant: "outline", size: "sm", className: "w-full justify-start", onClick: handleRewind, children: [_jsx(RotateCcw, { className: "w-4 h-4 mr-2 text-amber-400" }), "Rewind Mission to Step ", currentChk.step] }), _jsxs(Button, { variant: "primary", size: "sm", className: "w-full justify-start", onClick: handleFork, children: [_jsx(GitFork, { className: "w-4 h-4 mr-2" }), "Fork Counterfactual Branch"] }), _jsx("div", { className: "p-3 bg-muted/40 rounded border border-border/40 text-[11px] text-muted-foreground leading-relaxed", children: "Forking creates a clean sandbox branch from this exact point in time, enabling hypothetical chaos tests without altering the primary truth ledger." })] })] })] })] }));
};
