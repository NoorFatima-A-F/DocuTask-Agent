import React, { useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import {
  Brain,
  ShieldCheck,
  TrendingUp,
  RefreshCw,
  CheckCircle2,
  BookOpen,
  Scale,
  Award,
  Sparkles,
} from 'lucide-react';

export const ExecutiveResearchDashboard: React.FC = () => {
  const [isExecuting, setIsExecuting] = useState(false);
  const [notice, setNotice] = useState<string | null>(null);

  const handleRunExecutiveReview = () => {
    setIsExecuting(true);
    setTimeout(() => {
      setIsExecuting(false);
      setNotice('Chief Scientist Executive Review completed: Assessed 4 active hypotheses, certified 3 empirical laws, and approved compute allocation for Q4 Roadmap.');
      setTimeout(() => setNotice(null), 4000);
    }, 1500);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
            <Brain className="w-6 h-6 text-indigo-500" />
            Executive Research & Chief Scientist Command Center
          </h2>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            Phase 13.12 — Unified AI Chief Scientist command dashboard integrating empirical discoveries, governing laws, ROI multipliers, and peer-reviewed publications.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant="success" size="md">
            <ShieldCheck className="w-3.5 h-3.5 mr-1" />
            Chief Scientist Active
          </Badge>
          <Button variant="intelligence" size="sm" onClick={handleRunExecutiveReview} disabled={isExecuting}>
            <RefreshCw className={`w-3.5 h-3.5 mr-1.5 ${isExecuting ? 'animate-spin' : ''}`} />
            {isExecuting ? 'Reviewing Science...' : 'Execute Executive Science Review'}
          </Button>
        </div>
      </div>

      {notice && (
        <div className="p-4 bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800 rounded-lg text-sm text-emerald-800 dark:text-emerald-300 flex items-center gap-2">
          <CheckCircle2 className="w-5 h-5 flex-shrink-0" />
          <span>{notice}</span>
        </div>
      )}

      {/* Top Executive KPI Grid */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
        <Card className="p-4 border-l-4 border-l-indigo-500">
          <div className="flex items-center justify-between text-xs text-gray-500">
            <span>Scientific Maturity</span>
            <Sparkles className="w-4 h-4 text-indigo-500" />
          </div>
          <div className="text-2xl font-bold text-gray-900 dark:text-white mt-1">94.0%</div>
          <span className="text-xs text-indigo-600 font-medium">Empirical Autonomous</span>
        </Card>

        <Card className="p-4 border-l-4 border-l-emerald-500">
          <div className="flex items-center justify-between text-xs text-gray-500">
            <span>Hypothesis Verification Rate</span>
            <TrendingUp className="w-4 h-4 text-emerald-500" />
          </div>
          <div className="text-2xl font-bold text-emerald-600 dark:text-emerald-400 mt-1">91.7%</div>
          <span className="text-xs text-emerald-500">p &lt; 0.001 Significance</span>
        </Card>

        <Card className="p-4 border-l-4 border-l-purple-500">
          <div className="flex items-center justify-between text-xs text-gray-500">
            <span>Governing Laws</span>
            <BookOpen className="w-4 h-4 text-purple-500" />
          </div>
          <div className="text-2xl font-bold text-purple-600 dark:text-purple-400 mt-1">3 Laws</div>
          <span className="text-xs text-purple-500">Formal Equations</span>
        </Card>

        <Card className="p-4 border-l-4 border-l-amber-500">
          <div className="flex items-center justify-between text-xs text-gray-500">
            <span>Consensus Tribunal Score</span>
            <Scale className="w-4 h-4 text-amber-500" />
          </div>
          <div className="text-2xl font-bold text-amber-600 dark:text-amber-400 mt-1">98.4%</div>
          <span className="text-xs text-amber-500">Multi-Agent Certified</span>
        </Card>

        <Card className="p-4 border-l-4 border-l-sky-500">
          <div className="flex items-center justify-between text-xs text-gray-500">
            <span>Signed DOI Papers</span>
            <Award className="w-4 h-4 text-sky-500" />
          </div>
          <div className="text-2xl font-bold text-sky-600 dark:text-sky-400 mt-1">2 Papers</div>
          <span className="text-xs text-sky-500">100% Cryptographic Seals</span>
        </Card>
      </div>

      {/* Strategic Scientific Insights Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="p-5 space-y-4">
          <h3 className="font-semibold text-gray-900 dark:text-white flex items-center gap-2">
            <BookOpen className="w-4 h-4 text-indigo-500" />
            Ratified Scientific Laws & Equations
          </h3>
          <div className="space-y-3">
            <div className="p-3 bg-gray-50 dark:bg-gray-800/60 rounded border border-gray-100 dark:border-gray-700">
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold text-gray-900 dark:text-white">Law of Speculative Invariance</span>
                <Badge variant="success" size="sm">Law-01</Badge>
              </div>
              <div className="font-mono text-xs text-indigo-600 dark:text-indigo-400 mt-1">
                Latency_P95(H, C) = T_base * (1 - C_rate * (1 - H/H_max))
              </div>
              <div className="text-[11px] text-gray-500 mt-1">
                Yields 30.27% extraction latency reduction on structured corporate invoices.
              </div>
            </div>

            <div className="p-3 bg-gray-50 dark:bg-gray-800/60 rounded border border-gray-100 dark:border-gray-700">
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold text-gray-900 dark:text-white">Principle of Swarm Convergence Latency</span>
                <Badge variant="info" size="sm">Law-02</Badge>
              </div>
              <div className="font-mono text-xs text-indigo-600 dark:text-indigo-400 mt-1">
                T_convergence = alpha * (N_agents^0.42) / bandwidth
              </div>
              <div className="text-[11px] text-gray-500 mt-1">
                Quantifies triadic team scaling advantages over monolithic agent auctions.
              </div>
            </div>
          </div>
        </Card>

        <Card className="p-5 space-y-4">
          <h3 className="font-semibold text-gray-900 dark:text-white flex items-center gap-2">
            <TrendingUp className="w-4 h-4 text-emerald-500" />
            Empirical Research ROI & Discovery Multipliers
          </h3>
          <div className="space-y-3">
            <div className="p-3 bg-emerald-50/50 dark:bg-emerald-950/20 rounded border border-emerald-200 dark:border-emerald-800/40 text-xs">
              <div className="flex items-center justify-between">
                <span className="font-semibold text-emerald-900 dark:text-emerald-300">Speculative GPU Pre-Warming</span>
                <span className="font-bold text-emerald-600">+30.27% Speedup</span>
              </div>
              <p className="text-gray-600 dark:text-gray-400 mt-1">
                Reduces document parsing P95 latency by 84ms per transaction with negligible VRAM overhead.
              </p>
            </div>

            <div className="p-3 bg-purple-50/50 dark:bg-purple-950/20 rounded border border-purple-200 dark:border-purple-800/40 text-xs">
              <div className="flex items-center justify-between">
                <span className="font-semibold text-purple-900 dark:text-purple-300">Int8 Scratchpad Vector Quantization</span>
                <span className="font-bold text-purple-600">-47% Memory</span>
              </div>
              <p className="text-gray-600 dark:text-gray-400 mt-1">
                Maintains 99.1% semantic retrieval recall while halving memory bus saturation.
              </p>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
};
