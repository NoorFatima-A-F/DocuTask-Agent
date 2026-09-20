import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import {
  ShieldCheck,
  Play,
  RotateCw,
  Activity,
  Zap,
  CheckCircle2,
  Workflow,
  Server,
  Layers,
  Terminal,
} from 'lucide-react';
import { executionPlatformApiClient } from '../../services/executionPlatformApiClient';
import type { ExecutionPlatformOverview, MissionExecution } from '../../types/executionPlatform';

export const ExecutionExecutiveDashboard: React.FC = () => {
  const [overview, setOverview] = useState<ExecutionPlatformOverview | null>(null);
  const [recentMissions, setRecentMissions] = useState<MissionExecution[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [executingQuickGoal, setExecutingQuickGoal] = useState<boolean>(false);

  const loadData = async () => {
    try {
      setLoading(true);
      const [ov, mList] = await Promise.all([
        executionPlatformApiClient.getOverview(),
        executionPlatformApiClient.listMissions(),
      ]);
      setOverview(ov);
      setRecentMissions(mList.missions || []);
    } catch (err) {
      console.error('Failed to load execution overview:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleQuickExecute = async (goal: string) => {
    try {
      setExecutingQuickGoal(true);
      await executionPlatformApiClient.executeGoal({
        goal,
        dry_run: false,
        initiated_by: 'Executive Director Console',
      });
      await loadData();
    } catch (err) {
      console.error('Execution goal error:', err);
    } finally {
      setExecutingQuickGoal(false);
    }
  };

  if (loading && !overview) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="flex flex-col items-center gap-4">
          <RotateCw className="w-8 h-8 animate-spin text-purple-500" />
          <p className="text-gray-400">Loading Execution Platform Telemetry...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-gradient-to-r from-slate-900 via-purple-950 to-slate-900 p-6 rounded-2xl border border-purple-800/40 shadow-xl">
        <div>
          <div className="flex items-center gap-3">
            <h1 className="text-2xl font-bold text-white tracking-wide">
              Autonomous Real-World Execution Platform
            </h1>
            <Badge variant="intelligence">Phase 13.15 ARWE-UTOCOP</Badge>
          </div>
          <p className="text-purple-200/80 text-sm mt-1">
            Universal Tool Orchestration, Cyber-Physical Operations, Digital Twin Sandboxing & Cryptographic Ledgers
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Button variant="outline" onClick={loadData}>
            <span className="flex items-center gap-2">
              <RotateCw className="w-4 h-4" />
              Refresh
            </span>
          </Button>
          <Button
            variant="intelligence"
            onClick={() => handleQuickExecute('Deploy autonomous hotfix to canary and verify')}
            disabled={executingQuickGoal}
          >
            <span className="flex items-center gap-2">
              <Play className="w-4 h-4" />
              {executingQuickGoal ? 'Executing Mission...' : 'Execute Hotfix Mission'}
            </span>
          </Button>
        </div>
      </div>

      {/* Metric Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="bg-slate-900/60 border-slate-800 backdrop-blur">
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-slate-400">Active Connectors</CardTitle>
            <Server className="w-4 h-4 text-emerald-400" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-white">
              {overview?.connected_count || 0} / {overview?.total_connectors || 0}
            </div>
            <p className="text-xs text-emerald-400 mt-1 flex items-center gap-1">
              <CheckCircle2 className="w-3 h-3" /> All external gateways healthy
            </p>
          </CardContent>
        </Card>

        <Card className="bg-slate-900/60 border-slate-800 backdrop-blur">
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-slate-400">Registered Tools</CardTitle>
            <Zap className="w-4 h-4 text-amber-400" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-white">{overview?.total_tools || 0}</div>
            <p className="text-xs text-slate-400 mt-1">Across 8 taxonomy categories</p>
          </CardContent>
        </Card>

        <Card className="bg-slate-900/60 border-slate-800 backdrop-blur">
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-slate-400">Total Missions Run</CardTitle>
            <Workflow className="w-4 h-4 text-purple-400" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-white">{overview?.total_missions || 0}</div>
            <p className="text-xs text-purple-400 mt-1">
              {overview?.completed_missions || 0} completed successfully
            </p>
          </CardContent>
        </Card>

        <Card className="bg-slate-900/60 border-slate-800 backdrop-blur">
          <CardHeader className="flex flex-row items-center justify-between pb-2">
            <CardTitle className="text-sm font-medium text-slate-400">Cryptographic Audit Ledger</CardTitle>
            <ShieldCheck className="w-4 h-4 text-cyan-400" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-cyan-400">
              {overview?.audit_ledger_integrity ? '100% Valid' : 'Degraded'}
            </div>
            <p className="text-xs text-slate-400 mt-1">SHA-256 Chained Integrity</p>
          </CardContent>
        </Card>
      </div>

      {/* Core Invariant Workflow Visualizer */}
      <Card className="bg-slate-900/70 border-slate-800">
        <CardHeader>
          <CardTitle className="text-base text-white flex items-center gap-2">
            <Layers className="w-5 h-5 text-purple-400" />
            Core Autonomous Execution Invariant Pipeline
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap items-center gap-2 text-xs font-mono">
            {[
              'Goal Ingestion',
              'CPM Planning',
              'Tool Selection',
              'Capability Check',
              'Credential Vault',
              'Policy Gate',
              'Risk Scoring',
              'Simulation Sandbox',
              'Execution Dispatch',
              'Verification Cert',
              'Saga Rollback',
              'Audit Chain',
            ].map((step, idx) => (
              <div key={step} className="flex items-center gap-2">
                <span className="px-3 py-1.5 rounded-lg bg-purple-950/60 border border-purple-700/50 text-purple-200">
                  {idx + 1}. {step}
                </span>
                {idx < 11 && <span className="text-slate-600 font-bold">→</span>}
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Quick Mission Actions & Live Telemetry */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="lg:col-span-1 bg-slate-900/60 border-slate-800">
          <CardHeader>
            <CardTitle className="text-base text-white flex items-center gap-2">
              <Terminal className="w-4 h-4 text-purple-400" />
              Direct Goal Dispatcher
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <p className="text-xs text-slate-400">
              Trigger autonomous missions with automatic Critical Path DAG compilation and safety simulation:
            </p>
            <div className="space-y-2">
              <Button
                variant="outline"
                className="w-full justify-start text-xs text-left"
                onClick={() => handleQuickExecute('Deploy autonomous hotfix to canary and verify')}
                disabled={executingQuickGoal}
              >
                <span className="flex items-center gap-2">
                  <Play className="w-3.5 h-3.5 text-purple-400" />
                  K8s Canary Hotfix & Slack Broadcast
                </span>
              </Button>
              <Button
                variant="outline"
                className="w-full justify-start text-xs text-left"
                onClick={() => handleQuickExecute('Issue monthly customer invoice and store S3 receipt')}
                disabled={executingQuickGoal}
              >
                <span className="flex items-center gap-2">
                  <Play className="w-3.5 h-3.5 text-emerald-400" />
                  Stripe Customer Invoicing & S3 Vault
                </span>
              </Button>
              <Button
                variant="outline"
                className="w-full justify-start text-xs text-left"
                onClick={() => handleQuickExecute('Scrape portal status table and persist to DB')}
                disabled={executingQuickGoal}
              >
                <span className="flex items-center gap-2">
                  <Play className="w-3.5 h-3.5 text-cyan-400" />
                  Playwright Web Scrape & SQL Store
                </span>
              </Button>
            </div>
          </CardContent>
        </Card>

        <Card className="lg:col-span-2 bg-slate-900/60 border-slate-800">
          <CardHeader>
            <CardTitle className="text-base text-white flex items-center gap-2">
              <Activity className="w-4 h-4 text-emerald-400" />
              Recent Mission Executions
            </CardTitle>
          </CardHeader>
          <CardContent>
            {recentMissions.length === 0 ? (
              <div className="text-center py-8 text-slate-500 text-sm">
                No recent missions found. Launch a mission above to observe real-time telemetry.
              </div>
            ) : (
              <div className="space-y-3">
                {recentMissions.slice(0, 4).map((m) => (
                  <div
                    key={m.mission_id}
                    className="p-3 bg-slate-800/40 border border-slate-700/50 rounded-lg flex items-center justify-between"
                  >
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="text-sm font-semibold text-white">{m.goal}</span>
                        <Badge
                          variant={
                            m.status === 'completed'
                              ? 'success'
                              : m.status === 'executing'
                              ? 'intelligence'
                              : 'warning'
                          }
                        >
                          {m.status}
                        </Badge>
                      </div>
                      <p className="text-xs text-slate-400 mt-1">
                        ID: {m.mission_id} • Steps: {m.steps.length} • Duration: {m.total_execution_time_ms}ms
                      </p>
                    </div>
                    <Badge variant="outline">{m.risk_level} risk</Badge>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};
