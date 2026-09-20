import React, { useState, useEffect } from 'react';
import {
  AlertTriangle,
  Bug,
  Wrench,
  RefreshCw,
  Clock,
} from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { AIOperationsApiClient } from '../../services/aiOperationsApiClient';
import { FailureAnalysisResult } from '../../types/aiOperations';

export const FailureAnalysisStudio: React.FC = () => {
  const [failures, setFailures] = useState<FailureAnalysisResult[]>([]);
  const [selectedFailure, setSelectedFailure] = useState<FailureAnalysisResult | null>(null);
  const [loading, setLoading] = useState(true);

  const loadFailures = async () => {
    try {
      setLoading(true);
      const data = await AIOperationsApiClient.getFailureDiagnoses(50);
      setFailures(data);
      if (data.length > 0 && !selectedFailure) {
        setSelectedFailure(data[0] || null);
      }
    } catch (err) {
      console.error('Failed to load failure diagnoses:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadFailures();
  }, []);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between bg-slate-900/60 p-5 rounded-2xl border border-slate-800 backdrop-blur-md">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-rose-500/10 rounded-xl border border-rose-500/20">
            <Bug className="w-6 h-6 text-rose-400" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-white">Failure Analysis & Root-Cause Studio</h1>
            <p className="text-xs text-slate-400">Automated failure categorization, critical path bottlenecks, and AI remediation plans</p>
          </div>
        </div>
        <Button variant="outline" onClick={loadFailures} disabled={loading}>
          <span className="flex items-center gap-2">
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            Refresh
          </span>
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Failures List (4 cols) */}
        <div className="lg:col-span-4 space-y-3">
          <h2 className="text-xs font-semibold text-slate-400 uppercase tracking-wider px-1">Diagnosed Failure Incidents</h2>
          <div className="space-y-2 max-h-[600px] overflow-y-auto pr-1">
            {failures.map((f) => (
              <Card
                key={f.analysis_id}
                className={`p-3.5 cursor-pointer transition-all border ${
                  selectedFailure?.analysis_id === f.analysis_id
                    ? 'bg-rose-950/30 border-rose-500/50 shadow-md shadow-rose-950/20'
                    : 'bg-slate-900/40 border-slate-800/80 hover:bg-slate-800/40'
                }`}
                onClick={() => setSelectedFailure(f)}
              >
                <div className="flex items-center justify-between">
                  <span className="font-semibold text-white text-xs">{f.agent_id}</span>
                  <Badge variant="error">{f.category}</Badge>
                </div>
                <p className="text-xs text-slate-400 mt-1 line-clamp-2">{f.root_cause_summary}</p>
                <div className="flex items-center justify-between mt-2.5 text-[11px] text-slate-500 border-t border-slate-800/60 pt-2">
                  <span>Confidence: {(f.confidence * 100).toFixed(0)}%</span>
                  <span>{new Date(f.timestamp).toLocaleTimeString()}</span>
                </div>
              </Card>
            ))}
          </div>
        </div>

        {/* Selected Failure Details (8 cols) */}
        <div className="lg:col-span-8 space-y-4">
          {selectedFailure ? (
            <Card className="p-6 bg-slate-900/50 border-slate-800 space-y-5">
              <div className="flex items-start justify-between border-b border-slate-800 pb-4">
                <div>
                  <div className="flex items-center gap-2">
                    <Badge variant="error">{selectedFailure.category}</Badge>
                    <h2 className="text-base font-bold text-white">{selectedFailure.agent_id}</h2>
                  </div>
                  <p className="text-xs text-slate-400 font-mono mt-0.5">
                    Analysis ID: {selectedFailure.analysis_id} • Trace: {selectedFailure.trace_id}
                  </p>
                </div>
                <Badge variant="intelligence">{(selectedFailure.confidence * 100).toFixed(0)}% Diagnostic Match</Badge>
              </div>

              {/* Root Cause Summary */}
              <div className="p-4 bg-slate-950/80 rounded-xl border border-slate-800">
                <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1 flex items-center gap-1.5">
                  <AlertTriangle className="w-3.5 h-3.5 text-rose-400" /> Root Cause Diagnosis
                </h4>
                <p className="text-sm text-slate-200 leading-relaxed">{selectedFailure.root_cause_summary}</p>
              </div>

              {/* Critical Path Latency Waterfall */}
              <div>
                <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                  <Clock className="w-3.5 h-3.5 text-cyan-400" /> Critical Path Execution Tree
                </h4>
                <div className="space-y-1.5">
                  {selectedFailure.critical_path.map((step, idx) => (
                    <div key={idx} className="p-2.5 bg-slate-950/60 rounded-lg border border-slate-800/80 text-xs text-slate-300 font-mono flex items-center gap-2">
                      <span className="text-slate-500 font-semibold">{idx + 1}.</span>
                      <span>{step}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Suggested Remediation */}
              <div className="p-4 bg-emerald-950/20 border border-emerald-500/20 rounded-xl">
                <h4 className="text-xs font-semibold text-emerald-300 mb-1 flex items-center gap-1.5">
                  <Wrench className="w-3.5 h-3.5 text-emerald-400" /> Recommended AI Remediation
                </h4>
                <p className="text-xs text-slate-200 leading-relaxed">{selectedFailure.suggested_remediation}</p>
              </div>
            </Card>
          ) : (
            <Card className="p-8 text-center text-slate-400 bg-slate-900/40 border-slate-800">
              <Bug className="w-8 h-8 text-slate-600 mx-auto mb-2" />
              <p>Select a failure diagnosis to inspect root causes and remediation recommendations.</p>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
};
