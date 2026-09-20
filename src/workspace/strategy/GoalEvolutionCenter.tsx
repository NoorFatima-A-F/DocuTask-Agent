import React, { useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import {
  GitBranch,
  CheckCircle2,
  RefreshCw,
  Layers,
} from 'lucide-react';

interface GoalItem {
  id: string;
  title: string;
  description: string;
  priority: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';
  status: 'ACTIVE' | 'REFINING' | 'COMPLETED' | 'ARCHIVED';
  horizon: string;
  utilityScore: number;
  confidence: number;
  ageDays: number;
  costUsd: number;
  latencyGainPct: number;
  subgoalsCount: number;
  tags: string[];
}

export const GoalEvolutionCenter: React.FC = () => {
  const [goals, setGoals] = useState<GoalItem[]>([
    {
      id: 'goal-root-scale-100k',
      title: 'Scale Multi-Swarm Processing to 100k Daily Documents',
      description: 'Expand agentic extraction capacity with sub-250ms SLA and zero accuracy degradation.',
      priority: 'CRITICAL',
      status: 'ACTIVE',
      horizon: 'DAYS_90',
      utilityScore: 0.965,
      confidence: 0.982,
      ageDays: 12,
      costUsd: 2400.0,
      latencyGainPct: 35.0,
      subgoalsCount: 2,
      tags: ['scalability', 'swarm', 'throughput'],
    },
    {
      id: 'goal-sub-cache-warm',
      title: 'Deploy Speculative Zero-Copy Embedding Cache',
      description: 'Pre-compute document layout representations across recurrent corporate invoice templates.',
      priority: 'HIGH',
      status: 'ACTIVE',
      horizon: 'DAYS_30',
      utilityScore: 0.920,
      confidence: 0.990,
      ageDays: 5,
      costUsd: 450.0,
      latencyGainPct: 22.0,
      subgoalsCount: 0,
      tags: ['caching', 'latency', 'gpu'],
    },
    {
      id: 'goal-sub-strike-teams',
      title: 'Form Triadic Specialist Swarm Strike Teams',
      description: 'Pre-cluster extraction workers by document taxonomy to reduce inter-agent bidding friction.',
      priority: 'HIGH',
      status: 'ACTIVE',
      horizon: 'DAYS_30',
      utilityScore: 0.895,
      confidence: 0.975,
      ageDays: 7,
      costUsd: 600.0,
      latencyGainPct: 18.0,
      subgoalsCount: 0,
      tags: ['swarm', 'coalition', 'specialist'],
    },
    {
      id: 'goal-root-gov-integrity',
      title: 'Attain Continuous 100% Cryptographic Auditability',
      description: 'Ensure all autonomous interventions have SHA-256 state proofs and instant rollback points.',
      priority: 'CRITICAL',
      status: 'ACTIVE',
      horizon: 'DAYS_180',
      utilityScore: 0.980,
      confidence: 0.995,
      ageDays: 25,
      costUsd: 1200.0,
      latencyGainPct: 0.0,
      subgoalsCount: 0,
      tags: ['governance', 'cryptography', 'safety'],
    },
  ]);

  const [isEvolving, setIsEvolving] = useState(false);
  const [statusMessage, setStatusMessage] = useState<string | null>(null);

  const handleEvolve = () => {
    setIsEvolving(true);
    setTimeout(() => {
      setGoals((prev) =>
        prev.map((g) => ({
          ...g,
          ageDays: g.ageDays + 1,
          utilityScore: Math.min(0.99, g.utilityScore + 0.005),
        }))
      );
      setIsEvolving(false);
      setStatusMessage('Goal Evolution Cycle executed: 4 goals updated with refreshed utility and aging scores.');
      setTimeout(() => setStatusMessage(null), 4000);
    }, 1000);
  };

  const getPriorityBadgeVariant = (priority: string): 'error' | 'warning' | 'info' | 'default' => {
    switch (priority) {
      case 'CRITICAL':
        return 'error';
      case 'HIGH':
        return 'warning';
      case 'MEDIUM':
        return 'info';
      default:
        return 'default';
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
            <GitBranch className="w-6 h-6 text-indigo-500" />
            Autonomous Goal Evolution & HTN Decomposition Center
          </h2>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            Phase 13.11 — Hierarchical Task Network (HTN) & GOAP goal trees, utility scoring, and dynamic priority reprioritization.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="intelligence" size="sm" onClick={handleEvolve} disabled={isEvolving}>
            <RefreshCw className={`w-3.5 h-3.5 mr-1.5 ${isEvolving ? 'animate-spin' : ''}`} />
            {isEvolving ? 'Evolving Generation...' : 'Trigger Goal Evolution'}
          </Button>
        </div>
      </div>

      {statusMessage && (
        <div className="p-4 bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800 rounded-lg text-sm text-emerald-800 dark:text-emerald-300 flex items-center gap-2">
          <CheckCircle2 className="w-5 h-5 flex-shrink-0" />
          <span>{statusMessage}</span>
        </div>
      )}

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="p-4 border-l-4 border-l-indigo-500">
          <span className="text-xs font-medium text-gray-500">Active Strategic Goals</span>
          <div className="text-2xl font-bold text-gray-900 dark:text-white mt-1">{goals.length}</div>
          <span className="text-xs text-indigo-600 dark:text-indigo-400 font-medium">HTN Decomposed</span>
        </Card>
        <Card className="p-4 border-l-4 border-l-emerald-500">
          <span className="text-xs font-medium text-gray-500">Avg Composite Utility</span>
          <div className="text-2xl font-bold text-emerald-600 dark:text-emerald-400 mt-1">
            {(goals.reduce((acc, g) => acc + g.utilityScore, 0) / goals.length).toFixed(3)}
          </div>
          <span className="text-xs text-gray-400">Max: 1.000</span>
        </Card>
        <Card className="p-4 border-l-4 border-l-purple-500">
          <span className="text-xs font-medium text-gray-500">Bayesian Confidence</span>
          <div className="text-2xl font-bold text-purple-600 dark:text-purple-400 mt-1">98.5%</div>
          <span className="text-xs text-purple-500">Empirical Provenance</span>
        </Card>
        <Card className="p-4 border-l-4 border-l-amber-500">
          <span className="text-xs font-medium text-gray-500">Goal Conflict Status</span>
          <div className="text-2xl font-bold text-emerald-600 dark:text-emerald-400 mt-1">0 CONFLICTS</div>
          <span className="text-xs text-emerald-500">Deadlock-Free Tree</span>
        </Card>
      </div>

      {/* Goals Tree List */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-semibold text-gray-900 dark:text-white uppercase tracking-wider flex items-center gap-2">
            <Layers className="w-4 h-4 text-indigo-500" />
            Hierarchical Strategic Goal Tree
          </h3>
          <span className="text-xs text-gray-500">Automatic Reprioritization Active</span>
        </div>

        <div className="grid grid-cols-1 gap-4">
          {goals.map((goal) => (
            <Card key={goal.id} className="p-5 hover:shadow-md transition-shadow">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 pb-3 border-b border-gray-100 dark:border-gray-800">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-mono text-xs text-indigo-600 dark:text-indigo-400 font-semibold">{goal.id}</span>
                    <Badge variant={getPriorityBadgeVariant(goal.priority)} size="sm">
                      {goal.priority}
                    </Badge>
                    <Badge variant="outline" size="sm">
                      {goal.horizon}
                    </Badge>
                  </div>
                  <h4 className="font-semibold text-gray-900 dark:text-white text-base mt-1">{goal.title}</h4>
                  <p className="text-xs text-gray-500 dark:text-gray-400 mt-0.5">{goal.description}</p>
                </div>
                <div className="flex items-center gap-3 flex-shrink-0">
                  <div className="text-right">
                    <span className="text-xs text-gray-400 block">Utility Score</span>
                    <span className="text-lg font-bold text-indigo-600 dark:text-indigo-400 font-mono">
                      {goal.utilityScore.toFixed(3)}
                    </span>
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-2 md:grid-cols-5 gap-3 mt-4 text-xs">
                <div className="p-2.5 bg-gray-50 dark:bg-gray-900/40 rounded border border-gray-100 dark:border-gray-800">
                  <span className="text-gray-400 block mb-0.5">Budget Req</span>
                  <span className="font-semibold text-gray-800 dark:text-gray-200 font-mono">
                    ${goal.costUsd.toLocaleString()}
                  </span>
                </div>
                <div className="p-2.5 bg-gray-50 dark:bg-gray-900/40 rounded border border-gray-100 dark:border-gray-800">
                  <span className="text-gray-400 block mb-0.5">Latency Reduction</span>
                  <span className="font-semibold text-emerald-600 dark:text-emerald-400 font-mono">
                    +{goal.latencyGainPct}%
                  </span>
                </div>
                <div className="p-2.5 bg-gray-50 dark:bg-gray-900/40 rounded border border-gray-100 dark:border-gray-800">
                  <span className="text-gray-400 block mb-0.5">Confidence</span>
                  <span className="font-semibold text-purple-600 dark:text-purple-400 font-mono">
                    {(goal.confidence * 100).toFixed(1)}%
                  </span>
                </div>
                <div className="p-2.5 bg-gray-50 dark:bg-gray-900/40 rounded border border-gray-100 dark:border-gray-800">
                  <span className="text-gray-400 block mb-0.5">Goal Age</span>
                  <span className="font-semibold text-gray-700 dark:text-gray-300 font-mono">
                    {goal.ageDays} days
                  </span>
                </div>
                <div className="p-2.5 bg-gray-50 dark:bg-gray-900/40 rounded border border-gray-100 dark:border-gray-800">
                  <span className="text-gray-400 block mb-0.5">Subgoals Decomposed</span>
                  <span className="font-semibold text-indigo-600 dark:text-indigo-400 font-mono">
                    {goal.subgoalsCount} subtasks
                  </span>
                </div>
              </div>

              <div className="mt-3 flex items-center justify-between text-xs pt-2">
                <div className="flex items-center gap-1.5 flex-wrap">
                  {goal.tags.map((t, idx) => (
                    <span key={idx} className="px-2 py-0.5 bg-indigo-50 dark:bg-indigo-950/30 text-indigo-600 dark:text-indigo-400 rounded-full font-mono text-[10px]">
                      #{t}
                    </span>
                  ))}
                </div>
                <span className="text-emerald-600 dark:text-emerald-400 flex items-center gap-1 font-medium">
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  Status: {goal.status}
                </span>
              </div>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
};
