import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const NegotiationStudioView: React.FC = () => {
  const [selectedTab, setSelectedTab] = useState<'AUCTIONS' | 'TRADES' | 'CONTRACTS' | 'NASH'>('AUCTIONS');

  const auctions = [
    {
      id: 'auc_gpu_2026_01',
      resource: 'GPU_OCR_SLOT (4 Units)',
      winner: 'Extraction Department',
      winningBid: '85.0 Credits',
      clearingPrice: '62.0 Credits (Vickrey 2nd Price)',
      status: 'SETTLED',
      bids: [
        { dept: 'Extraction Department', amount: '85.0', utility: '0.95' },
        { dept: 'OCR Department', amount: '62.0', utility: '0.80' },
        { dept: 'Research Department', amount: '45.0', utility: '0.65' },
      ],
    },
  ];

  const trades = [
    {
      id: 'prop_trade_001',
      initiator: 'OCR Department',
      target: 'Research Department',
      offered: '2x OCR Worker Threads',
      requested: '50,000 Gemini Pro Tokens',
      duration: '300 seconds',
      status: 'ACCEPTED',
      rationale: 'Trading idle night worker threads for research token quota to parse multi-page dense ledger.',
    },
  ];

  const contracts = [
    {
      id: 'ctr_ocr_ext_001',
      provider: 'OCR Department',
      consumer: 'Extraction Department',
      resource: 'OCR_BOUNDING_BOX_STREAM',
      committedCapacity: '10.0 docs/sec',
      slaLatency: '< 250 ms',
      penaltyRate: '2.5 credits/sec',
      signature: 'ED25519_SIG_8F3A20B1',
      status: 'ACTIVE',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Top Controls */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 p-5 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-xl">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-2xl">⚖️</span>
            <h2 className="text-xl font-bold text-[#F8FAFC]">Autonomous Resource Negotiation & Market Floor</h2>
            <Badge variant="intelligence" size="sm">Game-Theoretic Economy</Badge>
          </div>
          <p className="text-sm text-[#94A3B8] mt-1">
            Vickrey second-price auctions, bilateral resource trades, Nash Bargaining allocations, and signed SLA contracts.
          </p>
        </div>

        <div className="flex gap-2">
          <button
            onClick={() => setSelectedTab('AUCTIONS')}
            className={`px-3 py-1.5 rounded-lg text-xs font-mono font-semibold transition-all ${
              selectedTab === 'AUCTIONS' ? 'bg-[#0066FF] text-white' : 'bg-[#1E293B] text-[#94A3B8] hover:text-white'
            }`}
          >
            Vickrey Auctions
          </button>
          <button
            onClick={() => setSelectedTab('TRADES')}
            className={`px-3 py-1.5 rounded-lg text-xs font-mono font-semibold transition-all ${
              selectedTab === 'TRADES' ? 'bg-[#0066FF] text-white' : 'bg-[#1E293B] text-[#94A3B8] hover:text-white'
            }`}
          >
            Bilateral Trades
          </button>
          <button
            onClick={() => setSelectedTab('CONTRACTS')}
            className={`px-3 py-1.5 rounded-lg text-xs font-mono font-semibold transition-all ${
              selectedTab === 'CONTRACTS' ? 'bg-[#0066FF] text-white' : 'bg-[#1E293B] text-[#94A3B8] hover:text-white'
            }`}
          >
            SLA Contracts
          </button>
          <button
            onClick={() => setSelectedTab('NASH')}
            className={`px-3 py-1.5 rounded-lg text-xs font-mono font-semibold transition-all ${
              selectedTab === 'NASH' ? 'bg-[#0066FF] text-white' : 'bg-[#1E293B] text-[#94A3B8] hover:text-white'
            }`}
          >
            Nash Bargaining
          </button>
        </div>
      </div>

      {/* Tab Panels */}
      {selectedTab === 'AUCTIONS' && (
        <div className="space-y-4">
          {auctions.map((auc) => (
            <Card key={auc.id} className="p-5 bg-[#0F172A] border-[#1E293B] space-y-4">
              <div className="flex items-start justify-between">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-base font-bold text-[#F8FAFC]">{auc.resource}</span>
                    <Badge variant="success" size="sm">{auc.status}</Badge>
                  </div>
                  <div className="text-xs text-[#94A3B8] font-mono mt-1">
                    Winner: <span className="text-[#38BDF8] font-bold">{auc.winner}</span> | Winning Bid: {auc.winningBid}
                  </div>
                </div>

                <div className="text-right">
                  <div className="text-xs text-[#64748B] font-mono uppercase">Vickrey Clearing Price</div>
                  <div className="text-sm font-bold font-mono text-[#10B981] mt-0.5">{auc.clearingPrice}</div>
                </div>
              </div>

              <div>
                <div className="text-xs font-mono text-[#94A3B8] uppercase mb-2">Sealed Bids Received</div>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                  {auc.bids.map((b, idx) => (
                    <div key={idx} className="p-3 rounded-lg bg-[#020617] border border-[#1E293B] text-xs font-mono">
                      <div className="text-[#F8FAFC] font-semibold">{b.dept}</div>
                      <div className="text-[#F59E0B] font-bold mt-1">{b.amount} Credits</div>
                      <div className="text-[#64748B] text-[10px] mt-0.5">Utility Weight: {b.utility}</div>
                    </div>
                  ))}
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}

      {selectedTab === 'TRADES' && (
        <div className="space-y-3">
          {trades.map((t) => (
            <Card key={t.id} className="p-4 bg-[#0F172A] border-[#1E293B] space-y-2">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <span className="text-sm font-bold text-[#F8FAFC]">{t.initiator} ⇄ {t.target}</span>
                  <Badge variant="success" size="sm">{t.status}</Badge>
                </div>
                <span className="text-xs text-[#64748B] font-mono">Duration: {t.duration}</span>
              </div>
              <div className="text-xs text-[#94A3B8]">{t.rationale}</div>
              <div className="grid grid-cols-2 gap-4 p-2 rounded bg-[#020617] border border-[#1E293B]/60 text-xs font-mono">
                <div>Offered: <span className="text-[#10B981]">{t.offered}</span></div>
                <div>Requested: <span className="text-[#00D2FF]">{t.requested}</span></div>
              </div>
            </Card>
          ))}
        </div>
      )}

      {selectedTab === 'CONTRACTS' && (
        <div className="space-y-3">
          {contracts.map((c) => (
            <Card key={c.id} className="p-4 bg-[#0F172A] border-[#1E293B] space-y-2">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <span className="text-sm font-bold text-[#F8FAFC]">{c.resource}</span>
                  <Badge variant="intelligence" size="sm">{c.status}</Badge>
                </div>
                <span className="text-xs text-[#10B981] font-mono font-semibold">{c.signature}</span>
              </div>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-2 text-xs font-mono text-[#94A3B8]">
                <div>Provider: <span className="text-[#F8FAFC]">{c.provider}</span></div>
                <div>Consumer: <span className="text-[#F8FAFC]">{c.consumer}</span></div>
                <div>Committed Capacity: <span className="text-[#00D2FF]">{c.committedCapacity}</span></div>
                <div>SLA Guarantee: <span className="text-[#F59E0B]">{c.slaLatency}</span></div>
              </div>
            </Card>
          ))}
        </div>
      )}

      {selectedTab === 'NASH' && (
        <Card className="p-5 bg-[#0F172A] border-[#1E293B] space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <span className="text-sm font-bold text-[#F8FAFC]">Nash Bargaining Pareto Frontier Allocation</span>
              <p className="text-xs text-[#94A3B8] mt-1">
                Maximizes joint surplus product: max (U_A - d_A)^0.6 * (U_B - d_B)^0.4 over 100 available GPU slots.
              </p>
            </div>
            <Badge variant="intelligence" size="sm">PARETO OPTIMAL</Badge>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="p-4 rounded-xl bg-[#020617] border border-[#1E293B] space-y-2">
              <div className="text-xs font-mono text-[#38BDF8] font-bold">Extraction Department (Weight 0.6)</div>
              <div className="text-2xl font-bold font-mono text-[#F8FAFC]">58.0 Units</div>
              <div className="text-[11px] text-[#64748B]">Disagreement fallback payoff: 10.0 units</div>
            </div>

            <div className="p-4 rounded-xl bg-[#020617] border border-[#1E293B] space-y-2">
              <div className="text-xs font-mono text-[#10B981] font-bold">OCR Department (Weight 0.4)</div>
              <div className="text-2xl font-bold font-mono text-[#F8FAFC]">42.0 Units</div>
              <div className="text-[11px] text-[#64748B]">Disagreement fallback payoff: 10.0 units</div>
            </div>
          </div>
        </Card>
      )}
    </div>
  );
};
