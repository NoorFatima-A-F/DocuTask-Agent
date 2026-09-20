import React, { useState, useEffect } from 'react';
import { Cpu, RefreshCw } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { knowledgeApiClient } from '../../services/knowledgeApiClient';
import { MemoryEntry } from '../../types/knowledge';

export const MemoryObservatory: React.FC = () => {
  const [memories, setMemories] = useState<MemoryEntry[]>([]);
  const [filterTier, setFilterTier] = useState<string>('ALL');

  const loadMemories = async () => {
    const data = await knowledgeApiClient.listMemories();
    setMemories(data);
  };

  useEffect(() => {
    loadMemories();
  }, []);

  const filtered = memories.filter(m => filterTier === 'ALL' || m.tier === filterTier);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-slate-100 flex items-center gap-2">
            <Cpu className="w-7 h-7 text-indigo-400" />
            Autonomous Agent Memory Observatory
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Observe working memory, episodic history, organizational knowledge, and procedural execution SOPs.
          </p>
        </div>
        <Button variant="outline" onClick={loadMemories}>
          <span className="flex items-center gap-2">
            <RefreshCw className="w-4 h-4" />
            Refresh Memories
          </span>
        </Button>
      </div>

      <div className="flex gap-2">
        {['ALL', 'SHORT_TERM', 'LONG_TERM', 'ORGANIZATIONAL', 'PROCEDURAL'].map((tier) => (
          <Button
            key={tier}
            variant={filterTier === tier ? 'primary' : 'outline'}
            size="sm"
            onClick={() => setFilterTier(tier)}
          >
            {tier.replace('_', ' ')}
          </Button>
        ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {filtered.map((mem) => (
          <Card key={mem.id} className="p-4 bg-slate-900/60 border-slate-800 space-y-3">
            <div className="flex justify-between items-center">
              <Badge variant="outline" className="text-indigo-400 border-indigo-500/30">
                {mem.tier}
              </Badge>
              <span className="text-xs font-mono text-slate-400">Access: {mem.access_count}x</span>
            </div>
            <h3 className="text-base font-semibold text-slate-200">{mem.key}</h3>
            <p className="text-xs text-slate-300 bg-slate-800/40 p-3 rounded border border-slate-700">
              {mem.content}
            </p>
          </Card>
        ))}
      </div>
    </div>
  );
};
