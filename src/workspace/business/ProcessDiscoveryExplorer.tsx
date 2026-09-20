import React, { useState, useEffect } from 'react';
import {
  Compass,
  RefreshCw,
  AlertTriangle,
} from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { BusinessApiClient } from '../../services/businessApiClient';
import { DiscoveredProcess } from '../../types/businessPlatform';

export const ProcessDiscoveryExplorer: React.FC = () => {
  const [discovered, setDiscovered] = useState<DiscoveredProcess[]>([]);
  const [loading, setLoading] = useState(true);

  const loadData = async () => {
    try {
      setLoading(true);
      const res = await BusinessApiClient.getDiscovery();
      setDiscovered(res);
    } catch (err) {
      console.error('Failed to load discovered processes:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/60 p-6 rounded-2xl border border-slate-800 backdrop-blur-md">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-indigo-500/10 rounded-xl border border-indigo-500/20 text-indigo-400">
            <Compass className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white">Process Mining & Discovery Explorer</h1>
            <p className="text-sm text-slate-400">
              Autonomous reconstruction of actual organizational workflows from ERP telemetry & audit logs
            </p>
          </div>
        </div>

        <Button variant="outline" onClick={loadData} disabled={loading}>
          <span className="flex items-center gap-2">
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            Refresh Mined Data
          </span>
        </Button>
      </div>

      {/* Discovered Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {discovered.map((d) => (
          <Card key={d.discovered_id} className="p-6 bg-slate-900/40 border-slate-800 space-y-4">
            <div className="flex justify-between items-start">
              <div>
                <h2 className="text-base font-bold text-white">{d.name}</h2>
                <span className="text-xs text-slate-400 font-mono">ID: {d.discovered_id}</span>
              </div>
              <Badge variant="intelligence">{d.variants_count} Path Variants</Badge>
            </div>

            <div className="grid grid-cols-3 gap-3 text-xs font-mono">
              <div className="p-3 bg-slate-800/40 rounded-lg border border-slate-700/60">
                <span className="text-slate-400 block text-[11px]">Frequency</span>
                <span className="text-white font-bold text-sm">{d.frequency.toLocaleString()} runs</span>
              </div>
              <div className="p-3 bg-slate-800/40 rounded-lg border border-slate-700/60">
                <span className="text-slate-400 block text-[11px]">Mean Duration</span>
                <span className="text-indigo-300 font-bold text-sm">{(d.mean_duration_sec / 60).toFixed(0)} mins</span>
              </div>
              <div className="p-3 bg-slate-800/40 rounded-lg border border-slate-700/60">
                <span className="text-slate-400 block text-[11px]">Conformance</span>
                <span className="text-emerald-400 font-bold text-sm">{(d.compliance_score * 100).toFixed(0)}%</span>
              </div>
            </div>

            {/* Bottlenecks */}
            <div className="space-y-2 pt-2 border-t border-slate-800">
              <span className="text-xs font-semibold text-slate-300 flex items-center gap-1.5">
                <AlertTriangle className="w-3.5 h-3.5 text-amber-400" />
                Discovered Bottleneck Steps
              </span>
              <div className="flex flex-wrap gap-1.5">
                {d.bottleneck_steps.map((b, idx) => (
                  <span
                    key={idx}
                    className="px-2.5 py-1 bg-amber-950/40 border border-amber-800/40 text-amber-300 rounded font-mono text-[11px]"
                  >
                    {b}
                  </span>
                ))}
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
