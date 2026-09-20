import React, { useState, useEffect } from 'react';
import {
  Award,
  CheckCircle2,
  AlertOctagon,
  Shield,
  Zap,
  Target,
  RefreshCw,
} from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { AIOperationsApiClient } from '../../services/aiOperationsApiClient';
import { EvaluationResult } from '../../types/aiOperations';

export const EvaluationCenter: React.FC = () => {
  const [evaluations, setEvaluations] = useState<EvaluationResult[]>([]);
  const [selectedEval, setSelectedEval] = useState<EvaluationResult | null>(null);
  const [loading, setLoading] = useState(true);

  const loadEvaluations = async () => {
    try {
      setLoading(true);
      const data = await AIOperationsApiClient.getEvaluationResults(50);
      setEvaluations(data);
      if (data.length > 0 && !selectedEval) {
        setSelectedEval(data[0] || null);
      }
    } catch (err) {
      console.error('Failed to load evaluation results:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadEvaluations();
  }, []);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between bg-slate-900/60 p-5 rounded-2xl border border-slate-800 backdrop-blur-md">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-emerald-500/10 rounded-xl border border-emerald-500/20">
            <Award className="w-6 h-6 text-emerald-400" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-white">Evaluation & LLM Judge Center</h1>
            <p className="text-xs text-slate-400">Continuous scoring of accuracy, grounding, safety alignment, and tool efficiency</p>
          </div>
        </div>
        <Button variant="outline" onClick={loadEvaluations} disabled={loading}>
          <span className="flex items-center gap-2">
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            Refresh
          </span>
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Eval History (4 cols) */}
        <div className="lg:col-span-4 space-y-3">
          <h2 className="text-xs font-semibold text-slate-400 uppercase tracking-wider px-1">Evaluation Benchmarks</h2>
          <div className="space-y-2 max-h-[600px] overflow-y-auto pr-1">
            {evaluations.map((ev) => (
              <Card
                key={ev.eval_id}
                className={`p-3.5 cursor-pointer transition-all border ${
                  selectedEval?.eval_id === ev.eval_id
                    ? 'bg-emerald-950/30 border-emerald-500/50 shadow-md shadow-emerald-950/20'
                    : 'bg-slate-900/40 border-slate-800/80 hover:bg-slate-800/40'
                }`}
                onClick={() => setSelectedEval(ev)}
              >
                <div className="flex items-center justify-between">
                  <span className="font-semibold text-white text-xs">{ev.agent_id}</span>
                  <Badge variant={ev.composite_quality_score >= 0.85 ? 'success' : 'warning'}>
                    {(ev.composite_quality_score * 100).toFixed(1)}% Quality
                  </Badge>
                </div>
                <div className="flex items-center justify-between mt-2.5 text-[11px] text-slate-400">
                  <span className="text-emerald-400">Grounding: {(ev.grounding_score * 100).toFixed(0)}%</span>
                  <span className="text-amber-400">Hallucination: {(ev.hallucination_index * 100).toFixed(1)}%</span>
                </div>
              </Card>
            ))}
          </div>
        </div>

        {/* Selected Eval Details (8 cols) */}
        <div className="lg:col-span-8 space-y-4">
          {selectedEval ? (
            <>
              <Card className="p-6 bg-slate-900/50 border-slate-800">
                <div className="flex items-start justify-between border-b border-slate-800 pb-4">
                  <div>
                    <h2 className="text-lg font-bold text-white">Evaluation Scorecard: {selectedEval.agent_id}</h2>
                    <p className="text-xs text-slate-400 font-mono mt-0.5">Eval ID: {selectedEval.eval_id}</p>
                  </div>
                  <div className="text-right">
                    <span className="text-2xl font-bold text-white">{(selectedEval.composite_quality_score * 100).toFixed(1)}%</span>
                    <p className="text-[11px] text-slate-400">Composite Score</p>
                  </div>
                </div>

                {/* Granular Metrics Grid */}
                <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 my-5">
                  <div className="p-3 bg-slate-950/50 rounded-xl border border-slate-800/60">
                    <span className="text-xs text-slate-400 flex items-center gap-1"><Target className="w-3.5 h-3.5 text-indigo-400" /> Task Success</span>
                    <p className="text-lg font-bold text-white mt-1">{(selectedEval.task_success_score * 100).toFixed(1)}%</p>
                  </div>
                  <div className="p-3 bg-slate-950/50 rounded-xl border border-slate-800/60">
                    <span className="text-xs text-slate-400 flex items-center gap-1"><CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" /> Grounding</span>
                    <p className="text-lg font-bold text-white mt-1">{(selectedEval.grounding_score * 100).toFixed(1)}%</p>
                  </div>
                  <div className="p-3 bg-slate-950/50 rounded-xl border border-slate-800/60">
                    <span className="text-xs text-slate-400 flex items-center gap-1"><AlertOctagon className="w-3.5 h-3.5 text-rose-400" /> Hallucination</span>
                    <p className="text-lg font-bold text-rose-300 mt-1">{(selectedEval.hallucination_index * 100).toFixed(1)}%</p>
                  </div>
                  <div className="p-3 bg-slate-950/50 rounded-xl border border-slate-800/60">
                    <span className="text-xs text-slate-400 flex items-center gap-1"><Shield className="w-3.5 h-3.5 text-cyan-400" /> Safety Alignment</span>
                    <p className="text-lg font-bold text-white mt-1">{(selectedEval.safety_score * 100).toFixed(1)}%</p>
                  </div>
                  <div className="p-3 bg-slate-950/50 rounded-xl border border-slate-800/60">
                    <span className="text-xs text-slate-400 flex items-center gap-1"><Zap className="w-3.5 h-3.5 text-amber-400" /> Tool Efficiency</span>
                    <p className="text-lg font-bold text-white mt-1">{(selectedEval.tool_efficiency_score * 100).toFixed(1)}%</p>
                  </div>
                  <div className="p-3 bg-slate-950/50 rounded-xl border border-slate-800/60">
                    <span className="text-xs text-slate-400 flex items-center gap-1"><Award className="w-3.5 h-3.5 text-indigo-400" /> LLM Judge</span>
                    <p className="text-lg font-bold text-white mt-1">{(selectedEval.llm_judge_score * 100).toFixed(1)}%</p>
                  </div>
                </div>

                {/* Judge Critique */}
                {selectedEval.judge_critique && (
                  <div className="p-4 bg-slate-950/60 rounded-xl border border-slate-800/80">
                    <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1 flex items-center gap-1.5">
                      <Award className="w-3.5 h-3.5 text-indigo-400" /> Automated Judge Critique
                    </h4>
                    <p className="text-xs text-slate-300 leading-relaxed">{selectedEval.judge_critique}</p>
                  </div>
                )}
              </Card>
            </>
          ) : (
            <Card className="p-8 text-center text-slate-400 bg-slate-900/40 border-slate-800">
              <Award className="w-8 h-8 text-slate-600 mx-auto mb-2" />
              <p>Select an evaluation result to view the comprehensive score breakdown.</p>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
};
