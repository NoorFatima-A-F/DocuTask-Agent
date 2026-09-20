import React from 'react';
import { History } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';

export const KnowledgeEvolution: React.FC = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-100 flex items-center gap-2">
          <History className="w-7 h-7 text-indigo-400" />
          Knowledge Evolution & Lineage Timeline
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          Track document updates, semantic diff history, and agent usage audit trails.
        </p>
      </div>

      <Card className="p-5 bg-slate-900/60 border-slate-800 space-y-4">
        <h2 className="text-base font-semibold text-slate-200 mb-2">Evolution Timeline</h2>
        <div className="space-y-3 border-l-2 border-slate-800 pl-4">
          <div className="relative">
            <Badge variant="info">2026-09-14 02:20</Badge>
            <p className="text-sm font-semibold text-slate-200 mt-1">Global Procurement Policy v2.0 Ingested</p>
            <p className="text-xs text-slate-400">Dual VP threshold updated from $25k to $50k. Reindexed into vector engine.</p>
          </div>
          <div className="relative">
            <Badge variant="success">2026-09-14 01:55</Badge>
            <p className="text-sm font-semibold text-slate-200 mt-1">SAP ERP Gateway Connected</p>
            <p className="text-xs text-slate-400">Ontology graph expanded with 12 new relational dependency edges.</p>
          </div>
        </div>
      </Card>
    </div>
  );
};
