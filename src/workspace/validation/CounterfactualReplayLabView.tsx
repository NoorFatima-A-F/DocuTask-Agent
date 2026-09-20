import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const CounterfactualReplayLabView: React.FC = () => {
  const [selectedScenario, setSelectedScenario] = useState('sc_nominal');

  const scenarios = [
    {
      id: 'sc_nominal',
      name: 'Nominal Production',
      desc: 'Standard operational conditions with stable low-latency responses.',
      latMultiplier: 1.0,
      costMultiplier: 1.0,
    },
    {
      id: 'sc_peak_load',
      name: 'Extreme Peak Queue Congestion',
      desc: 'Heavy queue backpressure causing 2.5x latency inflation on external LLM calls.',
      latMultiplier: 2.5,
      costMultiplier: 1.0,
    },
    {
      id: 'sc_degraded_scan',
      name: 'Degraded Physical Scan Quality',
      desc: 'Severe visual noise and skew lowering OCR recognition by 15%.',
      latMultiplier: 1.2,
      costMultiplier: 1.0,
    },
    {
      id: 'sc_cloud_rate_limit',
      name: 'Cloud API Rate-Limit Throttling',
      desc: 'Transient HTTP 429 throttling causing exponential backoff retries.',
      latMultiplier: 3.0,
      costMultiplier: 1.1,
    },
  ];

  const candidateBranches = [
    {
      branchId: 'FACTUAL-RUN',
      label: 'Factual Production Choice (Gemini 2.5 Flash)',
      accuracy: '96.2%',
      latency: '480 ms',
      cost: '$0.0018',
      utility: '0.884',
      regret: '0.000',
      isFactual: true,
      isOptimal: true,
    },
    {
      branchId: 'CF-PRO-001',
      label: 'What if Gemini 1.5 Pro was selected?',
      accuracy: '97.7%',
      latency: '1344 ms',
      cost: '$0.0153',
      utility: '0.812',
      regret: '+0.072',
      isFactual: false,
      isOptimal: false,
    },
    {
      branchId: 'CF-LITE-002',
      label: 'What if Gemini Flash-Lite was selected?',
      accuracy: '91.7%',
      latency: '216 ms',
      cost: '$0.0004',
      utility: '0.865',
      regret: '+0.019',
      isFactual: false,
      isOptimal: false,
    },
    {
      branchId: 'CF-NORETRY-003',
      label: 'What if Zero-Retry Fast-Fail policy was applied?',
      accuracy: '88.2%',
      latency: '336 ms',
      cost: '$0.0014',
      utility: '0.835',
      regret: '+0.049',
      isFactual: false,
      isOptimal: false,
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="p-6 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-xl">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xl">🔀</span>
              <h2 className="text-lg font-bold font-mono text-[#F8FAFC]">
                Counterfactual Simulator & Opportunity Cost Lab
              </h2>
              <Badge variant="success" size="sm">
                REPLAY READY
              </Badge>
            </div>
            <p className="text-sm font-mono text-[#94A3B8] mt-1">
              Simulate alternative decisions ("What if Pro?", "What if No Retry?") on historical missions to prove decision optimality.
            </p>
          </div>
        </div>
      </div>

      {/* Scenario Perturbation Selector */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {scenarios.map((sc) => (
          <div
            key={sc.id}
            onClick={() => setSelectedScenario(sc.id)}
            className={`p-4 rounded-xl cursor-pointer border transition-all ${
              selectedScenario === sc.id
                ? 'bg-blue-950/40 border-blue-500 shadow-lg shadow-blue-500/10'
                : 'bg-[#0F172A] border-[#1E293B] hover:border-[#334155]'
            }`}
          >
            <div className="flex items-center justify-between">
              <span className="font-mono text-xs font-bold text-[#F8FAFC]">{sc.name}</span>
              {selectedScenario === sc.id && (
                <Badge variant="info" size="sm">
                  ACTIVE
                </Badge>
              )}
            </div>
            <p className="text-[11px] font-mono text-[#94A3B8] mt-2">{sc.desc}</p>
          </div>
        ))}
      </div>

      {/* Branch Comparison Table */}
      <Card className="p-6 bg-[#0F172A] border-[#1E293B]">
        <h3 className="text-sm font-bold font-mono text-[#F8FAFC] mb-4">
          Factual vs Counterfactual Decision Differential
        </h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left font-mono text-xs">
            <thead>
              <tr className="border-b border-[#1E293B] text-[#94A3B8]">
                <th className="pb-3">Candidate Branch</th>
                <th className="pb-3">Simulated Acc</th>
                <th className="pb-3">Simulated Latency</th>
                <th className="pb-3">Simulated Cost</th>
                <th className="pb-3">Utility U(x)</th>
                <th className="pb-3">Planner Regret</th>
                <th className="pb-3">Verdict</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#1E293B]">
              {candidateBranches.map((b) => (
                <tr
                  key={b.branchId}
                  className={`hover:bg-[#1E293B]/40 transition-colors ${
                    b.isFactual ? 'bg-emerald-950/20' : ''
                  }`}
                >
                  <td className="py-3">
                    <div className="font-bold text-[#F8FAFC]">{b.label}</div>
                    <div className="text-[#64748B] text-[11px]">{b.branchId}</div>
                  </td>
                  <td className="py-3 text-cyan-400">{b.accuracy}</td>
                  <td className="py-3 text-[#E2E8F0]">{b.latency}</td>
                  <td className="py-3 text-[#E2E8F0]">{b.cost}</td>
                  <td className="py-3 text-indigo-400 font-bold">{b.utility}</td>
                  <td className="py-3">
                    <span className={b.isOptimal ? 'text-emerald-400 font-bold' : 'text-amber-400'}>
                      {b.regret}
                    </span>
                  </td>
                  <td className="py-3">
                    <Badge variant={b.isOptimal ? 'success' : 'default'} size="sm">
                      {b.isOptimal ? 'OPTIMAL FACTUAL' : 'SUB-OPTIMAL'}
                    </Badge>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
};
