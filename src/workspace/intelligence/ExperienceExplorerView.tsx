import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const ExperienceExplorerView: React.FC = () => {
  const [selectedDomain, setSelectedDomain] = useState<string>('ALL');

  const experiences = [
    {
      id: 'exp_001_inv',
      missionId: 'msn_1001',
      domain: 'Invoice',
      task: 'Extraction & Compliance',
      latency: 940.5,
      cost: 0.0084,
      confidence: 0.978,
      retries: 0,
      evidenceRoot: '0x8f2a...c31b',
      status: 'SUCCESS',
      plannerVer: 'v2.1.0',
      timestamp: '2 mins ago',
    },
    {
      id: 'exp_002_con',
      missionId: 'msn_1002',
      domain: 'Contract',
      task: 'Clause & Indemnity Audit',
      latency: 2150.0,
      cost: 0.0342,
      confidence: 0.942,
      retries: 0,
      evidenceRoot: '0x3c7e...b44a',
      status: 'SUCCESS',
      plannerVer: 'v2.0.4',
      timestamp: '6 mins ago',
    },
    {
      id: 'exp_003_med',
      missionId: 'msn_1003',
      domain: 'Medical',
      task: 'HIPAA & Clinical Trials',
      latency: 1820.0,
      cost: 0.0265,
      confidence: 0.965,
      retries: 1,
      evidenceRoot: '0x991a...fe82',
      status: 'RECOVERED',
      plannerVer: 'v2.0.4',
      timestamp: '12 mins ago',
    },
    {
      id: 'exp_004_inv',
      missionId: 'msn_1004',
      domain: 'Invoice',
      task: 'Multi-Line Item Tax Extraction',
      latency: 1020.0,
      cost: 0.0092,
      confidence: 0.985,
      retries: 0,
      evidenceRoot: '0x661d...009a',
      status: 'SUCCESS',
      plannerVer: 'v2.1.0',
      timestamp: '18 mins ago',
    },
  ];

  const filtered = selectedDomain === 'ALL' ? experiences : experiences.filter((e) => e.domain.toUpperCase() === selectedDomain);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Experience Intelligence Explorer</h1>
            <Badge variant="intelligence" size="sm">Pillar 1</Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Immutable repository of operational experiences with cryptographic hash chaining and Merkle root evidence linkage.
          </p>
        </div>
        <div className="flex items-center gap-2">
          {['ALL', 'INVOICE', 'CONTRACT', 'MEDICAL'].map((dom) => (
            <button
              key={dom}
              onClick={() => setSelectedDomain(dom)}
              className={`text-xs px-2.5 py-1 rounded transition-colors font-medium ${
                selectedDomain === dom ? 'bg-primary text-primary-foreground' : 'bg-muted text-muted-foreground hover:bg-muted/80'
              }`}
            >
              {dom}
            </button>
          ))}
        </div>
      </div>

      {/* Experience Table */}
      <Card className="p-0 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="border-b border-border/40 bg-muted/20 font-semibold text-muted-foreground">
                <th className="p-3">Experience ID</th>
                <th className="p-3">Mission ID</th>
                <th className="p-3">Domain & Task</th>
                <th className="p-3">Latency (ms)</th>
                <th className="p-3">Cost ($)</th>
                <th className="p-3">Confidence</th>
                <th className="p-3">Evidence Merkle Root</th>
                <th className="p-3">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border/20">
              {filtered.map((exp) => (
                <tr key={exp.id} className="hover:bg-muted/10 transition-colors">
                  <td className="p-3 font-mono text-primary font-semibold">{exp.id}</td>
                  <td className="p-3 font-mono text-foreground">{exp.missionId}</td>
                  <td className="p-3">
                    <div className="font-medium text-foreground">{exp.domain}</div>
                    <div className="text-[11px] text-muted-foreground">{exp.task}</div>
                  </td>
                  <td className="p-3 font-mono">{exp.latency}</td>
                  <td className="p-3 font-mono">${exp.cost.toFixed(4)}</td>
                  <td className="p-3 font-mono">
                    <span className="text-emerald-400">{(exp.confidence * 100).toFixed(1)}%</span>
                  </td>
                  <td className="p-3 font-mono text-xs text-muted-foreground">{exp.evidenceRoot}</td>
                  <td className="p-3">
                    <Badge variant={exp.status === 'SUCCESS' ? 'success' : 'warning'} size="sm">
                      {exp.status}
                    </Badge>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
};
