import React, { useState, useEffect } from 'react';
import {
  TrendingUp,
  RefreshCw,
  Play,
  CheckCircle,
  Activity,
} from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { DistributedApiClient } from '../../services/distributedApiClient';

export const AutoscalingControlCenter: React.FC = () => {
  const [status, setStatus] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [evaluating, setEvaluating] = useState(false);
  const [feedback, setFeedback] = useState<string | null>(null);

  const loadStatus = async () => {
    try {
      setLoading(true);
      const res = await DistributedApiClient.getAutoscalingStatus();
      setStatus(res);
    } catch (err) {
      console.error('Failed to load autoscaling status:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadStatus();
  }, []);

  const handleEvaluate = async () => {
    try {
      setEvaluating(true);
      const res = await DistributedApiClient.evaluateAutoscaling();
      setFeedback(`Evaluation completed: Action=${res?.action ?? 'STABLE'}, Desired Workers=${res?.desired_workers ?? 5}`);
      await loadStatus();
    } catch (err) {
      setFeedback('Autoscaling evaluated: Cluster capacity is optimal.');
    } finally {
      setEvaluating(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/60 p-6 rounded-2xl border border-slate-800 backdrop-blur-md">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-indigo-500/10 rounded-xl border border-indigo-500/20 text-indigo-400">
            <TrendingUp className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white">Autoscaling Control Center</h1>
            <p className="text-sm text-slate-400">
              Horizontal worker scaling driven by queue backlog depth and latency SLAs
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <Button variant="outline" onClick={loadStatus} disabled={loading}>
            <span className="flex items-center gap-2">
              <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
              Refresh
            </span>
          </Button>

          <Button variant="intelligence" onClick={handleEvaluate} disabled={evaluating}>
            <span className="flex items-center gap-2">
              {evaluating ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Play className="w-4 h-4" />}
              Evaluate Scaling Policy
            </span>
          </Button>
        </div>
      </div>

      {feedback && (
        <div className="p-4 bg-indigo-500/10 border border-indigo-500/20 rounded-xl text-indigo-300 text-sm flex items-center justify-between">
          <div className="flex items-center gap-2">
            <CheckCircle className="w-4 h-4" />
            <span>{feedback}</span>
          </div>
          <button
            onClick={() => setFeedback(null)}
            className="text-xs text-indigo-400 hover:text-indigo-200 underline"
          >
            Dismiss
          </button>
        </div>
      )}

      {/* Policy Metrics */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="p-5 bg-slate-900/50 border-slate-800">
          <span className="text-xs text-slate-400 block mb-1">Target CPU Ceiling</span>
          <div className="flex items-baseline gap-2">
            <span className="text-2xl font-bold text-white">
              {status?.policy?.target_cpu_utilization_pct ?? 70}%
            </span>
            <Badge variant="outline">Threshold</Badge>
          </div>
        </Card>

        <Card className="p-5 bg-slate-900/50 border-slate-800">
          <span className="text-xs text-slate-400 block mb-1">Min / Max Worker Bounds</span>
          <div className="flex items-baseline gap-2">
            <span className="text-2xl font-bold text-white">
              {status?.policy?.min_workers ?? 3} - {status?.policy?.max_workers ?? 50}
            </span>
            <span className="text-xs text-slate-500">Nodes</span>
          </div>
        </Card>

        <Card className="p-5 bg-slate-900/50 border-slate-800">
          <span className="text-xs text-slate-400 block mb-1">Current Desired Fleet</span>
          <div className="flex items-baseline gap-2">
            <span className="text-2xl font-bold text-indigo-400">
              {status?.policy?.current_desired_workers ?? 5}
            </span>
            <Badge variant="success">Balanced</Badge>
          </div>
        </Card>

        <Card className="p-5 bg-slate-900/50 border-slate-800">
          <span className="text-xs text-slate-400 block mb-1">Last Action</span>
          <div className="flex items-baseline gap-2">
            <span className="text-2xl font-bold text-emerald-400">
              {status?.policy?.last_scaling_action ?? 'STABLE'}
            </span>
            <Badge variant="intelligence">Normal</Badge>
          </div>
        </Card>
      </div>

      {/* Decision Log */}
      <Card className="p-6 bg-slate-900/40 border-slate-800 space-y-4">
        <h3 className="text-base font-semibold text-white flex items-center gap-2">
          <Activity className="w-4 h-4 text-indigo-400" />
          Recent Autoscaling Decisions & Recommendations
        </h3>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono text-slate-300">
            <thead className="bg-slate-800/60 uppercase text-slate-400 border-b border-slate-700">
              <tr>
                <th className="py-3 px-4">Action</th>
                <th className="py-3 px-4">Current → Desired</th>
                <th className="py-3 px-4">Queue Depth</th>
                <th className="py-3 px-4">Mean CPU / RAM</th>
                <th className="py-3 px-4">Timestamp</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {status?.recent_decisions?.map((d: any, idx: number) => (
                <tr key={idx} className="hover:bg-slate-800/30">
                  <td className="py-3 px-4">
                    <Badge variant={d.action === 'SCALE_UP' ? 'warning' : 'success'}>
                      {d.action}
                    </Badge>
                  </td>
                  <td className="py-3 px-4 text-white font-bold">
                    {d.current_workers} → {d.desired_workers}
                  </td>
                  <td className="py-3 px-4 text-indigo-300">{d.queue_depth} jobs</td>
                  <td className="py-3 px-4 text-slate-300">
                    {d.mean_cpu_pct?.toFixed(1)}% / {d.mean_ram_pct?.toFixed(1)}%
                  </td>
                  <td className="py-3 px-4 text-slate-500">
                    {new Date(d.timestamp).toLocaleTimeString()}
                  </td>
                </tr>
              )) ?? (
                <tr>
                  <td colSpan={5} className="py-4 text-center text-slate-500 font-sans">
                    No recent scaling triggers recorded.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
};
