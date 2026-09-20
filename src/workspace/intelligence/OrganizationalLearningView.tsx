import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const OrganizationalLearningView: React.FC = () => {
  const departments = [
    {
      id: 'fin_ops',
      name: 'Financial Operations Department',
      missions: 1420,
      successRate: 0.992,
      specialization: 0.94,
      throughput: 58.0,
      bottleneck: 0.04,
      reviewQuality: 0.98,
      capabilities: ['Invoice Extraction', 'Tax Reconciliation', 'Receipt Parsing'],
    },
    {
      id: 'legal_qa',
      name: 'Legal & Compliance Department',
      missions: 680,
      successRate: 0.978,
      specialization: 0.91,
      throughput: 22.0,
      bottleneck: 0.12,
      reviewQuality: 0.97,
      capabilities: ['Contract Review', 'Clause Indemnity', 'NDA Redaction'],
    },
    {
      id: 'health_rec',
      name: 'Healthcare Records Department',
      missions: 410,
      successRate: 0.985,
      specialization: 0.88,
      throughput: 30.0,
      bottleneck: 0.09,
      reviewQuality: 0.95,
      capabilities: ['HIPAA Redaction', 'Clinical Lab Panels', 'Intake Forms'],
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Organizational Learning Curves</h1>
            <Badge variant="intelligence" size="sm">Pillar 10</Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Departmental expertise accumulation, throughput specialization indices, and routing performance benchmarks.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant="success" size="md">
            Mean Success: 98.5%
          </Badge>
        </div>
      </div>

      {/* Departments Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {departments.map((d) => (
          <Card key={d.id} className="p-5 flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="font-mono text-xs text-primary font-semibold">{d.id}</span>
                <Badge variant="outline" size="sm">Spec: {(d.specialization * 100).toFixed(0)}%</Badge>
              </div>

              <h3 className="text-sm font-semibold text-foreground mb-1">{d.name}</h3>
              <div className="text-xs text-muted-foreground mb-4">Total Missions: <strong className="text-foreground">{d.missions}</strong></div>

              <div className="grid grid-cols-2 gap-2 p-2.5 rounded bg-muted/20 border border-border/40 mb-4 text-center text-xs">
                <div>
                  <div className="text-[10px] text-muted-foreground">Success Rate</div>
                  <div className="font-mono font-bold text-emerald-400">{(d.successRate * 100).toFixed(1)}%</div>
                </div>
                <div>
                  <div className="text-[10px] text-muted-foreground">Throughput</div>
                  <div className="font-mono font-bold text-foreground">{d.throughput} docs/min</div>
                </div>
                <div>
                  <div className="text-[10px] text-muted-foreground">Bottleneck Score</div>
                  <div className="font-mono font-bold text-emerald-400">{(d.bottleneck * 100).toFixed(1)}%</div>
                </div>
                <div>
                  <div className="text-[10px] text-muted-foreground">Review Quality</div>
                  <div className="font-mono font-bold text-primary">{(d.reviewQuality * 100).toFixed(1)}%</div>
                </div>
              </div>

              <div className="text-[11px] font-semibold text-muted-foreground mb-1.5">Specialized Capabilities</div>
              <div className="flex flex-wrap gap-1">
                {d.capabilities.map((c) => (
                  <span key={c} className="text-[10px] px-2 py-0.5 rounded bg-muted text-muted-foreground">
                    {c}
                  </span>
                ))}
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
