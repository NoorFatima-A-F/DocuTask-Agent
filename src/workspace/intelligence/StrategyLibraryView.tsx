import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const StrategyLibraryView: React.FC = () => {
  const [promotedOnly, setPromotedOnly] = useState<boolean>(false);

  const strategies = [
    {
      id: 'strat_inv_01',
      name: 'Optimized Invoice Parallel Fan-Out Strategy',
      domain: 'Invoice',
      version: '2.1.0',
      isPromoted: true,
      successRate: 0.994,
      meanLatency: 910.4,
      meanCost: 0.0078,
      sampleSize: 420,
      tools: ['tesseract_v2', 'schema_validator', 'gemini-1.5-flash'],
      failureModes: ['Low-resolution skew on line item headers'],
    },
    {
      id: 'strat_con_01',
      name: 'High-Fidelity Legal Contract Multi-Pass Strategy',
      domain: 'Contract',
      version: '1.4.0',
      isPromoted: true,
      successRate: 0.982,
      meanLatency: 2150.0,
      meanCost: 0.0320,
      sampleSize: 180,
      tools: ['pdfplumber_advanced', 'clause_extractor', 'gemini-1.5-pro'],
      failureModes: ['Unstandardized indemnification phrasing'],
    },
    {
      id: 'strat_med_01',
      name: 'Clinical Record & HIPAA Redaction Fast-Track',
      domain: 'Medical',
      version: '1.2.0',
      isPromoted: false,
      successRate: 0.965,
      meanLatency: 1750.0,
      meanCost: 0.0240,
      sampleSize: 95,
      tools: ['vision_multimodal_ocr', 'hipaa_guard', 'gemini-1.5-pro'],
      failureModes: ['Handwritten doctor signatures'],
    },
  ];

  const displayed = promotedOnly ? strategies.filter((s) => s.isPromoted) : strategies;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Strategy Mining Library</h1>
            <Badge variant="intelligence" size="sm">Pillar 2</Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Empirically mined and validated execution strategies with statistical performance profiles and failure mode catalog.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setPromotedOnly(!promotedOnly)}
            className={`text-xs px-3 py-1.5 rounded transition-colors font-medium ${
              promotedOnly ? 'bg-primary text-primary-foreground' : 'bg-muted text-muted-foreground'
            }`}
          >
            {promotedOnly ? 'Showing Promoted Only' : 'Show All Strategies'}
          </button>
        </div>
      </div>

      {/* Strategies Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {displayed.map((strat) => (
          <Card key={strat.id} className="p-5 flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between gap-2 mb-2">
                <span className="font-mono text-xs text-primary font-semibold">{strat.id}</span>
                <div className="flex items-center gap-1.5">
                  <Badge variant="outline" size="sm" className="font-mono">{strat.version}</Badge>
                  {strat.isPromoted && <Badge variant="success" size="sm">PROMOTED</Badge>}
                </div>
              </div>

              <h3 className="text-sm font-semibold text-foreground mb-2">{strat.name}</h3>
              <p className="text-xs text-muted-foreground mb-4">Domain: <strong className="text-foreground">{strat.domain}</strong></p>

              <div className="grid grid-cols-3 gap-2 p-2.5 rounded bg-muted/20 border border-border/40 mb-4 text-center">
                <div>
                  <div className="text-[10px] text-muted-foreground">Success Rate</div>
                  <div className="text-xs font-mono font-bold text-emerald-400">{(strat.successRate * 100).toFixed(1)}%</div>
                </div>
                <div>
                  <div className="text-[10px] text-muted-foreground">Mean Latency</div>
                  <div className="text-xs font-mono font-bold text-foreground">{strat.meanLatency.toFixed(0)} ms</div>
                </div>
                <div>
                  <div className="text-[10px] text-muted-foreground">Mean Cost</div>
                  <div className="text-xs font-mono font-bold text-foreground">${strat.meanCost.toFixed(4)}</div>
                </div>
              </div>

              <div className="mb-4">
                <div className="text-[11px] font-semibold text-muted-foreground mb-1">Recommended Tools</div>
                <div className="flex flex-wrap gap-1">
                  {strat.tools.map((t) => (
                    <span key={t} className="text-[10px] px-2 py-0.5 rounded bg-muted font-mono text-muted-foreground">
                      {t}
                    </span>
                  ))}
                </div>
              </div>
            </div>

            <div className="border-t border-border/40 pt-3 flex items-center justify-between text-xs text-muted-foreground">
              <span>Samples: {strat.sampleSize} runs</span>
              <button className="text-primary hover:underline font-medium">Inspect Lineage &rarr;</button>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
