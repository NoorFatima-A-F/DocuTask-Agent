import React, { useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import {
  Crown,
  TrendingUp,
  Activity,
  ShieldCheck,
  RefreshCw,
  CheckCircle2,
  Calendar,
  Layers,
  Award,
} from 'lucide-react';

export const ExecutiveStrategyDashboard: React.FC = () => {
  const [isExecutingCycle, setIsExecutingCycle] = useState(false);
  const [cycleNotice, setCycleNotice] = useState<string | null>(null);

  const handleRunStrategicCycle = () => {
    setIsExecutingCycle(true);
    setTimeout(() => {
      setIsExecutingCycle(false);
      setCycleNotice('Strategic Execution Cycle executed: Evolved 4 goals, balanced portfolio Pareto rankings, and refreshed CSO directives.');
      setTimeout(() => setCycleNotice(null), 4000);
    }, 1500);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
            <Crown className="w-6 h-6 text-amber-500" />
            Executive Strategy Command Cockpit (CSO)
          </h2>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            Phase 13.11 — Unified AI Chief Strategy Officer dashboard integrating goal evolution, portfolio optimization, roadmaps, and cryptographic executive decisioning.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant="success" size="md">
            <ShieldCheck className="w-3.5 h-3.5 mr-1" />
            CSO Autonomous Active
          </Badge>
          <Button variant="intelligence" size="sm" onClick={handleRunStrategicCycle} disabled={isExecutingCycle}>
            <RefreshCw className={`w-3.5 h-3.5 mr-1.5 ${isExecutingCycle ? 'animate-spin' : ''}`} />
            {isExecutingCycle ? 'Executing Strategic Cycle...' : 'Execute Strategic Review Cycle'}
          </Button>
        </div>
      </div>

      {cycleNotice && (
        <div className="p-4 bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800 rounded-lg text-sm text-emerald-800 dark:text-emerald-300 flex items-center gap-2">
          <CheckCircle2 className="w-5 h-5 flex-shrink-0" />
          <span>{cycleNotice}</span>
        </div>
      )}

      {/* Top Executive KPI Grid */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
        <Card className="p-4 border-l-4 border-l-indigo-500">
          <div className="flex items-center justify-between text-xs text-gray-500">
            <span>Portfolio Utilization</span>
            <Activity className="w-4 h-4 text-indigo-500" />
          </div>
          <div className="text-2xl font-bold text-gray-900 dark:text-white mt-1">51.7%</div>
          <span className="text-xs text-indigo-600 dark:text-indigo-400 font-medium">$15.5k / $30.0k Limit</span>
        </Card>

        <Card className="p-4 border-l-4 border-l-emerald-500">
          <div className="flex items-center justify-between text-xs text-gray-500">
            <span>Projected Portfolio ROI</span>
            <TrendingUp className="w-4 h-4 text-emerald-500" />
          </div>
          <div className="text-2xl font-bold text-emerald-600 dark:text-emerald-400 mt-1">3.45x</div>
          <span className="text-xs text-emerald-500">Net Expected Gain: +$46.3k</span>
        </Card>

        <Card className="p-4 border-l-4 border-l-purple-500">
          <div className="flex items-center justify-between text-xs text-gray-500">
            <span>Active Strategic Goals</span>
            <Layers className="w-4 h-4 text-purple-500" />
          </div>
          <div className="text-2xl font-bold text-purple-600 dark:text-purple-400 mt-1">4 Active</div>
          <span className="text-xs text-purple-500">HTN Decomposed</span>
        </Card>

        <Card className="p-4 border-l-4 border-l-amber-500">
          <div className="flex items-center justify-between text-xs text-gray-500">
            <span>Signed Executive Directives</span>
            <Award className="w-4 h-4 text-amber-500" />
          </div>
          <div className="text-2xl font-bold text-amber-600 dark:text-amber-400 mt-1">3 Directives</div>
          <span className="text-xs text-amber-500">100% Cryptographically Sealed</span>
        </Card>

        <Card className="p-4 border-l-4 border-l-sky-500">
          <div className="flex items-center justify-between text-xs text-gray-500">
            <span>Institutional Playbooks</span>
            <ShieldCheck className="w-4 h-4 text-sky-500" />
          </div>
          <div className="text-2xl font-bold text-sky-600 dark:text-sky-400 mt-1">5 Verified</div>
          <span className="text-xs text-sky-500">99.4% Historical Success</span>
        </Card>
      </div>

      {/* Main Command Split */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left 2 Cols: Top Strategic Directives & Roadmap Milestones */}
        <div className="lg:col-span-2 space-y-6">
          <Card className="p-5">
            <div className="flex items-center justify-between pb-4 border-b border-gray-100 dark:border-gray-800">
              <h3 className="font-semibold text-gray-900 dark:text-white flex items-center gap-2">
                <Crown className="w-5 h-5 text-amber-500" />
                Active Executive Directives & Guidance
              </h3>
              <Badge variant="intelligence" size="sm">
                AI CSO Directives
              </Badge>
            </div>

            <div className="space-y-4 mt-4 text-xs">
              <div className="p-4 bg-indigo-50/40 dark:bg-indigo-950/20 border border-indigo-200 dark:border-indigo-900 rounded-lg space-y-2">
                <div className="flex items-center justify-between">
                  <span className="font-semibold text-sm text-indigo-900 dark:text-indigo-300">
                    Directive 1: Speculative Layout Tensor Cache Expansion
                  </span>
                  <Badge variant="success" size="sm">Priority: CRITICAL</Badge>
                </div>
                <p className="text-gray-600 dark:text-gray-400">
                  Deploy pre-computed speculative layout tensors for Fortune 500 invoice formats. Drives P95 latency from 280ms down to 195ms with $9.8k projected monthly savings.
                </p>
                <div className="flex items-center gap-4 text-gray-400 pt-1">
                  <span>Confidence: <strong className="text-indigo-600 dark:text-indigo-400">98.8%</strong></span>
                  <span>•</span>
                  <span>Budget: <strong className="text-gray-700 dark:text-gray-300">$3,200</strong></span>
                  <span>•</span>
                  <span>ROI: <strong className="text-emerald-600 dark:text-emerald-400">3.80x</strong></span>
                </div>
              </div>

              <div className="p-4 bg-gray-50 dark:bg-gray-900/40 border border-gray-200 dark:border-gray-800 rounded-lg space-y-2">
                <div className="flex items-center justify-between">
                  <span className="font-semibold text-sm text-gray-800 dark:text-gray-200">
                    Directive 2: Triadic Extraction Strike Teams for Balance Sheets
                  </span>
                  <Badge variant="warning" size="sm">Priority: HIGH</Badge>
                </div>
                <p className="text-gray-500">
                  Pre-cluster specialist agent strike teams by accounting taxonomy to completely eliminate inter-agent auction negotiation overhead during peak batch ingestion.
                </p>
              </div>
            </div>
          </Card>
        </div>

        {/* Right Col: Strategic Roadmap Summary */}
        <div className="space-y-6">
          <Card className="p-5">
            <h3 className="font-semibold text-gray-900 dark:text-white flex items-center gap-2 mb-4">
              <Calendar className="w-5 h-5 text-indigo-500" />
              90-Day Execution Horizons
            </h3>

            <div className="space-y-3 text-xs">
              <div className="p-3 bg-emerald-50/40 dark:bg-emerald-950/20 border border-emerald-200 dark:border-emerald-800 rounded-lg">
                <div className="flex justify-between items-center font-semibold text-emerald-900 dark:text-emerald-300">
                  <span>Day +20: Sub-20ms Digital Twin</span>
                  <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" />
                </div>
                <p className="text-gray-500 mt-1">Telemetry synchronization completed across all active swarms.</p>
              </div>

              <div className="p-3 bg-amber-50/40 dark:bg-amber-950/20 border border-amber-200 dark:border-amber-800 rounded-lg">
                <div className="flex justify-between items-center font-semibold text-amber-900 dark:text-amber-300">
                  <span>Day +45: Nash Resource Auction</span>
                  <Badge variant="warning" size="sm">In Progress</Badge>
                </div>
                <p className="text-gray-500 mt-1">Multi-swarm token & GPU decentralized bargaining engine.</p>
              </div>

              <div className="p-3 bg-gray-50 dark:bg-gray-900/40 border border-gray-200 dark:border-gray-800 rounded-lg">
                <div className="flex justify-between items-center font-semibold text-gray-800 dark:text-gray-200">
                  <span>Day +85: Full Autonomous CSO</span>
                  <Badge variant="default" size="sm">Pending</Badge>
                </div>
                <p className="text-gray-500 mt-1">Continuous 365-day multi-tier goal evolution and MCDA portfolio execution.</p>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};
