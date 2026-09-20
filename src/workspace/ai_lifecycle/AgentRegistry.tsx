import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { AILifecycleApiClient } from '../../services/aiLifecycleApiClient';
import type { AgentApplication } from '../../types/aiLifecycle';
import { Box, User, Tag, Calendar, RefreshCw } from 'lucide-react';

export const AgentRegistry: React.FC = () => {
  const [agents, setAgents] = useState<AgentApplication[]>([]);
  const [loading, setLoading] = useState(true);
  const [filterCategory, setFilterCategory] = useState<string>('ALL');

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      const list = await AILifecycleApiClient.listAgents();
      setAgents(list);
      setLoading(false);
    };
    load();
  }, []);

  const filtered = filterCategory === 'ALL' ? agents : agents.filter((a) => a.category === filterCategory);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-3">
            <Box className="w-7 h-7 text-indigo-400" />
            Enterprise Agent Registry & Asset Catalog
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Centralized inventory of all governed AI applications, owners, version tags, and lifecycle states.
          </p>
        </div>
        <div className="flex gap-2">
          {['ALL', 'FINANCIAL_AUDIT', 'COMPLIANCE', 'LEGAL_ANALYSIS', 'AUTOMATION'].map((cat) => (
            <button
              key={cat}
              onClick={() => setFilterCategory(cat)}
              className={`px-3 py-1 text-xs rounded-lg border transition ${
                filterCategory === cat
                  ? 'bg-indigo-600 text-white border-indigo-500'
                  : 'bg-slate-800 text-slate-400 border-slate-700 hover:text-white'
              }`}
            >
              {cat}
            </button>
          ))}
        </div>
      </div>

      {loading ? (
        <div className="p-12 text-center text-slate-400">
          <RefreshCw className="w-6 h-6 animate-spin mx-auto mb-2" /> Loading Registry...
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {filtered.map((agent) => (
            <Card key={agent.agent_id} className="bg-slate-900/80 border-slate-800 flex flex-col justify-between">
              <CardHeader>
                <div className="flex items-center justify-between mb-2">
                  <Badge variant="intelligence">{agent.category}</Badge>
                  <Badge variant={agent.lifecycle_state === 'DEPLOYED' ? 'success' : 'warning'}>
                    {agent.lifecycle_state}
                  </Badge>
                </div>
                <CardTitle className="text-lg text-white">{agent.name}</CardTitle>
                <span className="text-xs font-mono text-slate-400">{agent.agent_id}</span>
              </CardHeader>
              <CardContent className="space-y-4">
                <p className="text-xs text-slate-300">{agent.description}</p>

                <div className="grid grid-cols-2 gap-2 text-xs bg-slate-800/40 p-3 rounded border border-slate-700/50">
                  <div className="flex items-center gap-2">
                    <User className="w-4 h-4 text-indigo-400" />
                    <div>
                      <span className="text-slate-400 block text-[10px]">Owner</span>
                      <span className="text-slate-200 font-medium truncate block">{agent.owner_email}</span>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <Calendar className="w-4 h-4 text-cyan-400" />
                    <div>
                      <span className="text-slate-400 block text-[10px]">Version</span>
                      <span className="text-slate-200 font-mono font-medium">v{agent.current_version}</span>
                    </div>
                  </div>
                </div>

                <div className="flex flex-wrap gap-1.5 pt-2 border-t border-slate-800">
                  {agent.tags.map((t) => (
                    <span key={t} className="text-[10px] bg-slate-800 text-slate-400 px-2 py-0.5 rounded border border-slate-700 flex items-center gap-1">
                      <Tag className="w-2.5 h-2.5" /> {t}
                    </span>
                  ))}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};
