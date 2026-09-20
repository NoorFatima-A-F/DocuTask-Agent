import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const ContinuousOptimizationTimelineView: React.FC = () => {
  const steps = [
    {
      time: '14:20:00',
      stage: 'DEPLOYED',
      title: 'Planner Kernel Updated to v2.1.0',
      description: 'Activated candidate strategy for Invoice domain with 22.4% latency drop.',
      evidence: '0x8f2a...c31b',
      status: 'success',
    },
    {
      time: '14:18:45',
      stage: 'EVIDENCE_VERIFIED',
      title: 'A/B Experiment #14 Concluded (p = 0.0004)',
      description: 'Welch t-test confirmed rejection of null hypothesis with t = -4.82 and Cohen d = -1.45.',
      evidence: '0x3c7e...b44a',
      status: 'success',
    },
    {
      time: '14:15:10',
      stage: 'EXPERIMENT_RUNNING',
      title: 'Initiated A/B Trial: Parallel vs Sequential DAG',
      description: 'Dispatched 20 shadow missions comparing Control (v2.0.4) against Candidate (v2.1.0).',
      evidence: '0x991a...fe82',
      status: 'info',
    },
    {
      time: '14:12:00',
      stage: 'HYPOTHESIS_FORMULATED',
      title: 'Synthesized Hypothesis: hyp_inv_parallel',
      description: 'Identified 240ms serialization overhead during OCR & table extraction.',
      evidence: '0x661d...009a',
      status: 'info',
    },
    {
      time: '14:00:00',
      stage: 'EXPERIENCE_EXTRACTED',
      title: 'Logged 50 Operational Experiences for Invoices',
      description: 'Compiled latency profiles, cost metrics, and error traces into append-only ledger.',
      evidence: '0x1122...3344',
      status: 'info',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Continuous Optimization Lifecycle Timeline</h1>
            <Badge variant="intelligence" size="sm">Pillar 11</Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Complete audit trail of every scientific transition: Observation &rarr; Hypothesis &rarr; Experiment &rarr; Verification &rarr; Deployment.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant="success" size="md">
            Audit Immutable
          </Badge>
        </div>
      </div>

      {/* Timeline */}
      <Card className="p-5 border-border/60">
        <div className="space-y-6 relative before:absolute before:inset-0 before:left-3.5 before:w-0.5 before:bg-border/60">
          {steps.map((step, idx) => (
            <div key={idx} className="relative flex items-start gap-4 pl-8">
              <div className="absolute left-2.5 top-1.5 w-2.5 h-2.5 rounded-full bg-primary ring-4 ring-background" />
              <div className="flex-1 p-3.5 rounded-lg border border-border/40 bg-muted/10">
                <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-1 mb-1">
                  <div className="flex items-center gap-2">
                    <span className="font-semibold text-xs text-foreground">{step.title}</span>
                    <Badge variant={step.status === 'success' ? 'success' : 'outline'} size="sm">
                      {step.stage}
                    </Badge>
                  </div>
                  <span className="text-[11px] font-mono text-muted-foreground">{step.time}</span>
                </div>
                <p className="text-xs text-muted-foreground mb-2">{step.description}</p>
                <div className="text-[11px] font-mono text-muted-foreground flex items-center gap-2">
                  <span>Merkle Root:</span>
                  <span className="text-emerald-400">{step.evidence}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
};
