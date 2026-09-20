import React from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import {
  Globe,
} from 'lucide-react';

interface OKRItem {
  id: string;
  objective: string;
  keyResults: { text: string; progressPct: number; status: string }[];
  horizon: string;
  owner: string;
}

export const LongTermPlanningCenter: React.FC = () => {
  const okrs: OKRItem[] = [
    {
      id: 'okr-01',
      objective: 'Achieve Sub-150ms Processing for 1M+ Daily Document Workloads',
      horizon: '3-Year Horizon (2026-2029)',
      owner: 'Autonomous Execution Swarm Federation',
      keyResults: [
        { text: 'Deploy zero-copy tensor caching across 100% of standard corporate schemas', progressPct: 88, status: 'ON_TRACK' },
        { text: 'Scale autonomous triadic strike teams across 12 distributed datacenters', progressPct: 65, status: 'IN_PROGRESS' },
        { text: 'Reduce end-to-end P99 tail latency below 200ms', progressPct: 74, status: 'ON_TRACK' },
      ],
    },
    {
      id: 'okr-02',
      objective: 'Establish Zero-Downtime Autonomous Cognitive Governance',
      horizon: '3-Year Horizon (2026-2029)',
      owner: 'Executive Strategy & Governance Oracle',
      keyResults: [
        { text: 'Attain 100% cryptographic SHA-256 auditability on all autonomous mutations', progressPct: 100, status: 'COMPLETED' },
        { text: 'Implement automated micro-rollback checkpoints with sub-5ms recovery', progressPct: 92, status: 'ON_TRACK' },
        { text: 'Integrate continuous multi-swarm Nash bargaining for resource fairness', progressPct: 85, status: 'ON_TRACK' },
      ],
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
            <Globe className="w-6 h-6 text-indigo-500" />
            Long-Term Enterprise Strategic Vision & OKR Center
          </h2>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            Phase 13.11 — Multi-year organizational objectives, high-level OKR progress tracking, and cognitive maturity index.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant="intelligence" size="md">
            Cognitive Maturity: Level 5 (Autonomous CSO)
          </Badge>
        </div>
      </div>

      {/* High-Level OKRs */}
      <div className="grid grid-cols-1 gap-6">
        {okrs.map((okr) => (
          <Card key={okr.id} className="p-6 border-l-4 border-l-indigo-600 hover:shadow-md transition-shadow">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 pb-4 border-b border-gray-100 dark:border-gray-800">
              <div>
                <div className="flex items-center gap-2">
                  <span className="font-mono text-xs text-indigo-600 dark:text-indigo-400 font-semibold">{okr.id}</span>
                  <Badge variant="outline" size="sm">
                    {okr.horizon}
                  </Badge>
                </div>
                <h3 className="text-lg font-bold text-gray-900 dark:text-white mt-1">{okr.objective}</h3>
                <span className="text-xs text-gray-400">Custodian: {okr.owner}</span>
              </div>
            </div>

            <div className="mt-4 space-y-3 text-xs">
              <span className="text-gray-400 font-semibold uppercase tracking-wider block">Key Deliverables & Progress:</span>
              {okr.keyResults.map((kr, idx) => (
                <div key={idx} className="p-3 bg-gray-50 dark:bg-gray-900/40 rounded-lg border border-gray-100 dark:border-gray-800 space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="font-medium text-gray-800 dark:text-gray-200">{kr.text}</span>
                    <Badge variant={kr.status === 'COMPLETED' ? 'success' : 'intelligence'} size="sm">
                      {kr.progressPct}%
                    </Badge>
                  </div>
                  <div className="w-full bg-gray-200 dark:bg-gray-800 rounded-full h-2 overflow-hidden">
                    <div
                      className="bg-indigo-600 h-2 rounded-full transition-all duration-500"
                      style={{ width: `${kr.progressPct}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
