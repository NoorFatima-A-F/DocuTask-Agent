import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import {
  Users,
  Cpu,
  Radio,
  Gavel,
  Vote,
  Shield,
  Activity,
  Award,
  Layers,
  Sparkles,
  RefreshCw,
  Send,
  PlusCircle,
} from 'lucide-react';

interface AgentRoleMetric {
  role: string;
  count: number;
  activeCount: number;
  color: string;
}

export const SwarmCommandCenter: React.FC = () => {
  const [broadcastMessage, setBroadcastMessage] = useState<string>('');
  const [broadcastSent, setBroadcastSent] = useState<boolean>(false);

  const roleMetrics: AgentRoleMetric[] = [
    { role: 'EXECUTIVE', count: 1, activeCount: 1, color: 'text-purple-400 bg-purple-500/10 border-purple-500/20' },
    { role: 'PLANNER', count: 2, activeCount: 2, color: 'text-indigo-400 bg-indigo-500/10 border-indigo-500/20' },
    { role: 'COORDINATOR', count: 3, activeCount: 2, color: 'text-blue-400 bg-blue-500/10 border-blue-500/20' },
    { role: 'SPECIALIST', count: 6, activeCount: 5, color: 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20' },
    { role: 'VALIDATOR', count: 3, activeCount: 3, color: 'text-cyan-400 bg-cyan-500/10 border-cyan-500/20' },
    { role: 'REVIEWER', count: 2, activeCount: 1, color: 'text-teal-400 bg-teal-500/10 border-teal-500/20' },
    { role: 'RESOURCE', count: 2, activeCount: 2, color: 'text-amber-400 bg-amber-500/10 border-amber-500/20' },
    { role: 'SECURITY', count: 2, activeCount: 2, color: 'text-rose-400 bg-rose-500/10 border-rose-500/20' },
  ];

  const handleBroadcast = (e: React.FormEvent) => {
    e.preventDefault();
    if (!broadcastMessage.trim()) return;
    setBroadcastSent(true);
    setTimeout(() => {
      setBroadcastSent(false);
      setBroadcastMessage('');
    }, 3000);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Swarm Command Center</h1>
            <Badge variant="success" size="sm" hasDot isPulsing>
              SOCIETY OPERATIONAL
            </Badge>
            <Badge variant="outline" size="sm">
              AMCN-SIP Phase 13.8
            </Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Real-time control plane for autonomous multi-agent coordination, bargaining, consensus, and coalition formation.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm">
            <RefreshCw className="w-3.5 h-3.5 mr-1.5" />
            Sync Topology
          </Button>
          <Button variant="primary" size="sm">
            <PlusCircle className="w-3.5 h-3.5 mr-1.5" />
            Spawn Agent
          </Button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="p-4 bg-purple-950/10 border-purple-500/20">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Active Agents</span>
            <Users className="w-4 h-4 text-purple-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-purple-400 mt-2">21 Agents</div>
          <div className="text-[11px] text-muted-foreground mt-1">8 specialized roles online</div>
        </Card>

        <Card className="p-4 bg-emerald-950/10 border-emerald-500/20">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Average Reputation</span>
            <Award className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-emerald-400 mt-2">0.978 / 1.0</div>
          <div className="text-[11px] text-muted-foreground mt-1">Mathematical decay calibrated</div>
        </Card>

        <Card className="p-4 bg-blue-950/10 border-blue-500/20">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Active Coalitions</span>
            <Layers className="w-4 h-4 text-blue-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-blue-400 mt-2">4 Strike Teams</div>
          <div className="text-[11px] text-muted-foreground mt-1">Synergy score: 0.94 avg</div>
        </Card>

        <Card className="p-4 bg-amber-950/10 border-amber-500/20">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Consensus Quorum</span>
            <Vote className="w-4 h-4 text-amber-400" />
          </div>
          <div className="text-2xl font-bold font-mono text-amber-400 mt-2">100% Signed</div>
          <div className="text-[11px] text-muted-foreground mt-1">SHA-256 agreement root verified</div>
        </Card>
      </div>

      {/* Role Distribution Grid */}
      <Card className="p-5 border-border/60">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <Cpu className="w-4 h-4 text-primary" />
            <h3 className="font-semibold text-sm">Agent Role Distribution & Concurrency</h3>
          </div>
          <span className="text-xs text-muted-foreground">Dynamic Autonomous Allocation</span>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          {roleMetrics.map(r => (
            <div key={r.role} className={`p-3 rounded-lg border ${r.color}`}>
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold">{r.role}</span>
                <span className="text-[11px] font-mono">{r.activeCount}/{r.count} Active</span>
              </div>
              <div className="w-full bg-background/50 h-1.5 rounded-full mt-2 overflow-hidden">
                <div
                  className="h-full bg-current rounded-full"
                  style={{ width: `${(r.activeCount / r.count) * 100}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </Card>

      {/* Quick Operations & Broadcast Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Broadcast Terminal */}
        <Card className="p-5 border-border/60">
          <div className="flex items-center gap-2 mb-3">
            <Radio className="w-4 h-4 text-blue-400" />
            <h3 className="font-semibold text-sm">Swarm Global Broadcast Hub</h3>
          </div>
          <p className="text-xs text-muted-foreground mb-4">
            Dispatch high-priority control directives to all active agents simultaneously via Publish-Subscribe topology.
          </p>

          <form onSubmit={handleBroadcast} className="space-y-3">
            <textarea
              rows={3}
              value={broadcastMessage}
              onChange={e => setBroadcastMessage(e.target.value)}
              placeholder="e.g. MISSION_QUOTA_RESET: Scale document batch concurrency to 8 threads under budget constraint..."
              className="w-full text-xs font-mono p-3 rounded-md bg-background border border-border/60 focus:outline-none focus:ring-1 focus:ring-primary"
            />
            <div className="flex items-center justify-between">
              <span className="text-[11px] text-muted-foreground">
                {broadcastSent ? (
                  <span className="text-emerald-400 font-semibold">✓ Directive Dispatched to 21 Agents</span>
                ) : (
                  'Signed with Swarm Master Key (Ed25519)'
                )}
              </span>
              <Button type="submit" size="sm" variant="primary" disabled={!broadcastMessage.trim()}>
                <Send className="w-3.5 h-3.5 mr-1.5" />
                Broadcast Directive
              </Button>
            </div>
          </form>
        </Card>

        {/* Swarm State Subsystems Status */}
        <Card className="p-5 border-border/60">
          <div className="flex items-center gap-2 mb-3">
            <Activity className="w-4 h-4 text-emerald-400" />
            <h3 className="font-semibold text-sm">Decentralized Society Health Matrix</h3>
          </div>

          <div className="space-y-3">
            <div className="flex items-center justify-between p-2.5 rounded-md bg-muted/20 border border-border/30">
              <div className="flex items-center gap-2">
                <Gavel className="w-4 h-4 text-purple-400" />
                <span className="text-xs font-medium">Bargaining & SLA Ledger</span>
              </div>
              <Badge variant="success" size="sm">0 Conflicts / Resolved</Badge>
            </div>

            <div className="flex items-center justify-between p-2.5 rounded-md bg-muted/20 border border-border/30">
              <div className="flex items-center gap-2">
                <Vote className="w-4 h-4 text-amber-400" />
                <span className="text-xs font-medium">Byzantine Consensus Engine</span>
              </div>
              <Badge variant="success" size="sm">Quorum 100%</Badge>
            </div>

            <div className="flex items-center justify-between p-2.5 rounded-md bg-muted/20 border border-border/30">
              <div className="flex items-center gap-2">
                <Shield className="w-4 h-4 text-rose-400" />
                <span className="text-xs font-medium">Anti-Usurpation Governance</span>
              </div>
              <Badge variant="success" size="sm">Tier 1-5 Enforced</Badge>
            </div>

            <div className="flex items-center justify-between p-2.5 rounded-md bg-muted/20 border border-border/30">
              <div className="flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-cyan-400" />
                <span className="text-xs font-medium">Collective Learning Graph</span>
              </div>
              <Badge variant="intelligence" size="sm">3 Strategies Mined</Badge>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
};
