/**
 * Phase 13.16: Autonomous World Modeling, Predictive Intelligence & Causal Reasoning Platform (AWMPICRP)
 * View 12: World Evolution Timeline & Event Stream
 */

import React, { useEffect, useState } from 'react';
import {
  Clock,
  RefreshCw,
  Activity,
  Sparkles,
  Zap,
  Brain,
  GitBranch,
  Flame,
} from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { WorldModelApiClient } from '../../services/worldModelApiClient';
import { WorldModelEvent, CognitiveMemoryRecord } from '../../types/worldModelPlatform';

export const WorldEvolutionTimeline: React.FC = () => {
  const [events, setEvents] = useState<WorldModelEvent[]>([]);
  const [memories, setMemories] = useState<CognitiveMemoryRecord[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [evRes, memRes] = await Promise.all([
        WorldModelApiClient.getEvents(50),
        WorldModelApiClient.getMemoryRecords(),
      ]);
      setEvents(evRes.events || []);
      setMemories(memRes.records || []);
    } catch (err) {
      console.error('Error fetching evolution timeline data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const getEventIcon = (type: string) => {
    if (type.includes('knowledge')) return Brain;
    if (type.includes('causal')) return GitBranch;
    if (type.includes('hypothesis')) return Flame;
    if (type.includes('scenario') || type.includes('counterfactual')) return Sparkles;
    return Zap;
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/80 border border-emerald-500/30 rounded-xl p-6">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-emerald-500/10 border border-emerald-500/30 rounded-lg text-emerald-400">
            <Clock className="w-6 h-6" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-2xl font-bold text-white tracking-tight">World Evolution Timeline</h1>
              <Badge variant="intelligence">Memory Consolidation & Audit</Badge>
            </div>
            <p className="text-sm text-slate-400">
              Audit trail of continuous world updates, cognitive learning cycles, and multi-tier memory retention.
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <Button variant="outline" onClick={fetchData} disabled={loading}>
            <span className="flex items-center gap-2">
              <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
              Refresh
            </span>
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Events Audit Trail Stream */}
        <div className="lg:col-span-2 space-y-4">
          <h3 className="text-base font-semibold text-white flex items-center gap-2">
            <Activity className="w-5 h-5 text-emerald-400" />
            Live World Model Event Stream ({events.length})
          </h3>

          <div className="space-y-3">
            {events.map((evt) => {
              const Icon = getEventIcon(evt.event_type);
              return (
                <div
                  key={evt.event_id}
                  className="p-4 bg-slate-900/60 rounded-lg border border-slate-800 space-y-2 hover:border-slate-700 transition-all text-xs"
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <div className="p-1.5 bg-slate-800 rounded text-emerald-400">
                        <Icon className="w-4 h-4" />
                      </div>
                      <span className="font-mono text-emerald-400 font-semibold">{evt.event_type}</span>
                    </div>
                    <span className="text-[11px] text-slate-400">
                      {new Date(evt.timestamp || Date.now()).toLocaleTimeString()}
                    </span>
                  </div>

                  <pre className="p-2.5 bg-slate-950/80 rounded border border-slate-800/80 font-mono text-[11px] text-slate-300 whitespace-pre-wrap overflow-x-auto">
                    {JSON.stringify(evt.payload || {}, null, 2)}
                  </pre>
                </div>
              );
            })}
          </div>
        </div>

        {/* Consolidated Cognitive Memories */}
        <div className="space-y-4">
          <h3 className="text-base font-semibold text-white flex items-center gap-2">
            <Brain className="w-5 h-5 text-purple-400" />
            Consolidated Cognitive Memory
          </h3>

          <div className="space-y-3">
            {memories.map((mem) => (
              <Card key={mem.record_id} className="bg-slate-900/60 border-slate-800 p-4 space-y-2.5">
                <div className="flex items-center justify-between">
                  <Badge variant="intelligence">{mem.tier}</Badge>
                  <span className="text-[10px] text-slate-400 font-mono">
                    Importance: {Math.round((mem.importance_score || 0.9) * 100)}%
                  </span>
                </div>

                <div className="text-xs font-semibold text-slate-200">
                  {mem.content?.concept || mem.content?.lesson || JSON.stringify(mem.content)}
                </div>

                <div className="flex items-center justify-between text-[11px] text-slate-400 pt-1">
                  <span>Access Count: <strong className="text-white">{mem.access_count || 1}</strong></span>
                  <div className="flex gap-1">
                    {(mem.associations || ['world_model']).slice(0, 3).map((a, i) => (
                      <span key={i} className="px-1.5 py-0.5 rounded bg-slate-800 text-[10px] text-slate-300">
                        {a}
                      </span>
                    ))}
                  </div>
                </div>
              </Card>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
