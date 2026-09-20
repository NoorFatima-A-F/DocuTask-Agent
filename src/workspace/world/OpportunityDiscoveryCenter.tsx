import React from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import {
  Zap,
  PlusCircle,
  CheckCircle2,
} from 'lucide-react';

interface OpportunityItem {
  id: string;
  title: string;
  category: string;
  description: string;
  latencyGainPct: number;
  costSavingPct: number;
  confidence: number;
  directive: string;
}

export const OpportunityDiscoveryCenter: React.FC = () => {
  const opportunities: OpportunityItem[] = [
    {
      id: 'opp-01',
      title: 'Shared Corporate Invoice Header Caching',
      category: 'CACHING_OPTIMIZATION',
      description: 'Recurring corporate invoice formats share 85% identical header tokens across vendor documents.',
      latencyGainPct: 28.0,
      costSavingPct: 22.0,
      confidence: 0.985,
      directive: 'Enable zero-copy speculative embedding cache for top 50 corporate invoice schemas.',
    },
    {
      id: 'opp-02',
      title: 'Triadic Extraction Strike Team Template',
      category: 'WORKFLOW_REUSE',
      description: 'Pre-compose specialist agent coalitions for multi-column balance sheets to bypass auction renegotiation latency.',
      latencyGainPct: 19.5,
      costSavingPct: 8.0,
      confidence: 0.992,
      directive: 'Deploy pre-warmed triadic agent coalition template on high-volume accounting queues.',
    },
    {
      id: 'opp-03',
      title: 'Lock-Free Memory Buffer Migration',
      category: 'AGENT_SPECIALIZATION',
      description: 'Transition hot fact telemetry from mutex locks to atomic circular ring buffers.',
      latencyGainPct: 15.0,
      costSavingPct: 5.0,
      confidence: 0.978,
      directive: 'Activate zero-lock ring buffer in event routing subsystem.',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Opportunity Discovery Center</h1>
            <Badge variant="intelligence" size="sm" hasDot isPulsing>
              SYNERGY MINER ACTIVE
            </Badge>
            <Badge variant="outline" size="sm">
              AWM-PSDTIP Phase 13.10
            </Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Autonomous discovery of unexploited capability synergies, workflow reuse, caching potential, and proactive execution accelerations.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="intelligence" size="sm">
            <PlusCircle className="w-3.5 h-3.5 mr-1.5" />
            Discover New Opportunities
          </Button>
        </div>
      </div>

      {/* Opportunities List */}
      <div className="space-y-4">
        {opportunities.map((opp) => (
          <Card key={opp.id} className="p-5 border-border/40 space-y-4 hover:border-purple-500/30 transition-colors">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <Badge variant="intelligence" size="sm">
                    {opp.category.replace(/_/g, ' ')}
                  </Badge>
                  <h2 className="text-base font-semibold text-foreground">{opp.title}</h2>
                </div>
                <p className="text-xs text-muted-foreground">{opp.description}</p>
              </div>
              <div className="flex items-center gap-2">
                <Badge variant="success" size="sm">
                  +{opp.latencyGainPct}% Speed
                </Badge>
                <Badge variant="info" size="sm">
                  -{opp.costSavingPct}% Cost
                </Badge>
              </div>
            </div>

            {/* Actionable Directive */}
            <div className="flex items-center gap-2 text-xs text-purple-300 bg-purple-950/20 p-2.5 rounded border border-purple-500/30">
              <Zap className="w-3.5 h-3.5 text-purple-400 flex-shrink-0" />
              <span>Actionable Directive: {opp.directive}</span>
            </div>

            <div className="flex items-center justify-between text-xs pt-2 border-t border-border/30">
              <div className="flex items-center gap-1.5 text-muted-foreground font-mono">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                <span>Confidence: {(opp.confidence * 100).toFixed(1)}%</span>
              </div>
              <Button variant="outline" size="sm">
                Apply Recommended Optimization
              </Button>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
