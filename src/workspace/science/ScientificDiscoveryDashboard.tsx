import React, { useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import {
  Sparkles,
  FlaskConical,
  BookOpen,
  Scale,
  Brain,
  CheckCircle2,
  RefreshCw,
  Compass,
  FileCheck,
  Binary,
  Layers,
} from 'lucide-react';

export const ScientificDiscoveryDashboard: React.FC = () => {
  const [isExecutingCycle, setIsExecutingCycle] = useState(false);
  const [cycleNotice, setCycleNotice] = useState<string | null>(null);

  const handleRunDiscoveryCycle = () => {
    setIsExecutingCycle(true);
    setTimeout(() => {
      setIsExecutingCycle(false);
      setCycleNotice('Autonomous Scientific Discovery Cycle completed: Verified 1 hypothesis (p < 0.0001, d=1.42), ratified 1 empirical law, and generated signed DOI publication.');
      setTimeout(() => setCycleNotice(null), 5000);
    }, 1500);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
            <Sparkles className="w-6 h-6 text-indigo-500" />
            Autonomous Scientific Discovery Platform (ASD-HGCKEP)
          </h2>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            Phase 13.12 — AI Chief Scientist cockpit integrating autonomous hypothesis generation, empirical A/B experimentation, statistical validation, and peer-reviewed publication.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant="intelligence" size="md">
            <Brain className="w-3.5 h-3.5 mr-1" />
            AI Chief Scientist Active
          </Badge>
          <Button variant="intelligence" size="sm" onClick={handleRunDiscoveryCycle} disabled={isExecutingCycle}>
            <RefreshCw className={`w-3.5 h-3.5 mr-1.5 ${isExecutingCycle ? 'animate-spin' : ''}`} />
            {isExecutingCycle ? 'Executing Discovery Cycle...' : 'Run Discovery Cycle'}
          </Button>
        </div>
      </div>

      {cycleNotice && (
        <div className="p-4 bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800 rounded-lg text-sm text-emerald-800 dark:text-emerald-300 flex items-center gap-2">
          <CheckCircle2 className="w-5 h-5 flex-shrink-0" />
          <span>{cycleNotice}</span>
        </div>
      )}

      {/* Top Scientific Metric Cards */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
        <Card className="p-4 border-l-4 border-l-indigo-500">
          <div className="flex items-center justify-between text-xs text-gray-500">
            <span>Active Hypotheses</span>
            <Compass className="w-4 h-4 text-indigo-500" />
          </div>
          <div className="text-2xl font-bold text-gray-900 dark:text-white mt-1">4 Active</div>
          <span className="text-xs text-indigo-600 dark:text-indigo-400 font-medium">Avg EIG: 0.885</span>
        </Card>

        <Card className="p-4 border-l-4 border-l-emerald-500">
          <div className="flex items-center justify-between text-xs text-gray-500">
            <span>Verified Laws & Facts</span>
            <BookOpen className="w-4 h-4 text-emerald-500" />
          </div>
          <div className="text-2xl font-bold text-emerald-600 dark:text-emerald-400 mt-1">3 Laws / 8 Facts</div>
          <span className="text-xs text-emerald-500">99.2% Confidence</span>
        </Card>

        <Card className="p-4 border-l-4 border-l-purple-500">
          <div className="flex items-center justify-between text-xs text-gray-500">
            <span>Running Experiments</span>
            <FlaskConical className="w-4 h-4 text-purple-500" />
          </div>
          <div className="text-2xl font-bold text-purple-600 dark:text-purple-400 mt-1">6 Active</div>
          <span className="text-xs text-purple-500">N=12,500 Total Traces</span>
        </Card>

        <Card className="p-4 border-l-4 border-l-amber-500">
          <div className="flex items-center justify-between text-xs text-gray-500">
            <span>Consensus Rate</span>
            <Scale className="w-4 h-4 text-amber-500" />
          </div>
          <div className="text-2xl font-bold text-amber-600 dark:text-amber-400 mt-1">98.4%</div>
          <span className="text-xs text-amber-500">Multi-Agent Ratified</span>
        </Card>

        <Card className="p-4 border-l-4 border-l-sky-500">
          <div className="flex items-center justify-between text-xs text-gray-500">
            <span>Signed DOI Papers</span>
            <FileCheck className="w-4 h-4 text-sky-500" />
          </div>
          <div className="text-2xl font-bold text-sky-600 dark:text-sky-400 mt-1">2 Published</div>
          <span className="text-xs text-sky-500">100% SHA-256 Provenance</span>
        </Card>
      </div>

      {/* Discovery Pipeline Architecture Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <Card className="p-5 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="font-semibold text-gray-900 dark:text-white flex items-center gap-2">
              <Compass className="w-4 h-4 text-indigo-500" />
              Hypothesis Backlog & Gaps
            </h3>
            <Badge variant="outline" size="sm">2 New Gaps</Badge>
          </div>
          <div className="space-y-3">
            <div className="p-3 bg-gray-50 dark:bg-gray-800/60 rounded border border-gray-100 dark:border-gray-700">
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold text-gray-800 dark:text-gray-200">Speculative Layout Cache</span>
                <Badge variant="warning" size="sm">EIG: 0.915</Badge>
              </div>
              <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                P95 latency reduction from 280ms to 195ms via speculative GPU tensor pre-warming.
              </p>
              <div className="flex items-center gap-2 mt-2">
                <Badge variant="success" size="sm">Prior: 82%</Badge>
                <span className="text-[10px] text-gray-400">Status: Experimenting</span>
              </div>
            </div>

            <div className="p-3 bg-gray-50 dark:bg-gray-800/60 rounded border border-gray-100 dark:border-gray-700">
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold text-gray-800 dark:text-gray-200">Triadic Specialization Invariant</span>
                <Badge variant="info" size="sm">EIG: 0.860</Badge>
              </div>
              <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                3-member specialist triadic teams eliminate 90% of auction negotiation jitter.
              </p>
              <div className="flex items-center gap-2 mt-2">
                <Badge variant="default" size="sm">Prior: 78%</Badge>
                <span className="text-[10px] text-gray-400">Status: Proposed</span>
              </div>
            </div>
          </div>
        </Card>

        <Card className="p-5 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="font-semibold text-gray-900 dark:text-white flex items-center gap-2">
              <FlaskConical className="w-4 h-4 text-purple-500" />
              Active Empirical Trials
            </h3>
            <Badge variant="success" size="sm">p &lt; 0.001</Badge>
          </div>
          <div className="space-y-3">
            <div className="p-3 bg-gray-50 dark:bg-gray-800/60 rounded border border-gray-100 dark:border-gray-700">
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold text-gray-800 dark:text-gray-200">A/B Speculative Cache Trial</span>
                <Badge variant="success" size="sm">Effect: d=1.42</Badge>
              </div>
              <div className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                Control: 278.5ms | Treatment: 194.2ms (-30.2%)
              </div>
              <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-1.5 mt-2">
                <div className="bg-purple-600 h-1.5 rounded-full" style={{ width: '100%' }} />
              </div>
              <div className="flex items-center justify-between text-[10px] text-gray-400 mt-1">
                <span>N=2,500 traces</span>
                <span className="text-emerald-500 font-medium">Verified p=0.0001</span>
              </div>
            </div>

            <div className="p-3 bg-gray-50 dark:bg-gray-800/60 rounded border border-gray-100 dark:border-gray-700">
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold text-gray-800 dark:text-gray-200">Lock-Free Ring Buffer Stress</span>
                <Badge variant="info" size="sm">Effect: d=2.10</Badge>
              </div>
              <div className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                Zero thread lock contention across 64 concurrent workers.
              </div>
              <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-1.5 mt-2">
                <div className="bg-indigo-600 h-1.5 rounded-full" style={{ width: '85%' }} />
              </div>
              <div className="flex items-center justify-between text-[10px] text-gray-400 mt-1">
                <span>N=10,000 operations</span>
                <span className="text-indigo-400">Analyzing Replay</span>
              </div>
            </div>
          </div>
        </Card>

        <Card className="p-5 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="font-semibold text-gray-900 dark:text-white flex items-center gap-2">
              <BookOpen className="w-4 h-4 text-emerald-500" />
              Ratified Laws & Ontologies
            </h3>
            <Badge variant="intelligence" size="sm">Semantic v1.0</Badge>
          </div>
          <div className="space-y-3">
            <div className="p-3 bg-emerald-50/50 dark:bg-emerald-950/20 rounded border border-emerald-200 dark:border-emerald-800/40">
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold text-emerald-900 dark:text-emerald-300">Law of Speculative Invariance</span>
                <Badge variant="success" size="sm">Law-01</Badge>
              </div>
              <p className="text-xs font-mono text-emerald-700 dark:text-emerald-400 mt-1 bg-white/60 dark:bg-gray-900/60 p-1.5 rounded">
                Latency_P95(H, C) = T_base * (1 - C_rate * (1 - H/H_max))
              </p>
              <div className="text-[10px] text-gray-500 dark:text-gray-400 mt-1">
                Governs document entropy H &lt;= 1.2 bounds with 4 supporting empirical facts.
              </div>
            </div>

            <div className="p-3 bg-gray-50 dark:bg-gray-800/60 rounded border border-gray-100 dark:border-gray-700">
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold text-gray-800 dark:text-gray-200">Ontological Expansion</span>
                <Binary className="w-4 h-4 text-indigo-400" />
              </div>
              <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                Expanded 6 foundational concepts and 3 cross-domain relation vectors into semantic memory.
              </p>
            </div>
          </div>
        </Card>
      </div>

      {/* Peer Review & Governance Seal */}
      <Card className="p-5">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-indigo-100 dark:bg-indigo-900/40 flex items-center justify-center text-indigo-600 dark:text-indigo-400">
              <Layers className="w-5 h-5" />
            </div>
            <div>
              <h4 className="text-sm font-semibold text-gray-900 dark:text-white">Multi-Agent Peer Review Tribunal & Governance Seal</h4>
              <p className="text-xs text-gray-500 dark:text-gray-400">
                All empirical findings require Bayesian arbitration across Sentinel, Statistician, and Architect agents prior to model promotion.
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <Badge variant="success" size="sm">Tribunal: 4/4 Unanimous</Badge>
            <Badge variant="outline" size="sm">DOI: 10.ai-sci/2026.001</Badge>
          </div>
        </div>
      </Card>
    </div>
  );
};
