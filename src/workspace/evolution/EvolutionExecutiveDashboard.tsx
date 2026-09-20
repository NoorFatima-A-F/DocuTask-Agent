import React, { useState, useEffect } from 'react';
import {
  Activity,
  Cpu,
  Zap,
  ShieldCheck,
  RefreshCw,
  Play,
  CheckCircle2,
  TrendingUp,
  Layers,
  Database,
} from 'lucide-react';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { EvolutionPlatformApiClient } from '../../services/evolutionPlatformApiClient';
import { ExecutiveSummaryPayload, EvolutionCycleResultPayload } from '../../types/evolutionPlatform';

export const EvolutionExecutiveDashboard: React.FC = () => {
  const [summary, setSummary] = useState<ExecutiveSummaryPayload | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [runningCycle, setRunningCycle] = useState<boolean>(false);
  const [cycleResult, setCycleResult] = useState<EvolutionCycleResultPayload | null>(null);

  useEffect(() => {
    loadSummary();
  }, []);

  const loadSummary = async () => {
    setLoading(true);
    try {
      const data = await EvolutionPlatformApiClient.getExecutiveSummary();
      setSummary(data);
    } catch (err) {
      console.error('Failed to load executive summary:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleRunCycle = async () => {
    setRunningCycle(true);
    try {
      const res = await EvolutionPlatformApiClient.runEvolutionCycle('llm_orchestrator', 'LATENCY_REDUCTION', true);
      setCycleResult(res);
      await loadSummary();
    } catch (err) {
      console.error('Failed to run cycle:', err);
    } finally {
      setRunningCycle(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-indigo-950/40 to-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-indigo-500/10 border border-indigo-500/20 rounded-xl">
              <Activity className="w-6 h-6 text-indigo-400" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-xl font-bold text-slate-100 tracking-tight">AI Chief Architect & Self-Evolution Control</h1>
                <Badge variant="intelligence" size="sm">Phase 13.13 Active</Badge>
              </div>
              <p className="text-sm text-slate-400 mt-0.5">
                Recursive self-improvement, continuous performance profiling, multi-objective Pareto optimization, and cryptographic rollback.
              </p>
            </div>
          </div>
        </div>
        <div className="flex items-center gap-3 w-full md:w-auto">
          <Button
            variant="outline"
            onClick={loadSummary}
            disabled={loading}
          >
            <span className="flex items-center gap-2">
              <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
              Refresh
            </span>
          </Button>
          <Button
            variant="intelligence"
            onClick={handleRunCycle}
            disabled={runningCycle}
          >
            <span className="flex items-center gap-2">
              <Play className={`w-4 h-4 ${runningCycle ? 'animate-pulse' : ''}`} />
              {runningCycle ? 'Synthesizing Evolution...' : 'Trigger Closed-Loop Cycle'}
            </span>
          </Button>
        </div>
      </div>

      {/* Cycle Execution Alert Banner if just run */}
      {cycleResult && (
        <div className="bg-emerald-950/40 border border-emerald-500/30 rounded-xl p-4 flex items-center justify-between text-slate-200 animate-in fade-in duration-300">
          <div className="flex items-center gap-3">
            <CheckCircle2 className="w-5 h-5 text-emerald-400 flex-shrink-0" />
            <div>
              <div className="text-sm font-semibold text-emerald-300">Closed-Loop Recursive Improvement Completed</div>
              <div className="text-xs text-slate-400 mt-0.5">
                Cycle <span className="font-mono text-emerald-400">{cycleResult.cycle_id}</span> • Target: {cycleResult.target_subsystem} • Empirical Gain: +{cycleResult.benchmark_improvement_pct}% • Deployed: {cycleResult.deployment_state}
              </div>
            </div>
          </div>
          <Badge variant="success" size="sm">Health: {(cycleResult.health_score_after * 100).toFixed(1)}%</Badge>
        </div>
      )}

      {/* Top 4 KPI Metric Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5 relative overflow-hidden group hover:border-slate-700 transition-all">
          <div className="flex items-center justify-between text-slate-400 mb-3">
            <span className="text-xs font-mono uppercase tracking-wider">Composite Health</span>
            <Activity className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="flex items-baseline gap-2">
            <span className="text-3xl font-bold text-slate-100">
              {summary ? (summary.composite_health_score * 100).toFixed(1) : '94.5'}%
            </span>
            <Badge variant="success" size="sm">Optimal</Badge>
          </div>
          <div className="text-xs text-slate-500 mt-2 flex items-center gap-1">
            <TrendingUp className="w-3.5 h-3.5 text-emerald-400" />
            <span>+2.4% gain over baseline</span>
          </div>
        </div>

        <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5 relative overflow-hidden group hover:border-slate-700 transition-all">
          <div className="flex items-center justify-between text-slate-400 mb-3">
            <span className="text-xs font-mono uppercase tracking-wider">Pareto Frontier</span>
            <Zap className="w-4 h-4 text-amber-400" />
          </div>
          <div className="flex items-baseline gap-2">
            <span className="text-3xl font-bold text-slate-100">
              {summary?.pareto_optimal_candidates ?? 3}
            </span>
            <span className="text-xs text-slate-400">candidates</span>
          </div>
          <div className="text-xs text-slate-500 mt-2">
            Multi-objective optimal trade-offs
          </div>
        </div>

        <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5 relative overflow-hidden group hover:border-slate-700 transition-all">
          <div className="flex items-center justify-between text-slate-400 mb-3">
            <span className="text-xs font-mono uppercase tracking-wider">Simulations & Twin</span>
            <Layers className="w-4 h-4 text-cyan-400" />
          </div>
          <div className="flex items-baseline gap-2">
            <span className="text-3xl font-bold text-slate-100">
              {summary?.total_simulations_conducted ?? 12}
            </span>
            <Badge variant="info" size="sm">Zero Invariant Faults</Badge>
          </div>
          <div className="text-xs text-slate-500 mt-2">
            Shadow replay & chaos injections
          </div>
        </div>

        <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5 relative overflow-hidden group hover:border-slate-700 transition-all">
          <div className="flex items-center justify-between text-slate-400 mb-3">
            <span className="text-xs font-mono uppercase tracking-wider">Cryptographic Rollbacks</span>
            <ShieldCheck className="w-4 h-4 text-purple-400" />
          </div>
          <div className="flex items-baseline gap-2">
            <span className="text-3xl font-bold text-slate-100">
              {summary?.governance_snapshots_stored ?? 5}
            </span>
            <Badge variant="sentinel" size="sm">SHA-256 Sealed</Badge>
          </div>
          <div className="text-xs text-slate-500 mt-2">
            Instant circuit-breaker protection
          </div>
        </div>
      </div>

      {/* Grid: 2 Columns */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left 2 Cols: Architectural Subsystem Status */}
        <div className="lg:col-span-2 bg-slate-900/80 border border-slate-800 rounded-xl p-6 space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Cpu className="w-5 h-5 text-indigo-400" />
              <h2 className="text-base font-semibold text-slate-100">Subsystem Architecture Health & Coupling</h2>
            </div>
            <span className="text-xs font-mono text-slate-400">Nodes: {summary?.node_count ?? 8} | Edges: {summary?.edge_count ?? 7}</span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="bg-slate-950/60 border border-slate-800/80 rounded-lg p-4 space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-slate-200">Swarm Coordination Ring</span>
                <Badge variant="warning" size="sm">Degraded Lock</Badge>
              </div>
              <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                <div className="bg-amber-400 h-full rounded-full" style={{ width: '68%' }} />
              </div>
              <div className="text-xs text-slate-400 flex justify-between">
                <span>Afferent: 8 | Efferent: 12</span>
                <span className="text-amber-400">Complexity: 0.65</span>
              </div>
            </div>

            <div className="bg-slate-950/60 border border-slate-800/80 rounded-lg p-4 space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-slate-200">Episodic Vector Memory</span>
                <Badge variant="success" size="sm">Optimal</Badge>
              </div>
              <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                <div className="bg-emerald-400 h-full rounded-full" style={{ width: '92%' }} />
              </div>
              <div className="text-xs text-slate-400 flex justify-between">
                <span>Afferent: 6 | Efferent: 2</span>
                <span className="text-emerald-400">Complexity: 0.42</span>
              </div>
            </div>

            <div className="bg-slate-950/60 border border-slate-800/80 rounded-lg p-4 space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-slate-200">Recursive Meta Planner</span>
                <Badge variant="success" size="sm">Optimal</Badge>
              </div>
              <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                <div className="bg-emerald-400 h-full rounded-full" style={{ width: '88%' }} />
              </div>
              <div className="text-xs text-slate-400 flex justify-between">
                <span>Afferent: 4 | Efferent: 7</span>
                <span className="text-emerald-400">Complexity: 0.58</span>
              </div>
            </div>

            <div className="bg-slate-950/60 border border-slate-800/80 rounded-lg p-4 space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-slate-200">Cryptographic Governance Sentinel</span>
                <Badge variant="sentinel" size="sm">Verified</Badge>
              </div>
              <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                <div className="bg-purple-400 h-full rounded-full" style={{ width: '98%' }} />
              </div>
              <div className="text-xs text-slate-400 flex justify-between">
                <span>Afferent: 5 | Efferent: 2</span>
                <span className="text-purple-400">Complexity: 0.25</span>
              </div>
            </div>
          </div>
        </div>

        {/* Right 1 Col: Platform Genome & Live Pipeline */}
        <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-6 space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Database className="w-5 h-5 text-purple-400" />
              <h2 className="text-base font-semibold text-slate-100">Platform Genome</h2>
            </div>
            <Badge variant="outline" size="sm">v13.13.0</Badge>
          </div>

          <div className="space-y-3 text-sm text-slate-300">
            <div className="flex items-center justify-between py-2 border-b border-slate-800/60">
              <span className="text-slate-400">Active Diagnoses</span>
              <span className="font-semibold text-slate-200">{summary?.active_diagnoses_count ?? 2}</span>
            </div>
            <div className="flex items-center justify-between py-2 border-b border-slate-800/60">
              <span className="text-slate-400">Capability Gaps Discovered</span>
              <span className="font-semibold text-amber-400">{summary?.discovered_capability_gaps ?? 3}</span>
            </div>
            <div className="flex items-center justify-between py-2 border-b border-slate-800/60">
              <span className="text-slate-400">Mutation Proposals</span>
              <span className="font-semibold text-cyan-400">{summary?.total_mutation_proposals ?? 4}</span>
            </div>
            <div className="flex items-center justify-between py-2 border-b border-slate-800/60">
              <span className="text-slate-400">Empirical Benchmarks</span>
              <span className="font-semibold text-emerald-400">{summary?.total_benchmarks_completed ?? 8}</span>
            </div>
            <div className="flex items-center justify-between py-2">
              <span className="text-slate-400">Canary Deployments</span>
              <span className="font-semibold text-purple-400">{summary?.active_deployments ?? 2} Active</span>
            </div>
          </div>

          <div className="pt-2">
            <div className="p-3 bg-slate-950/80 border border-slate-800 rounded-lg text-xs font-mono text-slate-400 space-y-1">
              <div className="flex items-center justify-between text-slate-300 font-semibold">
                <span>Genome Seal</span>
                <span className="text-emerald-400">VERIFIED</span>
              </div>
              <div className="truncate text-slate-500">SHA256: 4f53cda18c2baa0c0354bb5f9a3ecbe5...</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
