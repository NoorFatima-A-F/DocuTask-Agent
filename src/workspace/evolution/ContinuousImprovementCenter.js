import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Sparkles, Play, CheckCircle2, } from 'lucide-react';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { EvolutionPlatformApiClient } from '../../services/evolutionPlatformApiClient';
export const ContinuousImprovementCenter = () => {
    const [running, setRunning] = useState(false);
    const [currentStep, setCurrentStep] = useState(0);
    const [result, setResult] = useState(null);
    // Configuration
    const [targetSubsystem, setTargetSubsystem] = useState('llm_orchestrator');
    const [objective, setObjective] = useState('LATENCY_REDUCTION');
    const [autoDeploy] = useState(true);
    const steps = [
        'Profile Runtime Telemetry',
        'Diagnose Bottlenecks',
        'Detect Capability Gaps',
        'Pareto Frontier Search',
        'Synthesize Mutation Diff',
        'Shadow Replay Simulation',
        'Side-by-Side Benchmark',
        'Cryptographic Governance Seal',
        'Canary Progressive Rollout',
        'Platform Genome Commit',
    ];
    const handleStartEvolution = async () => {
        setRunning(true);
        setResult(null);
        setCurrentStep(1);
        // Simulated progress steps for smooth UX
        const interval = setInterval(() => {
            setCurrentStep((prev) => (prev < 9 ? prev + 1 : prev));
        }, 400);
        try {
            const res = await EvolutionPlatformApiClient.runEvolutionCycle(targetSubsystem, objective, autoDeploy);
            clearInterval(interval);
            setCurrentStep(10);
            setResult(res);
        }
        catch (err) {
            clearInterval(interval);
            console.error('Evolution cycle failed:', err);
        }
        finally {
            setRunning(false);
        }
    };
    return (_jsxs("div", { className: "space-y-6", children: [_jsx("div", { className: "bg-gradient-to-r from-slate-900 via-indigo-950/40 to-slate-900 border border-slate-800 rounded-2xl p-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-4 shadow-xl", children: _jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2.5 bg-indigo-500/10 border border-indigo-500/20 rounded-xl", children: _jsx(Sparkles, { className: "w-6 h-6 text-indigo-400" }) }), _jsxs("div", { children: [_jsxs("div", { className: "flex items-center gap-2", children: [_jsx("h1", { className: "text-xl font-bold text-slate-100", children: "Continuous Closed-Loop Self-Evolution Studio" }), _jsx(Badge, { variant: "intelligence", size: "sm", children: "Autonomous AI Chief Architect" })] }), _jsx("p", { className: "text-sm text-slate-400 mt-0.5", children: "Execute full 10-stage end-to-end recursive self-evolution cycles with automated simulation, benchmarking, governance, and canary promotion." })] })] }) }), _jsxs("div", { className: "bg-slate-900/80 border border-slate-800 rounded-xl p-6 space-y-4", children: [_jsx("h2", { className: "text-base font-semibold text-slate-100", children: "Configure Evolution Parameters" }), _jsxs("div", { className: "grid grid-cols-1 md:grid-cols-3 gap-5", children: [_jsxs("div", { children: [_jsx("label", { className: "text-xs font-medium text-slate-400 block mb-1", children: "Target Subsystem" }), _jsxs("select", { value: targetSubsystem, onChange: (e) => setTargetSubsystem(e.target.value), disabled: running, className: "w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-indigo-500", children: [_jsx("option", { value: "llm_orchestrator", children: "LLM Orchestrator & Planner" }), _jsx("option", { value: "memory_layer", children: "Episodic Vector Memory" }), _jsx("option", { value: "swarm_coordination", children: "Swarm Coordination Ring" }), _jsx("option", { value: "document_parser", children: "Document Layout Parser" })] })] }), _jsxs("div", { children: [_jsx("label", { className: "text-xs font-medium text-slate-400 block mb-1", children: "Evolution Objective" }), _jsxs("select", { value: objective, onChange: (e) => setObjective(e.target.value), disabled: running, className: "w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-indigo-500", children: [_jsx("option", { value: "LATENCY_REDUCTION", children: "Latency Reduction (Lock-Free SIMD)" }), _jsx("option", { value: "TOKEN_EFFICIENCY", children: "Token Efficiency (Context Pruning)" }), _jsx("option", { value: "ACCURACY_MAXIMIZATION", children: "Accuracy Maximization" }), _jsx("option", { value: "COST_MINIMIZATION", children: "Cost Minimization" })] })] }), _jsx("div", { className: "flex flex-col justify-end", children: _jsx(Button, { variant: "intelligence", onClick: handleStartEvolution, disabled: running, children: _jsxs("span", { className: "flex items-center gap-2", children: [_jsx(Play, { className: `w-4 h-4 ${running ? 'animate-spin' : ''}` }), running ? 'Executing 10-Stage Cycle...' : 'Launch Self-Evolution Cycle'] }) }) })] })] }), _jsxs("div", { className: "bg-slate-900/80 border border-slate-800 rounded-xl p-6 space-y-4", children: [_jsx("h2", { className: "text-base font-semibold text-slate-100", children: "10-Stage Recursive Pipeline Execution" }), _jsx("div", { className: "grid grid-cols-2 md:grid-cols-5 gap-3 font-mono text-xs", children: steps.map((step, idx) => {
                            const stepNum = idx + 1;
                            const isDone = currentStep > stepNum || (currentStep === 10 && stepNum === 10);
                            const isCurrent = currentStep === stepNum && running;
                            return (_jsxs("div", { className: `p-3 rounded-lg border flex flex-col justify-between space-y-2 transition-all ${isDone
                                    ? 'bg-emerald-950/30 border-emerald-500/40 text-emerald-300'
                                    : isCurrent
                                        ? 'bg-indigo-950/40 border-indigo-500 text-indigo-200 animate-pulse'
                                        : 'bg-slate-950/60 border-slate-800/80 text-slate-500'}`, children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("span", { className: "text-[10px] font-bold", children: ["STAGE ", stepNum] }), isDone ? _jsx(CheckCircle2, { className: "w-3.5 h-3.5 text-emerald-400" }) : null] }), _jsx("div", { className: "text-xs font-medium leading-snug", children: step })] }, idx));
                        }) })] }), result && (_jsxs("div", { className: "bg-slate-900/80 border border-emerald-500/30 rounded-xl p-6 space-y-4 shadow-xl", children: [_jsxs("div", { className: "flex items-center justify-between pb-3 border-b border-slate-800", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx(CheckCircle2, { className: "w-6 h-6 text-emerald-400" }), _jsxs("div", { children: [_jsx("h3", { className: "text-base font-bold text-slate-100", children: "Evolution Cycle Complete & Verified" }), _jsxs("span", { className: "text-xs text-slate-400 font-mono", children: ["Cycle ID: ", result.cycle_id] })] })] }), _jsx(Badge, { variant: "success", size: "sm", children: result.deployment_state })] }), _jsxs("div", { className: "grid grid-cols-2 md:grid-cols-4 gap-4 font-mono text-xs", children: [_jsxs("div", { className: "bg-slate-950/80 p-3 rounded-lg border border-slate-800", children: [_jsx("div", { className: "text-slate-500 text-[10px]", children: "HEALTH BEFORE" }), _jsxs("div", { className: "text-slate-300 text-sm font-bold", children: [(result.health_score_before * 100).toFixed(1), "%"] })] }), _jsxs("div", { className: "bg-slate-950/80 p-3 rounded-lg border border-slate-800", children: [_jsx("div", { className: "text-slate-500 text-[10px]", children: "HEALTH AFTER" }), _jsxs("div", { className: "text-emerald-400 text-sm font-bold", children: [(result.health_score_after * 100).toFixed(1), "%"] })] }), _jsxs("div", { className: "bg-slate-950/80 p-3 rounded-lg border border-slate-800", children: [_jsx("div", { className: "text-slate-500 text-[10px]", children: "EMPIRICAL GAIN" }), _jsxs("div", { className: "text-emerald-400 text-sm font-bold", children: ["+", result.benchmark_improvement_pct, "%"] })] }), _jsxs("div", { className: "bg-slate-950/80 p-3 rounded-lg border border-slate-800", children: [_jsx("div", { className: "text-slate-500 text-[10px]", children: "GOVERNANCE" }), _jsx("div", { className: "text-purple-300 text-sm font-bold", children: result.governance_approved ? 'APPROVED' : 'PENDING' })] })] })] }))] }));
};
