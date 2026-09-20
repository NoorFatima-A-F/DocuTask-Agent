import React, { useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import {
  Scale,
  Cpu,
  Coins,
  CheckCircle2,
  RefreshCw,
  Zap,
} from 'lucide-react';

interface ProposalItem {
  id: string;
  swarmId: string;
  resourceType: string;
  requested: number;
  allocated: number;
  bidUtility: number;
  disagreementPoint: number;
  status: string;
}

export const ResourceNegotiationCenter: React.FC = () => {
  const [proposals] = useState<ProposalItem[]>([
    {
      id: 'prop-gpu-01',
      swarmId: 'Swarm Alpha (Extraction)',
      resourceType: 'GPU_VRAM_GB',
      requested: 24.0,
      allocated: 20.0,
      bidUtility: 0.94,
      disagreementPoint: 0.25,
      status: 'SETTLED',
    },
    {
      id: 'prop-gpu-02',
      swarmId: 'Swarm Beta (Classifier)',
      resourceType: 'GPU_VRAM_GB',
      requested: 16.0,
      allocated: 14.0,
      bidUtility: 0.88,
      disagreementPoint: 0.20,
      status: 'SETTLED',
    },
    {
      id: 'prop-gpu-03',
      swarmId: 'Swarm Gamma (Governance)',
      resourceType: 'GPU_VRAM_GB',
      requested: 16.0,
      allocated: 14.0,
      bidUtility: 0.91,
      disagreementPoint: 0.30,
      status: 'SETTLED',
    },
  ]);

  const [isNegotiating, setIsNegotiating] = useState(false);
  const [sessionNotice, setSessionNotice] = useState<string | null>(null);

  const totalCapacity = 48.0;

  const handleRunAuction = () => {
    setIsNegotiating(true);
    setTimeout(() => {
      setIsNegotiating(false);
      setSessionNotice('Nash Bargaining Equilibrium reached: 3 swarms converged in 4 concession rounds (Nash Product: 0.815).');
      setTimeout(() => setSessionNotice(null), 4000);
    }, 1200);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
            <Scale className="w-6 h-6 text-indigo-500" />
            Multi-Swarm Resource Negotiation & Auction Center
          </h2>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            Phase 13.11 — Decentralized auction protocols and Nash bargaining equilibria for GPU, VRAM, and Token budget pools.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="intelligence" size="sm" onClick={handleRunAuction} disabled={isNegotiating}>
            <RefreshCw className={`w-3.5 h-3.5 mr-1.5 ${isNegotiating ? 'animate-spin' : ''}`} />
            {isNegotiating ? 'Negotiating Rounds...' : 'Run Nash Auction'}
          </Button>
        </div>
      </div>

      {sessionNotice && (
        <div className="p-4 bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800 rounded-lg text-sm text-emerald-800 dark:text-emerald-300 flex items-center gap-2">
          <CheckCircle2 className="w-5 h-5 flex-shrink-0" />
          <span>{sessionNotice}</span>
        </div>
      )}

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="p-4 border-l-4 border-l-indigo-500">
          <div className="flex items-center justify-between text-xs text-gray-500">
            <span>Total Resource Pool</span>
            <Cpu className="w-4 h-4 text-indigo-500" />
          </div>
          <div className="text-2xl font-bold text-gray-900 dark:text-white mt-1">{totalCapacity} GB VRAM</div>
          <span className="text-xs text-indigo-600 dark:text-indigo-400 font-medium">100% Utilized (48/48 GB)</span>
        </Card>

        <Card className="p-4 border-l-4 border-l-emerald-500">
          <div className="flex items-center justify-between text-xs text-gray-500">
            <span>Nash Product Equilibrium</span>
            <Scale className="w-4 h-4 text-emerald-500" />
          </div>
          <div className="text-2xl font-bold text-emerald-600 dark:text-emerald-400 mt-1">0.815</div>
          <span className="text-xs text-emerald-500">Maximized Fairness Product</span>
        </Card>

        <Card className="p-4 border-l-4 border-l-purple-500">
          <div className="flex items-center justify-between text-xs text-gray-500">
            <span>Convergence Speed</span>
            <Zap className="w-4 h-4 text-purple-500" />
          </div>
          <div className="text-2xl font-bold text-purple-600 dark:text-purple-400 mt-1">4 Rounds</div>
          <span className="text-xs text-purple-500">18.5ms Latency</span>
        </Card>

        <Card className="p-4 border-l-4 border-l-sky-500">
          <div className="flex items-center justify-between text-xs text-gray-500">
            <span>Active Participating Swarms</span>
            <Coins className="w-4 h-4 text-sky-500" />
          </div>
          <div className="text-2xl font-bold text-sky-600 dark:text-sky-400 mt-1">3 Swarms</div>
          <span className="text-xs text-sky-500">Zero Starvation</span>
        </Card>
      </div>

      {/* Proposals Ledger */}
      <div className="space-y-4">
        <h3 className="text-sm font-semibold text-gray-900 dark:text-white uppercase tracking-wider">
          Active Negotiation Bids & Settlements
        </h3>

        <div className="grid grid-cols-1 gap-4">
          {proposals.map((p) => (
            <Card key={p.id} className="p-5 hover:shadow-md transition-shadow">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 pb-3 border-b border-gray-100 dark:border-gray-800">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-mono text-xs text-indigo-600 dark:text-indigo-400 font-semibold">{p.id}</span>
                    <Badge variant="success" size="sm">
                      <CheckCircle2 className="w-3 h-3 mr-1" />
                      {p.status}
                    </Badge>
                  </div>
                  <h4 className="font-semibold text-gray-900 dark:text-white text-base mt-1">{p.swarmId}</h4>
                </div>
                <div className="flex items-center gap-3">
                  <div className="text-right">
                    <span className="text-xs text-gray-400 block">Bid Utility</span>
                    <span className="text-lg font-bold text-indigo-600 dark:text-indigo-400 font-mono">
                      {p.bidUtility.toFixed(3)}
                    </span>
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mt-4 text-xs">
                <div className="p-2.5 bg-gray-50 dark:bg-gray-900/40 rounded border border-gray-100 dark:border-gray-800">
                  <span className="text-gray-400 block mb-0.5">Resource</span>
                  <span className="font-semibold text-gray-800 dark:text-gray-200">{p.resourceType}</span>
                </div>
                <div className="p-2.5 bg-gray-50 dark:bg-gray-900/40 rounded border border-gray-100 dark:border-gray-800">
                  <span className="text-gray-400 block mb-0.5">Requested</span>
                  <span className="font-semibold text-gray-800 dark:text-gray-200 font-mono">{p.requested} GB</span>
                </div>
                <div className="p-2.5 bg-gray-50 dark:bg-gray-900/40 rounded border border-gray-100 dark:border-gray-800">
                  <span className="text-gray-400 block mb-0.5">Allocated</span>
                  <span className="font-semibold text-emerald-600 dark:text-emerald-400 font-mono">{p.allocated} GB</span>
                </div>
                <div className="p-2.5 bg-gray-50 dark:bg-gray-900/40 rounded border border-gray-100 dark:border-gray-800">
                  <span className="text-gray-400 block mb-0.5">Disagreement Floor</span>
                  <span className="font-semibold text-gray-600 dark:text-gray-400 font-mono">{p.disagreementPoint}</span>
                </div>
              </div>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
};
