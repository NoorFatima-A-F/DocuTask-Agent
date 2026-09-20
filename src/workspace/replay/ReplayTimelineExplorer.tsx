import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Clock, Search, Layers, CheckCircle2, ChevronRight, Hash } from 'lucide-react';

interface TimelineEventItem {
  id: string;
  cursor: number;
  type: string;
  subsystem: string;
  timestamp: string;
  summary: string;
  payloadJson: string;
}

const mockTimelineEvents: TimelineEventItem[] = [
  { id: 'evt_001', cursor: 0, type: 'mission.started', subsystem: 'mission', timestamp: '00:00:01', summary: 'Mission Ingestion initialized', payloadJson: '{"goal": "Process multi-page enterprise invoice"}' },
  { id: 'evt_002', cursor: 1, type: 'planner.lifecycle.transition', subsystem: 'planner', timestamp: '00:00:02', summary: 'Planner entered GOAL_ANALYSIS state', payloadJson: '{"state": "GOAL_ANALYSIS"}' },
  { id: 'evt_003', cursor: 2, type: 'planner.task_decomposed', subsystem: 'planner', timestamp: '00:00:03', summary: 'Decomposed into OCR, Schema, and SMT tasks', payloadJson: '{"tasks_count": 3}' },
  { id: 'evt_004', cursor: 3, type: 'schedule.assigned', subsystem: 'scheduler', timestamp: '00:00:04', summary: 'Task task_ocr_01 allocated to worker_gpu_01', payloadJson: '{"worker_id": "worker_gpu_01"}' },
  { id: 'evt_005', cursor: 4, type: 'worker.started', subsystem: 'worker', timestamp: '00:00:05', summary: 'Worker worker_gpu_01 started OCR pipeline', payloadJson: '{"role": "ocr_specialist"}' },
  { id: 'evt_006', cursor: 5, type: 'worker.completed', subsystem: 'worker', timestamp: '00:00:08', summary: 'OCR step finished in 285ms (confidence 0.96)', payloadJson: '{"duration_ms": 285.0}' },
  { id: 'evt_007', cursor: 6, type: 'confidence.evaluated', subsystem: 'confidence', timestamp: '00:00:09', summary: 'Confidence evaluated via WeightedEnsemble (v1.3.0)', payloadJson: '{"overall_score": 0.942}' },
  { id: 'evt_008', cursor: 7, type: 'truth.invariant.checked', subsystem: 'truth', timestamp: '00:00:12', summary: 'SMT total balance proof satisfied: Subtotal + Tax == Total', payloadJson: '{"passed": true}' },
  { id: 'evt_009', cursor: 8, type: 'truth.merkle_root.sealed', subsystem: 'truth', timestamp: '00:00:13', summary: 'Sealed Merkle root into immutable truth chain', payloadJson: '{"merkle_root": "sha256:7fa189c4..."}' },
  { id: 'evt_010', cursor: 9, type: 'mission.completed', subsystem: 'mission', timestamp: '00:00:15', summary: 'Mission finished successfully with 100% truth proofs', payloadJson: '{"final_confidence": 0.9842}' },
];

