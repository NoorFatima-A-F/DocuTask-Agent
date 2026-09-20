import React, { useState, useEffect } from 'react';
import { Activity, Cpu } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { knowledgeApiClient } from '../../services/knowledgeApiClient';
import { KnowledgeQualityReport } from '../../types/knowledge';

export const KnowledgeQualityCenter: React.FC = () => {
  const [report, setReport] = useState<KnowledgeQualityReport | null>(null);

  const loadReport = async () => {
    const data = await knowledgeApiClient.getQualityReport();
    setReport(data);
  };

  useEffect(() => {
    loadReport();
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-slate-100 flex items-center gap-2">
            <Activity className="w-7 h-7 text-emerald-400" />
            Knowledge Quality & Conflict Intelligence
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Detect policy discrepancies, outdated versions, duplicate documents, and evaluate reliability index.
          </p>
        </div>
        <Button variant="intelligence" onClick={() => knowledgeApiClient.runOptimization()}>
          <span className="flex items-center gap-2">
            <Cpu className="w-4 h-4" />
            Auto-Reconcile Conflicts
          </span>
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card className="p-4 bg-slate-900/60 border-slate-800">
          <span className="text-xs text-slate-400 uppercase font-semibold">Freshness Score</span>
          <p className="text-2xl font-bold text-emerald-400 mt-1">{((report?.freshness_index || 0.96) * 100).toFixed(0)}%</p>
        </Card>
        <Card className="p-4 bg-slate-900/60 border-slate-800">
          <span className="text-xs text-slate-400 uppercase font-semibold">Reliability Index</span>
          <p className="text-2xl font-bold text-cyan-400 mt-1">{((report?.avg_reliability_score || 0.95) * 100).toFixed(0)}%</p>
        </Card>
        <Card className="p-4 bg-slate-900/60 border-slate-800">
          <span className="text-xs text-slate-400 uppercase font-semibold">Active Conflicts</span>
          <p className="text-2xl font-bold text-slate-100 mt-1">{report?.active_conflicts.length || 0}</p>
        </Card>
      </div>

      <Card className="p-5 bg-slate-900/60 border-slate-800 space-y-4">
        <h2 className="text-base font-semibold text-slate-200">Policy Conflict Audit Log</h2>
        {report?.active_conflicts.length === 0 ? (
          <div className="p-4 text-center text-sm text-emerald-400 bg-emerald-950/20 border border-emerald-500/30 rounded-lg">
            ✓ Zero policy conflicts or version discrepancies detected.
          </div>
        ) : (
          report?.active_conflicts.map((conf) => (
            <div key={conf.id} className="p-4 rounded-lg bg-amber-950/20 border border-amber-500/30 space-y-2">
              <div className="flex justify-between items-center">
                <Badge variant="warning">{conf.severity} SEVERITY</Badge>
                <span className="text-xs text-slate-400 font-mono">{conf.id}</span>
              </div>
              <p className="text-sm font-semibold text-amber-200">{conf.conflict_topic}</p>
              <p className="text-xs text-slate-300">{conf.recommended_resolution}</p>
            </div>
          ))
        )}
      </Card>
    </div>
  );
};
