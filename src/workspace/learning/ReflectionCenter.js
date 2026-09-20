import { jsx as _jsx, jsxs as _jsxs } from "react/jsx-runtime";
import { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { BrainCircuit, Sparkles, CheckCircle2, AlertTriangle, ArrowUpRight, Cpu, Activity, RefreshCw } from 'lucide-react';
export const ReflectionCenter = () => {
    const [selectedMission, setSelectedMission] = useState('mission-001');
    const [isReflecting, setIsReflecting] = useState(false);
    const reflectionData = {
        reflectionId: 'refl_89f1a02',
        missionId: selectedMission,
        targetReplayHash: 'sha256:7f9a2b1c4e0d98',
        overallEfficiency: 96.4,
        status: 'VERIFIED',
        macroKpis: {
            throughput: '14.8 tasks/sec',
            duration: '2.45s',
            slaCompliance: '99.2%',
            totalCost: '$0.0034 USD',
        },
        plannerMetrics: {
            goalsPlanned: 4,
            replanningEpisodes: 1,
            mutationsCount: 2,
            parallelWavefronts: 3,
            schedulingEfficiency: 96.2,
        },
        workerMetrics: {
            totalTasks: 14,
            utilizationRate: 88.4,
            toolReliability: 97.8,
            workerDrift: 0,
            retryRate: 4.0,
        },
        confidenceMetrics: {
            avgConfidence: 94.6,
            minConfidence: 88.0,
            maxConfidence: 98.5,
            stabilityScore: 96.2,
            posteriorGain: '+8.5%',
        },
        failureEpisodes: [
            {
                id: 'fail-ep-001',
                task: 'task-ocr-shard-03',
                cause: 'OCR rate throttle limit (429 Too Many Requests)',
                mitigation: 'Exponential backoff with 250ms base jitter',
                recoveryMs: 240,
                severity: 'LOW',
            },
        ],
        successEpisodes: [
            {
                id: 'succ-ep-001',
                pathway: 'Vectorized Batch Partitioning',
                gain: '+34.2% speedup',
                confidencePeak: '98.5%',
            },
            {
                id: 'succ-ep-002',
                pathway: 'SMT Invariant Schema Verification',
                gain: '100% truth consistency',
                confidencePeak: '99.9%',
            },
        ],
        recommendations: [
            'Promote dynamic OCR sharding to baseline planner template',
            'Maintain minimum 0.85 posterior confidence floor on entity extraction',
            'Adopt 3-way parallel wavefront executor for document sets > 10 pages',
        ],
    };
    const handleTriggerReflection = () => {
        setIsReflecting(true);
        setTimeout(() => {
            setIsReflecting(false);
        }, 800);
    };
    return (_jsxs("div", { className: "p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]", children: [_jsxs("div", { className: "flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6", children: [_jsxs("div", { className: "flex items-center gap-3", children: [_jsx("div", { className: "p-2 bg-gradient-to-br from-indigo-500/20 to-purple-500/20 border border-indigo-500/30 rounded-xl text-indigo-400", children: _jsx(BrainCircuit, { className: "w-5 h-5" }) }), _jsxs("div", { children: [_jsxs("h1", { className: "text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2", children: ["Autonomous Reflection Center", _jsx(Badge, { variant: "intelligence", size: "sm", children: "Phase 13.5 Active" })] }), _jsx("p", { className: "text-xs text-[#94A3B8] font-mono", children: "Deep multi-perspective cognitive evaluation across planner decompositions, worker executions, and confidence lineage" })] })] }), _jsxs("div", { className: "flex items-center gap-3", children: [_jsxs("select", { value: selectedMission, onChange: (e) => setSelectedMission(e.target.value), className: "bg-[#0F172A] border border-[#334155] rounded-lg px-3 py-1.5 text-xs font-mono text-white focus:outline-none focus:border-indigo-500", children: [_jsx("option", { value: "mission-001", children: "Mission: mission-001 (Multi-Invoice)" }), _jsx("option", { value: "mission-002", children: "Mission: mission-002 (Legal Contract)" }), _jsx("option", { value: "mission-003", children: "Mission: mission-003 (Receipt Wavefront)" })] }), _jsxs("button", { onClick: handleTriggerReflection, disabled: isReflecting, className: "flex items-center gap-2 px-3 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-xs font-mono transition-colors disabled:opacity-50", children: [_jsx(RefreshCw, { className: `w-3.5 h-3.5 ${isReflecting ? 'animate-spin' : ''}` }), isReflecting ? 'Reflecting...' : 'Run Reflection'] })] })] }), _jsxs(Card, { className: "p-6 rounded-2xl border border-indigo-500/40 bg-gradient-to-br from-[#0F172A] to-[#161936] font-mono shadow-[0_0_20px_rgba(99,102,241,0.15)] space-y-4", children: [_jsxs("div", { className: "flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-4", children: [_jsxs("div", { children: [_jsx("span", { className: "text-xs text-[#64748B] block", children: "AGGREGATE REFLECTION EFFICIENCY" }), _jsxs("div", { className: "flex items-baseline gap-3 mt-1", children: [_jsxs("span", { className: "text-4xl font-extrabold text-white tracking-tight", children: [reflectionData.overallEfficiency, "%"] }), _jsx(Badge, { variant: "success", size: "sm", children: "Optimal Execution" })] })] }), _jsxs("div", { className: "text-right text-xs text-[#94A3B8] space-y-1", children: [_jsxs("div", { children: ["Replay Grounding: ", _jsx("span", { className: "text-indigo-400", children: reflectionData.targetReplayHash })] }), _jsxs("div", { children: ["Reflection ID: ", _jsx("span", { className: "text-white", children: reflectionData.reflectionId })] })] })] }), _jsxs("div", { className: "grid grid-cols-2 sm:grid-cols-4 gap-4 pt-2", children: [_jsxs("div", { className: "p-3 bg-[#0B1120]/60 rounded-xl border border-[#1E293B]", children: [_jsx("span", { className: "text-[11px] text-[#64748B] block", children: "Throughput Velocity" }), _jsx("span", { className: "text-lg font-bold text-cyan-400 mt-0.5 block", children: reflectionData.macroKpis.throughput })] }), _jsxs("div", { className: "p-3 bg-[#0B1120]/60 rounded-xl border border-[#1E293B]", children: [_jsx("span", { className: "text-[11px] text-[#64748B] block", children: "Execution Duration" }), _jsx("span", { className: "text-lg font-bold text-indigo-400 mt-0.5 block", children: reflectionData.macroKpis.duration })] }), _jsxs("div", { className: "p-3 bg-[#0B1120]/60 rounded-xl border border-[#1E293B]", children: [_jsx("span", { className: "text-[11px] text-[#64748B] block", children: "SLA Adherence" }), _jsx("span", { className: "text-lg font-bold text-emerald-400 mt-0.5 block", children: reflectionData.macroKpis.slaCompliance })] }), _jsxs("div", { className: "p-3 bg-[#0B1120]/60 rounded-xl border border-[#1E293B]", children: [_jsx("span", { className: "text-[11px] text-[#64748B] block", children: "Compute Cost" }), _jsx("span", { className: "text-lg font-bold text-purple-400 mt-0.5 block", children: reflectionData.macroKpis.totalCost })] })] })] }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-3 gap-6", children: [_jsxs(Card, { className: "p-5 rounded-xl border border-[#1E293B] bg-[#0F172A] font-mono space-y-4", children: [_jsxs("div", { className: "flex items-center justify-between border-b border-[#1E293B] pb-3", children: [_jsxs("span", { className: "text-xs font-bold text-indigo-400 flex items-center gap-1.5", children: [_jsx(Cpu, { className: "w-4 h-4" }), "Planner Reflection"] }), _jsxs(Badge, { variant: "outline", size: "sm", children: [reflectionData.plannerMetrics.schedulingEfficiency, "% Sched Eff"] })] }), _jsxs("div", { className: "space-y-2.5 text-xs", children: [_jsxs("div", { className: "flex justify-between text-[#94A3B8]", children: [_jsx("span", { children: "Goals Planned" }), _jsx("span", { className: "text-white font-bold", children: reflectionData.plannerMetrics.goalsPlanned })] }), _jsxs("div", { className: "flex justify-between text-[#94A3B8]", children: [_jsx("span", { children: "Replanning Episodes" }), _jsx("span", { className: "text-amber-400 font-bold", children: reflectionData.plannerMetrics.replanningEpisodes })] }), _jsxs("div", { className: "flex justify-between text-[#94A3B8]", children: [_jsx("span", { children: "Plan Mutations" }), _jsx("span", { className: "text-cyan-400 font-bold", children: reflectionData.plannerMetrics.mutationsCount })] }), _jsxs("div", { className: "flex justify-between text-[#94A3B8]", children: [_jsx("span", { children: "Parallel Wavefronts" }), _jsx("span", { className: "text-emerald-400 font-bold", children: reflectionData.plannerMetrics.parallelWavefronts })] })] })] }), _jsxs(Card, { className: "p-5 rounded-xl border border-[#1E293B] bg-[#0F172A] font-mono space-y-4", children: [_jsxs("div", { className: "flex items-center justify-between border-b border-[#1E293B] pb-3", children: [_jsxs("span", { className: "text-xs font-bold text-teal-400 flex items-center gap-1.5", children: [_jsx(Activity, { className: "w-4 h-4" }), "Worker Execution Reflection"] }), _jsxs(Badge, { variant: "outline", size: "sm", children: [reflectionData.workerMetrics.utilizationRate, "% Util"] })] }), _jsxs("div", { className: "space-y-2.5 text-xs", children: [_jsxs("div", { className: "flex justify-between text-[#94A3B8]", children: [_jsx("span", { children: "Total Worker Tasks" }), _jsx("span", { className: "text-white font-bold", children: reflectionData.workerMetrics.totalTasks })] }), _jsxs("div", { className: "flex justify-between text-[#94A3B8]", children: [_jsx("span", { children: "Tool Reliability" }), _jsxs("span", { className: "text-emerald-400 font-bold", children: [reflectionData.workerMetrics.toolReliability, "%"] })] }), _jsxs("div", { className: "flex justify-between text-[#94A3B8]", children: [_jsx("span", { children: "Worker Drift" }), _jsx("span", { className: "text-white font-bold", children: reflectionData.workerMetrics.workerDrift })] }), _jsxs("div", { className: "flex justify-between text-[#94A3B8]", children: [_jsx("span", { children: "Retry Rate" }), _jsxs("span", { className: "text-amber-400 font-bold", children: [reflectionData.workerMetrics.retryRate, "%"] })] })] })] }), _jsxs(Card, { className: "p-5 rounded-xl border border-[#1E293B] bg-[#0F172A] font-mono space-y-4", children: [_jsxs("div", { className: "flex items-center justify-between border-b border-[#1E293B] pb-3", children: [_jsxs("span", { className: "text-xs font-bold text-cyan-400 flex items-center gap-1.5", children: [_jsx(Sparkles, { className: "w-4 h-4" }), "Confidence Calibration"] }), _jsx(Badge, { variant: "success", size: "sm", children: reflectionData.confidenceMetrics.posteriorGain })] }), _jsxs("div", { className: "space-y-2.5 text-xs", children: [_jsxs("div", { className: "flex justify-between text-[#94A3B8]", children: [_jsx("span", { children: "Mean Posterior" }), _jsxs("span", { className: "text-cyan-400 font-bold", children: [reflectionData.confidenceMetrics.avgConfidence, "%"] })] }), _jsxs("div", { className: "flex justify-between text-[#94A3B8]", children: [_jsx("span", { children: "Stability Score" }), _jsxs("span", { className: "text-emerald-400 font-bold", children: [reflectionData.confidenceMetrics.stabilityScore, "%"] })] }), _jsxs("div", { className: "flex justify-between text-[#94A3B8]", children: [_jsx("span", { children: "Confidence Range" }), _jsxs("span", { className: "text-white font-bold", children: ["[", reflectionData.confidenceMetrics.minConfidence, "%, ", reflectionData.confidenceMetrics.maxConfidence, "%]"] })] }), _jsxs("div", { className: "flex justify-between text-[#94A3B8]", children: [_jsx("span", { children: "Calibration Status" }), _jsx("span", { className: "text-emerald-400 font-bold", children: "Zero Drift" })] })] })] })] }), _jsxs("div", { className: "grid grid-cols-1 lg:grid-cols-2 gap-6", children: [_jsxs(Card, { className: "p-5 rounded-xl border border-[#1E293B] bg-[#0F172A] font-mono space-y-4", children: [_jsx("span", { className: "text-xs font-bold text-white block", children: "Isolated Execution Episodes" }), _jsxs("div", { className: "space-y-3", children: [reflectionData.failureEpisodes.map((f) => (_jsxs("div", { className: "p-3 bg-red-500/10 border border-red-500/20 rounded-xl space-y-1.5 text-xs", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("span", { className: "text-red-400 font-bold flex items-center gap-1.5", children: [_jsx(AlertTriangle, { className: "w-3.5 h-3.5" }), "Failure Episode: ", f.task] }), _jsxs(Badge, { variant: "error", size: "sm", children: ["Recovered (", f.recoveryMs, "ms)"] })] }), _jsx("p", { className: "text-[#94A3B8]", children: f.cause }), _jsxs("p", { className: "text-emerald-400 text-[11px]", children: ["Mitigation: ", f.mitigation] })] }, f.id))), reflectionData.successEpisodes.map((s) => (_jsxs("div", { className: "p-3 bg-emerald-500/10 border border-emerald-500/20 rounded-xl space-y-1 text-xs", children: [_jsxs("div", { className: "flex items-center justify-between", children: [_jsxs("span", { className: "text-emerald-400 font-bold flex items-center gap-1.5", children: [_jsx(CheckCircle2, { className: "w-3.5 h-3.5" }), "Success Episode: ", s.pathway] }), _jsx("span", { className: "text-cyan-400 font-bold", children: s.gain })] }), _jsxs("p", { className: "text-[#94A3B8] text-[11px]", children: ["Confidence peak reached: ", s.confidencePeak] })] }, s.id)))] })] }), _jsxs(Card, { className: "p-5 rounded-xl border border-[#1E293B] bg-[#0F172A] font-mono space-y-4", children: [_jsx("span", { className: "text-xs font-bold text-white block", children: "Institutional Action Recommendations" }), _jsx("div", { className: "space-y-2.5", children: reflectionData.recommendations.map((rec, idx) => (_jsxs("div", { className: "p-3 bg-[#0B1120] border border-[#1E293B] rounded-xl flex items-start gap-2.5 text-xs", children: [_jsx(ArrowUpRight, { className: "w-4 h-4 text-indigo-400 shrink-0 mt-0.5" }), _jsx("span", { className: "text-[#F8FAFC]", children: rec })] }, idx))) })] })] })] }));
};
