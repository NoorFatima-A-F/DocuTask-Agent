import React, { useState, useEffect } from 'react';
import {
  ListFilter,
  Layers,
  RefreshCw,
  ShieldAlert,
} from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { DistributedApiClient } from '../../services/distributedApiClient';
import { QueueChannelMetrics } from '../../types/distributedPlatform';

export const DistributedQueueMonitor: React.FC = () => {
  const [metrics, setMetrics] = useState<QueueChannelMetrics[]>([]);
  const [loading, setLoading] = useState(true);

  const loadMetrics = async () => {
    try {
      setLoading(true);
      const res = await DistributedApiClient.getQueueMetrics();
      setMetrics(res);
    } catch (err) {
      console.error('Failed to load queue metrics:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadMetrics();
    const interval = setInterval(loadMetrics, 8000);
    return () => clearInterval(interval);
  }, []);

  const totalQueued = metrics.reduce((acc, curr) => acc + curr.total_depth, 0);
  const totalDLQ = metrics.reduce((acc, curr) => acc + curr.dlq_depth, 0);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/60 p-6 rounded-2xl border border-slate-800 backdrop-blur-md">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-indigo-500/10 rounded-xl border border-indigo-500/20 text-indigo-400">
            <Layers className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white">Distributed Queue Monitor</h1>
            <p className="text-sm text-slate-400">
              Multi-Priority Deficit Round-Robin Queues & Dead-Letter Isolation
            </p>
          </div>
        </div>

        <Button variant="outline" onClick={loadMetrics} disabled={loading}>
          <span className="flex items-center gap-2">
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            Refresh Queues
          </span>
        </Button>
      </div>

      {/* Top Stat Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <Card className="p-5 bg-slate-900/50 border-slate-800">
          <span className="text-xs text-slate-400 block mb-1">Total Active Backlog</span>
          <div className="flex items-baseline gap-2">
            <span className="text-2xl font-bold text-white">{totalQueued}</span>
            <span className="text-xs text-indigo-400">enqueued messages</span>
          </div>
        </Card>

        <Card className="p-5 bg-slate-900/50 border-slate-800">
          <span className="text-xs text-slate-400 block mb-1">Dead-Letter Queue (DLQ)</span>
          <div className="flex items-baseline gap-2">
            <span className="text-2xl font-bold text-emerald-400">{totalDLQ}</span>
            <Badge variant={totalDLQ === 0 ? 'success' : 'error'}>
              {totalDLQ === 0 ? 'Zero Failed' : 'Action Required'}
            </Badge>
          </div>
        </Card>

        <Card className="p-5 bg-slate-900/50 border-slate-800">
          <span className="text-xs text-slate-400 block mb-1">Active Queue Channels</span>
          <div className="flex items-baseline gap-2">
            <span className="text-2xl font-bold text-white">{metrics.length}</span>
            <span className="text-xs text-slate-500">Channels Registered</span>
          </div>
        </Card>
      </div>

      {/* Queue Channels Detail Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {metrics.map((ch) => (
          <Card key={ch.channel_name} className="p-6 bg-slate-900/40 border-slate-800 space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <div className="flex items-center gap-2">
                <ListFilter className="w-4 h-4 text-indigo-400" />
                <h3 className="font-bold text-white text-base font-mono">{ch.channel_name}</h3>
              </div>
              <Badge variant="intelligence">{ch.total_depth} Pending</Badge>
            </div>

            {/* Priority breakdown */}
            <div className="space-y-3 text-xs">
              <div>
                <div className="flex justify-between mb-1">
                  <span className="text-red-400 font-semibold flex items-center gap-1">
                    <span className="w-2 h-2 rounded-full bg-red-400" /> CRITICAL (P0)
                  </span>
                  <span className="font-mono text-white">{ch.critical_depth}</span>
                </div>
                <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                  <div
                    className="bg-red-500 h-full rounded-full"
                    style={{ width: `${ch.total_depth ? (ch.critical_depth / ch.total_depth) * 100 : 0}%` }}
                  />
                </div>
              </div>

              <div>
                <div className="flex justify-between mb-1">
                  <span className="text-amber-400 font-semibold flex items-center gap-1">
                    <span className="w-2 h-2 rounded-full bg-amber-400" /> HIGH (P1)
                  </span>
                  <span className="font-mono text-white">{ch.high_depth}</span>
                </div>
                <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                  <div
                    className="bg-amber-500 h-full rounded-full"
                    style={{ width: `${ch.total_depth ? (ch.high_depth / ch.total_depth) * 100 : 0}%` }}
                  />
                </div>
              </div>

              <div>
                <div className="flex justify-between mb-1">
                  <span className="text-indigo-400 font-semibold flex items-center gap-1">
                    <span className="w-2 h-2 rounded-full bg-indigo-400" /> NORMAL (P2)
                  </span>
                  <span className="font-mono text-white">{ch.normal_depth}</span>
                </div>
                <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                  <div
                    className="bg-indigo-500 h-full rounded-full"
                    style={{ width: `${ch.total_depth ? (ch.normal_depth / ch.total_depth) * 100 : 0}%` }}
                  />
                </div>
              </div>

              <div>
                <div className="flex justify-between mb-1">
                  <span className="text-slate-400 font-semibold flex items-center gap-1">
                    <span className="w-2 h-2 rounded-full bg-slate-400" /> BATCH (P3)
                  </span>
                  <span className="font-mono text-white">{ch.batch_depth}</span>
                </div>
                <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                  <div
                    className="bg-slate-600 h-full rounded-full"
                    style={{ width: `${ch.total_depth ? (ch.batch_depth / ch.total_depth) * 100 : 0}%` }}
                  />
                </div>
              </div>
            </div>

            <div className="pt-3 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">
              <span className="flex items-center gap-1">
                <ShieldAlert className="w-3.5 h-3.5 text-slate-500" />
                Dead Letter: <strong className="text-white ml-1">{ch.dlq_depth}</strong>
              </span>
              <span className="text-emerald-400 font-mono text-[11px]">Fair-Share Allocator: Active</span>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
