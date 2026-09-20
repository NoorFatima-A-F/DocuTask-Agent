import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const HypothesisLaboratoryView: React.FC = () => {
  const [activeTab, setActiveTab] = useState<string>('ALL');

  const hypotheses = [
    {
      id: 'hyp_inv_parallel',
      title: 'Parallel Sub-DAG Fan-Out for Invoices',
      category: 'LATENCY_REDUCTION',
      domain: 'Invoice',
      premise: 'Sequential OCR and table extraction accounts for 940ms latency.',
      action: 'Execute table parsing and metadata extraction concurrently in parallel DAG workers.',
      baseline: '940.0 ms',
      expected: '720.0 ms',
      delta: '-23.4%',
      status: 'VALIDATED',
      pValue: 'p = 0.0004',
    },
    {
      id: 'hyp_con_preval',
      title: 'Pre-validation Invariant Guard for Contracts',
      category: 'RETRY_MINIMIZATION',
      domain: 'Contract',
      premise: 'Contract missions exhibit 0.18 retry rate due to missing liability clauses.',
      action: 'Inject pre-extraction schema invariant validation node in DAG pipeline.',
      baseline: '0.18 retries',
      expected: '0.02 retries',
      delta: '-88.9%',
      status: 'VALIDATED',
      pValue: 'p = 0.0012',
    },
    {
      id: 'hyp_med_flash',
      title: 'Vision-Multimodal Direct Tiering for Medical Docs',
      category: 'COST_OPTIMIZATION',
      domain: 'Medical',
      premise: 'High-clarity medical PDFs can be reliably extracted via multimodal vision directly.',
      action: 'Route clear medical scans directly to vision multimodal pipeline.',
      baseline: '$0.028',
      expected: '$0.016',
      delta: '-42.8%',
      status: 'IN_EXPERIMENT',
      pValue: 'Pending A/B',
    },
    {
      id: 'hyp_receipt_ocr',
      title: 'Heuristic Bounding Box Pre-filter for Receipts',
      category: 'LATENCY_REDUCTION',
      domain: 'Receipt',
      premise: 'Full-page OCR on thermal receipts processes excessive background noise.',
      action: 'Crop active receipt bounding box prior to OCR parse.',
      baseline: '850.0 ms',
      expected: '550.0 ms',
      delta: '-35.3%',
      status: 'PROPOSED',
      pValue: 'Unscheduled',
    },
  ];

  const filtered = activeTab === 'ALL' ? hypotheses : hypotheses.filter((h) => h.status === activeTab);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Hypothesis Formulation Laboratory</h1>
            <Badge variant="intelligence" size="sm">Pillar 4</Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Automated discovery of optimization hypotheses from empirical failure patterns and prediction error bottlenecks.
          </p>
        </div>
        <div className="flex items-center gap-2">
          {['ALL', 'VALIDATED', 'IN_EXPERIMENT', 'PROPOSED'].map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`text-xs px-2.5 py-1 rounded transition-colors font-medium ${
                activeTab === tab ? 'bg-primary text-primary-foreground' : 'bg-muted text-muted-foreground'
              }`}
            >
              {tab}
            </button>
          ))}
        </div>
      </div>

      {/* Hypotheses List */}
      <div className="space-y-3">
        {filtered.map((hyp) => (
          <Card key={hyp.id} className="p-4 border-border/60">
            <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-3 mb-2">
              <div>
                <div className="flex items-center gap-2">
                  <span className="font-mono text-xs text-primary font-semibold">{hyp.id}</span>
                  <Badge variant={hyp.status === 'VALIDATED' ? 'success' : hyp.status === 'IN_EXPERIMENT' ? 'warning' : 'outline'} size="sm">
                    {hyp.status}
                  </Badge>
                  <span className="text-[11px] text-muted-foreground font-mono">[{hyp.domain}]</span>
                </div>
                <h3 className="text-sm font-semibold text-foreground mt-1">{hyp.title}</h3>
              </div>
              <div className="text-right">
                <div className="text-xs font-semibold text-emerald-400">{hyp.pValue}</div>
                <div className="text-[10px] text-muted-foreground">Category: {hyp.category}</div>
              </div>
            </div>

            <p className="text-xs text-muted-foreground mb-3">{hyp.premise}</p>

            <div className="p-2.5 rounded bg-muted/20 border border-border/40 text-xs flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
              <div>
                <strong className="text-foreground">Proposed Action:</strong> <span className="text-muted-foreground">{hyp.action}</span>
              </div>
              <div className="flex items-center gap-3 shrink-0">
                <span className="text-muted-foreground">Baseline: <strong className="text-foreground">{hyp.baseline}</strong></span>
                <span className="text-muted-foreground">&rarr; Expected: <strong className="text-emerald-400">{hyp.expected}</strong> ({hyp.delta})</span>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
