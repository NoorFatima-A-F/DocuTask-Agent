import React, { useState, useEffect } from 'react';
import {
  BarChart3,
  Play,
  RefreshCw,
  Clock,
  Zap,
  Target,
} from 'lucide-react';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { EvolutionPlatformApiClient } from '../../services/evolutionPlatformApiClient';
import { BenchmarkComparisonPayload } from '../../types/evolutionPlatform';

export const BenchmarkAnalyticsCenter: React.FC = () => {
  const [benchmarks, setBenchmarks] = useState<BenchmarkComparisonPayload[]>([]);
  const [latestBenchmark, setLatestBenchmark] = useState<BenchmarkComparisonPayload | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [running, setRunning] = useState<boolean>(false);

  useEffect(() => {
    loadBenchmarks();
  }, []);

  const loadBenchmarks = async () => {
    setLoading(true);
    try {
      const data = await EvolutionPlatformApiClient.listBenchmarks();
      setBenchmarks(data);
      if (data.length > 0) {
        const last = data[data.length - 1];
        if (last) setLatestBenchmark(last);
      }
    } catch (err) {
      console.error('Failed to load benchmarks:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleRunBenchmark = async () => {
    setRunning(true);
    try {
      const res = await EvolutionPlatformApiClient.runBenchmark({
        baseline_version: 'v13.12-prod',
        candidate_version: `v13.13-eval-${Math.random().toString(36).substring(2, 6)}`,
        test_case_count: 500,
      });
      setLatestBenchmark(res);
      setBenchmarks((prev) => [...prev, res]);
    } catch (err) {
      console.error('Benchmark error:', err);
    } finally {
      setRunning(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-slate-900 via-slate-900 to-slate-950 border border-slate-800 rounded-2xl p-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-4 shadow-xl">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-emerald-500/10 border border-emerald-500/20 rounded-xl">
            <BarChart3 className="w-6 h-6 text-emerald-400" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl font-bold text-slate-100">Empirical Benchmark Analytics Center</h1>
              <Badge variant="success" size="sm">Side-by-Side Trials</Badge>
            </div>
            <p className="text-sm text-slate-400 mt-0.5">
              Empirical side-by-side comparative testing across thousands of synthetic and production workloads.
            </p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <Button
            variant="outline"
            onClick={loadBenchmarks}
            disabled={loading}
          >
            <span className="flex items-center gap-2">
              <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
              Refresh
            </span>
          </Button>
          <Button
            variant="intelligence"
            onClick={handleRunBenchmark}
            disabled={running}
          >
            <span className="flex items-center gap-2">
              <Play className={`w-4 h-4 ${running ? 'animate-spin' : ''}`} />
              {running ? 'Executing 500 Trials...' : 'Run Empirical Benchmark'}
            </span>
          </Button>
        </div>
      </div>

      {/* Latest Benchmark Head-to-Head Card */}
      {latestBenchmark && (
        <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-6 space-y-5">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 pb-4 border-b border-slate-800">
            <div>
              <div className="flex items-center gap-3">
                <h2 className="text-base font-bold text-slate-100">
                  {latestBenchmark.baseline_version} vs. {latestBenchmark.candidate_version}
                </h2>
                <Badge
                  variant={latestBenchmark.status === 'PASSED' ? 'success' : 'error'}
                  size="sm"
                >
                  {latestBenchmark.status}
                </Badge>
              </div>
              <span className="text-xs text-slate-400 font-mono mt-0.5 block">
                {latestBenchmark.test_cases_run} test cases evaluated • Safe: {latestBenchmark.safety_compliance_score === 1.0 ? '100%' : 'Degraded'}
              </span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-xs text-slate-400">Net Improvement:</span>
              <span className="text-xl font-bold text-emerald-400 font-mono">
                +{latestBenchmark.improvement_score_pct.toFixed(1)}%
              </span>
            </div>
          </div>

          {/* Side-by-side metric tiles */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 font-mono">
            {/* Latency */}
            <div className="bg-slate-950/80 border border-slate-800 rounded-lg p-4 space-y-2">
              <div className="flex items-center justify-between text-xs text-slate-400">
                <span className="flex items-center gap-1.5">
                  <Clock className="w-4 h-4 text-indigo-400" />
                  P95 Latency
                </span>
                <span className="text-emerald-400 font-bold">
                  -{(((latestBenchmark.baseline_latency_p95 - latestBenchmark.candidate_latency_p95) / latestBenchmark.baseline_latency_p95) * 100).toFixed(1)}%
                </span>
              </div>
              <div className="flex items-baseline justify-between pt-1">
                <div className="text-xs text-slate-500">
                  Base: <span className="text-slate-300">{latestBenchmark.baseline_latency_p95.toFixed(1)}ms</span>
                </div>
                <div className="text-sm font-bold text-indigo-300">
                  Cand: {latestBenchmark.candidate_latency_p95.toFixed(1)}ms
                </div>
              </div>
            </div>

            {/* Token Cost */}
            <div className="bg-slate-950/80 border border-slate-800 rounded-lg p-4 space-y-2">
              <div className="flex items-center justify-between text-xs text-slate-400">
                <span className="flex items-center gap-1.5">
                  <Zap className="w-4 h-4 text-amber-400" />
                  Token Cost / Task
                </span>
                <span className="text-emerald-400 font-bold">
                  -{(((latestBenchmark.baseline_token_cost - latestBenchmark.candidate_token_cost) / latestBenchmark.baseline_token_cost) * 100).toFixed(1)}%
                </span>
              </div>
              <div className="flex items-baseline justify-between pt-1">
                <div className="text-xs text-slate-500">
                  Base: <span className="text-slate-300">${latestBenchmark.baseline_token_cost.toFixed(4)}</span>
                </div>
                <div className="text-sm font-bold text-amber-300">
                  Cand: ${latestBenchmark.candidate_token_cost.toFixed(4)}
                </div>
              </div>
            </div>

            {/* Accuracy */}
            <div className="bg-slate-950/80 border border-slate-800 rounded-lg p-4 space-y-2">
              <div className="flex items-center justify-between text-xs text-slate-400">
                <span className="flex items-center gap-1.5">
                  <Target className="w-4 h-4 text-emerald-400" />
                  Accuracy
                </span>
                <span className="text-emerald-400 font-bold">
                  +{(((latestBenchmark.candidate_accuracy - latestBenchmark.baseline_accuracy) / latestBenchmark.baseline_accuracy) * 100).toFixed(2)}%
                </span>
              </div>
              <div className="flex items-baseline justify-between pt-1">
                <div className="text-xs text-slate-500">
                  Base: <span className="text-slate-300">{(latestBenchmark.baseline_accuracy * 100).toFixed(1)}%</span>
                </div>
                <div className="text-sm font-bold text-emerald-300">
                  Cand: {(latestBenchmark.candidate_accuracy * 100).toFixed(1)}%
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Historical Benchmarks List */}
      <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-6 space-y-4">
        <h2 className="text-base font-semibold text-slate-100">Benchmark Trial History</h2>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-300 font-mono">
            <thead className="bg-slate-950/60 text-slate-400 border-b border-slate-800 uppercase tracking-wider">
              <tr>
                <th className="py-2.5 px-3">Trial ID</th>
                <th className="py-2.5 px-3">Baseline</th>
                <th className="py-2.5 px-3">Candidate</th>
                <th className="py-2.5 px-3">P95 Δ</th>
                <th className="py-2.5 px-3">Cost Δ</th>
                <th className="py-2.5 px-3">Net Score</th>
                <th className="py-2.5 px-3">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {benchmarks.slice().reverse().map((b) => (
                <tr key={b.comparison_id} className="hover:bg-slate-800/30 transition-colors">
                  <td className="py-2.5 px-3 font-semibold text-slate-300">{b.comparison_id}</td>
                  <td className="py-2.5 px-3 text-slate-400">{b.baseline_version}</td>
                  <td className="py-2.5 px-3 text-indigo-300">{b.candidate_version}</td>
                  <td className="py-2.5 px-3 text-emerald-400">
                    -{(((b.baseline_latency_p95 - b.candidate_latency_p95) / b.baseline_latency_p95) * 100).toFixed(1)}%
                  </td>
                  <td className="py-2.5 px-3 text-emerald-400">
                    -{(((b.baseline_token_cost - b.candidate_token_cost) / b.baseline_token_cost) * 100).toFixed(1)}%
                  </td>
                  <td className="py-2.5 px-3 font-bold text-emerald-400">+{b.improvement_score_pct.toFixed(1)}%</td>
                  <td className="py-2.5 px-3">
                    <Badge variant={b.status === 'PASSED' ? 'success' : 'error'} size="sm">
                      {b.status}
                    </Badge>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
