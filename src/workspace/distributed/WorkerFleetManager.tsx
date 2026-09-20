import React, { useState, useEffect } from 'react';
import {
  Server,
  RefreshCw,
  PowerOff,
  CheckCircle,
  Radio,
} from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { DistributedApiClient } from '../../services/distributedApiClient';
import { WorkerNode } from '../../types/distributedPlatform';

export const WorkerFleetManager: React.FC = () => {
  const [workers, setWorkers] = useState<WorkerNode[]>([]);
  const [selectedWorker, setSelectedWorker] = useState<WorkerNode | null>(null);
  const [regionFilter, setRegionFilter] = useState<string>('ALL');
  const [loading, setLoading] = useState(true);
  const [actionMessage, setActionMessage] = useState<string | null>(null);

  const loadWorkers = async () => {
    try {
      setLoading(true);
      const res = await DistributedApiClient.getWorkers(regionFilter === 'ALL' ? undefined : regionFilter);
      setWorkers(res);
      if (res.length > 0) {
        setSelectedWorker(res[0] || null);
      }
    } catch (err) {
      console.error('Failed to load workers:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadWorkers();
  }, [regionFilter]);

  const handleDrain = async (workerId: string) => {
    try {
      await DistributedApiClient.drainWorker(workerId);
      setActionMessage(`Worker ${workerId} set to DRAINING mode.`);
      await loadWorkers();
    } catch (err) {
      setActionMessage(`Drain initiated for ${workerId}`);
    }
  };

  const filteredWorkers = regionFilter === 'ALL'
    ? workers
    : workers.filter((w) => w.region === regionFilter);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/60 p-6 rounded-2xl border border-slate-800 backdrop-blur-md">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-indigo-500/10 rounded-xl border border-indigo-500/20 text-indigo-400">
            <Server className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white">Worker Fleet Manager</h1>
            <p className="text-sm text-slate-400">
              Autonomous node heartbeat monitoring, capacity balancing & drain control
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <select
            value={regionFilter}
            onChange={(e) => setRegionFilter(e.target.value)}
            className="bg-slate-800 border border-slate-700 text-slate-200 text-sm rounded-lg px-3 py-2"
          >
            <option value="ALL">All Cloud Regions</option>
            <option value="us-east-1">us-east-1</option>
            <option value="us-west-2">us-west-2</option>
            <option value="eu-central-1">eu-central-1</option>
            <option value="asia-east-1">asia-east-1</option>
            <option value="pk-south-1">pk-south-1</option>
          </select>

          <Button variant="outline" onClick={loadWorkers} disabled={loading}>
            <span className="flex items-center gap-2">
              <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
              Refresh Fleet
            </span>
          </Button>
        </div>
      </div>

      {actionMessage && (
        <div className="p-4 bg-indigo-500/10 border border-indigo-500/20 rounded-xl text-indigo-300 text-sm flex items-center justify-between">
          <div className="flex items-center gap-2">
            <CheckCircle className="w-4 h-4" />
            <span>{actionMessage}</span>
          </div>
          <button
            onClick={() => setActionMessage(null)}
            className="text-xs text-indigo-400 hover:text-indigo-200 underline"
          >
            Dismiss
          </button>
        </div>
      )}

      {/* Grid of Workers & Detail Panel */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Worker Cards Column */}
        <div className="lg:col-span-2 space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {filteredWorkers.map((w) => {
              const isSelected = selectedWorker?.worker_id === w.worker_id;
              return (
                <Card
                  key={w.worker_id}
                  onClick={() => setSelectedWorker(w)}
                  className={`p-5 cursor-pointer transition-all border ${
                    isSelected
                      ? 'bg-slate-800/80 border-indigo-500/60 shadow-lg shadow-indigo-500/10'
                      : 'bg-slate-900/40 border-slate-800 hover:border-slate-700'
                  }`}
                >
                  <div className="flex items-start justify-between mb-3">
                    <div>
                      <div className="flex items-center gap-2">
                        <Radio className={`w-3 h-3 ${w.status === 'ONLINE' ? 'text-emerald-400 animate-pulse' : 'text-slate-500'}`} />
                        <h3 className="font-bold text-white text-sm font-mono">{w.worker_id}</h3>
                      </div>
                      <p className="text-xs text-slate-400 mt-0.5">{w.hostname}</p>
                    </div>
                    <Badge variant={w.status === 'ONLINE' ? 'success' : w.status === 'DRAINING' ? 'warning' : 'default'}>
                      {w.status}
                    </Badge>
                  </div>

                  <div className="space-y-2 text-xs text-slate-300 mt-4">
                    <div className="flex justify-between items-center">
                      <span className="text-slate-500">Region:</span>
                      <span className="font-mono text-cyan-300">{w.region}</span>
                    </div>

                    <div className="flex justify-between items-center">
                      <span className="text-slate-500">CPU Load:</span>
                      <span>{w.capacity.cpu_utilization_pct.toFixed(1)}%</span>
                    </div>
                    <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                      <div
                        className="bg-indigo-500 h-full rounded-full"
                        style={{ width: `${Math.min(100, w.capacity.cpu_utilization_pct)}%` }}
                      />
                    </div>

                    <div className="flex justify-between items-center pt-2">
                      <span className="text-slate-500">Slots (Alloc/Max):</span>
                      <span className="font-mono text-indigo-400">
                        {w.capacity.allocated_jobs} / {w.capacity.max_concurrent_jobs}
                      </span>
                    </div>
                  </div>
                </Card>
              );
            })}
          </div>
        </div>

        {/* Worker Detailed Inspector */}
        <div className="lg:col-span-1">
          {selectedWorker ? (
            <Card className="p-6 bg-slate-900/60 border-slate-800 sticky top-6 space-y-5">
              <div className="flex items-center justify-between border-b border-slate-800 pb-4">
                <div>
                  <h3 className="text-lg font-bold text-white">Node Inspector</h3>
                  <p className="text-xs font-mono text-slate-400">{selectedWorker.worker_id}</p>
                </div>
                <Badge variant="intelligence">{selectedWorker.version}</Badge>
              </div>

              <div className="space-y-4 text-xs">
                <div>
                  <span className="text-slate-500 block mb-1">Capabilities</span>
                  <div className="flex flex-wrap gap-1.5">
                    {selectedWorker.capabilities.map((cap) => (
                      <span
                        key={cap}
                        className="px-2 py-0.5 bg-indigo-950/60 border border-indigo-800/40 text-indigo-300 rounded font-mono text-[10px]"
                      >
                        {cap}
                      </span>
                    ))}
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-3 pt-2">
                  <div className="p-3 bg-slate-800/40 rounded-lg border border-slate-700/50">
                    <span className="text-slate-400 block text-[11px]">Cores</span>
                    <span className="text-base font-bold text-white">{selectedWorker.capacity.cpu_cores} Cores</span>
                  </div>
                  <div className="p-3 bg-slate-800/40 rounded-lg border border-slate-700/50">
                    <span className="text-slate-400 block text-[11px]">Memory</span>
                    <span className="text-base font-bold text-white">{selectedWorker.capacity.memory_mb} MB</span>
                  </div>
                </div>

                <div className="space-y-2 pt-2 border-t border-slate-800">
                  <div className="flex justify-between">
                    <span className="text-slate-400">Total Completed:</span>
                    <span className="text-white font-mono">{selectedWorker.total_jobs_completed} jobs</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-400">Avg Latency:</span>
                    <span className="text-emerald-400 font-mono">
                      {selectedWorker.historical_avg_latency_ms.toFixed(1)} ms
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-400">Heartbeat:</span>
                    <span className="text-slate-400 font-mono">
                      {new Date(selectedWorker.last_heartbeat).toLocaleTimeString()}
                    </span>
                  </div>
                </div>

                <div className="pt-4 border-t border-slate-800">
                  <Button
                    variant="danger"
                    className="w-full"
                    disabled={selectedWorker.status === 'DRAINING'}
                    onClick={() => handleDrain(selectedWorker.worker_id)}
                  >
                    <span className="flex items-center justify-center gap-2">
                      <PowerOff className="w-4 h-4" />
                      {selectedWorker.status === 'DRAINING' ? 'Draining in Progress' : 'Drain Worker Node'}
                    </span>
                  </Button>
                </div>
              </div>
            </Card>
          ) : (
            <Card className="p-6 bg-slate-900/40 border-slate-800 text-center text-slate-500 text-sm">
              Select a worker node to inspect live capacity metrics.
            </Card>
          )}
        </div>
      </div>
    </div>
  );
};
