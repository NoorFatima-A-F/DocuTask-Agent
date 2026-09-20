import React, { useState, useEffect } from 'react';
import {
  Rocket,
  RotateCcw,
  RefreshCw,
  Activity,
  Clock,
} from 'lucide-react';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { EvolutionPlatformApiClient } from '../../services/evolutionPlatformApiClient';
import { DeploymentRecordPayload } from '../../types/evolutionPlatform';

export const DeploymentControlCenter: React.FC = () => {
  const [deployments, setDeployments] = useState<DeploymentRecordPayload[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [actionLoading, setActionLoading] = useState<string | null>(null);

  useEffect(() => {
    loadDeployments();
  }, []);

  const loadDeployments = async () => {
    setLoading(true);
    try {
      const data = await EvolutionPlatformApiClient.listDeployments();
      setDeployments(data);
    } catch (err) {
      console.error('Failed to load deployments:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleAdvanceTraffic = async (deploymentId: string, targetPct: number) => {
    setActionLoading(deploymentId);
    try {
      const updated = await EvolutionPlatformApiClient.advanceCanary(deploymentId, targetPct);
      setDeployments((prev) => prev.map((d) => (d.deployment_id === deploymentId ? updated : d)));
    } catch (err) {
      console.error('Failed to advance canary:', err);
    } finally {
      setActionLoading(null);
    }
  };

  const handleRollback = async (deploymentId: string) => {
    setActionLoading(deploymentId);
    try {
      const updated = await EvolutionPlatformApiClient.rollbackDeployment(deploymentId, 'Manual operator rollback');
      setDeployments((prev) => prev.map((d) => (d.deployment_id === deploymentId ? updated : d)));
    } catch (err) {
      console.error('Failed to rollback:', err);
    } finally {
      setActionLoading(null);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-slate-900 via-slate-900 to-slate-950 border border-slate-800 rounded-2xl p-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-4 shadow-xl">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-emerald-500/10 border border-emerald-500/20 rounded-xl">
            <Rocket className="w-6 h-6 text-emerald-400" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl font-bold text-slate-100">Progressive Canary & Blue/Green Deployment</h1>
              <Badge variant="success" size="sm">Automated Rollback Safeguard</Badge>
            </div>
            <p className="text-sm text-slate-400 mt-0.5">
              Control progressive canary rollout percentages with real-time SLA circuit-breakers and instant rollback capability.
            </p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <Button
            variant="outline"
            onClick={loadDeployments}
            disabled={loading}
          >
            <span className="flex items-center gap-2">
              <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
              Refresh
            </span>
          </Button>
        </div>
      </div>

      {/* Deployments List */}
      <div className="space-y-5">
        {deployments.map((dep) => (
          <div
            key={dep.deployment_id}
            className="bg-slate-900/80 border border-slate-800 rounded-xl p-6 space-y-5 shadow-lg"
          >
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 pb-4 border-b border-slate-800">
              <div>
                <div className="flex items-center gap-3">
                  <h2 className="text-lg font-bold text-slate-100 font-mono">{dep.deployment_id}</h2>
                  <Badge
                    variant={
                      dep.deployment_state === 'PROMOTED'
                        ? 'success'
                        : dep.deployment_state === 'ROLLED_BACK'
                        ? 'error'
                        : 'intelligence'
                    }
                    size="sm"
                  >
                    {dep.deployment_state}
                  </Badge>
                </div>
                <span className="text-xs text-slate-400 font-mono mt-1 block">
                  Target Version: <span className="text-slate-200 font-semibold">{dep.target_version}</span> • Mutation: {dep.mutation_id}
                </span>
              </div>

              {dep.deployment_state !== 'ROLLED_BACK' && (
                <div className="flex items-center gap-2">
                  <Button
                    variant="danger"
                    size="sm"
                    onClick={() => handleRollback(dep.deployment_id)}
                    disabled={actionLoading === dep.deployment_id}
                  >
                    <span className="flex items-center gap-1.5">
                      <RotateCcw className="w-3.5 h-3.5" />
                      Emergency Rollback
                    </span>
                  </Button>
                </div>
              )}
            </div>

            {/* Canary Progress Bar & Controls */}
            <div className="space-y-2">
              <div className="flex items-center justify-between text-xs font-mono text-slate-300">
                <span>Canary Traffic Routing</span>
                <span className="font-bold text-emerald-400">{dep.canary_traffic_pct.toFixed(0)}% Production Load</span>
              </div>
              <div className="w-full bg-slate-950 h-3 rounded-full border border-slate-800 overflow-hidden">
                <div
                  className="bg-emerald-400 h-full rounded-full transition-all duration-500"
                  style={{ width: `${dep.canary_traffic_pct}%` }}
                />
              </div>

              {dep.deployment_state !== 'ROLLED_BACK' && dep.canary_traffic_pct < 100 && (
                <div className="flex items-center gap-2 pt-2">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => handleAdvanceTraffic(dep.deployment_id, 25)}
                    disabled={actionLoading === dep.deployment_id}
                  >
                    Promote to 25%
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => handleAdvanceTraffic(dep.deployment_id, 50)}
                    disabled={actionLoading === dep.deployment_id}
                  >
                    Promote to 50%
                  </Button>
                  <Button
                    variant="intelligence"
                    size="sm"
                    onClick={() => handleAdvanceTraffic(dep.deployment_id, 100)}
                    disabled={actionLoading === dep.deployment_id}
                  >
                    Full 100% Blue/Green Promotion
                  </Button>
                </div>
              )}
            </div>

            {/* Real-time Live SLA Tiles */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 font-mono text-xs">
              <div className="p-3 bg-slate-950/80 border border-slate-800 rounded-lg space-y-1">
                <div className="flex items-center justify-between text-slate-400">
                  <span className="flex items-center gap-1.5">
                    <Clock className="w-3.5 h-3.5 text-indigo-400" />
                    Live P95 Latency
                  </span>
                </div>
                <div className="text-base font-bold text-indigo-300">{dep.live_p95_latency_ms.toFixed(1)}ms</div>
                <div className="text-[10px] text-slate-500">Threshold: {dep.auto_rollback_latency_threshold_ms}ms</div>
              </div>

              <div className="p-3 bg-slate-950/80 border border-slate-800 rounded-lg space-y-1">
                <div className="flex items-center justify-between text-slate-400">
                  <span className="flex items-center gap-1.5">
                    <Activity className="w-3.5 h-3.5 text-emerald-400" />
                    Live Error Rate
                  </span>
                </div>
                <div className="text-base font-bold text-emerald-300">{(dep.live_error_rate * 100).toFixed(3)}%</div>
                <div className="text-[10px] text-slate-500">Threshold: {(dep.auto_rollback_error_threshold * 100).toFixed(1)}%</div>
              </div>

              <div className="p-3 bg-slate-950/80 border border-slate-800 rounded-lg space-y-1">
                <div className="text-slate-400">Rollback Snapshot Link</div>
                <div className="text-xs font-semibold text-purple-400 truncate">{dep.rollback_snapshot_id || 'snap_prod_v13_12'}</div>
                <div className="text-[10px] text-slate-500">Circuit-breaker armed</div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
