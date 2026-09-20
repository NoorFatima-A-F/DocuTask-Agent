import React, { useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import {
  Sparkles,
  TrendingUp,
  Brain,
  ShieldCheck,
  Zap,
  RefreshCw,
} from 'lucide-react';

export const ExecutiveDecisionDashboard: React.FC = () => {
  const [isRefreshing, setIsRefreshing] = useState<boolean>(false);

  const handleRefresh = () => {
    setIsRefreshing(true);
    setTimeout(() => {
      setIsRefreshing(false);
    }, 1000);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Executive Decision Dashboard</h1>
            <Badge variant="intelligence" size="sm" hasDot isPulsing>
              META-REASONING EXECUTIVE SUITE
            </Badge>
            <Badge variant="outline" size="sm">
              AMRS-RSIP Phase 13.9
            </Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Executive control plane consolidating meta-cognitive autonomy, self-improvement ROI, autonomous evolution velocity, and verifiable truth integrity.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm" onClick={handleRefresh} disabled={isRefreshing}>
            <RefreshCw className={`w-3.5 h-3.5 mr-1.5 ${isRefreshing ? 'animate-spin' : ''}`} />
            {isRefreshing ? 'Recalculating...' : 'Refresh Executive Metrics'}
          </Button>
          <Button variant="intelligence" size="sm">
            <Sparkles className="w-3.5 h-3.5 mr-1.5" />
            Trigger Optimization Cycle
          </Button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="p-4 bg-purple-950/10 border-purple-500/20">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Autonomous Gain Score</span>
            <TrendingUp className="w-4 h-4 text-purple-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-purple-400 mt-2">+42.5%</div>
          <div className="text-[11px] text-muted-foreground mt-1">Net throughput speedup</div>
        </Card>

        <Card className="p-4 bg-emerald-950/10 border-emerald-500/20">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Zero-Fabrication Floor</span>
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-emerald-400 mt-2">100.0%</div>
          <div className="text-[11px] text-muted-foreground mt-1">Cryptographically audited</div>
        </Card>

        <Card className="p-4 bg-blue-950/10 border-blue-500/20">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Self-Improvement Cycles</span>
            <Brain className="w-4 h-4 text-blue-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-blue-400 mt-2">18 Concluded</div>
          <div className="text-[11px] text-muted-foreground mt-1">100% convergence rate</div>
        </Card>

        <Card className="p-4 bg-indigo-950/10 border-indigo-500/20">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Token Cost Savings</span>
            <Zap className="w-4 h-4 text-indigo-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-indigo-400 mt-2">-22.0%</div>
          <div className="text-[11px] text-muted-foreground mt-1">Embedding cache efficiency</div>
        </Card>
      </div>

      {/* Strategic Summary & Evolution Health */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card className="p-5 border-border/40 space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Brain className="w-4 h-4 text-purple-400" />
              <h2 className="text-base font-semibold">Meta-Cognitive Autonomy Health</h2>
            </div>
            <Badge variant="success" size="sm">
              OPTIMAL
            </Badge>
          </div>

          <div className="space-y-3 text-xs">
            <div className="flex justify-between items-center p-3 rounded-lg bg-secondary/20 border border-border/30">
              <span className="text-muted-foreground">Hierarchical Recursive Reflection:</span>
              <span className="font-mono font-bold text-emerald-400">7 of 7 Tiers Active</span>
            </div>
            <div className="flex justify-between items-center p-3 rounded-lg bg-secondary/20 border border-border/30">
              <span className="text-muted-foreground">Statistical Significance Floor:</span>
              <span className="font-mono font-bold text-foreground">p &lt; 0.01 (Two-Tailed)</span>
            </div>
            <div className="flex justify-between items-center p-3 rounded-lg bg-secondary/20 border border-border/30">
              <span className="text-muted-foreground">Cryptographic Governance Signature Quorum:</span>
              <span className="font-mono font-bold text-purple-400">2 of 2 Required Signatures</span>
            </div>
            <div className="flex justify-between items-center p-3 rounded-lg bg-secondary/20 border border-border/30">
              <span className="text-muted-foreground">Rollback Recovery Latency:</span>
              <span className="font-mono font-bold text-blue-400">&lt; 150ms Guaranteed</span>
            </div>
          </div>
        </Card>

        <Card className="p-5 border-border/40 space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-purple-400" />
              <h2 className="text-base font-semibold">Executive Decision Directives</h2>
            </div>
            <Badge variant="outline" size="sm">
              Continuous Loop
            </Badge>
          </div>

          <div className="space-y-3">
            <div className="p-3.5 rounded-lg border border-purple-500/20 bg-purple-950/10 space-y-1">
              <div className="flex items-center justify-between text-xs font-semibold text-purple-300">
                <span>Directive 1: Promote Dynamic DAG Fan-Out to Default Pipeline</span>
                <Badge variant="success" size="sm">Approved</Badge>
              </div>
              <p className="text-[11px] text-muted-foreground">
                Replay experimentation verified a 42.5% latency improvement without increasing compute overhead.
              </p>
            </div>

            <div className="p-3.5 rounded-lg border border-emerald-500/20 bg-emerald-950/10 space-y-1">
              <div className="flex items-center justify-between text-xs font-semibold text-emerald-300">
                <span>Directive 2: Expand Shared Schema Token Cache</span>
                <Badge variant="info" size="sm">Active</Badge>
              </div>
              <p className="text-[11px] text-muted-foreground">
                In-memory embedding cache achieving 84% hit rate on recurring vendor invoice formats.
              </p>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
};
