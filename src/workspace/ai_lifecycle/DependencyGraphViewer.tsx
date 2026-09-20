import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { AILifecycleApiClient } from '../../services/aiLifecycleApiClient';
import type { AgentDependency } from '../../types/aiLifecycle';
import { Network, CheckCircle2, RefreshCw } from 'lucide-react';

export const DependencyGraphViewer: React.FC = () => {
  const [dependencies, setDependencies] = useState<AgentDependency[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      const list = await AILifecycleApiClient.listDependencies('agt_acme_invoice_reconciler');
      setDependencies(list);
      setLoading(false);
    };
    load();
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-3">
            <Network className="w-7 h-7 text-indigo-400" />
            Agent Dependency DAG & Breaking Change Inspector
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Tracks relationships between agents, tools, models, connectors, datasets, and policies.
          </p>
        </div>
      </div>

      <Card className="bg-slate-900/80 border-slate-800">
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="text-base text-white">Dependency Graph for Autonomous Invoice Reconciler</CardTitle>
            <Badge variant="success" className="flex items-center gap-1">
              <CheckCircle2 className="w-3.5 h-3.5" /> No Breaking Changes
            </Badge>
          </div>
        </CardHeader>
        <CardContent className="space-y-3">
          {loading ? (
            <div className="p-8 text-center text-slate-400">
              <RefreshCw className="w-6 h-6 animate-spin mx-auto mb-2" /> Loading Dependency DAG...
            </div>
          ) : (
            dependencies.map((dep) => (
              <div
                key={dep.dep_id}
                className="p-3 bg-slate-800/40 rounded border border-slate-700/50 flex items-center justify-between"
              >
                <div>
                  <div className="flex items-center gap-2">
                    <Badge variant="intelligence">{dep.dependency_type}</Badge>
                    <span className="text-sm font-semibold text-white">{dep.target_resource_name}</span>
                  </div>
                  <span className="text-xs text-slate-400 font-mono mt-1 block">{dep.target_resource_id}</span>
                </div>
                <Badge variant={dep.is_breaking_change ? 'error' : 'outline'}>
                  {dep.is_breaking_change ? 'BREAKING' : 'COMPATIBLE'}
                </Badge>
              </div>
            ))
          )}
        </CardContent>
      </Card>
    </div>
  );
};
