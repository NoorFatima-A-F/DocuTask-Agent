import React, { useState, useEffect } from 'react';
import { Card } from '../../components/ui/Card';
import { workforceApiClient } from '../../services/workforceApiClient';
import { WorkforcePerformanceMetric } from '../../types/workforce';
import { Activity, Flame, HeartHandshake } from 'lucide-react';

export const PerformanceAnalytics: React.FC = () => {
  const [metric, setMetric] = useState<WorkforcePerformanceMetric | null>(null);

  useEffect(() => {
    workforceApiClient.getPerformance().then(setMetric);
  }, []);

  return (
    <div className="space-y-6">
      <div className="bg-slate-900/60 p-5 rounded-2xl border border-slate-800">
        <h1 className="text-2xl font-bold text-white flex items-center gap-3">
          <span className="p-2 bg-rose-500/20 text-rose-400 rounded-xl">📊</span>
          Workforce Performance Analytics
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          Fleet Productivity, Burnout Risk, Collaboration Metrics, and Innovation Speed
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="p-5 bg-slate-900/50 border-slate-800">
          <div className="flex justify-between items-center text-xs text-slate-400">
            <span>Fleet Utilization</span>
            <Activity className="w-4 h-4 text-indigo-400" />
          </div>
          <div className="text-3xl font-bold text-white mt-2">
            {Math.round((metric?.workforce_utilization_rate ?? 0.83) * 100)}%
          </div>
          <p className="text-xs text-slate-500 mt-1">Active / Total Capacity</p>
        </Card>

        <Card className="p-5 bg-slate-900/50 border-slate-800">
          <div className="flex justify-between items-center text-xs text-slate-400">
            <span>Collaboration Index</span>
            <HeartHandshake className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-3xl font-bold text-emerald-400 mt-2">
            {metric?.collaboration_index ?? 0.94}
          </div>
          <p className="text-xs text-slate-500 mt-1">Cross-Agent Consensus Velocity</p>
        </Card>

        <Card className="p-5 bg-slate-900/50 border-slate-800">
          <div className="flex justify-between items-center text-xs text-slate-400">
            <span>Burnout Risk Index</span>
            <Flame className="w-4 h-4 text-amber-400" />
          </div>
          <div className="text-3xl font-bold text-amber-400 mt-2">
            {Math.round((metric?.workforce_burnout_risk ?? 0.04) * 100)}%
          </div>
          <p className="text-xs text-slate-500 mt-1">Safe Load Margins</p>
        </Card>
      </div>
    </div>
  );
};
