import React, { useState } from 'react';
import {
  Sparkles,
  Play,
  CheckCircle2,
} from 'lucide-react';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { EvolutionPlatformApiClient } from '../../services/evolutionPlatformApiClient';
import { EvolutionCycleResultPayload } from '../../types/evolutionPlatform';

export const ContinuousImprovementCenter: React.FC = () => {
  const [running, setRunning] = useState<boolean>(false);
  const [currentStep, setCurrentStep] = useState<number>(0);
  const [result, setResult] = useState<EvolutionCycleResultPayload | null>(null);

  // Configuration
  const [targetSubsystem, setTargetSubsystem] = useState<string>('llm_orchestrator');
  const [objective, setObjective] = useState<string>('LATENCY_REDUCTION');
  const [autoDeploy] = useState<boolean>(true);

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
    } catch (err) {
      clearInterval(interval);
      console.error('Evolution cycle failed:', err);
    } finally {
      setRunning(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-slate-900 via-indigo-950/40 to-slate-900 border border-slate-800 rounded-2xl p-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-4 shadow-xl">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-indigo-500/10 border border-indigo-500/20 rounded-xl">
            <Sparkles className="w-6 h-6 text-indigo-400" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl font-bold text-slate-100">Continuous Closed-Loop Self-Evolution Studio</h1>
              <Badge variant="intelligence" size="sm">Autonomous AI Chief Architect</Badge>
            </div>
            <p className="text-sm text-slate-400 mt-0.5">
              Execute full 10-stage end-to-end recursive self-evolution cycles with automated simulation, benchmarking, governance, and canary promotion.
            </p>
          </div>
        </div>
      </div>

      {/* Control Card */}
      <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-6 space-y-4">
        <h2 className="text-base font-semibold text-slate-100">Configure Evolution Parameters</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
          <div>
            <label className="text-xs font-medium text-slate-400 block mb-1">Target Subsystem</label>
            <select
              value={targetSubsystem}
              onChange={(e) => setTargetSubsystem(e.target.value)}
              disabled={running}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-indigo-500"
            >
              <option value="llm_orchestrator">LLM Orchestrator & Planner</option>
              <option value="memory_layer">Episodic Vector Memory</option>
              <option value="swarm_coordination">Swarm Coordination Ring</option>
              <option value="document_parser">Document Layout Parser</option>
            </select>
          </div>

          <div>
            <label className="text-xs font-medium text-slate-400 block mb-1">Evolution Objective</label>
            <select
              value={objective}
              onChange={(e) => setObjective(e.target.value)}
              disabled={running}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-indigo-500"
            >
              <option value="LATENCY_REDUCTION">Latency Reduction (Lock-Free SIMD)</option>
              <option value="TOKEN_EFFICIENCY">Token Efficiency (Context Pruning)</option>
              <option value="ACCURACY_MAXIMIZATION">Accuracy Maximization</option>
              <option value="COST_MINIMIZATION">Cost Minimization</option>
            </select>
          </div>

          <div className="flex flex-col justify-end">
            <Button
              variant="intelligence"
              onClick={handleStartEvolution}
              disabled={running}
            >
              <span className="flex items-center gap-2">
                <Play className={`w-4 h-4 ${running ? 'animate-spin' : ''}`} />
                {running ? 'Executing 10-Stage Cycle...' : 'Launch Self-Evolution Cycle'}
              </span>
            </Button>
          </div>
        </div>
      </div>

      {/* 10-Stage Progress Stepper */}
      <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-6 space-y-4">
        <h2 className="text-base font-semibold text-slate-100">10-Stage Recursive Pipeline Execution</h2>

        <div className="grid grid-cols-2 md:grid-cols-5 gap-3 font-mono text-xs">
          {steps.map((step, idx) => {
            const stepNum = idx + 1;
            const isDone = currentStep > stepNum || (currentStep === 10 && stepNum === 10);
            const isCurrent = currentStep === stepNum && running;

            return (
              <div
                key={idx}
                className={`p-3 rounded-lg border flex flex-col justify-between space-y-2 transition-all ${
                  isDone
                    ? 'bg-emerald-950/30 border-emerald-500/40 text-emerald-300'
                    : isCurrent
                    ? 'bg-indigo-950/40 border-indigo-500 text-indigo-200 animate-pulse'
                    : 'bg-slate-950/60 border-slate-800/80 text-slate-500'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-bold">STAGE {stepNum}</span>
                  {isDone ? <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" /> : null}
                </div>
                <div className="text-xs font-medium leading-snug">{step}</div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Result Outcome Display */}
      {result && (
        <div className="bg-slate-900/80 border border-emerald-500/30 rounded-xl p-6 space-y-4 shadow-xl">
          <div className="flex items-center justify-between pb-3 border-b border-slate-800">
            <div className="flex items-center gap-3">
              <CheckCircle2 className="w-6 h-6 text-emerald-400" />
              <div>
                <h3 className="text-base font-bold text-slate-100">Evolution Cycle Complete & Verified</h3>
                <span className="text-xs text-slate-400 font-mono">Cycle ID: {result.cycle_id}</span>
              </div>
            </div>
            <Badge variant="success" size="sm">{result.deployment_state}</Badge>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 font-mono text-xs">
            <div className="bg-slate-950/80 p-3 rounded-lg border border-slate-800">
              <div className="text-slate-500 text-[10px]">HEALTH BEFORE</div>
              <div className="text-slate-300 text-sm font-bold">{(result.health_score_before * 100).toFixed(1)}%</div>
            </div>
            <div className="bg-slate-950/80 p-3 rounded-lg border border-slate-800">
              <div className="text-slate-500 text-[10px]">HEALTH AFTER</div>
              <div className="text-emerald-400 text-sm font-bold">{(result.health_score_after * 100).toFixed(1)}%</div>
            </div>
            <div className="bg-slate-950/80 p-3 rounded-lg border border-slate-800">
              <div className="text-slate-500 text-[10px]">EMPIRICAL GAIN</div>
              <div className="text-emerald-400 text-sm font-bold">+{result.benchmark_improvement_pct}%</div>
            </div>
            <div className="bg-slate-950/80 p-3 rounded-lg border border-slate-800">
              <div className="text-slate-500 text-[10px]">GOVERNANCE</div>
              <div className="text-purple-300 text-sm font-bold">{result.governance_approved ? 'APPROVED' : 'PENDING'}</div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
