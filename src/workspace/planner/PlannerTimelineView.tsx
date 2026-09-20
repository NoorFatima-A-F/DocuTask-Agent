import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Clock } from 'lucide-react';

export const PlannerTimelineView: React.FC = () => {
  const events = [
    { id: 'evt-p01-001', time: '14:20:00.120', type: 'PlannerCreated', actor: 'ChiefPlanner', summary: 'Planner instantiated with correlation token corr-mission-fin-001.' },
    { id: 'evt-p01-002', time: '14:20:00.350', type: 'PlannerStateChanged', actor: 'ChiefPlanner', summary: 'Transitioned from CREATED to GOAL_ANALYSIS.' },
    { id: 'evt-p01-003', time: '14:20:00.580', type: 'PlannerStateChanged', actor: 'ChiefPlanner', summary: 'Transitioned from GOAL_ANALYSIS to PLAN_SYNTHESIS.' },
    { id: 'evt-p01-004', time: '14:20:00.890', type: 'PlannerStateChanged', actor: 'ChiefPlanner', summary: 'Generated 9 DAG tasks and reached READY state.' },
    { id: 'evt-p01-005', time: '14:20:01.100', type: 'PlannerStateChanged', actor: 'ChiefPlanner', summary: 'Dispatched Wavefront 1, transitioned to EXECUTING.' },
  ];

  return (
    <div className="p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6">
        <div className="space-y-1">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-gradient-to-br from-cyan-500/20 to-blue-500/20 border border-cyan-500/30 rounded-xl text-cyan-400">
              <Clock className="w-5 h-5" />
            </div>
            <div>
              <h1 className="text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2">
                Event-Sourced Planner Execution Timeline
                <Badge variant="success" size="sm">Phase 13.1 Connected</Badge>
              </h1>
              <p className="text-xs text-[#94A3B8] font-mono">
                Chronological sequence of all planner actions, DAG synthesis steps, and dispatch decisions
              </p>
            </div>
          </div>
        </div>

        <Badge variant="intelligence" size="md">Immutable Sequence</Badge>
      </div>

      {/* Timeline List */}
      <div className="space-y-3 font-mono">
        {events.map((evt, idx) => (
          <Card key={evt.id} className="p-4 rounded-xl border border-[#1E293B] bg-[#0F172A] flex items-center justify-between gap-4">
            <div className="flex items-center gap-4">
              <div className="w-8 h-8 rounded-lg bg-[#131D35] border border-[#1E293B] flex items-center justify-center text-xs font-bold text-cyan-400">
                0{idx + 1}
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <span className="text-xs font-bold text-white">{evt.type}</span>
                  <Badge variant="default" size="sm">{evt.actor}</Badge>
                </div>
                <p className="text-xs text-[#94A3B8] mt-1">{evt.summary}</p>
              </div>
            </div>

            <div className="text-right text-xs">
              <span className="text-[#64748B] block text-[10px]">{evt.id}</span>
              <span className="text-white font-semibold">{evt.time}</span>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
