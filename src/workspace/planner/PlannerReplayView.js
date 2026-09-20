import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { RotateCcw, Play, Pause, FastForward } from 'lucide-react';
export const PlannerReplayView = () => {
    const [currentStep, setCurrentStep] = useState(3);
    const [isPlaying, setIsPlaying] = useState(false);
    const replaySteps = [
        { offset: 0, time: '14:20:00.120', action: 'PlannerCreated', state: 'CREATED', desc: 'Planner initialized from mission request.' },
        { offset: 1, time: '14:20:00.350', action: 'GoalParsed', state: 'GOAL_ANALYSIS', desc: 'Decomposed SLA constraints and invariants.' },
        { offset: 2, time: '14:20:00.420', action: 'PlanGenerated', state: 'PLAN_SYNTHESIS', desc: 'Synthesized 9-node DAG with parallel wavefronts.' },
        { offset: 3, time: '14:20:00.600', action: 'TaskSplitRequested', state: 'DAG_MUTATION', desc: 'Split OCR stage into 2 parallel sub-tasks.' },
        { offset: 4, time: '14:20:00.720', action: 'WorkerAssigned', state: 'DISPATCH', desc: 'Assigned worker-ocr-01 and worker-ocr-02.' },
        { offset: 5, time: '14:20:01.100', action: 'ExecutionStarted', state: 'EXECUTING', desc: 'Dispatched Wavefront 1 tasks.' },
        { offset: 6, time: '14:20:02.100', action: 'MissionCompleted', state: 'COMPLETED', desc: 'Verified all invariants and committed truth hash.' },
    ];
    return (_jsxs("div", { className: "p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]", children: [_jsxs("div", { className: "flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6", children: [_jsx("div", { className: "space-y-1", children: _jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2 bg-gradient-to-br from-cyan-500/20 to-blue-500/20 border border-cyan-500/30 rounded-xl text-cyan-400", children: _jsx(RotateCcw, { className: "w-5 h-5" }) }), _jsxs("div", { children: [_jsxs("h1", { className: "text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2", children: ["Planner Deterministic Replay Studio", _jsx(Badge, { variant: "success", size: "sm", children: "Phase 13.1 Event-Replayable" })] }), _jsx("p", { className: "text-xs text-[#94A3B8] font-mono", children: "Step-by-step reconstruction of planner decisions and DAG mutations directly from immutable Event Store" })] })] }) }), _jsxs("div", { className: "flex items-center gap-2", children: [_jsxs(Button, { onClick: () => setIsPlaying(!isPlaying), variant: isPlaying ? 'danger' : 'primary', size: "sm", children: [isPlaying ? _jsx(Pause, { className: "w-3.5 h-3.5 mr-1" }) : _jsx(Play, { className: "w-3.5 h-3.5 mr-1" }), isPlaying ? 'Pause Replay' : 'Play Replay'] }), _jsxs(Button, { onClick: () => setCurrentStep(prev => Math.min(replaySteps.length - 1, prev + 1)), variant: "secondary", size: "sm", children: [_jsx(FastForward, { className: "w-3.5 h-3.5 mr-1" }), "Step Forward"] })] })] }), _jsxs(Card, { className: "p-5 rounded-2xl border border-[#1E293B] bg-[#0F172A] space-y-3 font-mono", children: [_jsxs("div", { className: "flex items-center justify-between text-xs", children: [_jsxs("span", { className: "text-[#94A3B8]", children: ["REPLAY PROGRESS: STEP ", currentStep + 1, " OF ", replaySteps.length] }), _jsx("span", { className: "text-cyan-400 font-bold", children: replaySteps[currentStep]?.time ?? '' })] }), _jsx("div", { className: "w-full bg-[#131D35] h-2.5 rounded-full overflow-hidden", children: _jsx("div", { className: "bg-gradient-to-r from-cyan-500 to-indigo-500 h-full transition-all duration-300", style: { width: `${((currentStep + 1) / replaySteps.length) * 100}%` } }) })] }), _jsx("div", { className: "space-y-3 font-mono", children: replaySteps.map((step, idx) => {
                    const isCurrent = currentStep === idx;
                    const isPast = currentStep > idx;
                    return (_jsxs(Card, { onClick: () => setCurrentStep(idx), className: `p-4 rounded-xl border transition-all cursor-pointer flex items-center justify-between ${isCurrent
                            ? 'border-cyan-500 bg-[#131D35] shadow-[0_0_12px_rgba(0,210,255,0.2)]'
                            : isPast
                                ? 'border-emerald-500/30 bg-[#0F172A]'
                                : 'border-[#1E293B] bg-[#0A0F1D]/50 opacity-60'}`, children: [_jsxs("div", { className: "flex items-center gap-4", children: [_jsxs("div", { className: `w-8 h-8 rounded-lg flex items-center justify-center text-xs font-bold ${isCurrent ? 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/30' : 'bg-[#131D35] text-[#64748B]'}`, children: ["#", step.offset] }), _jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("span", { className: "text-xs font-bold text-white", children: step.action }), _jsx(Badge, { variant: "outline", size: "sm", children: step.state })] }), _jsx("p", { className: "text-xs text-[#94A3B8] mt-0.5", children: step.desc })] })] }), _jsxs("div", { className: "text-right text-xs", children: [_jsx("span", { className: "text-white font-semibold", children: step.time }), _jsx(Badge, { variant: isCurrent ? 'intelligence' : isPast ? 'success' : 'outline', size: "sm", className: "ml-2", children: isCurrent ? 'CURRENT' : isPast ? 'REPLAYED' : 'PENDING' })] })] }, step.offset));
                }) })] }));
};
