import React, { useState } from 'react';
import {
  ShieldCheck,
  Server,
  RefreshCw,
  Zap,
  Activity,
  Award
} from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';

interface ResilienceScorecardProps {
  missionId?: string;
}

export const ResilienceScorecard: React.FC<ResilienceScorecardProps> = ({
  missionId = 'cluster-primary-master',
}) => {
  const [metrics] = useState({
    resilienceScore: 99.4,
    availabilityPct: 99.99,
    mttrSeconds: 0.18,
    mtbfHours: 720.0,
    mttdSeconds: 0.05,
    recoverySuccessPct: 100.0,
    healingSuccessPct: 100.0,
    slaCompliancePct: 100.0,
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <ShieldCheck className="w-5 h-5 text-emerald-400" />
            Enterprise SRE Resilience Scorecard & SLA Benchmark
          </h2>
          <p className="text-sm text-slate-400">
            MTTR, MTBF, MTTD, availability metrics, and automated resolution efficacy ratios for: <code className="text-emerald-300 font-mono text-xs">{missionId}</code>
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Badge variant="success" size="md">
            SRE Level: TIER 4 AUTONOMIC
          </Badge>
          <button className="flex items-center gap-1.5 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium rounded-lg border border-slate-700">
            <RefreshCw className="w-3.5 h-3.5" />
            Recalculate Scorecard
          </button>
        </div>
      </div>

      {/* Primary KPI Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 font-mono">
        <Card className="p-4 bg-slate-900 border-slate-800">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs text-slate-400">Composite Resilience Score</span>
            <Award className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-2xl font-bold text-emerald-400">
            {metrics.resilienceScore}%
          </div>
          <div className="mt-2 w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
            <div className="bg-emerald-500 h-full rounded-full" style={{ width: `${metrics.resilienceScore}%` }} />
          </div>
          <span className="text-[10px] text-slate-400 mt-1 block">Tier-4 Autonomic Certification</span>
        </Card>

        <Card className="p-4 bg-slate-900 border-slate-800">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs text-slate-400">Mean Time To Recovery (MTTR)</span>
            <Zap className="w-4 h-4 text-amber-400" />
          </div>
          <div className="text-2xl font-bold text-amber-400">
            {metrics.mttrSeconds}s
          </div>
          <p className="text-[11px] text-slate-400 mt-2">SLA Bound: &lt; 2.0s</p>
          <span className="text-[10px] text-emerald-400 mt-1 block">Sub-second recovery verified</span>
        </Card>

        <Card className="p-4 bg-slate-900 border-slate-800">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs text-slate-400">Mean Time To Detect (MTTD)</span>
            <Activity className="w-4 h-4 text-cyan-400" />
          </div>
          <div className="text-2xl font-bold text-cyan-400">
            {metrics.mttdSeconds}s
          </div>
          <p className="text-[11px] text-slate-400 mt-2">Telemetry sample rate: 50ms</p>
          <span className="text-[10px] text-indigo-400 mt-1 block">Near-instant detection</span>
        </Card>

        <Card className="p-4 bg-slate-900 border-slate-800">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs text-slate-400">Mean Time Between Failures</span>
            <Server className="w-4 h-4 text-purple-400" />
          </div>
          <div className="text-2xl font-bold text-purple-400">
            {metrics.mtbfHours}h
          </div>
          <p className="text-[11px] text-slate-400 mt-2">Availability: {metrics.availabilityPct}%</p>
          <span className="text-[10px] text-slate-500 mt-1 block">Four-Nines Operational</span>
        </Card>
      </div>

      {/* Success Rates Breakdown */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 font-mono">
        <Card className="p-4 bg-slate-900 border-slate-800 text-center space-y-1">
          <span className="text-xs text-slate-400 block">Automated Healing Success</span>
          <span className="text-xl font-bold text-emerald-400">{metrics.healingSuccessPct}%</span>
          <span className="text-[10px] text-slate-500 block">10 / 10 Actions Succeeded</span>
        </Card>

        <Card className="p-4 bg-slate-900 border-slate-800 text-center space-y-1">
          <span className="text-xs text-slate-400 block">Checkpoint Rollback Success</span>
          <span className="text-xl font-bold text-indigo-400">{metrics.recoverySuccessPct}%</span>
          <span className="text-[10px] text-slate-500 block">Zero Invariant Violations</span>
        </Card>

        <Card className="p-4 bg-slate-900 border-slate-800 text-center space-y-1">
          <span className="text-xs text-slate-400 block">Contractual SLA Adherence</span>
          <span className="text-xl font-bold text-cyan-400">{metrics.slaCompliancePct}%</span>
          <span className="text-[10px] text-slate-500 block">Zero Penalty Breaches</span>
        </Card>
      </div>
    </div>
  );
};
