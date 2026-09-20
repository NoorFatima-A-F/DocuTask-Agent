import React, { useState, useEffect } from 'react';
import {
  Sparkles,
  CheckCircle2,
  XCircle,
  RefreshCw,
} from 'lucide-react';
import { DecisionIntelligenceApiClient } from '../../services/decisionIntelligenceApiClient';
import { SensingActionRecommendation } from '../../types/decisionIntelligence';

export const EVOIExplorerPanel: React.FC = () => {
  const [recommendations, setRecommendations] = useState<SensingActionRecommendation[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [systemEntropy, setSystemEntropy] = useState<number>(3.42);

  useEffect(() => {
    loadEVOI();
  }, []);

  const loadEVOI = async () => {
    setLoading(true);
    try {
      const data = await DecisionIntelligenceApiClient.evaluateEVOI();
      setRecommendations(data.recommendations);
      setSystemEntropy(data.current_system_entropy);
    } catch (e) {
      console.error('Failed to load EVOI recommendations:', e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header & Entropy Tradeoff Banner */}
      <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-3">
          <div>
            <h3 className="text-sm font-bold font-mono text-cyan-300 flex items-center gap-2">
              <Sparkles className="w-4 h-4 text-cyan-400" />
              Active Information Gathering & Expected Value of Information (EVOI)
            </h3>
            <p className="text-xs text-slate-400 mt-0.5">
              Strict mathematical gating of sensing actions: only execute exploratory probes when Expected Information Gain &gt; Execution Delay & Token Cost.
            </p>
          </div>

          <button
            onClick={loadEVOI}
            disabled={loading}
            className="flex items-center gap-2 px-3 py-1.5 bg-cyan-950/40 hover:bg-cyan-900/50 border border-cyan-800 text-cyan-300 rounded-lg text-xs font-mono transition-all disabled:opacity-50 self-start sm:self-auto"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
            Recalculate EVOI
          </button>
        </div>

        {/* LaTeX EVOI Formula Bar */}
        <div className="p-3 bg-slate-950/90 border border-slate-800 rounded-lg flex flex-col md:flex-row md:items-center justify-between gap-3 text-xs font-mono">
          <div className="text-purple-300 flex items-center gap-2">
            <span className="text-slate-400">Objective:</span>
            <span className="font-bold">
              EVOI(A) = E_o[max_a U(a, b_o)] - max_a U(a, b) - Cost(A)
            </span>
          </div>
          <div className="text-slate-400 text-right text-[11px]">
            Current Shannon Entropy: <span className="text-cyan-300 font-bold">{systemEntropy.toFixed(3)} bits</span>
          </div>
        </div>
      </div>

      {/* Sensing Action Candidates Cards */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h4 className="text-xs font-mono uppercase tracking-wider text-slate-400">
            Evaluated Sensing Actions ({recommendations.length})
          </h4>
          <span className="text-[10px] font-mono text-slate-500">
            Sorted by Net EVOI (Highest Utility Yield First)
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {recommendations.map((rec) => {
            const isPositive = rec.net_evoi > 0;
            return (
              <div
                key={rec.action_id}
                className={`bg-slate-900/90 border rounded-xl p-5 space-y-4 transition-all ${
                  rec.recommended
                    ? 'border-emerald-500/50 shadow-lg shadow-emerald-950/20'
                    : 'border-slate-800/90 opacity-80'
                }`}
              >
                <div className="flex items-start justify-between">
                  <div>
                    <h5 className="text-sm font-bold font-mono text-slate-100 flex items-center gap-2">
                      {rec.action_id}
                    </h5>
                    <span className="text-[10px] font-mono text-cyan-400 uppercase">
                      Target: {rec.target_variable}
                    </span>
                  </div>

                  <span
                    className={`px-2.5 py-1 rounded text-xs font-mono font-bold flex items-center gap-1.5 border ${
                      rec.recommended
                        ? 'bg-emerald-950/80 text-emerald-300 border-emerald-800'
                        : 'bg-rose-950/80 text-rose-300 border-rose-800'
                    }`}
                  >
                    {rec.recommended ? (
                      <>
                        <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                        RECOMMENDED
                      </>
                    ) : (
                      <>
                        <XCircle className="w-3.5 h-3.5 text-rose-400" />
                        REJECTED (COST EXCESS)
                      </>
                    )}
                  </span>
                </div>

                {/* Quantitative Tradeoff Grid */}
                <div className="grid grid-cols-3 gap-2">
                  <div className="bg-slate-950/70 border border-slate-800 rounded-lg p-2.5 text-center">
                    <div className="text-[10px] font-mono text-slate-400 uppercase">Info Gain ΔH</div>
                    <div className="text-sm font-bold font-mono text-cyan-300 mt-0.5">
                      +{rec.expected_information_gain_bits.toFixed(2)} b
                    </div>
                  </div>

                  <div className="bg-slate-950/70 border border-slate-800 rounded-lg p-2.5 text-center">
                    <div className="text-[10px] font-mono text-slate-400 uppercase">Delay Penalty</div>
                    <div className="text-sm font-bold font-mono text-amber-300 mt-0.5">
                      -{(rec.delay_penalty * 100).toFixed(1)}%
                    </div>
                  </div>

                  <div className="bg-slate-950/70 border border-slate-800 rounded-lg p-2.5 text-center">
                    <div className="text-[10px] font-mono text-slate-400 uppercase">Net EVOI Yield</div>
                    <div
                      className={`text-sm font-bold font-mono mt-0.5 ${
                        isPositive ? 'text-emerald-400' : 'text-rose-400'
                      }`}
                    >
                      {isPositive ? '+' : ''}
                      {rec.net_evoi.toFixed(4)}
                    </div>
                  </div>
                </div>

                {/* Scientific Rationale */}
                <div className="p-3 bg-slate-950/80 border border-slate-800/80 rounded-lg text-xs font-mono text-slate-300">
                  <span className="text-slate-400">Scientific Provenance: </span>
                  {rec.scientific_rationale}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
