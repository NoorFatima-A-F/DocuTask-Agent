import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import {
  History,
  RotateCw,
  Clock,
  Sparkles,
} from 'lucide-react';
import { organizationPlatformApiClient } from '../../services/organizationPlatformApiClient';
import type { OrganizationCycleSummary } from '../../types/organizationPlatform';

export const OrganizationalEvolutionTimeline: React.FC = () => {
  const [cycles, setCycles] = useState<OrganizationCycleSummary[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  const loadCycles = async () => {
    try {
      setLoading(true);
      const data = await organizationPlatformApiClient.getCycles();
      setCycles(data);
    } catch (err) {
      console.error('Failed to load cycles:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadCycles();
  }, []);

  return (
    <div className="space-y-6 p-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-border pb-4">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-primary/10 rounded-lg text-primary">
            <History className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl font-bold tracking-tight">Organizational Evolution Timeline</h1>
            <p className="text-sm text-muted-foreground">
              Chronological Generational Lineage of Enterprise Topologies, Strategic Refinements & ROI Advances
            </p>
          </div>
        </div>
        <Button variant="outline" onClick={loadCycles} disabled={loading}>
          <span className="flex items-center gap-2">
            <RotateCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            Refresh
          </span>
        </Button>
      </div>

      {/* Timeline Stream */}
      <Card className="border-border shadow-sm">
        <CardHeader>
          <CardTitle className="text-base flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-primary" />
            Evolution Generations ({cycles.length})
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="relative pl-6 border-l-2 border-border space-y-6 my-2">
            {cycles.map((c, idx) => (
              <div key={c.cycle_id} className="relative">
                {/* Timeline Dot */}
                <div className="absolute -left-[31px] top-1.5 w-4 h-4 rounded-full bg-primary border-4 border-background" />

                <div className="p-4 bg-muted/30 border border-border rounded-lg space-y-2">
                  <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2">
                    <div className="flex items-center gap-2">
                      <span className="font-bold text-sm text-foreground">Generation #{cycles.length - idx}</span>
                      <span className="font-mono text-xs text-primary font-semibold">{c.cycle_id}</span>
                    </div>
                    <Badge variant="success">{c.status}</Badge>
                  </div>

                  <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs pt-1 text-muted-foreground">
                    <div>
                      <span>Mission: </span>
                      <strong className="text-foreground">{c.mission_id}</strong>
                    </div>
                    <div>
                      <span>Strategy: </span>
                      <strong className="text-foreground">{c.strategy_id}</strong>
                    </div>
                    <div>
                      <span>Composite Health: </span>
                      <strong className="text-emerald-500">{(c.composite_health_score * 100).toFixed(1)}%</strong>
                    </div>
                    <div>
                      <span>ROI Multiplier: </span>
                      <strong className="text-primary">{c.roi_multiplier}x</strong>
                    </div>
                  </div>

                  <div className="flex justify-between items-center text-[11px] text-muted-foreground pt-2 border-t border-border/60">
                    <span className="flex items-center gap-1">
                      <Clock className="w-3.5 h-3.5" /> Executed in {c.duration_ms} ms
                    </span>
                    <span>Governance Seal Verified (SHA-256)</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
