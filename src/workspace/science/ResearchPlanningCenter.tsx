import React, { useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import {
  MapPin,
  Cpu,
  TrendingUp,
  Compass,
  CheckCircle2,
  Calendar,
} from 'lucide-react';

interface StreamItem {
  id: string;
  name: string;
  domain: string;
  priority: 'BREAKTHROUGH' | 'HIGH' | 'MEDIUM';
  computeUnits: number;
  activeHypotheses: number;
  completedExperiments: number;
  deliverable: string;
}

export const ResearchPlanningCenter: React.FC = () => {
  const [allocationNotice, setAllocationNotice] = useState<string | null>(null);

  const streams: StreamItem[] = [
    {
      id: 'stream-01',
      name: 'Low-Latency Speculative Acceleration',
      domain: 'Memory & Caching',
      priority: 'BREAKTHROUGH',
      computeUnits: 64,
      activeHypotheses: 2,
      completedExperiments: 5,
      deliverable: 'Sub-150ms P95 universal document extraction across all schemas.',
    },
    {
      id: 'stream-02',
      name: 'Swarm Triadic Coordination Dynamics',
      domain: 'Swarm Intelligence',
      priority: 'HIGH',
      computeUnits: 48,
      activeHypotheses: 1,
      completedExperiments: 3,
      deliverable: 'Elimination of auction bidding latency under >10,000 tasks/min.',
    },
    {
      id: 'stream-03',
      name: 'Deterministic Memory Provenance & Replay',
      domain: 'Resilience & Truth',
      priority: 'HIGH',
      computeUnits: 32,
      activeHypotheses: 1,
      completedExperiments: 4,
      deliverable: 'Zero-overhead continuous audit replay verification.',
    },
  ];

  const handleReallocateCompute = () => {
    setAllocationNotice('Autonomous Research Scheduler dynamically re-allocated 64 compute units to Breakthrough Stream-01 based on high EIG score (0.915).');
    setTimeout(() => setAllocationNotice(null), 4000);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
            <MapPin className="w-6 h-6 text-indigo-500" />
            Strategic Research Planning & Roadmap Center
          </h2>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            Coordinates parallel scientific research streams, schedules autonomous compute unit budgets, and tracks strategic milestones.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="intelligence" size="sm" onClick={handleReallocateCompute}>
            <Cpu className="w-3.5 h-3.5 mr-1.5" />
            Optimize Compute Allocation
          </Button>
        </div>
      </div>

      {allocationNotice && (
        <div className="p-4 bg-indigo-50 dark:bg-indigo-950/40 border border-indigo-200 dark:border-indigo-800 rounded-lg text-sm text-indigo-800 dark:text-indigo-300 flex items-center gap-2">
          <CheckCircle2 className="w-5 h-5 flex-shrink-0" />
          <span>{allocationNotice}</span>
        </div>
      )}

      {/* Top Planning Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="p-4 border-l-4 border-l-indigo-500">
          <div className="flex items-center justify-between text-xs text-gray-500">
            <span>Total Compute Budget</span>
            <Cpu className="w-4 h-4 text-indigo-500" />
          </div>
          <div className="text-2xl font-bold text-gray-900 dark:text-white mt-1">192 Units</div>
          <span className="text-xs text-indigo-600">144 Allocated / 48 Buffer</span>
        </Card>

        <Card className="p-4 border-l-4 border-l-emerald-500">
          <div className="flex items-center justify-between text-xs text-gray-500">
            <span>Active Scientific Streams</span>
            <Compass className="w-4 h-4 text-emerald-500" />
          </div>
          <div className="text-2xl font-bold text-emerald-600 dark:text-emerald-400 mt-1">3 Streams</div>
          <span className="text-xs text-emerald-500">1 Breakthrough Priority</span>
        </Card>

        <Card className="p-4 border-l-4 border-l-purple-500">
          <div className="flex items-center justify-between text-xs text-gray-500">
            <span>Research ROI Multiplier</span>
            <TrendingUp className="w-4 h-4 text-purple-500" />
          </div>
          <div className="text-2xl font-bold text-purple-600 dark:text-purple-400 mt-1">4.10x</div>
          <span className="text-xs text-purple-500">Value of verified laws vs compute cost</span>
        </Card>

        <Card className="p-4 border-l-4 border-l-amber-500">
          <div className="flex items-center justify-between text-xs text-gray-500">
            <span>Roadmap Horizon</span>
            <Calendar className="w-4 h-4 text-amber-500" />
          </div>
          <div className="text-2xl font-bold text-amber-600 dark:text-amber-400 mt-1">2026-Q4</div>
          <span className="text-xs text-amber-500">3 of 5 Milestones Achieved</span>
        </Card>
      </div>

      {/* Research Streams Cards */}
      <div className="space-y-4">
        {streams.map(stream => (
          <Card key={stream.id} className="p-5 space-y-4">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-2 border-b border-gray-100 dark:border-gray-800 pb-3">
              <div>
                <div className="flex items-center gap-2">
                  <span className="font-mono text-xs text-indigo-500 font-semibold">{stream.id}</span>
                  <Badge variant="outline" size="sm">Domain: {stream.domain}</Badge>
                  <Badge variant={stream.priority === 'BREAKTHROUGH' ? 'warning' : 'info'} size="sm">
                    {stream.priority}
                  </Badge>
                </div>
                <h3 className="text-base font-semibold text-gray-900 dark:text-white mt-1">{stream.name}</h3>
              </div>
              <div className="flex items-center gap-2">
                <Badge variant="intelligence" size="sm">
                  <Cpu className="w-3.5 h-3.5 mr-1" />
                  {stream.computeUnits} Compute Units
                </Badge>
              </div>
            </div>

            <p className="text-xs text-gray-600 dark:text-gray-300">
              <strong className="text-gray-800 dark:text-gray-200">Target Deliverable:</strong> {stream.deliverable}
            </p>

            <div className="grid grid-cols-2 gap-4 bg-gray-50 dark:bg-gray-800/40 p-3 rounded-lg text-xs">
              <div>
                <span className="text-gray-400">Active Hypotheses:</span>
                <div className="font-bold text-gray-900 dark:text-white text-sm">{stream.activeHypotheses}</div>
              </div>
              <div>
                <span className="text-gray-400">Completed Empirical Experiments:</span>
                <div className="font-bold text-emerald-600 dark:text-emerald-400 text-sm">{stream.completedExperiments}</div>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
