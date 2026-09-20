import React, { useState, useEffect } from 'react';
import {
  BarChart3,
  RefreshCw,
} from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { BusinessApiClient } from '../../services/businessApiClient';
import { KPIDefinition } from '../../types/businessPlatform';

export const KPIDashboard: React.FC = () => {
  const [kpis, setKpis] = useState<KPIDefinition[]>([]);
  const [loading, setLoading] = useState(true);

  const loadKpis = async () => {
    try {
      setLoading(true);
      const res = await BusinessApiClient.getKPIs();
      setKpis(res);
    } catch (err) {
      console.error('Failed to load KPIs:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadKpis();
  }, []);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/60 p-6 rounded-2xl border border-slate-800 backdrop-blur-md">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-indigo-500/10 rounded-xl border border-indigo-500/20 text-indigo-400">
            <BarChart3 className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white">Enterprise KPI Scorecard</h1>
            <p className="text-sm text-slate-400">
              Value accounting, turnaround velocity, unit processing economics & automation ROI
            </p>
          </div>
        </div>

        <Button variant="outline" onClick={loadKpis} disabled={loading}>
          <span className="flex items-center gap-2">
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            Refresh
          </span>
        </Button>
      </div>

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {kpis.map((k) => (
          <Card key={k.kpi_id} className="p-5 bg-slate-900/40 border-slate-800 space-y-3">
            <div className="flex justify-between items-start">
              <span className="text-xs text-slate-400 block font-medium">{k.name}</span>
              <Badge variant="success">{k.trend}</Badge>
            </div>

            <div className="flex items-baseline gap-2">
              <span className="text-2xl font-bold text-white font-mono">
                {k.unit === 'USD' ? `$${k.current_value.toLocaleString()}` : `${k.current_value} ${k.unit}`}
              </span>
            </div>

            <div className="pt-2 border-t border-slate-800/80 text-xs text-slate-400 flex justify-between">
              <span>Legacy Benchmark:</span>
              <span className="font-mono text-slate-300">
                {k.unit === 'USD' ? `$${k.benchmark_value}` : `${k.benchmark_value} ${k.unit}`}
              </span>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
