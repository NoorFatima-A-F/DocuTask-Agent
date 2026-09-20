import React, { useState, useEffect } from 'react';
import { Target, RefreshCw } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { cognitiveApiClient } from '../../services/cognitiveApiClient';
import { DecisionRecord } from '../../types/cognitive';

export const DecisionIntelligenceExplorer: React.FC = () => {
  const [decisions, setDecisions] = useState<DecisionRecord[]>([]);

  const loadData = async () => {
    const data = await cognitiveApiClient.listDecisions();
    setDecisions(data);
  };

  useEffect(() => {
    loadData();
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-slate-100 flex items-center gap-2">
            <Target className="w-7 h-7 text-indigo-400" />
            Enterprise Decision Intelligence Explorer
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Tracks autonomous decision objects, reasoning rationales, alternatives, and verifies expected vs. actual outcomes.
          </p>
        </div>
        <Button variant="outline" onClick={loadData}>
          <span className="flex items-center gap-2">
            <RefreshCw className="w-4 h-4" />
            Refresh
          </span>
        </Button>
      </div>

      <div className="space-y-4">
        {decisions.map((dec) => (
          <Card key={dec.id} className="p-5 bg-slate-900/60 border-slate-800 space-y-4">
            <div className="flex justify-between items-start">
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <Badge variant="outline" className="text-indigo-400 border-indigo-500/30">
                    Confidence: {(dec.confidence_score * 100).toFixed(0)}%
                  </Badge>
                  <Badge variant={dec.outcome_matched ? 'success' : 'warning'}>
                    {dec.outcome_matched ? 'Outcome Calibrated & Matched' : 'Pending Verification'}
                  </Badge>
                </div>
                <h3 className="text-lg font-semibold text-slate-200">{dec.decision_topic}</h3>
              </div>
              <span className="text-xs font-mono text-slate-400">{dec.id}</span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
              <div className="p-3 bg-slate-800/40 rounded border border-slate-700/60 space-y-1">
                <span className="font-semibold text-slate-400 uppercase">Chosen Action:</span>
                <p className="text-slate-200 font-medium">{dec.chosen_action}</p>
                <p className="text-slate-400 mt-2">Rationale: {dec.reasoning_rationale}</p>
              </div>
              <div className="p-3 bg-slate-800/40 rounded border border-slate-700/60 space-y-1">
                <span className="font-semibold text-slate-400 uppercase">Expected vs Actual:</span>
                <p className="text-emerald-400">Expected: {JSON.stringify(dec.expected_outcome)}</p>
                <p className="text-cyan-400">Actual: {JSON.stringify(dec.actual_outcome || 'Observing live metrics...')}</p>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
