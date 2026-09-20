import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Clock, TrendingUp, ArrowRight, ShieldCheck, CheckCircle2 } from 'lucide-react';

interface TimelineEvent {
  step: number;
  time: string;
  label: string;
  dimension: string;
  scoreBefore: number;
  scoreAfter: number;
  delta: number;
  triggerEvent: string;
  confidenceInterval: string;
}

const timelineData: TimelineEvent[] = [
  {
    step: 1,
    time: '22:45:00',
    label: 'Prior Initialization',
    dimension: 'All Dimensions',
    scoreBefore: 50.0,
    scoreAfter: 85.0,
    delta: 35.0,
    triggerEvent: 'dag.init',
    confidenceInterval: '[80.0%, 90.0%]',
  },
  {
    step: 2,
    time: '22:45:08',
    label: 'OCR Parsing Complete',
    dimension: 'OCR Quality',
    scoreBefore: 85.0,
    scoreAfter: 94.2,
    delta: 9.2,
    triggerEvent: 'ocr.completed',
    confidenceInterval: '[92.5%, 95.9%]',
  },
  {
    step: 3,
    time: '22:45:15',
    label: 'Schema Validation Succeeded',
    dimension: 'Schema Extraction',
    scoreBefore: 94.2,
    scoreAfter: 97.5,
    delta: 3.3,
    triggerEvent: 'schema.validated',
    confidenceInterval: '[96.2%, 98.8%]',
  },
  {
    step: 4,
    time: '22:45:21',
    label: 'Invariant Verification Passed',
    dimension: 'Invariant Validation',
    scoreBefore: 97.5,
    scoreAfter: 98.42,
    delta: 0.92,
    triggerEvent: 'ledger.invariants.ok',
    confidenceInterval: '[97.8%, 99.0%]',
  },
];

export const ConfidenceTimeline: React.FC = () => {
  return (
    <div className="p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6">
        <div className="space-y-1">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-gradient-to-br from-indigo-500/20 to-purple-500/20 border border-indigo-500/30 rounded-xl text-indigo-400">
              <Clock className="w-5 h-5" />
            </div>
            <div>
              <h1 className="text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2">
                Confidence Progression Timeline
                <Badge variant="intelligence" size="sm">Bayesian Update Flow</Badge>
              </h1>
              <p className="text-xs text-slate-400">
                Step-by-step evidence accumulation and posterior confidence calculation over execution lifecycle.
              </p>
            </div>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <Badge variant="success" size="sm">Converged: 98.42%</Badge>
        </div>
      </div>

      {/* Timeline List */}
      <div className="space-y-4">
        {timelineData.map((ev, idx) => (
          <Card key={ev.step} className="p-4 bg-[#0F172A] border-[#1E293B] hover:border-indigo-500/40 transition-all">
            <div className="flex flex-wrap items-center justify-between gap-4">
              <div className="flex items-center gap-4">
                <div className="flex flex-col items-center justify-center w-10 h-10 rounded-xl bg-indigo-500/10 border border-indigo-500/30 text-indigo-400 font-mono font-bold text-sm">
                  #{ev.step}
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-semibold text-slate-100 text-sm">{ev.label}</span>
                    <Badge variant="outline" size="sm">{ev.dimension}</Badge>
                    <span className="text-xs text-slate-500 font-mono">@{ev.time}</span>
                  </div>
                  <div className="text-xs text-slate-400 font-mono mt-1 flex items-center gap-2">
                    <span>Trigger: <span className="text-indigo-300">{ev.triggerEvent}</span></span>
                    <span>•</span>
                    <span>95% CI: <span className="text-slate-300">{ev.confidenceInterval}</span></span>
                  </div>
                </div>
              </div>

              <div className="flex items-center gap-6">
                <div className="text-right font-mono">
                  <div className="text-xs text-slate-400 flex items-center gap-1.5 justify-end">
                    <span>{ev.scoreBefore.toFixed(1)}%</span>
                    <ArrowRight className="w-3 h-3 text-slate-500" />
                    <span className="text-indigo-400 font-bold text-sm">{ev.scoreAfter.toFixed(2)}%</span>
                  </div>
                  <div className="text-[11px] text-emerald-400 font-semibold flex items-center gap-1 justify-end mt-0.5">
                    <TrendingUp className="w-3 h-3" />
                    +{ev.delta.toFixed(2)}%
                  </div>
                </div>
                {idx === timelineData.length - 1 ? (
                  <Badge variant="success" size="sm" className="flex items-center gap-1">
                    <ShieldCheck className="w-3 h-3" />
                    Final
                  </Badge>
                ) : (
                  <Badge variant="info" size="sm" className="flex items-center gap-1">
                    <CheckCircle2 className="w-3 h-3" />
                    Passed
                  </Badge>
                )}
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
