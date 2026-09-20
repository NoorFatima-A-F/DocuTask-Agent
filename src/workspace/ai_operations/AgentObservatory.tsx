import React, { useState, useEffect } from 'react';
import {
  Activity,
  Cpu,
  Layers,
  HardDrive,
  RefreshCw,
  Clock,
  Zap,
} from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { AIOperationsApiClient } from '../../services/aiOperationsApiClient';
import { AgentTelemetry } from '../../types/aiOperations';

export const AgentObservatory: React.FC = () => {
  const [agents, setAgents] = useState<AgentTelemetry[]>([]);
  const [selectedAgent, setSelectedAgent] = useState<AgentTelemetry | null>(null);
  const [loading, setLoading] = useState(true);

  const loadAgents = async () => {
    try {
      setLoading(true);
      const data = await AIOperationsApiClient.getFleetTelemetry();
      setAgents(data);
      if (data.length > 0 && !selectedAgent) {
        setSelectedAgent(data[0] || null);
      }
    } catch (err) {
      console.error('Failed to load fleet observatory data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAgents();
  }, []);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between bg-slate-900/60 p-5 rounded-2xl border border-slate-800 backdrop-blur-md">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-cyan-500/10 rounded-xl border border-cyan-500/20">
            <Activity className="w-6 h-6 text-cyan-400" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-white">Agent Fleet Observatory</h1>
            <p className="text-xs text-slate-400">Deep telemetry, latency percentiles, and hardware resource utilization</p>
          </div>
        </div>
        <Button variant="outline" onClick={loadAgents} disabled={loading}>
          <span className="flex items-center gap-2">
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            Refresh
          </span>
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Agent Selector List */}
        <div className="space-y-3 lg:col-span-1">
          <h2 className="text-xs font-semibold text-slate-400 uppercase tracking-wider px-1">Agent Fleet</h2>
          {agents.map((agent) => (
            <Card
              key={agent.agent_id}
              className={`p-4 cursor-pointer transition-all border ${
                selectedAgent?.agent_id === agent.agent_id
                  ? 'bg-cyan-950/30 border-cyan-500/50 shadow-lg shadow-cyan-950/20'
                  : 'bg-slate-900/40 border-slate-800/80 hover:bg-slate-800/40'
              }`}
              onClick={() => setSelectedAgent(agent)}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2.5">
                  <div
                    className={`w-2.5 h-2.5 rounded-full ${
                      agent.health_status === 'HEALTHY'
                        ? 'bg-emerald-400'
                        : agent.health_status === 'DEGRADED'
                        ? 'bg-amber-400'
                        : 'bg-rose-400'
                    }`}
                  />
                  <h3 className="font-semibold text-white text-sm">{agent.agent_name}</h3>
                </div>
                <Badge variant={agent.health_status === 'HEALTHY' ? 'success' : 'warning'}>
                  {agent.health_status}
                </Badge>
              </div>
              <p className="text-xs text-slate-400 mt-1 line-clamp-1">{agent.role}</p>
              <div className="flex items-center justify-between mt-3 text-xs text-slate-400 border-t border-slate-800/60 pt-2">
                <span>{(agent.success_rate * 100).toFixed(1)}% Success</span>
                <span>{agent.p95_latency_ms} ms p95</span>
              </div>
            </Card>
          ))}
        </div>

        {/* Selected Agent Details */}
        <div className="lg:col-span-2 space-y-4">
          {selectedAgent ? (
            <>
              <Card className="p-6 bg-slate-900/50 border-slate-800">
                <div className="flex items-start justify-between border-b border-slate-800 pb-4">
                  <div>
                    <h2 className="text-lg font-bold text-white">{selectedAgent.agent_name}</h2>
                    <p className="text-xs text-slate-400 font-mono mt-0.5">{selectedAgent.agent_id} • {selectedAgent.version}</p>
                  </div>
                  <Badge variant={selectedAgent.health_status === 'HEALTHY' ? 'success' : 'warning'}>
                    {selectedAgent.health_status}
                  </Badge>
                </div>

                <div className="grid grid-cols-2 sm:grid-cols-3 gap-4 my-5">
                  <div className="bg-slate-950/40 p-3 rounded-xl border border-slate-800/60">
                    <span className="text-xs text-slate-400 flex items-center gap-1.5"><Clock className="w-3.5 h-3.5 text-cyan-400" /> Avg Latency</span>
                    <p className="text-xl font-bold text-white mt-1">{selectedAgent.avg_latency_ms} ms</p>
                  </div>
                  <div className="bg-slate-950/40 p-3 rounded-xl border border-slate-800/60">
                    <span className="text-xs text-slate-400 flex items-center gap-1.5"><Clock className="w-3.5 h-3.5 text-amber-400" /> p95 / p99 Latency</span>
                    <p className="text-xl font-bold text-white mt-1">{selectedAgent.p95_latency_ms} / {selectedAgent.p99_latency_ms} ms</p>
                  </div>
                  <div className="bg-slate-950/40 p-3 rounded-xl border border-slate-800/60">
                    <span className="text-xs text-slate-400 flex items-center gap-1.5"><Zap className="w-3.5 h-3.5 text-indigo-400" /> Token Burn</span>
                    <p className="text-xl font-bold text-white mt-1">{selectedAgent.total_tokens_consumed.toLocaleString()}</p>
                  </div>
                </div>

                {/* Resource Utilization */}
                <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Resource Utilization</h4>
                <div className="grid grid-cols-2 gap-4">
                  <div className="p-4 bg-slate-950/40 rounded-xl border border-slate-800/60">
                    <div className="flex items-center justify-between text-xs text-slate-400 mb-1.5">
                      <span className="flex items-center gap-1.5"><Cpu className="w-3.5 h-3.5 text-emerald-400" /> CPU Allocation</span>
                      <span className="font-semibold text-white">{selectedAgent.resource_utilization?.cpu_pct ?? 15}%</span>
                    </div>
                    <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                      <div className="bg-emerald-400 h-full rounded-full" style={{ width: `${selectedAgent.resource_utilization?.cpu_pct ?? 15}%` }} />
                    </div>
                  </div>
                  <div className="p-4 bg-slate-950/40 rounded-xl border border-slate-800/60">
                    <div className="flex items-center justify-between text-xs text-slate-400 mb-1.5">
                      <span className="flex items-center gap-1.5"><HardDrive className="w-3.5 h-3.5 text-indigo-400" /> Memory Footprint</span>
                      <span className="font-semibold text-white">{selectedAgent.resource_utilization?.memory_mb ?? 256} MB</span>
                    </div>
                    <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                      <div className="bg-indigo-400 h-full rounded-full" style={{ width: `${Math.min(100, ((selectedAgent.resource_utilization?.memory_mb ?? 256) / 1024) * 100)}%` }} />
                    </div>
                  </div>
                </div>
              </Card>
            </>
          ) : (
            <Card className="p-8 text-center text-slate-400 bg-slate-900/40 border-slate-800">
              <Layers className="w-8 h-8 text-slate-600 mx-auto mb-2" />
              <p>Select an agent to view real-time telemetry and resource telemetry.</p>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
};
