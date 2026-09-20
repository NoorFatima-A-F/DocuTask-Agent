import React, { useState, useEffect } from 'react';
import {
  History,
  RefreshCw,
} from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { AIOperationsApiClient } from '../../services/aiOperationsApiClient';

export const AIEvolutionTimeline: React.FC = () => {
  const [events, setEvents] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const loadTimeline = async () => {
    try {
      setLoading(true);
      const [prompts, exps, proposals, logs] = await Promise.all([
        AIOperationsApiClient.getPrompts(),
        AIOperationsApiClient.getExperiments(),
        AIOperationsApiClient.getProposals(),
        AIOperationsApiClient.getGovernanceAuditLogs(),
      ]);

      const mergedEvents = [
        ...prompts.map((p) => ({
          id: p.prompt_id,
          title: `Prompt Version ${p.version} Created`,
          category: 'PROMPT',
          agent: p.agent_id,
          details: p.mutation_notes || 'System instruction baseline',
          timestamp: p.created_at,
          status: p.active ? 'ACTIVE' : 'CANDIDATE',
        })),
        ...exps.map((e) => ({
          id: e.experiment_id,
          title: `Canary Experiment: ${e.name}`,
          category: 'EXPERIMENT',
          agent: e.agent_id,
          details: `Validated ${e.candidate_version} vs ${e.control_version} (p=${e.p_value})`,
          timestamp: e.started_at,
          status: e.status,
        })),
        ...proposals.map((pr) => ({
          id: pr.proposal_id,
          title: `Self-Improvement Proposal: ${pr.title}`,
          category: 'PROPOSAL',
          agent: pr.target_agent_id,
          details: `Expected quality gain: +${(pr.expected_quality_delta * 100).toFixed(0)}%`,
          timestamp: pr.created_at,
          status: pr.status,
        })),
        ...logs.map((l) => ({
          id: l.audit_id,
          title: `Governance Event: ${l.event_type}`,
          category: 'GOVERNANCE',
          agent: l.agent_id || 'System',
          details: l.action_summary,
          timestamp: l.timestamp,
          status: l.compliance_passed ? 'COMPLIANT' : 'FLAGGED',
        })),
      ];

      mergedEvents.sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime());
      setEvents(mergedEvents);
    } catch (err) {
      console.error('Failed to load evolution timeline:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadTimeline();
  }, []);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between bg-slate-900/60 p-5 rounded-2xl border border-slate-800 backdrop-blur-md">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-indigo-500/10 rounded-xl border border-indigo-500/20">
            <History className="w-6 h-6 text-indigo-400" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-white">AI Evolution & Operational Timeline</h1>
            <p className="text-xs text-slate-400">Chronological history of prompts, canary validations, model upgrades, and governance checkpoints</p>
          </div>
        </div>
        <Button variant="outline" onClick={loadTimeline} disabled={loading}>
          <span className="flex items-center gap-2">
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            Refresh
          </span>
        </Button>
      </div>

      {/* Timeline Stream */}
      <Card className="p-6 bg-slate-900/50 border-slate-800">
        <div className="space-y-6 relative before:absolute before:inset-0 before:left-3.5 before:w-0.5 before:bg-slate-800">
          {events.map((ev, idx) => (
            <div key={ev.id || idx} className="relative flex items-start gap-4 pl-8">
              <div
                className={`absolute left-2 top-1.5 w-3.5 h-3.5 rounded-full border-2 border-slate-950 ${
                  ev.category === 'PROMPT'
                    ? 'bg-purple-400'
                    : ev.category === 'EXPERIMENT'
                    ? 'bg-cyan-400'
                    : ev.category === 'PROPOSAL'
                    ? 'bg-indigo-400'
                    : 'bg-emerald-400'
                }`}
              />
              <div className="flex-1 bg-slate-950/60 p-4 rounded-xl border border-slate-800/80 hover:border-slate-700/80 transition-colors">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Badge
                      variant={
                        ev.category === 'PROMPT'
                          ? 'intelligence'
                          : ev.category === 'EXPERIMENT'
                          ? 'info'
                          : ev.category === 'PROPOSAL'
                          ? 'sentinel'
                          : 'success'
                      }
                    >
                      {ev.category}
                    </Badge>
                    <span className="text-xs font-semibold text-slate-300 font-mono">{ev.agent}</span>
                  </div>
                  <span className="text-[11px] text-slate-500">{new Date(ev.timestamp).toLocaleString()}</span>
                </div>

                <h3 className="font-semibold text-white text-sm mt-2">{ev.title}</h3>
                <p className="text-xs text-slate-400 mt-1">{ev.details}</p>

                <div className="mt-2.5 flex items-center justify-between text-[11px] text-slate-500 border-t border-slate-800/60 pt-2">
                  <span className="font-mono">ID: {ev.id}</span>
                  <Badge variant="outline">{ev.status}</Badge>
                </div>
              </div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
};