export const ReplayTimelineExplorer: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedSubsystem, setSelectedSubsystem] = useState('ALL');
  const [selectedEvent, setSelectedEvent] = useState<TimelineEventItem | null>(mockTimelineEvents[0] || null);

  const filtered = mockTimelineEvents.filter((ev) => {
    const matchesSearch = ev.id.toLowerCase().includes(searchTerm.toLowerCase()) ||
      ev.type.toLowerCase().includes(searchTerm.toLowerCase()) ||
      ev.summary.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesSub = selectedSubsystem === 'ALL' || ev.subsystem === selectedSubsystem;
    return matchesSearch && matchesSub;
  });

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
                Replay Timeline Explorer
                <Badge variant="intelligence" size="sm">Immutable Chronology</Badge>
              </h1>
              <p className="text-xs text-slate-400">
                Inspect raw domain event streams with cryptographic payload verification and subsystem categorization.
              </p>
            </div>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <Badge variant="success" size="sm">{filtered.length} Events Listed</Badge>
        </div>
      </div>

      {/* Filters */}
      <div className="flex flex-wrap items-center gap-4 bg-[#0F172A] p-4 rounded-xl border border-[#1E293B]">
        <div className="relative flex-1 min-w-[240px]">
          <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
          <input
            type="text"
            placeholder="Search events by ID, type, summary..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-9 pr-4 py-2 bg-[#0B1120] border border-[#1E293B] rounded-lg text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-indigo-500"
          />
        </div>

        <select
          value={selectedSubsystem}
          onChange={(e) => setSelectedSubsystem(e.target.value)}
          className="bg-[#0B1120] border border-[#1E293B] rounded-lg px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-indigo-500"
        >
          <option value="ALL">All Subsystems</option>
          <option value="mission">Mission</option>
          <option value="planner">Planner</option>
          <option value="scheduler">Scheduler</option>
          <option value="worker">Worker</option>
          <option value="confidence">Confidence</option>
          <option value="truth">Truth</option>
        </select>
      </div>

      {/* Split Viewer */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Timeline list */}
        <Card className="lg:col-span-2 p-4 bg-[#0F172A] border-[#1E293B] space-y-2 max-h-[600px] overflow-y-auto">
          {filtered.map((ev) => {
            const isSelected = selectedEvent?.id === ev.id;
            return (
              <div
                key={ev.id}
                onClick={() => setSelectedEvent(ev)}
                className={`p-3 rounded-lg border transition-all cursor-pointer flex items-center justify-between font-mono text-xs ${
                  isSelected
                    ? 'bg-indigo-500/10 border-indigo-500/50 text-white'
                    : 'bg-slate-900/40 border-slate-800 text-slate-300 hover:bg-slate-800/60'
                }`}
              >
                <div className="flex items-center gap-3">
                  <div className="w-6 h-6 rounded bg-slate-800 flex items-center justify-center text-[10px] text-slate-400 font-bold">
                    #{ev.cursor}
                  </div>
                  <div>
                    <div className="font-bold text-slate-100 flex items-center gap-2">
                      <span>{ev.type}</span>
                      <Badge variant="outline" size="sm">{ev.subsystem}</Badge>
                    </div>
                    <div className="text-[11px] text-slate-400 mt-0.5">{ev.summary}</div>
                  </div>
                </div>

                <div className="flex items-center gap-2 text-slate-500 text-[11px]">
                  <span>{ev.timestamp}</span>
                  <ChevronRight className="w-3.5 h-3.5" />
                </div>
              </div>
            );
          })}
        </Card>

        {/* Selected Event JSON Inspector */}
        <Card className="p-5 bg-[#0F172A] border-[#1E293B] flex flex-col justify-between font-mono text-xs">
          <div className="space-y-3">
            <div className="flex items-center justify-between border-b border-slate-800 pb-2">
              <span className="font-bold text-slate-200 flex items-center gap-1.5">
                <Hash className="w-3.5 h-3.5 text-indigo-400" />
                {selectedEvent?.id}
              </span>
              <Badge variant="success" size="sm">
                <CheckCircle2 className="w-3 h-3 inline mr-1" />
                Verified
              </Badge>
            </div>

            <div className="text-slate-400 space-y-1">
              <div>Type: <span className="text-indigo-300 font-bold">{selectedEvent?.type}</span></div>
              <div>Subsystem: <span className="text-slate-200 capitalize">{selectedEvent?.subsystem}</span></div>
              <div>Timestamp: <span className="text-slate-300">{selectedEvent?.timestamp}</span></div>
            </div>

            <div className="space-y-1">
              <div className="text-slate-400 font-semibold flex items-center gap-1">
                <Layers className="w-3.5 h-3.5" /> Payload Details:
              </div>
              <pre className="p-3 bg-slate-950 rounded-lg border border-slate-800 text-[11px] text-cyan-300 overflow-x-auto">
                {JSON.stringify(JSON.parse(selectedEvent?.payloadJson || '{}'), null, 2)}
              </pre>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
};
