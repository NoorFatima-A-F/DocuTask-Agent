import React, { useState, useEffect } from 'react';
import {
  Activity,
  ShieldCheck,
  Zap,
  Play,
  RotateCw,
  Clock,
  DollarSign,
  TrendingUp,
} from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { AIOperationsApiClient } from '../../services/aiOperationsApiClient';
import { OperationsOverview, AgentTelemetry } from '../../types/aiOperations';

export const AIOperationsExecutiveDashboard: React.FC = () => {
  const [overview, setOverview] = useState<OperationsOverview | null>(null);
  const [fleet, setFleet] = useState<AgentTelemetry[]>([]);
  const [loading, setLoading] = useState(true);
  const [runningCycle, setRunningCycle] = useState(false);
  const [cycleResult, setCycleResult] = useState<any>(null);

  const loadData = async () => {
    try {
      setLoading(true);
      const [ov, fl] = await Promise.all([
        AIOperationsApiClient.getOverview(),
        AIOperationsApiClient.getFleetTelemetry(),
      ]);
      setOverview(ov);
      setFleet(fl);
    } catch (err) {
      console.error('Failed to load AI operations overview:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleRunOperationsCycle = async () => {
    try {
      setRunningCycle(true);
      const res = await AIOperationsApiClient.runOperationsCycle('agent_chief_architect');
      setCycleResult(res);
      await loadData();
    } catch (err) {
      console.error('Failed to run operations cycle:', err);
    } finally {
      setRunningCycle(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 bg-slate-900/60 p-6 rounded-2xl border border-slate-800/80 backdrop-blur-md">
        <div>
          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-indigo-500/10 rounded-xl border border-indigo-500/20">
              <Activity className="w-6 h-6 text-indigo-400" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-white tracking-tight">AI Operations Control Center</h1>
              <p className="text-sm text-slate-400">Enterprise Agent Observability, Evaluation & Controlled Improvement</p>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <Button variant="outline" onClick={loadData} disabled={loading}>
            <span className="flex items-center gap-2">
              <RotateCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
              Refresh
            </span>
          </Button>
          <Button variant="intelligence" onClick={handleRunOperationsCycle} disabled={runningCycle}>
            <span className="flex items-center gap-2">
              <Play className={`w-4 h-4 ${runningCycle ? 'animate-spin' : ''}`} />
              {runningCycle ? 'Running Cycle...' : 'Execute Operations Cycle'}
            </span>
          </Button>
        </div>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="p-5 bg-slate-900/40 border-slate-800">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-slate-400">Fleet Health</span>
            <ShieldCheck className="w-5 h-5 text-emerald-400" />
          </div>
          <div className="mt-2 flex items-baseline gap-2">
            <span className="text-3xl font-bold text-white">{overview?.fleet_health_score ?? 100}%</span>
            <Badge variant="success">Optimal</Badge>
          </div>
          <p className="mt-1 text-xs text-slate-500">
            {overview?.healthy_agents ?? 0} Healthy / {overview?.degraded_agents ?? 0} Degraded
          </p>
        </Card>

        <Card className="p-5 bg-slate-900/40 border-slate-800">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-slate-400">Avg p95 Latency</span>
            <Clock className="w-5 h-5 text-cyan-400" />
          </div>
          <div className="mt-2 flex items-baseline gap-2">
            <span className="text-3xl font-bold text-white">{overview?.mean_fleet_latency_ms ?? 0}</span>
            <span className="text-xs text-slate-400">ms</span>
          </div>
          <p className="mt-1 text-xs text-slate-500">SLA compliance: {overview?.sla_compliance_pct ?? 99.9}%</p>
        </Card>

        <Card className="p-5 bg-slate-900/40 border-slate-800">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-slate-400">Total Tokens</span>
            <Zap className="w-5 h-5 text-amber-400" />
          </div>
          <div className="mt-2 flex items-baseline gap-2">
            <span className="text-3xl font-bold text-white">
              {(overview?.total_tokens_consumed ?? 0).toLocaleString()}
            </span>
          </div>
          <p className="mt-1 text-xs text-slate-500">{overview?.total_invocations ?? 0} total invocations</p>
        </Card>

        <Card className="p-5 bg-slate-900/40 border-slate-800">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-slate-400">Total Cost</span>
            <DollarSign className="w-5 h-5 text-indigo-400" />
          </div>
          <div className="mt-2 flex items-baseline gap-2">
            <span className="text-3xl font-bold text-white">${overview?.total_cost_usd ?? 0.0}</span>
            <Badge variant="intelligence">Controlled</Badge>
          </div>
          <p className="mt-1 text-xs text-slate-500">Error rate: {((overview?.mean_fleet_error_rate ?? 0) * 100).toFixed(2)}%</p>
        </Card>
      </div>

      {/* Cycle Execution Notification */}
      {cycleResult && (
        <Card className="p-5 bg-indigo-950/30 border-indigo-500/30">
          <div className="flex items-start justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-indigo-500/20 rounded-lg">
                <TrendingUp className="w-5 h-5 text-indigo-400" />
              </div>
              <div>
                <h3 className="text-sm font-semibold text-white">Autonomous AI Operations Cycle Completed</h3>
                <p className="text-xs text-slate-400 mt-0.5">
                  Evaluated {cycleResult.agent_id} • Generated proposal: {cycleResult.improvement_proposal?.proposal_id} • Canary validated
                </p>
              </div>
            </div>
            <Badge variant="success">Executed</Badge>
          </div>
        </Card>
      )}

      {/* Fleet Agents Table */}
      <Card className="p-6 bg-slate-900/40 border-slate-800">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-lg font-semibold text-white">Active Agent Fleet</h2>
            <p className="text-xs text-slate-400">Real-time status, token throughput, and latency distribution</p>
          </div>
          <Badge variant="outline">{fleet.length} Agents Enrolled</Badge>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead>
              <tr className="border-b border-slate-800 text-slate-400 text-xs uppercase tracking-wider">
                <th className="pb-3 font-medium">Agent</th>
                <th className="pb-3 font-medium">Role</th>
                <th className="pb-3 font-medium">Status</th>
                <th className="pb-3 font-medium">Success Rate</th>
                <th className="pb-3 font-medium">p95 Latency</th>
                <th className="pb-3 font-medium">Tokens / Cost</th>
                <th className="pb-3 font-medium">Invocations</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {fleet.map((agent) => (
                <tr key={agent.agent_id} className="hover:bg-slate-800/30 transition-colors">
                  <td className="py-3.5">
                    <div className="flex items-center gap-2.5">
                      <div className="w-2 h-2 rounded-full bg-indigo-400" />
                      <span className="font-medium text-white">{agent.agent_name}</span>
                    </div>
                    <span className="text-xs text-slate-500 font-mono ml-4.5">{agent.version}</span>
                  </td>
                  <td className="py-3.5 text-slate-300 text-xs">{agent.role}</td>
                  <td className="py-3.5">
                    <Badge
                      variant={
                        agent.health_status === 'HEALTHY'
                          ? 'success'
                          : agent.health_status === 'DEGRADED'
                          ? 'warning'
                          : 'error'
                      }
                    >
                      {agent.health_status}
                    </Badge>
                  </td>
                  <td className="py-3.5">
                    <span className="font-semibold text-slate-200">{(agent.success_rate * 100).toFixed(1)}%</span>
                  </td>
                  <td className="py-3.5 text-slate-300">{agent.p95_latency_ms} ms</td>
                  <td className="py-3.5">
                    <div className="text-xs text-slate-200">{agent.total_tokens_consumed.toLocaleString()} tok</div>
                    <div className="text-[11px] text-slate-500">${agent.total_cost_usd}</div>
                  </td>
                  <td className="py-3.5 text-slate-300">{agent.total_invocations}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
};
