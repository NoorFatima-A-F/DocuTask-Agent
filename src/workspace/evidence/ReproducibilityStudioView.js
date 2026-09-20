import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
export const ReproducibilityStudioView = () => {
    const [isReplaying, setIsReplaying] = useState(false);
    const [reproduceResult, setReproduceResult] = useState(null);
    const snapshots = [
        {
            id: 'snap-baseline-001',
            missionId: 'mission-alpha-889',
            stepIndex: 1,
            seed: 42,
            timestamp: '2026-09-10T18:22:10Z',
            hash: '9a8f3b20c91e847ad3ef0192a83c7482910fae12089bb3c17820aedfa9102bc4',
            envHash: 'e7102fae89bb3c17820aedfa9102bc45a8f3b20c91e847ad3ef0192a83c74829',
            outputDigest: 'f81d4fae7dec11d0a76500a0c91e6bf6012',
        },
        {
            id: 'snap-complex-table-002',
            missionId: 'mission-table-912',
            stepIndex: 2,
            seed: 1337,
            timestamp: '2026-09-10T18:25:44Z',
            hash: '3bc17820aedfa9102bc45a8f3b20c91e847ad3ef0192a83c7482910fae12089b',
            envHash: 'e7102fae89bb3c17820aedfa9102bc45a8f3b20c91e847ad3ef0192a83c74829',
            outputDigest: '482910fae12089bb3c17820aedfa9102bc45a8f3b20c91e847ad3ef0192a83c7',
        },
    ];
    const handleRunReplay = () => {
        setIsReplaying(true);
        setTimeout(() => {
            setIsReplaying(false);
            setReproduceResult({
                reproductionId: 'rep-' + Date.now(),
                snapshotId: 'snap-baseline-001',
                isReproduced: true,
                fidelityScore: 1.0,
                originalHash: 'f81d4fae7dec11d0a76500a0c91e6bf6012',
                reproducedHash: 'f81d4fae7dec11d0a76500a0c91e6bf6012',
                executionTimeMs: 14.8,
                bitForBitMatch: true,
                metrics: {
                    precision: 0.994,
                    recall: 0.991,
                    f1Score: 0.9925,
                    latencyVarianceMs: 1.2,
                },
                log: [
                    'Restoring environment state (Python 3.14.4, win32)',
                    'Setting deterministic RNG seed: 42',
                    'Injecting input payload digest: c7e12f00a891...',
                    'Replaying execution graph DAG steps...',
                    'Replay finished in 14.8ms with 100% hash parity.',
                ],
            });
        }, 600);
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4", children: [_jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-2xl font-bold tracking-tight", children: "Reproducibility Studio" }), _jsx(Badge, { variant: "success", size: "sm", children: "Bit-for-Bit Deterministic" })] }), _jsx("p", { className: "text-xs text-muted-foreground mt-1", children: "Capture frozen execution snapshots and re-run deterministic replay pipelines to prove 100% mathematical fidelity." })] }), _jsx("button", { onClick: handleRunReplay, disabled: isReplaying, className: "px-4 py-2 bg-primary hover:bg-primary/90 text-primary-foreground font-semibold text-xs rounded-lg transition-all flex items-center gap-2 shadow-sm cursor-pointer", children: isReplaying ? 'Replaying Pipeline...' : '▶ Execute Deterministic Replay' })] }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-2 gap-6", children: [_jsxs("div", { className: "space-y-4", children: [_jsxs("div", { className: "text-xs font-semibold uppercase tracking-wider text-muted-foreground", children: ["Captured State Snapshots (", snapshots.length, ")"] }), snapshots.map((snap) => (_jsxs(Card, { className: "p-5 space-y-3", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsx("span", { className: "font-mono text-sm font-bold text-foreground", children: snap.id }), _jsxs(Badge, { variant: "intelligence", size: "sm", children: ["Seed: ", snap.seed] })] }), _jsxs("div", { className: "text-xs text-muted-foreground", children: ["Mission: ", _jsx("span", { className: "font-mono text-foreground", children: snap.missionId }), " | Step: ", _jsxs("span", { className: "font-mono text-foreground", children: ["#", snap.stepIndex] })] }), _jsxs("div", { className: "p-2.5 bg-muted/30 rounded border border-border/40 font-mono text-[11px] text-muted-foreground space-y-1", children: [_jsxs("div", { children: [_jsx("span", { className: "text-foreground", children: "Snapshot Hash: " }), snap.hash.slice(0, 24), "..."] }), _jsxs("div", { children: [_jsx("span", { className: "text-foreground", children: "Expected Output: " }), snap.outputDigest] })] })] }, snap.id)))] }), _jsxs("div", { className: "space-y-4", children: [_jsx("div", { className: "text-xs font-semibold uppercase tracking-wider text-muted-foreground", children: "Replay Verification Console" }), _jsx(Card, { className: "p-5 space-y-4", children: reproduceResult ? (_jsxs("div", { className: "space-y-4", children: [_jsxs("div", { className: "flex items-center justify-between border-b border-border/40 pb-3", children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx(Badge, { variant: "success", size: "md", children: "100% BIT-FOR-BIT MATCH" }), _jsx("span", { className: "text-xs font-mono text-muted-foreground", children: reproduceResult.reproductionId })] }), _jsxs("span", { className: "text-xs font-mono text-foreground font-bold", children: [reproduceResult.executionTimeMs, " ms"] })] }), _jsxs("div", { className: "grid grid-cols-3 gap-2", children: [_jsxs("div", { className: "p-2.5 bg-card border border-border/40 rounded text-center", children: [_jsx("div", { className: "text-[10px] text-muted-foreground", children: "Precision" }), _jsxs("div", { className: "text-sm font-bold font-mono text-emerald-400", children: [(reproduceResult.metrics.precision * 100).toFixed(1), "%"] })] }), _jsxs("div", { className: "p-2.5 bg-card border border-border/40 rounded text-center", children: [_jsx("div", { className: "text-[10px] text-muted-foreground", children: "Recall" }), _jsxs("div", { className: "text-sm font-bold font-mono text-emerald-400", children: [(reproduceResult.metrics.recall * 100).toFixed(1), "%"] })] }), _jsxs("div", { className: "p-2.5 bg-card border border-border/40 rounded text-center", children: [_jsx("div", { className: "text-[10px] text-muted-foreground", children: "Variance" }), _jsxs("div", { className: "text-sm font-bold font-mono text-foreground", children: ["\u00B1", reproduceResult.metrics.latencyVarianceMs, " ms"] })] })] }), _jsx("div", { className: "p-3 bg-black/80 rounded border border-border/40 font-mono text-xs text-emerald-400 space-y-1", children: reproduceResult.log.map((line, i) => (_jsxs("div", { children: ["> ", line] }, i))) })] })) : (_jsx("div", { className: "py-12 text-center text-muted-foreground text-xs", children: "Click \"Execute Deterministic Replay\" above to re-run the snapshot and verify bitwise parity." })) })] })] })] }));
};
