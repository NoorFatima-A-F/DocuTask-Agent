import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { BrainCircuit, Sparkles, CheckCircle2, AlertTriangle, ArrowUpRight, Cpu, Activity, RefreshCw } from 'lucide-react';

export const ReflectionCenter: React.FC = () => {
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

  return (
    <div className="p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-gradient-to-br from-indigo-500/20 to-purple-500/20 border border-indigo-500/30 rounded-xl text-indigo-400">
            <BrainCircuit className="w-5 h-5" />
          </div>
          <div>
            <h1 className="text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2">
              Autonomous Reflection Center
              <Badge variant="intelligence" size="sm">Phase 13.5 Active</Badge>
            </h1>
            <p className="text-xs text-[#94A3B8] font-mono">
              Deep multi-perspective cognitive evaluation across planner decompositions, worker executions, and confidence lineage
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <select
            value={selectedMission}
            onChange={(e) => setSelectedMission(e.target.value)}
            className="bg-[#0F172A] border border-[#334155] rounded-lg px-3 py-1.5 text-xs font-mono text-white focus:outline-none focus:border-indigo-500"
          >
            <option value="mission-001">Mission: mission-001 (Multi-Invoice)</option>
            <option value="mission-002">Mission: mission-002 (Legal Contract)</option>
            <option value="mission-003">Mission: mission-003 (Receipt Wavefront)</option>
          </select>
          <button
            onClick={handleTriggerReflection}
            disabled={isReflecting}
            className="flex items-center gap-2 px-3 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded-lg text-xs font-mono transition-colors disabled:opacity-50"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${isReflecting ? 'animate-spin' : ''}`} />
            {isReflecting ? 'Reflecting...' : 'Run Reflection'}
          </button>
        </div>
      </div>

      {/* Hero Overview Scorecard */}
      <Card className="p-6 rounded-2xl border border-indigo-500/40 bg-gradient-to-br from-[#0F172A] to-[#161936] font-mono shadow-[0_0_20px_rgba(99,102,241,0.15)] space-y-4">
        <div className="flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-4">
          <div>
            <span className="text-xs text-[#64748B] block">AGGREGATE REFLECTION EFFICIENCY</span>
            <div className="flex items-baseline gap-3 mt-1">
              <span className="text-4xl font-extrabold text-white tracking-tight">{reflectionData.overallEfficiency}%</span>
              <Badge variant="success" size="sm">Optimal Execution</Badge>
            </div>
          </div>
          <div className="text-right text-xs text-[#94A3B8] space-y-1">
            <div>Replay Grounding: <span className="text-indigo-400">{reflectionData.targetReplayHash}</span></div>
            <div>Reflection ID: <span className="text-white">{reflectionData.reflectionId}</span></div>
          </div>
        </div>

        {/* 4 Macro KPI Pillars */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 pt-2">
          <div className="p-3 bg-[#0B1120]/60 rounded-xl border border-[#1E293B]">
            <span className="text-[11px] text-[#64748B] block">Throughput Velocity</span>
            <span className="text-lg font-bold text-cyan-400 mt-0.5 block">{reflectionData.macroKpis.throughput}</span>
          </div>
          <div className="p-3 bg-[#0B1120]/60 rounded-xl border border-[#1E293B]">
            <span className="text-[11px] text-[#64748B] block">Execution Duration</span>
            <span className="text-lg font-bold text-indigo-400 mt-0.5 block">{reflectionData.macroKpis.duration}</span>
          </div>
          <div className="p-3 bg-[#0B1120]/60 rounded-xl border border-[#1E293B]">
            <span className="text-[11px] text-[#64748B] block">SLA Adherence</span>
            <span className="text-lg font-bold text-emerald-400 mt-0.5 block">{reflectionData.macroKpis.slaCompliance}</span>
          </div>
          <div className="p-3 bg-[#0B1120]/60 rounded-xl border border-[#1E293B]">
            <span className="text-[11px] text-[#64748B] block">Compute Cost</span>
            <span className="text-lg font-bold text-purple-400 mt-0.5 block">{reflectionData.macroKpis.totalCost}</span>
          </div>
        </div>
      </Card>

      {/* Multi-Perspective Analysis Grids */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Planner Perspective */}
        <Card className="p-5 rounded-xl border border-[#1E293B] bg-[#0F172A] font-mono space-y-4">
          <div className="flex items-center justify-between border-b border-[#1E293B] pb-3">
            <span className="text-xs font-bold text-indigo-400 flex items-center gap-1.5">
              <Cpu className="w-4 h-4" />
              Planner Reflection
            </span>
            <Badge variant="outline" size="sm">{reflectionData.plannerMetrics.schedulingEfficiency}% Sched Eff</Badge>
          </div>
          <div className="space-y-2.5 text-xs">
            <div className="flex justify-between text-[#94A3B8]">
              <span>Goals Planned</span>
              <span className="text-white font-bold">{reflectionData.plannerMetrics.goalsPlanned}</span>
            </div>
            <div className="flex justify-between text-[#94A3B8]">
              <span>Replanning Episodes</span>
              <span className="text-amber-400 font-bold">{reflectionData.plannerMetrics.replanningEpisodes}</span>
            </div>
            <div className="flex justify-between text-[#94A3B8]">
              <span>Plan Mutations</span>
              <span className="text-cyan-400 font-bold">{reflectionData.plannerMetrics.mutationsCount}</span>
            </div>
            <div className="flex justify-between text-[#94A3B8]">
              <span>Parallel Wavefronts</span>
              <span className="text-emerald-400 font-bold">{reflectionData.plannerMetrics.parallelWavefronts}</span>
            </div>
          </div>
        </Card>

        {/* Worker Perspective */}
        <Card className="p-5 rounded-xl border border-[#1E293B] bg-[#0F172A] font-mono space-y-4">
          <div className="flex items-center justify-between border-b border-[#1E293B] pb-3">
            <span className="text-xs font-bold text-teal-400 flex items-center gap-1.5">
              <Activity className="w-4 h-4" />
              Worker Execution Reflection
            </span>
            <Badge variant="outline" size="sm">{reflectionData.workerMetrics.utilizationRate}% Util</Badge>
          </div>
          <div className="space-y-2.5 text-xs">
            <div className="flex justify-between text-[#94A3B8]">
              <span>Total Worker Tasks</span>
              <span className="text-white font-bold">{reflectionData.workerMetrics.totalTasks}</span>
            </div>
            <div className="flex justify-between text-[#94A3B8]">
              <span>Tool Reliability</span>
              <span className="text-emerald-400 font-bold">{reflectionData.workerMetrics.toolReliability}%</span>
            </div>
            <div className="flex justify-between text-[#94A3B8]">
              <span>Worker Drift</span>
              <span className="text-white font-bold">{reflectionData.workerMetrics.workerDrift}</span>
            </div>
            <div className="flex justify-between text-[#94A3B8]">
              <span>Retry Rate</span>
              <span className="text-amber-400 font-bold">{reflectionData.workerMetrics.retryRate}%</span>
            </div>
          </div>
        </Card>

        {/* Confidence Perspective */}
        <Card className="p-5 rounded-xl border border-[#1E293B] bg-[#0F172A] font-mono space-y-4">
          <div className="flex items-center justify-between border-b border-[#1E293B] pb-3">
            <span className="text-xs font-bold text-cyan-400 flex items-center gap-1.5">
              <Sparkles className="w-4 h-4" />
              Confidence Calibration
            </span>
            <Badge variant="success" size="sm">{reflectionData.confidenceMetrics.posteriorGain}</Badge>
          </div>
          <div className="space-y-2.5 text-xs">
            <div className="flex justify-between text-[#94A3B8]">
              <span>Mean Posterior</span>
              <span className="text-cyan-400 font-bold">{reflectionData.confidenceMetrics.avgConfidence}%</span>
            </div>
            <div className="flex justify-between text-[#94A3B8]">
              <span>Stability Score</span>
              <span className="text-emerald-400 font-bold">{reflectionData.confidenceMetrics.stabilityScore}%</span>
            </div>
            <div className="flex justify-between text-[#94A3B8]">
              <span>Confidence Range</span>
              <span className="text-white font-bold">[{reflectionData.confidenceMetrics.minConfidence}%, {reflectionData.confidenceMetrics.maxConfidence}%]</span>
            </div>
            <div className="flex justify-between text-[#94A3B8]">
              <span>Calibration Status</span>
              <span className="text-emerald-400 font-bold">Zero Drift</span>
            </div>
          </div>
        </Card>
      </div>

      {/* Episodes & Institutional Recommendations */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Isolated Episodes */}
        <Card className="p-5 rounded-xl border border-[#1E293B] bg-[#0F172A] font-mono space-y-4">
          <span className="text-xs font-bold text-white block">Isolated Execution Episodes</span>
          
          <div className="space-y-3">
            {reflectionData.failureEpisodes.map((f) => (
              <div key={f.id} className="p-3 bg-red-500/10 border border-red-500/20 rounded-xl space-y-1.5 text-xs">
                <div className="flex items-center justify-between">
                  <span className="text-red-400 font-bold flex items-center gap-1.5">
                    <AlertTriangle className="w-3.5 h-3.5" />
                    Failure Episode: {f.task}
                  </span>
                  <Badge variant="error" size="sm">Recovered ({f.recoveryMs}ms)</Badge>
                </div>
                <p className="text-[#94A3B8]">{f.cause}</p>
                <p className="text-emerald-400 text-[11px]">Mitigation: {f.mitigation}</p>
              </div>
            ))}

            {reflectionData.successEpisodes.map((s) => (
              <div key={s.id} className="p-3 bg-emerald-500/10 border border-emerald-500/20 rounded-xl space-y-1 text-xs">
                <div className="flex items-center justify-between">
                  <span className="text-emerald-400 font-bold flex items-center gap-1.5">
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    Success Episode: {s.pathway}
                  </span>
                  <span className="text-cyan-400 font-bold">{s.gain}</span>
                </div>
                <p className="text-[#94A3B8] text-[11px]">Confidence peak reached: {s.confidencePeak}</p>
              </div>
            ))}
          </div>
        </Card>

        {/* Recommendations */}
        <Card className="p-5 rounded-xl border border-[#1E293B] bg-[#0F172A] font-mono space-y-4">
          <span className="text-xs font-bold text-white block">Institutional Action Recommendations</span>
          <div className="space-y-2.5">
            {reflectionData.recommendations.map((rec, idx) => (
              <div key={idx} className="p-3 bg-[#0B1120] border border-[#1E293B] rounded-xl flex items-start gap-2.5 text-xs">
                <ArrowUpRight className="w-4 h-4 text-indigo-400 shrink-0 mt-0.5" />
                <span className="text-[#F8FAFC]">{rec}</span>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </div>
  );
};
