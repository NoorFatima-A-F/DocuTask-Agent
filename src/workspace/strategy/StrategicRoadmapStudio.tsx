import React, { useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import {
  Compass,
  Calendar,
  CheckCircle2,
  Clock,
} from 'lucide-react';

interface MilestoneItem {
  id: string;
  title: string;
  description: string;
  targetDayOffset: number;
  durationDays: number;
  deliverables: string[];
  confidence: number;
  status: 'COMPLETED' | 'IN_PROGRESS' | 'PENDING';
  assignedSwarm: string;
  isCriticalPath: boolean;
}

export const StrategicRoadmapStudio: React.FC = () => {
  const [selectedHorizon, setSelectedHorizon] = useState<'30d' | '90d' | '180d' | '365d'>('90d');

  const roadmapData: Record<
    '30d' | '90d' | '180d' | '365d',
    {
      title: string;
      theme: string;
      budgetUsd: number;
      roiMultiplier: number;
      milestones: MilestoneItem[];
    }
  > = {
    '30d': {
      title: '30-Day Rapid Throughput & Speculative Cache Rollout',
      theme: 'Low-Latency Cache Ingestion & Specialist Coalition Pre-Warming',
      budgetUsd: 4200.0,
      roiMultiplier: 3.80,
      milestones: [
        {
          id: 'ms-30d-01',
          title: 'Speculative Layout Cache Activation',
          description: 'Zero-copy tensor cache for recurrent corporate invoice headers.',
          targetDayOffset: 5,
          durationDays: 5,
          deliverables: ['Pre-warmed tensor buffer', 'Sub-50ms cache hit path'],
          confidence: 0.988,
          status: 'COMPLETED',
          assignedSwarm: 'Optimization Swarm Alpha',
          isCriticalPath: true,
        },
        {
          id: 'ms-30d-02',
          title: 'Triadic Strike Team Pre-Warming',
          description: 'Pre-cluster extraction workers to eliminate runtime bidding latency.',
          targetDayOffset: 12,
          durationDays: 7,
          deliverables: ['Triadic agent coalition template', '18% latency reduction'],
          confidence: 0.975,
          status: 'IN_PROGRESS',
          assignedSwarm: 'Swarm Coalition Beta',
          isCriticalPath: true,
        },
        {
          id: 'ms-30d-03',
          title: '30-Day Benchmark Audit & Certification',
          description: 'Run automated stress benchmarks and export truth verification certificate.',
          targetDayOffset: 28,
          durationDays: 4,
          deliverables: ['Signed provenance audit', '100k doc/day throughput verification'],
          confidence: 0.992,
          status: 'PENDING',
          assignedSwarm: 'Executive Governance Oracle',
          isCriticalPath: true,
        },
      ],
    },
    '90d': {
      title: '90-Day Enterprise Strategic Expansion',
      theme: 'Multi-Swarm Autonomous Governance & Digital Twin Decisioning',
      budgetUsd: 14500.0,
      roiMultiplier: 3.45,
      milestones: [
        {
          id: 'ms-90d-01',
          title: 'Predictive Digital Twin Synchronization Sub-20ms',
          description: 'Live twin state telemetry across all active worker swarms.',
          targetDayOffset: 20,
          durationDays: 15,
          deliverables: ['Sub-20ms twin sync', 'Pareto optimal Monte Carlo engine'],
          confidence: 0.980,
          status: 'COMPLETED',
          assignedSwarm: 'World Model Core',
          isCriticalPath: true,
        },
        {
          id: 'ms-90d-02',
          title: 'Autonomous Multi-Swarm Resource Negotiation',
          description: 'Nash-equilibrium auction protocols for GPU and token distribution.',
          targetDayOffset: 45,
          durationDays: 20,
          deliverables: ['Decentralized token exchange', 'Dynamic GPU priority scheduler'],
          confidence: 0.965,
          status: 'IN_PROGRESS',
          assignedSwarm: 'Swarm Negotiation Bus',
          isCriticalPath: true,
        },
        {
          id: 'ms-90d-03',
          title: 'Executive Strategic Decision Support System',
          description: 'AI Chief Strategy Officer (CSO) dashboard with continuous MCDA.',
          targetDayOffset: 85,
          durationDays: 25,
          deliverables: ['Executive Cockpit UI', '100% cryptographically audited approvals'],
          confidence: 0.970,
          status: 'PENDING',
          assignedSwarm: 'Executive Strategy Runtime',
          isCriticalPath: true,
        },
      ],
    },
    '180d': {
      title: '180-Day Semi-Annual Scale & Self-Improvement',
      theme: 'Institutional Memory Synthesis & Long-Horizon Policy Evolution',
      budgetUsd: 28000.0,
      roiMultiplier: 4.10,
      milestones: [
        {
          id: 'ms-180d-01',
          title: 'Institutional Knowledge Graph Expansion',
          description: 'Consolidate 100,000+ mission traces into reusable organizational playbooks.',
          targetDayOffset: 60,
          durationDays: 30,
          deliverables: ['Playbook knowledge store', 'Continuous anti-pattern detector'],
          confidence: 0.955,
          status: 'PENDING',
          assignedSwarm: 'Institutional Memory Core',
          isCriticalPath: true,
        },
        {
          id: 'ms-180d-02',
          title: 'Continuous Multi-Year Goal Evolution Engine',
          description: 'Autonomous strategy mutation and Pareto rebalancing.',
          targetDayOffset: 150,
          durationDays: 45,
          deliverables: ['Self-updating roadmaps', 'Automated budget reallocation'],
          confidence: 0.940,
          status: 'PENDING',
          assignedSwarm: 'Cognitive Evolution Swarm',
          isCriticalPath: true,
        },
      ],
    },
    '365d': {
      title: '365-Day Fully Autonomous Cognitive Enterprise',
      theme: 'Zero-Human-Intervention Autonomous Enterprise Strategy Execution',
      budgetUsd: 55000.0,
      roiMultiplier: 5.50,
      milestones: [
        {
          id: 'ms-365d-01',
          title: 'Autonomous Corporate Strategy Orchestration',
          description: 'End-to-end mission portfolio decomposition and self-executing governance.',
          targetDayOffset: 300,
          durationDays: 65,
          deliverables: ['Autonomous CSO agent runtime', 'Multi-datacenter swarm federation'],
          confidence: 0.925,
          status: 'PENDING',
          assignedSwarm: 'Global Enterprise Federation',
          isCriticalPath: true,
        },
      ],
    },
  };

  const currentRoadmap = roadmapData[selectedHorizon];

  const getStatusBadge = (status: 'COMPLETED' | 'IN_PROGRESS' | 'PENDING') => {
    switch (status) {
      case 'COMPLETED':
        return (
          <Badge variant="success" size="sm">
            <CheckCircle2 className="w-3 h-3 mr-1" />
            COMPLETED
          </Badge>
        );
      case 'IN_PROGRESS':
        return (
          <Badge variant="warning" size="sm">
            <Clock className="w-3 h-3 mr-1" />
            IN PROGRESS
          </Badge>
        );
      case 'PENDING':
        return (
          <Badge variant="default" size="sm">
            PENDING
          </Badge>
        );
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
            <Compass className="w-6 h-6 text-indigo-500" />
            Strategic Multi-Horizon Roadmap Studio
          </h2>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            Phase 13.11 — Autonomous 30d, 90d, 180d, and 365-day strategic execution roadmaps with weighted interval critical path analysis.
          </p>
        </div>
        <div className="flex items-center gap-2 bg-gray-100 dark:bg-gray-800 p-1 rounded-lg">
          {(['30d', '90d', '180d', '365d'] as const).map((h) => (
            <button
              key={h}
              onClick={() => setSelectedHorizon(h)}
              className={`px-3 py-1.5 text-xs font-semibold rounded-md transition-colors ${
                selectedHorizon === h
                  ? 'bg-indigo-600 text-white shadow-sm'
                  : 'text-gray-600 dark:text-gray-300 hover:text-indigo-600'
              }`}
            >
              {h.toUpperCase()} Roadmap
            </button>
          ))}
        </div>
      </div>

      {/* Roadmap Summary Card */}
      <Card className="p-5 border-l-4 border-l-indigo-600 bg-indigo-50/20 dark:bg-indigo-950/20">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <Badge variant="intelligence" size="sm">
                {selectedHorizon.toUpperCase()} HORIZON
              </Badge>
              <h3 className="text-lg font-bold text-gray-900 dark:text-white">{currentRoadmap.title}</h3>
            </div>
            <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">Theme: {currentRoadmap.theme}</p>
          </div>
          <div className="flex items-center gap-6">
            <div className="text-right">
              <span className="text-xs text-gray-400 block">Estimated Budget</span>
              <span className="text-lg font-bold text-gray-900 dark:text-white font-mono">
                ${currentRoadmap.budgetUsd.toLocaleString()}
              </span>
            </div>
            <div className="text-right">
              <span className="text-xs text-gray-400 block">Projected ROI</span>
              <span className="text-lg font-bold text-emerald-600 dark:text-emerald-400 font-mono">
                {currentRoadmap.roiMultiplier}x
              </span>
            </div>
          </div>
        </div>
      </Card>

      {/* Milestones Visual Timeline */}
      <div className="space-y-4">
        <h3 className="text-sm font-semibold text-gray-900 dark:text-white uppercase tracking-wider flex items-center gap-2">
          <Calendar className="w-4 h-4 text-indigo-500" />
          Milestones & Critical Path Timeline
        </h3>

        <div className="relative border-l-2 border-indigo-200 dark:border-indigo-900 ml-4 space-y-6 pb-2">
          {currentRoadmap.milestones.map((ms) => (
            <div key={ms.id} className="relative pl-6">
              {/* Dot on timeline */}
              <div className="absolute -left-[9px] top-1.5 w-4 h-4 rounded-full bg-indigo-600 border-2 border-white dark:border-gray-900" />

              <Card className="p-5 hover:shadow-md transition-shadow">
                <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 pb-3 border-b border-gray-100 dark:border-gray-800">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="font-mono text-xs text-indigo-600 dark:text-indigo-400 font-semibold">{ms.id}</span>
                      <span className="text-xs text-gray-400">Day +{ms.targetDayOffset} ({ms.durationDays}d duration)</span>
                      {ms.isCriticalPath && (
                        <Badge variant="warning" size="sm">
                          CRITICAL PATH
                        </Badge>
                      )}
                    </div>
                    <h4 className="font-semibold text-gray-900 dark:text-white text-base mt-1">{ms.title}</h4>
                    <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">{ms.description}</p>
                  </div>
                  <div className="flex items-center gap-3">
                    {getStatusBadge(ms.status)}
                  </div>
                </div>

                <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                  <div>
                    <span className="text-gray-400 block mb-1">Key Deliverables:</span>
                    <div className="space-y-1">
                      {ms.deliverables.map((d, dIdx) => (
                        <div key={dIdx} className="flex items-center gap-1.5 text-gray-700 dark:text-gray-300">
                          <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500 flex-shrink-0" />
                          <span>{d}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                  <div className="space-y-2">
                    <div className="flex items-center justify-between">
                      <span className="text-gray-400">Assigned Swarm:</span>
                      <span className="font-semibold text-indigo-600 dark:text-indigo-400">{ms.assignedSwarm}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-gray-400">Bayesian Confidence:</span>
                      <span className="font-semibold text-purple-600 dark:text-purple-400">{(ms.confidence * 100).toFixed(1)}%</span>
                    </div>
                  </div>
                </div>
              </Card>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
