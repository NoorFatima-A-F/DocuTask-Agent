import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const DigitalTwinMonitorView: React.FC = () => {
  const [activeShadowTraffic, setActiveShadowTraffic] = useState(true);

  const shadowRecords = [
    {
      shadowId: 'shw_99182',
      missionId: 'MIS-INV-8821',
      targetPolicy: 'v4.2-pareto (Production)',
      shadowPolicy: 'v5.0-bayesian (Candidate)',
      agreementScore: '99.4%',
      latencyDivergence: '+3.8%',
      tokenDelta: '+25 tokens',
      sandboxStatus: 'MUTATION_INTERCEPTED',
      fidelity: 'HIGH_FIDELITY',
    },
    {
      shadowId: 'shw_99183',
      missionId: 'MIS-TABLE-4412',
      targetPolicy: 'v4.2-pareto (Production)',
      shadowPolicy: 'v5.0-bayesian (Candidate)',
      agreementScore: '98.1%',
      latencyDivergence: '-12.4%',
      tokenDelta: '-150 tokens',
      sandboxStatus: 'ISOLATED_SUCCESS',
      fidelity: 'HIGH_FIDELITY',
    },
    {
      shadowId: 'shw_99184',
      missionId: 'MIS-KYC-0034',
      targetPolicy: 'v4.2-pareto (Production)',
      shadowPolicy: 'v5.0-bayesian (Candidate)',
      agreementScore: '100.0%',
      latencyDivergence: '+0.5%',
      tokenDelta: '0 tokens',
      sandboxStatus: 'ISOLATED_SUCCESS',
      fidelity: 'HIGH_FIDELITY',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="p-6 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-xl">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xl">👥</span>
              <h2 className="text-lg font-bold font-mono text-[#F8FAFC]">
                Digital Twin Shadow Execution & Safety Sandbox
              </h2>
              <Badge variant="success" size="sm">
                SANDBOX ISOLATED
              </Badge>
            </div>
            <p className="text-sm font-mono text-[#94A3B8] mt-1">
              Zero-risk mirrored execution of production traffic against experimental candidate models and policies.
            </p>
          </div>
          <div className="flex items-center gap-3">
            <span className="text-xs font-mono text-[#94A3B8]">Shadow Traffic Mirroring:</span>
            <button
              onClick={() => setActiveShadowTraffic(!activeShadowTraffic)}
              className={`px-3 py-1.5 rounded-lg text-xs font-mono font-medium transition-all ${
                activeShadowTraffic
                  ? 'bg-emerald-600 text-white'
                  : 'bg-[#1E293B] text-[#94A3B8]'
              }`}
            >
              {activeShadowTraffic ? '● 100% MIRRORED' : '○ PAUSED'}
            </button>
          </div>
        </div>
      </div>

      {/* Safety Sandbox Invariant Status */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="p-4 bg-[#0F172A] border-[#1E293B]">
          <div className="text-xs font-mono text-[#94A3B8]">Database Mutation Shield</div>
          <div className="text-xl font-bold font-mono text-emerald-400 mt-1">ACTIVE (100% BLOCKED)</div>
          <div className="text-[11px] font-mono text-[#64748B] mt-1">Virtual state interceptors</div>
        </Card>
        <Card className="p-4 bg-[#0F172A] border-[#1E293B]">
          <div className="text-xs font-mono text-[#94A3B8]">Average Output Agreement</div>
          <div className="text-2xl font-bold font-mono text-cyan-400 mt-1">99.1%</div>
          <div className="text-[11px] font-mono text-[#64748B] mt-1">High fidelity mirroring</div>
        </Card>
        <Card className="p-4 bg-[#0F172A] border-[#1E293B]">
          <div className="text-xs font-mono text-[#94A3B8]">Production Latency Impact</div>
          <div className="text-2xl font-bold font-mono text-emerald-400 mt-1">0.00 ms</div>
          <div className="text-[11px] font-mono text-[#64748B] mt-1">Asynchronous sidecar execution</div>
        </Card>
        <Card className="p-4 bg-[#0F172A] border-[#1E293B]">
          <div className="text-xs font-mono text-[#94A3B8]">Overall Twin Status</div>
          <div className="text-xl font-bold font-mono text-indigo-400 mt-1">HIGH_FIDELITY</div>
          <div className="text-[11px] font-mono text-[#64748B] mt-1">Parity with prod environment</div>
        </Card>
      </div>

      {/* Shadow Execution Streams */}
      <Card className="p-6 bg-[#0F172A] border-[#1E293B]">
        <h3 className="text-sm font-bold font-mono text-[#F8FAFC] mb-4">
          Live Mirrored Shadow Execution Stream
        </h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left font-mono text-xs">
            <thead>
              <tr className="border-b border-[#1E293B] text-[#94A3B8]">
                <th className="pb-3">Shadow Run ID</th>
                <th className="pb-3">Production vs Candidate Policy</th>
                <th className="pb-3">Output Agreement</th>
                <th className="pb-3">Latency Divergence</th>
                <th className="pb-3">Sandbox Security</th>
                <th className="pb-3">Fidelity Grade</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#1E293B]">
              {shadowRecords.map((s) => (
                <tr key={s.shadowId} className="hover:bg-[#1E293B]/40 transition-colors">
                  <td className="py-3 font-bold text-[#F8FAFC]">{s.shadowId}</td>
                  <td className="py-3">
                    <div className="text-[#E2E8F0]">{s.targetPolicy}</div>
                    <div className="text-indigo-400 text-[11px]">↳ {s.shadowPolicy}</div>
                  </td>
                  <td className="py-3 text-cyan-400 font-bold">{s.agreementScore}</td>
                  <td className="py-3 text-emerald-400">{s.latencyDivergence}</td>
                  <td className="py-3">
                    <Badge variant="warning" size="sm">
                      {s.sandboxStatus}
                    </Badge>
                  </td>
                  <td className="py-3">
                    <Badge variant="success" size="sm">
                      {s.fidelity}
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
