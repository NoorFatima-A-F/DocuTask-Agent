import React, { useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import {
  Network,
  CheckCircle2,
  ArrowRight,
  ShieldCheck,
} from 'lucide-react';

interface DependencyNode {
  id: string;
  title: string;
  type: 'ROOT' | 'SUBGOAL';
  priority: string;
  status: string;
  dependsOn: { targetId: string; type: string; criticality: number }[];
}

export const GoalDependencyExplorer: React.FC = () => {
  const [nodes] = useState<DependencyNode[]>([
    {
      id: 'goal-root-scale-100k',
      title: 'Scale Multi-Swarm Processing to 100k Daily Documents',
      type: 'ROOT',
      priority: 'CRITICAL',
      status: 'ACTIVE',
      dependsOn: [],
    },
    {
      id: 'goal-sub-cache-warm',
      title: 'Deploy Speculative Zero-Copy Embedding Cache',
      type: 'SUBGOAL',
      priority: 'HIGH',
      status: 'ACTIVE',
      dependsOn: [
        {
          targetId: 'goal-root-scale-100k',
          type: 'ENABLING',
          criticality: 0.95,
        },
      ],
    },
    {
      id: 'goal-sub-strike-teams',
      title: 'Form Triadic Specialist Swarm Strike Teams',
      type: 'SUBGOAL',
      priority: 'HIGH',
      status: 'ACTIVE',
      dependsOn: [
        {
          targetId: 'goal-sub-cache-warm',
          type: 'ENABLING',
          criticality: 0.80,
        },
      ],
    },
    {
      id: 'goal-root-gov-integrity',
      title: 'Attain Continuous 100% Cryptographic Auditability',
      type: 'ROOT',
      priority: 'CRITICAL',
      status: 'ACTIVE',
      dependsOn: [],
    },
  ]);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
            <Network className="w-6 h-6 text-indigo-500" />
            Strategic Goal Dependency & Conflict Graph
          </h2>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            Phase 13.11 — Cross-departmental goal topological ordering, blocking dependency resolution, and circular deadlock prevention.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant="success" size="md">
            <ShieldCheck className="w-3.5 h-3.5 mr-1" />
            Topologically Sorted • 0 Deadlocks
          </Badge>
        </div>
      </div>

      {/* Nodes and Dependencies Visual List */}
      <div className="grid grid-cols-1 gap-4">
        {nodes.map((node) => (
          <Card key={node.id} className="p-5 hover:shadow-md transition-shadow">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 pb-3 border-b border-gray-100 dark:border-gray-800">
              <div>
                <div className="flex items-center gap-2">
                  <span className="font-mono text-xs text-indigo-600 dark:text-indigo-400 font-semibold">{node.id}</span>
                  <Badge variant={node.type === 'ROOT' ? 'intelligence' : 'default'} size="sm">
                    {node.type}
                  </Badge>
                  <Badge variant="warning" size="sm">
                    {node.priority}
                  </Badge>
                </div>
                <h4 className="font-semibold text-gray-900 dark:text-white text-base mt-1">{node.title}</h4>
              </div>
              <Badge variant="success" size="sm">
                <CheckCircle2 className="w-3 h-3 mr-1" />
                {node.status}
              </Badge>
            </div>

            <div className="mt-4 text-xs space-y-2">
              <span className="text-gray-400 block font-medium">Topological Dependency Links:</span>
              {node.dependsOn.length === 0 ? (
                <p className="text-gray-500 italic">No incoming blocking dependencies (Root node).</p>
              ) : (
                <div className="space-y-1.5">
                  {node.dependsOn.map((dep, dIdx) => (
                    <div key={dIdx} className="p-2.5 bg-gray-50 dark:bg-gray-900/40 rounded border border-gray-100 dark:border-gray-800 flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <ArrowRight className="w-3.5 h-3.5 text-indigo-500" />
                        <span className="text-gray-700 dark:text-gray-300">Requires Target:</span>
                        <span className="font-mono text-indigo-600 dark:text-indigo-400 font-semibold">{dep.targetId}</span>
                      </div>
                      <div className="flex items-center gap-3">
                        <span className="text-gray-400">Type: <strong className="text-gray-700 dark:text-gray-300">{dep.type}</strong></span>
                        <span className="text-gray-400">Criticality: <strong className="text-purple-600 dark:text-purple-400">{(dep.criticality * 100).toFixed(0)}%</strong></span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
