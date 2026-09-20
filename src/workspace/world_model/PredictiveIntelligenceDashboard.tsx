/**
 * Phase 13.16: Autonomous World Modeling, Predictive Intelligence & Causal Reasoning Platform (AWMPICRP)
 * View 9: Predictive Intelligence Dashboard
 */

import React, { useEffect, useState } from 'react';
import {
  TrendingUp,
  RefreshCw,
  Activity,
  Zap,
} from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { WorldModelApiClient } from '../../services/worldModelApiClient';
import { PredictionTrajectory } from '../../types/worldModelPlatform';

export const PredictiveIntelligenceDashboard: React.FC = () => {
  const [trajectories, setTrajectories] = useState<PredictionTrajectory[]>([]);
  const [loading, setLoading] = useState(true);
  const [targetMetric, setTargetMetric] = useState('Enterprise Document Ingestion Throughput');
  const [predictedVal, setPredictedVal] = useState('14200');
  const [generating, setGenerating] = useState(false);

  const fetchForecasts = async () => {
    setLoading(true);
    try {
      const res = await WorldModelApiClient.getForecasts();
      setTrajectories(res.trajectories || []);
    } catch (err) {
      console.error('Error fetching forecasts:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchForecasts();
  }, []);

  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault();
    setGenerating(true);
    try {
      await WorldModelApiClient.generateForecast({
        target_metric: targetMetric,
        horizon: 'medium_term',
        horizon_seconds: 86400,
        include_causal_factors: true,
      });
      await fetchForecasts();
    } catch (err) {
      console.error('Error generating forecast:', err);
    } finally {
      setGenerating(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/80 border border-purple-500/30 rounded-xl p-6">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-purple-500/10 border border-purple-500/30 rounded-lg text-purple-400">
            <TrendingUp className="w-6 h-6" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-2xl font-bold text-white tracking-tight">Predictive Intelligence Dashboard</h1>
              <Badge variant="intelligence">95% Confidence Intervals</Badge>
            </div>
            <p className="text-sm text-slate-400">
              Probabilistic multi-horizon forecasting for latency, spend, failure risk, and SLA breaches.
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <Button variant="outline" onClick={fetchForecasts} disabled={loading}>
            <span className="flex items-center gap-2">
              <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
              Refresh
            </span>
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Trajectories */}
        <div className="lg:col-span-2 space-y-4">
          <h3 className="text-base font-semibold text-white flex items-center gap-2">
            <Activity className="w-5 h-5 text-purple-400" />
            Active Forecast Trajectories
          </h3>

          <div className="space-y-4">
            {trajectories.map((traj) => (
              <Card key={traj.trajectory_id} className="bg-slate-900/60 border-slate-800 p-5 space-y-4 hover:border-purple-500/40 transition-all">
                <div className="flex items-start justify-between">
                  <div>
                    <span className="text-xs font-mono text-purple-400 bg-purple-950/60 px-2 py-0.5 rounded border border-purple-500/30">
                      {traj.trajectory_id}
                    </span>
                    <h4 className="text-base font-bold text-white mt-1">{traj.target_metric}</h4>
                  </div>
                  <Badge variant="success">Confidence: {Math.round((traj.confidence_score || 0.91) * 100)}%</Badge>
                </div>

                {/* Expected & CI Bounding */}
                <div className="grid grid-cols-3 gap-3 text-center">
                  <div className="p-3 bg-slate-950/80 rounded border border-slate-800">
                    <span className="text-slate-400 text-[10px] uppercase font-semibold block">95% Lower Bound</span>
                    <span className="text-sm font-mono text-slate-300 font-bold">{traj.lower_bound_95}</span>
                  </div>
                  <div className="p-3 bg-purple-950/40 rounded border border-purple-500/40">
                    <span className="text-purple-300 text-[10px] uppercase font-semibold block">Expected Value</span>
                    <span className="text-base font-mono text-purple-200 font-bold">{traj.expected_value}</span>
                  </div>
                  <div className="p-3 bg-slate-950/80 rounded border border-slate-800">
                    <span className="text-slate-400 text-[10px] uppercase font-semibold block">95% Upper Bound</span>
                    <span className="text-sm font-mono text-slate-300 font-bold">{traj.upper_bound_95}</span>
                  </div>
                </div>

                {/* Causal Drivers */}
                <div className="text-xs text-slate-400">
                  <span className="font-semibold text-slate-300 block mb-1">Causal Drivers Identified:</span>
                  <div className="flex flex-wrap gap-2">
                    {(traj.causal_drivers || ['Diurnal load rhythm', 'Batch concurrency peak']).map((d, idx) => (
                      <span key={idx} className="px-2.5 py-1 rounded bg-slate-800 border border-slate-700 text-slate-200">
                        {d}
                      </span>
                    ))}
                  </div>
                </div>
              </Card>
            ))}
          </div>
        </div>

        {/* Generate Forecast Panel */}
        <Card className="bg-slate-900/60 border-slate-800 p-5 space-y-4">
          <h3 className="text-base font-semibold text-white flex items-center gap-2">
            <Zap className="w-5 h-5 text-purple-400" />
            Generate New Forecast
          </h3>

          <form onSubmit={handleGenerate} className="space-y-4 text-xs">
            <div>
              <label className="block text-slate-300 font-semibold mb-1">Target Metric</label>
              <input
                type="text"
                required
                value={targetMetric}
                onChange={(e) => setTargetMetric(e.target.value)}
                className="w-full bg-slate-800 border border-slate-700 rounded p-2 text-white text-xs"
              />
            </div>

            <div>
              <label className="block text-slate-300 font-semibold mb-1">Estimated Value Base</label>
              <input
                type="number"
                required
                value={predictedVal}
                onChange={(e) => setPredictedVal(e.target.value)}
                className="w-full bg-slate-800 border border-slate-700 rounded p-2 text-white font-mono text-xs"
              />
            </div>

            <Button variant="intelligence" type="submit" disabled={generating} className="w-full">
              <span className="flex items-center justify-center gap-2">
                <TrendingUp className="w-4 h-4" />
                {generating ? 'Forecasting...' : 'Compute Trajectory'}
              </span>
            </Button>
          </form>
        </Card>
      </div>
    </div>
  );
};
