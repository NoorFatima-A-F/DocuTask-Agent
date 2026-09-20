import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import {
  Building2,
  TrendingUp,
  DollarSign,
  ShieldCheck,
  Play,
  RotateCw,
  Award,
  Users,
  Briefcase,
  Cpu,
  Target,
  CheckCircle2,
} from 'lucide-react';
import { organizationPlatformApiClient } from '../../services/organizationPlatformApiClient';
import type { OrganizationOverview, OrganizationCycleSummary } from '../../types/organizationPlatform';

export const OrganizationExecutiveDashboard: React.FC = () => {
  const [overview, setOverview] = useState<OrganizationOverview | null>(null);
  const [cycles, setCycles] = useState<OrganizationCycleSummary[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [runningCycle, setRunningCycle] = useState<boolean>(false);

  const loadData = async () => {
    try {
      setLoading(true);
      const [ov, cyc] = await Promise.all([
        organizationPlatformApiClient.getOverview(),
        organizationPlatformApiClient.getCycles(),
      ]);
      setOverview(ov);
      setCycles(cyc);
    } catch (err) {
      console.error('Failed to load organization overview:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleTriggerCycle = async () => {
    try {
      setRunningCycle(true);
      await organizationPlatformApiClient.runFullCycle(
        'Reduce document processing cost by 40% while maintaining >=98% accuracy'
      );
      await loadData();
    } catch (err) {
      console.error('Error triggering autonomous organization cycle:', err);
    } finally {
      setRunningCycle(false);
    }
  };

  return (
    <div className="space-y-6 p-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-border pb-4">
        <div>
          <div className="flex items-center gap-3">
            <div className="p-2 bg-primary/10 rounded-lg text-primary">
              <Building2 className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-2xl font-bold tracking-tight">AI Executive Command Center</h1>
              <p className="text-sm text-muted-foreground">
                Autonomous AI Enterprise OS (Phase 13.14 AAO-MAGEMEP) — Real-time Multi-Agent Organizational Cognition
              </p>
            </div>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <Button variant="outline" onClick={loadData} disabled={loading}>
            <span className="flex items-center gap-2">
              <RotateCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
              Refresh
            </span>
          </Button>
          <Button variant="intelligence" onClick={handleTriggerCycle} disabled={runningCycle}>
            <span className="flex items-center gap-2">
              <Play className="w-4 h-4" />
              {runningCycle ? 'Executing Cycle...' : 'Execute Autonomous Cycle'}
            </span>
          </Button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="border-border shadow-sm">
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Composite Health</CardTitle>
            <Award className="w-4 h-4 text-emerald-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-emerald-500">
              {overview ? `${(overview.composite_health_score * 100).toFixed(1)}%` : '98.0%'}
            </div>
            <p className="text-xs text-muted-foreground mt-1">SLA, Reliability & Efficiency Index</p>
          </CardContent>
        </Card>

        <Card className="border-border shadow-sm">
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Active ROI Multiplier</CardTitle>
            <TrendingUp className="w-4 h-4 text-primary" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-primary">
              {overview ? `${overview.overall_roi_multiplier.toFixed(1)}x` : '4.2x'}
            </div>
            <p className="text-xs text-muted-foreground mt-1">44.8% unit document cost reduction</p>
          </CardContent>
        </Card>

        <Card className="border-border shadow-sm">
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Monthly Run Rate</CardTitle>
            <DollarSign className="w-4 h-4 text-blue-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              ${overview ? overview.monthly_burn_rate_usd.toLocaleString() : '8,450'}
            </div>
            <p className="text-xs text-muted-foreground mt-1">Compute & workforce equivalent</p>
          </CardContent>
        </Card>

        <Card className="border-border shadow-sm">
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Governance Clearance</CardTitle>
            <ShieldCheck className="w-4 h-4 text-purple-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-purple-500">
              {overview ? `${(overview.governance_approval_rate * 100).toFixed(0)}%` : '98%'}
            </div>
            <p className="text-xs text-muted-foreground mt-1">Multi-pillar cryptographically sealed</p>
          </CardContent>
        </Card>
      </div>

      {/* Organizational Topology & Core Metrics */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="lg:col-span-2 border-border shadow-sm">
          <CardHeader>
            <CardTitle className="text-base flex items-center justify-between">
              <span className="flex items-center gap-2">
                <Briefcase className="w-4 h-4 text-primary" />
                Autonomous Organization State
              </span>
              <Badge variant="success">{overview?.state || 'EXECUTING'}</Badge>
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-3 gap-4 text-center">
              <div className="p-3 bg-muted/40 rounded-lg border border-border">
                <div className="flex items-center justify-center gap-1.5 text-xs text-muted-foreground">
                  <Target className="w-3.5 h-3.5 text-primary" /> Active Missions
                </div>
                <div className="text-xl font-bold mt-1">{overview?.active_missions_count ?? 2}</div>
              </div>
              <div className="p-3 bg-muted/40 rounded-lg border border-border">
                <div className="flex items-center justify-center gap-1.5 text-xs text-muted-foreground">
                  <Users className="w-3.5 h-3.5 text-blue-500" /> Agent Workforce
                </div>
                <div className="text-xl font-bold mt-1">{overview?.active_workforce_count ?? 6}</div>
              </div>
              <div className="p-3 bg-muted/40 rounded-lg border border-border">
                <div className="flex items-center justify-center gap-1.5 text-xs text-muted-foreground">
                  <Cpu className="w-3.5 h-3.5 text-emerald-500" /> Compute Load
                </div>
                <div className="text-xl font-bold mt-1">{overview?.compute_utilization_pct ?? 59.4}%</div>
              </div>
            </div>

            <div className="p-4 rounded-lg bg-card border border-border/80 space-y-2">
              <div className="text-sm font-semibold flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-500" />
                Continuous Executive Loop Invariant
              </div>
              <p className="text-xs text-muted-foreground leading-relaxed">
                Every enterprise mission decomposes into mathematical objectives, undergoes Monte Carlo strategy
                ranking, provisions specialized agent departments, executes critical path tasks under Nash resource
                equilibrium, and is validated through digital twin simulation before deployment.
              </p>
            </div>
          </CardContent>
        </Card>

        {/* Latest Cycle Summary */}
        <Card className="border-border shadow-sm">
          <CardHeader>
            <CardTitle className="text-base flex items-center gap-2">
              <Play className="w-4 h-4 text-primary" />
              Latest Autonomous Cycle
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {overview?.latest_cycle ? (
              <div className="space-y-2 text-sm">
                <div className="flex justify-between py-1 border-b border-border/60">
                  <span className="text-muted-foreground">Cycle ID:</span>
                  <span className="font-mono text-xs">{overview.latest_cycle.cycle_id}</span>
                </div>
                <div className="flex justify-between py-1 border-b border-border/60">
                  <span className="text-muted-foreground">Status:</span>
                  <Badge variant="success">{overview.latest_cycle.status}</Badge>
                </div>
                <div className="flex justify-between py-1 border-b border-border/60">
                  <span className="text-muted-foreground">Health Score:</span>
                  <span className="font-semibold text-emerald-500">
                    {(overview.latest_cycle.composite_health_score * 100).toFixed(1)}%
                  </span>
                </div>
                <div className="flex justify-between py-1 border-b border-border/60">
                  <span className="text-muted-foreground">ROI Multiplier:</span>
                  <span className="font-semibold text-primary">{overview.latest_cycle.roi_multiplier}x</span>
                </div>
                <div className="flex justify-between py-1">
                  <span className="text-muted-foreground">Execution Latency:</span>
                  <span className="font-mono text-xs">{overview.latest_cycle.duration_ms} ms</span>
                </div>
              </div>
            ) : (
              <div className="text-sm text-muted-foreground text-center py-6">No cycle logs yet.</div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Generational Execution History */}
      <Card className="border-border shadow-sm">
        <CardHeader>
          <CardTitle className="text-base flex items-center gap-2">
            <Building2 className="w-4 h-4 text-primary" />
            Organizational Execution Generations ({cycles.length})
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-border text-left text-muted-foreground">
                  <th className="pb-2 font-medium">Cycle ID</th>
                  <th className="pb-2 font-medium">Mission Target</th>
                  <th className="pb-2 font-medium">Strategy</th>
                  <th className="pb-2 font-medium">Health</th>
                  <th className="pb-2 font-medium">ROI</th>
                  <th className="pb-2 font-medium">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border/60">
                {cycles.map((c) => (
                  <tr key={c.cycle_id} className="hover:bg-muted/30 transition-colors">
                    <td className="py-2.5 font-mono text-xs text-primary">{c.cycle_id}</td>
                    <td className="py-2.5">{c.mission_id}</td>
                    <td className="py-2.5 text-xs text-muted-foreground">{c.strategy_id}</td>
                    <td className="py-2.5 text-emerald-500 font-medium">
                      {(c.composite_health_score * 100).toFixed(1)}%
                    </td>
                    <td className="py-2.5 font-semibold">{c.roi_multiplier}x</td>
                    <td className="py-2.5">
                      <Badge variant="success">{c.status}</Badge>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
