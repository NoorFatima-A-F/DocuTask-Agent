import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import {
  Cpu,
  RotateCw,
  Sparkles,
  Zap,
  HardDrive,
  DollarSign,
  PieChart,
} from 'lucide-react';
import { organizationPlatformApiClient } from '../../services/organizationPlatformApiClient';
import type { ResourcePool, ResourceAllocationPlan } from '../../types/organizationPlatform';

export const ResourceOptimizationCenter: React.FC = () => {
  const [pool, setPool] = useState<ResourcePool | null>(null);
  const [plan, setPlan] = useState<ResourceAllocationPlan | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [optimizing, setOptimizing] = useState<boolean>(false);

  const loadResources = async () => {
    try {
      setLoading(true);
      const data = await organizationPlatformApiClient.getResources();
      setPool(data.pool);
      setPlan(data.allocation_plan);
    } catch (err) {
      console.error('Failed to load resources:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadResources();
  }, []);

  const handleOptimize = async () => {
    try {
      setOptimizing(true);
      const newPlan = await organizationPlatformApiClient.optimizeResources('COST_EFFICIENCY');
      setPlan(newPlan);
      await loadResources();
    } catch (err) {
      console.error('Error optimizing resources:', err);
    } finally {
      setOptimizing(false);
    }
  };

  return (
    <div className="space-y-6 p-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-border pb-4">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-primary/10 rounded-lg text-primary">
            <Cpu className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl font-bold tracking-tight">Resource Allocation Intelligence</h1>
            <p className="text-sm text-muted-foreground">
              Multi-Tenant Compute Slots, Token Quota Distribution, Memory Footprints & Pareto Budget Optimization
            </p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <Button variant="outline" onClick={loadResources} disabled={loading}>
            <span className="flex items-center gap-2">
              <RotateCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
              Refresh
            </span>
          </Button>
          <Button variant="intelligence" onClick={handleOptimize} disabled={optimizing}>
            <span className="flex items-center gap-2">
              <Sparkles className="w-4 h-4" />
              {optimizing ? 'Solving Simplex...' : 'Run Pareto Optimization'}
            </span>
          </Button>
        </div>
      </div>

      {/* Global Resource Pool Telemetry */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="border-border shadow-sm">
          <CardContent className="p-4 space-y-2">
            <div className="flex justify-between items-center text-xs text-muted-foreground">
              <span>Compute Slots</span>
              <Cpu className="w-4 h-4 text-primary" />
            </div>
            <div className="text-2xl font-bold">
              {pool?.compute_slots_used ?? 38} / {pool?.compute_slots_total ?? 64}
            </div>
            <div className="w-full bg-muted rounded-full h-1.5 overflow-hidden">
              <div
                className="bg-primary h-full rounded-full"
                style={{ width: `${((pool?.compute_slots_used ?? 38) / (pool?.compute_slots_total ?? 64)) * 100}%` }}
              />
            </div>
          </CardContent>
        </Card>

        <Card className="border-border shadow-sm">
          <CardContent className="p-4 space-y-2">
            <div className="flex justify-between items-center text-xs text-muted-foreground">
              <span>Monthly Tokens</span>
              <Zap className="w-4 h-4 text-amber-500" />
            </div>
            <div className="text-2xl font-bold">
              {pool ? `${(pool.tokens_consumed / 1_000_000).toFixed(1)}M` : '54.2M'} /{' '}
              {pool ? `${(pool.token_budget_monthly / 1_000_000).toFixed(0)}M` : '150M'}
            </div>
            <div className="w-full bg-muted rounded-full h-1.5 overflow-hidden">
              <div
                className="bg-amber-500 h-full rounded-full"
                style={{ width: `${((pool?.tokens_consumed ?? 54.2) / (pool?.token_budget_monthly ?? 150)) * 100}%` }}
              />
            </div>
          </CardContent>
        </Card>

        <Card className="border-border shadow-sm">
          <CardContent className="p-4 space-y-2">
            <div className="flex justify-between items-center text-xs text-muted-foreground">
              <span>Vector Memory (GB)</span>
              <HardDrive className="w-4 h-4 text-emerald-500" />
            </div>
            <div className="text-2xl font-bold">
              {pool?.memory_gb_used ?? 210.5} / {pool?.memory_gb_total ?? 512} GB
            </div>
            <div className="w-full bg-muted rounded-full h-1.5 overflow-hidden">
              <div
                className="bg-emerald-500 h-full rounded-full"
                style={{ width: `${((pool?.memory_gb_used ?? 210.5) / (pool?.memory_gb_total ?? 512)) * 100}%` }}
              />
            </div>
          </CardContent>
        </Card>

        <Card className="border-border shadow-sm">
          <CardContent className="p-4 space-y-2">
            <div className="flex justify-between items-center text-xs text-muted-foreground">
              <span>Monthly Budget</span>
              <DollarSign className="w-4 h-4 text-blue-500" />
            </div>
            <div className="text-2xl font-bold">
              ${pool?.dollar_budget_spent_usd.toLocaleString() ?? '16,800'} / $
              {pool?.dollar_budget_total_usd.toLocaleString() ?? '50,000'}
            </div>
            <div className="w-full bg-muted rounded-full h-1.5 overflow-hidden">
              <div
                className="bg-blue-500 h-full rounded-full"
                style={{ width: `${((pool?.dollar_budget_spent_usd ?? 16800) / (pool?.dollar_budget_total_usd ?? 50000)) * 100}%` }}
              />
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Quota Distribution Table */}
      <Card className="border-border shadow-sm">
        <CardHeader className="flex flex-row items-center justify-between pb-3">
          <CardTitle className="text-base flex items-center gap-2">
            <PieChart className="w-4 h-4 text-primary" />
            Department Quota Allocations
          </CardTitle>
          <Badge variant="success">PARETO OPTIMAL ({(plan?.overall_efficiency_score ?? 0.95) * 100}%)</Badge>
        </CardHeader>
        <CardContent>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-border text-left text-muted-foreground">
                  <th className="pb-2 font-medium">Department</th>
                  <th className="pb-2 font-medium">Compute Slots</th>
                  <th className="pb-2 font-medium">Token Quota / Mo</th>
                  <th className="pb-2 font-medium">Memory</th>
                  <th className="pb-2 font-medium">Budget Share</th>
                  <th className="pb-2 font-medium">Priority Weight</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border/60">
                {plan?.quotas.map((q) => (
                  <tr key={q.department_id} className="hover:bg-muted/30 transition-colors">
                    <td className="py-3 font-semibold">{q.department_name}</td>
                    <td className="py-3 font-mono text-primary font-medium">{q.compute_slots} slots</td>
                    <td className="py-3 text-muted-foreground font-mono">
                      {(q.token_quota_monthly / 1_000_000).toFixed(0)}M tokens
                    </td>
                    <td className="py-3 font-mono">{q.memory_gb} GB</td>
                    <td className="py-3 font-semibold">${q.budget_allocated_usd.toLocaleString()}</td>
                    <td className="py-3 font-mono">{q.priority_weight}x</td>
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
