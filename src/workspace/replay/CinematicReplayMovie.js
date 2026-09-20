import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState, useEffect } from 'react';
import { useWorkspace } from '../context/WorkspaceContext';
import { CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { AgentPresenceBadge } from '../../components/presence/AgentPresenceBadge';
export const CinematicReplayMovie = () => {
    const { replaySnapshots, currentReplayStep, setReplayStep, stepForwardReplay, stepBackwardReplay, } = useWorkspace();
    const [isPlaying, setIsPlaying] = useState(false);
    const [speedMultiplier, setSpeedMultiplier] = useState(1);
    const activeSnapshot = replaySnapshots[currentReplayStep - 1] || replaySnapshots[0] || null;
    useEffect(() => {
        if (!isPlaying)
            return;
        const intervalMs = Math.round(2400 / speedMultiplier);
        const interval = setInterval(() => {
            if (currentReplayStep >= replaySnapshots.length) {
                setIsPlaying(false);
            }
            else {
                stepForwardReplay();
            }
        }, intervalMs);
        return () => clearInterval(interval);
    }, [isPlaying, speedMultiplier, currentReplayStep, replaySnapshots.length, stepForwardReplay]);
    return (_jsxs("div", { className: "w-full flex flex-col h-[700px] rounded-2xl bg-[#0F172A]/95 border border-cyan-500/40 shadow-[0_0_40px_rgba(0,102,255,0.2)] overflow-hidden", children: [_jsxs(CardHeader, { className: "flex flex-row items-center justify-between py-4 px-6 border-b border-[#1E293B] bg-[#0A0F1D]", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "h-3 w-3 rounded-full bg-red-500 animate-pulse" }), _jsxs("div", { children: [_jsx(CardTitle, { className: "text-sm font-bold text-[#F8FAFC]", children: "Cinematic Mission Replay (Movie Mode)" }), _jsxs("span", { className: "text-[11px] text-[#00D2FF] font-mono", children: ["SCENE ", currentReplayStep, " OF ", replaySnapshots.length, " \u2022 PROVENANCE PLAYBACK"] })] })] }), _jsx("div", { className: "flex items-center gap-2", children: [1, 2, 4].map((spd) => (_jsxs("button", { onClick: () => setSpeedMultiplier(spd), className: `px-2 py-1 rounded text-[11px] font-mono font-bold transition-all ${speedMultiplier === spd
                                ? 'bg-cyan-400 text-slate-950 shadow-[0_0_10px_rgba(0,210,255,0.8)]'
                                : 'bg-[#131D35] text-[#64748B] hover:text-[#F8FAFC]'}`, children: [spd, "x"] }, spd))) })] }), _jsxs(CardContent, { className: "flex-1 overflow-y-auto p-6 flex flex-col justify-between space-y-6 bg-gradient-to-b from-[#0A0F1D] to-[#0F172A]", children: [activeSnapshot && (_jsxs("div", { className: "space-y-6", children: [_jsxs("div", { className: "p-4 rounded-2xl bg-[#131D35]/80 border border-[#334155] shadow-lg flex flex-col sm:flex-row sm:items-center justify-between gap-4", children: [_jsxs("div", { className: "flex-1", children: [_jsx("span", { className: "text-[10px] font-mono uppercase text-[#00D2FF] tracking-widest block mb-1", children: "Agent In Focus:" }), _jsx(AgentPresenceBadge, { role: activeSnapshot.activeAgent, name: `${activeSnapshot.activeAgent.charAt(0) + activeSnapshot.activeAgent.slice(1).toLowerCase()} Agent`, status: "EXECUTING", currentThought: activeSnapshot.thoughtContent, confidence: activeSnapshot.currentConfidence })] }), _jsxs("div", { className: "text-right font-mono shrink-0", children: [_jsx("span", { className: "text-xs text-[#94A3B8] block", children: "Timestamp:" }), _jsxs("span", { className: "text-sm font-bold text-[#F8FAFC]", children: [activeSnapshot.timestampUtc, " UTC"] }), _jsxs(Badge, { variant: "intelligence", size: "sm", className: "mt-1", children: ["Phase: ", activeSnapshot.stageName] })] })] }), _jsxs("div", { className: "p-6 rounded-2xl bg-[#0A0F1D] border border-cyan-500/30 text-center space-y-3", children: [_jsx("span", { className: "text-[10px] font-mono uppercase tracking-widest text-[#64748B]", children: "Autonomous Cognition Subtitles:" }), _jsxs("p", { className: "text-base lg:text-lg font-medium text-[#F8FAFC] max-w-2xl mx-auto leading-relaxed italic", children: ["\"", activeSnapshot.thoughtContent, "\""] }), _jsxs("span", { className: "text-xs font-mono text-[#10B981] block", children: ["\u2605 ", activeSnapshot.thoughtTitle] })] })] })), _jsxs("div", { className: "p-4 rounded-xl bg-[#131D35] border border-[#1E293B] space-y-3", children: [_jsxs("div", { className: "flex items-center justify-between text-xs font-mono text-[#94A3B8]", children: [_jsxs("span", { children: ["00:0", currentReplayStep] }), _jsxs("span", { className: "text-[#00D2FF] font-bold", children: ["Confidence: ", ((activeSnapshot?.currentConfidence || 0) * 100).toFixed(1), "%"] }), _jsxs("span", { children: ["00:0", replaySnapshots.length] })] }), _jsx("input", { type: "range", min: 1, max: replaySnapshots.length, value: currentReplayStep, onChange: (e) => setReplayStep(Number(e.target.value)), className: "w-full accent-cyan-400 cursor-pointer" }), _jsxs("div", { className: "flex items-center justify-between pt-1", children: [_jsx(Button, { variant: "ghost", size: "sm", onClick: stepBackwardReplay, disabled: currentReplayStep <= 1, children: "\u23EE Back" }), _jsx(Button, { variant: "intelligence", size: "md", onClick: () => setIsPlaying(!isPlaying), className: "px-6 font-bold", children: isPlaying ? '⏸ Pause' : '▶ Play Movie' }), _jsx(Button, { variant: "ghost", size: "sm", onClick: stepForwardReplay, disabled: currentReplayStep >= replaySnapshots.length, children: "Next \u23ED" })] })] })] })] }));
};
