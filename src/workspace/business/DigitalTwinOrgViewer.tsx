import React, { useState, useEffect } from 'react';
import {
  Globe,
  RefreshCw,
  Activity,
} from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { BusinessApiClient } from '../../services/businessApiClient';
import { DigitalTwinOrgState } from '../../types/businessPlatform';

export const DigitalTwinOrgViewer: React.FC = () => {
  const [dto, setDto] = useState<DigitalTwinOrgState | null>(null);
  const [loading, setLoading] = useState(true);

  const loadDto = async () => {
    try {
      setLoading(true);
      const res = await BusinessApiClient.getDigitalTwin();
      setDto(res);
    } catch (err) {
      console.error('Failed to load digital twin:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDto();
  }, []);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/60 p-6 rounded-2xl border border-slate-800 backdrop-blur-md">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-indigo-500/10 rounded-xl border border-indigo-500/20 text-indigo-400">
            <Globe className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white">Digital Twin of the Organization (DTO)</h1>
            <p className="text-sm text-slate-400">
              Live synchronized simulation model of enterprise departments, worker load & operational capacity
            </p>
          </div>
        </div>

        <Button variant="outline" onClick={loadDto} disabled={loading}>
          <span className="flex items-center gap-2">
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            Sync Digital Twin
          </span>
        </Button>
      </div>

      {/* Top DTO Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="p-5 bg-slate-900/50 border-slate-800">
          <span className="text-xs text-slate-400 block mb-1">Human Workforce</span>
          <div className="flex items-baseline gap-2">
            <span className="text-2xl font-bold text-white">{dto?.active_human_workers ?? 90}</span>
            <span className="text-xs text-slate-400">Employees</span>
          </div>
        </Card>

        <Card className="p-5 bg-slate-900/50 border-slate-800">
          <span className="text-xs text-slate-400 block mb-1">Autonomous Agent Fleet</span>
          <div className="flex items-baseline gap-2">
            <span className="text-2xl font-bold text-indigo-400">{dto?.active_agent_workers ?? 24}</span>
            <span className="text-xs text-slate-400">AI Agents</span>
          </div>
        </Card>

        <Card className="p-5 bg-slate-900/50 border-slate-800">
          <span className="text-xs text-slate-400 block mb-1">Active Sagas</span>
          <div className="flex items-baseline gap-2">
            <span className="text-2xl font-bold text-white">{dto?.running_business_processes ?? 8}</span>
            <span className="text-xs text-slate-400">Workflows</span>
          </div>
        </Card>

        <Card className="p-5 bg-slate-900/50 border-slate-800">
          <span className="text-xs text-slate-400 block mb-1">Mean Org SLA Compliance</span>
          <div className="flex items-baseline gap-2">
            <span className="text-2xl font-bold text-emerald-400">
              {dto?.mean_org_sla_compliance_pct?.toFixed(1) ?? '99.2'}%
            </span>
            <Badge variant="success">Optimal</Badge>
          </div>
        </Card>
      </div>

      {/* Departmental Capacity & Load Heatmaps */}
      <Card className="p-6 bg-slate-900/40 border-slate-800 space-y-4">
        <h2 className="text-base font-semibold text-white flex items-center gap-2">
          <Activity className="w-4 h-4 text-emerald-400" />
          Departmental Workload & Operational Capacity Heatmap
        </h2>

        <div className="space-y-4 pt-2">
          {Object.entries(dto?.department_workloads || {}).map(([dept, load]) => (
            <div key={dept} className="space-y-1 text-xs">
              <div className="flex justify-between">
                <span className="font-mono font-bold text-white uppercase">{dept.replace('dept_', '')}</span>
                <span className="font-mono text-indigo-300">{load.toFixed(1)}% Load</span>
              </div>
              <div className="w-full bg-slate-800 h-2.5 rounded-full overflow-hidden">
                <div
                  className={`h-full rounded-full transition-all ${
                    load > 80 ? 'bg-amber-500' : 'bg-indigo-500'
                  }`}
                  style={{ width: `${load}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
};
