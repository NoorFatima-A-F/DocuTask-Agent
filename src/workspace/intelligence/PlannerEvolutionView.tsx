import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const PlannerEvolutionView: React.FC = () => {
  const [activeVersion, setActiveVersion] = useState<string>('v2.1.0');

  const versions = [
    {
      versionId: 'v2.1.0',
      parent: 'v2.0.4',
      status: 'ACTIVE',
      createdAt: 'Today, 14:20',
      justification: 'Promoted after A/B trial #14 proved 22.4% latency drop with p < 0.001.',
      params: {
        explorationWeight: 0.12,
        latencyPenaltyFactor: 0.48,
        costPenaltyFactor: 0.30,
        confidenceThreshold: 0.92,
        maxDagDepth: 6,
        defaultOcrEngine: 'tesseract_v2_optimized',
      },
    },
    {
      versionId: 'v2.0.4',
      parent: 'v1.0.0',
      status: 'ARCHIVED',
      createdAt: 'Yesterday, 18:00',
      justification: 'Contract invariant validation node integration.',
      params: {
        explorationWeight: 0.18,
        latencyPenaltyFactor: 0.42,
        costPenaltyFactor: 0.30,
        confidenceThreshold: 0.90,
        maxDagDepth: 5,
        defaultOcrEngine: 'tesseract_v2',
      },
    },
    {
      versionId: 'v1.0.0',
      parent: 'None',
      status: 'BASELINE',
      createdAt: 'Initial Release',
      justification: 'Initial factory configuration.',
      params: {
        explorationWeight: 0.25,
        latencyPenaltyFactor: 0.35,
        costPenaltyFactor: 0.30,
        confidenceThreshold: 0.88,
        maxDagDepth: 5,
        defaultOcrEngine: 'tesseract_v2',
      },
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Scientific Planner Evolution</h1>
            <Badge variant="intelligence" size="sm">Pillar 3</Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Auditable progression of versioned planner hyperparameters with 1-click deterministic rollback.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant="success" size="md">
            Active: {activeVersion}
          </Badge>
        </div>
      </div>

      {/* Version Progression Tree */}
      <div className="space-y-4">
        {versions.map((ver) => (
          <Card key={ver.versionId} className={`p-5 border-border/60 ${ver.status === 'ACTIVE' ? 'ring-1 ring-primary/40 bg-primary/5' : ''}`}>
            <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-3 mb-3">
              <div>
                <div className="flex items-center gap-2">
                  <span className="font-mono text-base font-bold text-foreground">{ver.versionId}</span>
                  <Badge variant={ver.status === 'ACTIVE' ? 'success' : 'outline'} size="sm">
                    {ver.status}
                  </Badge>
                  <span className="text-xs text-muted-foreground">Parent: <strong className="font-mono">{ver.parent}</strong></span>
                </div>
                <p className="text-xs text-muted-foreground mt-1">{ver.justification}</p>
              </div>
              <div className="flex items-center gap-2">
                {ver.status !== 'ACTIVE' && (
                  <button
                    onClick={() => setActiveVersion(ver.versionId)}
                    className="text-xs px-3 py-1.5 rounded bg-muted hover:bg-muted/80 text-foreground font-medium transition-colors"
                  >
                    Rollback to this Version
                  </button>
                )}
              </div>
            </div>

            {/* Hyperparameters */}
            <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2 text-center text-xs">
              <div className="p-2 rounded bg-muted/20 border border-border/40">
                <div className="text-[10px] text-muted-foreground">Exploration Weight</div>
                <div className="font-mono font-bold text-foreground mt-0.5">{ver.params.explorationWeight}</div>
              </div>
              <div className="p-2 rounded bg-muted/20 border border-border/40">
                <div className="text-[10px] text-muted-foreground">Latency Penalty</div>
                <div className="font-mono font-bold text-foreground mt-0.5">{ver.params.latencyPenaltyFactor}</div>
              </div>
              <div className="p-2 rounded bg-muted/20 border border-border/40">
                <div className="text-[10px] text-muted-foreground">Cost Penalty</div>
                <div className="font-mono font-bold text-foreground mt-0.5">{ver.params.costPenaltyFactor}</div>
              </div>
              <div className="p-2 rounded bg-muted/20 border border-border/40">
                <div className="text-[10px] text-muted-foreground">Conf Threshold</div>
                <div className="font-mono font-bold text-emerald-400 mt-0.5">{ver.params.confidenceThreshold}</div>
              </div>
              <div className="p-2 rounded bg-muted/20 border border-border/40">
                <div className="text-[10px] text-muted-foreground">Max DAG Depth</div>
                <div className="font-mono font-bold text-foreground mt-0.5">{ver.params.maxDagDepth}</div>
              </div>
              <div className="p-2 rounded bg-muted/20 border border-border/40">
                <div className="text-[10px] text-muted-foreground">Default OCR Engine</div>
                <div className="font-mono text-[11px] text-primary truncate mt-0.5">{ver.params.defaultOcrEngine}</div>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
