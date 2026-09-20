import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { RotateCcw, Play, Pause, FastForward } from 'lucide-react';

export const PlannerReplayView: React.FC = () => {
  const [currentStep, setCurrentStep] = useState<number>(3);
  const [isPlaying, setIsPlaying] = useState<boolean>(false);

  const replaySteps = [
    { offset: 0, time: '14:20:00.120', action: 'PlannerCreated', state: 'CREATED', desc: 'Planner initialized from mission request.' },
    { offset: 1, time: '14:20:00.350', action: 'GoalParsed', state: 'GOAL_ANALYSIS', desc: 'Decomposed SLA constraints and invariants.' },
    { offset: 2, time: '14:20:00.420', action: 'PlanGenerated', state: 'PLAN_SYNTHESIS', desc: 'Synthesized 9-node DAG with parallel wavefronts.' },
    { offset: 3, time: '14:20:00.600', action: 'TaskSplitRequested', state: 'DAG_MUTATION', desc: 'Split OCR stage into 2 parallel sub-tasks.' },
    { offset: 4, time: '14:20:00.720', action: 'WorkerAssigned', state: 'DISPATCH', desc: 'Assigned worker-ocr-01 and worker-ocr-02.' },
    { offset: 5, time: '14:20:01.100', action: 'ExecutionStarted', state: 'EXECUTING', desc: 'Dispatched Wavefront 1 tasks.' },
    { offset: 6, time: '14:20:02.100', action: 'MissionCompleted', state: 'COMPLETED', desc: 'Verified all invariants and committed truth hash.' },
  ];

  return (
    <div className="p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6">
        <div className="space-y-1">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-gradient-to-br from-cyan-500/20 to-blue-500/20 border border-cyan-500/30 rounded-xl text-cyan-400">
              <RotateCcw className="w-5 h-5" />
            </div>
            <div>
              <h1 className="text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2">
                Planner Deterministic Replay Studio
                <Badge variant="success" size="sm">Phase 13.1 Event-Replayable</Badge>
              </h1>
              <p className="text-xs text-[#94A3B8] font-mono">
                Step-by-step reconstruction of planner decisions and DAG mutations directly from immutable Event Store
              </p>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <Button
            onClick={() => setIsPlaying(!isPlaying)}
            variant={isPlaying ? 'danger' : 'primary'}
            size="sm"
          >
            {isPlaying ? <Pause className="w-3.5 h-3.5 mr-1" /> : <Play className="w-3.5 h-3.5 mr-1" />}
            {isPlaying ? 'Pause Replay' : 'Play Replay'}
          </Button>
          <Button
            onClick={() => setCurrentStep(prev => Math.min(replaySteps.length - 1, prev + 1))}
            variant="secondary"
            size="sm"
          >
            <FastForward className="w-3.5 h-3.5 mr-1" />
            Step Forward
          </Button>
        </div>
      </div>

      {/* Progress Scrubber */}
      <Card className="p-5 rounded-2xl border border-[#1E293B] bg-[#0F172A] space-y-3 font-mono">
        <div className="flex items-center justify-between text-xs">
          <span className="text-[#94A3B8]">REPLAY PROGRESS: STEP {currentStep + 1} OF {replaySteps.length}</span>
          <span className="text-cyan-400 font-bold">{replaySteps[currentStep]?.time ?? ''}</span>
        </div>

        <div className="w-full bg-[#131D35] h-2.5 rounded-full overflow-hidden">
          <div
            className="bg-gradient-to-r from-cyan-500 to-indigo-500 h-full transition-all duration-300"
            style={{ width: `${((currentStep + 1) / replaySteps.length) * 100}%` }}
          />
        </div>
      </Card>

      {/* Step Sequence */}
      <div className="space-y-3 font-mono">
        {replaySteps.map((step, idx) => {
          const isCurrent = currentStep === idx;
          const isPast = currentStep > idx;

          return (
            <Card
              key={step.offset}
              onClick={() => setCurrentStep(idx)}
              className={`p-4 rounded-xl border transition-all cursor-pointer flex items-center justify-between ${
                isCurrent
                  ? 'border-cyan-500 bg-[#131D35] shadow-[0_0_12px_rgba(0,210,255,0.2)]'
                  : isPast
                  ? 'border-emerald-500/30 bg-[#0F172A]'
                  : 'border-[#1E293B] bg-[#0A0F1D]/50 opacity-60'
              }`}
            >
              <div className="flex items-center gap-4">
                <div className={`w-8 h-8 rounded-lg flex items-center justify-center text-xs font-bold ${
                  isCurrent ? 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/30' : 'bg-[#131D35] text-[#64748B]'
                }`}>
                  #{step.offset}
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-bold text-white">{step.action}</span>
                    <Badge variant="outline" size="sm">{step.state}</Badge>
                  </div>
                  <p className="text-xs text-[#94A3B8] mt-0.5">{step.desc}</p>
                </div>
              </div>

              <div className="text-right text-xs">
                <span className="text-white font-semibold">{step.time}</span>
                <Badge variant={isCurrent ? 'intelligence' : isPast ? 'success' : 'outline'} size="sm" className="ml-2">
                  {isCurrent ? 'CURRENT' : isPast ? 'REPLAYED' : 'PENDING'}
                </Badge>
              </div>
            </Card>
          );
        })}
      </div>
    </div>
  );
};
