import React, { useState, useEffect } from 'react';
import {
  Users,
  RefreshCw,
  Trophy,
  DollarSign,
  Vote,
} from 'lucide-react';
import { CognitiveEvolutionApiClient } from '../../services/cognitiveEvolutionApiClient';
import { DeliberationSessionSummaryPayload } from '../../types/cognitiveEvolution';

export const MultiAgentCouncilPanel: React.FC = () => {
  const [session, setSession] = useState<DeliberationSessionSummaryPayload | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    loadCouncilSession();
  }, []);

  const loadCouncilSession = async () => {
    setLoading(true);
    try {
      const data = await CognitiveEvolutionApiClient.conveneCouncilDeliberation('mission_council_alpha');
      setSession(data);
    } catch (e) {
      console.error('Failed to convene council session:', e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 font-mono">
      {/* Top Banner & Consensus Verdict */}
      <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-3">
          <div>
            <h3 className="text-sm font-bold text-cyan-300 flex items-center gap-2">
              <Users className="w-4 h-4 text-cyan-400" />
              Autonomous Multi-Agent Deliberation Council (8 Specialized Agents)
            </h3>
            <p className="text-xs text-slate-400 mt-0.5">
              Structured pre-execution debate, preference ranking aggregation, Borda voting, and incentive-compatible Vickrey auctions.
            </p>
          </div>

          <button
            onClick={loadCouncilSession}
            disabled={loading}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-cyan-950/50 hover:bg-cyan-900/60 border border-cyan-800 text-cyan-300 rounded-lg text-xs font-bold transition-all disabled:opacity-50"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
            Re-deliberate Council
          </button>
        </div>

        {/* Verdict Callout */}
        <div className="p-4 bg-cyan-950/30 border border-cyan-800/60 rounded-lg flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs">
          <div className="flex items-center gap-2 text-cyan-300">
            <Trophy className="w-4 h-4 text-amber-400 shrink-0" />
            <span className="font-bold">{session?.voting_tally.deliberation_verdict}</span>
          </div>
          <div className="text-[11px] text-slate-400 shrink-0">
            Consensus Entropy:{' '}
            <span className="text-purple-300 font-bold">{session?.voting_tally.consensus_entropy_bits.toFixed(3)} bits</span>
          </div>
        </div>
      </div>

      {/* Agents Arguments & Borda Tally Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left: 8 Agent Advocacy Stream */}
        <div className="lg:col-span-2 space-y-3">
          <div className="text-xs uppercase text-slate-400 tracking-wider">Agent Deliberation Arguments</div>
          <div className="space-y-2.5">
            {session?.agent_arguments.map((arg) => (
              <div
                key={arg.agent_id}
                className="p-3.5 bg-slate-900/80 border border-slate-800/90 rounded-lg space-y-1.5 text-xs"
              >
                <div className="flex items-center justify-between">
                  <span className="font-bold text-slate-200 flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full bg-cyan-400" />
                    {arg.agent_role}
                  </span>
                  <span className="text-[10px] px-2 py-0.5 rounded bg-slate-800 text-cyan-300 border border-slate-700">
                    Voted: {arg.preferred_strategy_id}
                  </span>
                </div>
                <p className="text-[11px] text-slate-400 pl-4">{arg.advocacy_argument}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Right: Borda Points Table & Vickrey Auction Ledger */}
        <div className="space-y-4">
          <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-4 space-y-3">
            <div className="text-xs uppercase text-slate-400 tracking-wider flex items-center gap-1.5">
              <Vote className="w-3.5 h-3.5 text-cyan-400" />
              Borda Point Standings
            </div>
            <div className="space-y-2">
              {Object.entries(session?.voting_tally.borda_points || {}).map(([strat, pts], idx) => (
                <div key={strat} className="flex items-center justify-between p-2 bg-slate-950/70 border border-slate-800 rounded text-xs">
                  <span className="text-slate-300 font-bold">{idx + 1}. {strat}</span>
                  <span className="text-emerald-400 font-bold">{pts} pts</span>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-4 space-y-3">
            <div className="text-xs uppercase text-slate-400 tracking-wider flex items-center gap-1.5">
              <DollarSign className="w-3.5 h-3.5 text-amber-400" />
              Vickrey Second-Price Auction Ledger
            </div>
            <div className="p-3 bg-slate-950/80 border border-slate-800 rounded text-xs space-y-1">
              <div className="text-slate-300 font-bold">Task: task_neural_ocr</div>
              <div className="text-slate-400">Winning Agent: <span className="text-cyan-300">RISK_AGENT</span></div>
              <div className="text-slate-400">Clearing Price: <span className="text-emerald-400">10.0 credits</span></div>
              <div className="text-[10px] text-slate-500">Incentive-compatible second price settlement</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
