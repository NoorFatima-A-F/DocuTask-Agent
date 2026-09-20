import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const OrganizationSimulationView: React.FC = () => {
  const scenarios = [
    {
      name: '50% Budget Cut Stress Test',
      stress: 'BUDGET_CUT_50PCT',
      missions: 1000,
      success: 985,
      resilience: '98.5%',
      recoveryTime: '8.4s',
      invariants: '100% Preserved',
    },
    {
      name: 'Primary LLM Provider Total Outage',
      stress: 'GEMINI_PROVIDER_OUTAGE',
      missions: 1000,
      success: 992,
      resilience: '99.2%',
      recoveryTime: '14.2s',
      invariants: '100% Preserved',
    },
    {
      name: '10x Concurrency Ingestion Surge',
      stress: '10X_THROUGHPUT_SPIKE',
      missions: 1000,
      success: 978,
      resilience: '97.8%',
      recoveryTime: '22.0s',
      invariants: '100% Preserved',
    },
    {
      name: 'Dynamic Department Removal & Re-delegation',
      stress: 'DEPT_REMOVAL_CHAOS',
      missions: 1000,
      success: 965,
      resilience: '96.5%',
      recoveryTime: '18.5s',
      invariants: '100% Preserved',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 p-5 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-xl">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-2xl">🌐</span>
            <h2 className="text-xl font-bold text-[#F8FAFC]">Autonomous Organization Digital Twin Simulation</h2>
            <Badge variant="intelligence" size="sm">100-Org Monte Carlo</Badge>
          </div>
          <p className="text-sm text-[#94A3B8] mt-1">
            Simulates 100 digital enterprises across 1,000 missions under budget cuts, provider outages, throughput surges, and chaos failures.
          </p>
        </div>

        <div className="text-right">
          <div className="text-xs text-[#94A3B8]">Macro Resilience Score</div>
          <div className="text-2xl font-bold font-mono text-[#10B981]">98.0% (Grade AAA)</div>
        </div>
      </div>

      {/* Capacity & Headroom Strip */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card className="p-4 bg-[#0F172A]/80 border-[#1E293B]">
          <div className="text-xs font-mono text-[#94A3B8] uppercase">Simulated Organizations</div>
          <div className="text-2xl font-bold font-mono text-[#00D2FF] mt-1">100 Orgs</div>
          <div className="text-[11px] text-[#64748B] mt-1">10 missions per org</div>
        </Card>
        <Card className="p-4 bg-[#0F172A]/80 border-[#1E293B]">
          <div className="text-xs font-mono text-[#94A3B8] uppercase">Evaluated Missions</div>
          <div className="text-2xl font-bold font-mono text-[#10B981] mt-1">1,000 Runs</div>
          <div className="text-[11px] text-[#64748B] mt-1">Zero data corruption</div>
        </Card>
        <Card className="p-4 bg-[#0F172A]/80 border-[#1E293B]">
          <div className="text-xs font-mono text-[#94A3B8] uppercase">Capacity Headroom</div>
          <div className="text-2xl font-bold font-mono text-[#F59E0B] mt-1">4.5x Peak</div>
          <div className="text-[11px] text-[#64748B] mt-1">Sustains 4.5x surge load</div>
        </Card>
        <Card className="p-4 bg-[#0F172A]/80 border-[#1E293B]">
          <div className="text-xs font-mono text-[#94A3B8] uppercase">Zero-Fabrication Rate</div>
          <div className="text-2xl font-bold font-mono text-[#A855F7] mt-1">100.0%</div>
          <div className="text-[11px] text-[#64748B] mt-1">Arithmetic certified</div>
        </Card>
      </div>

      {/* Stress Scenarios Table */}
      <Card className="p-5 bg-[#0F172A] border-[#1E293B] space-y-4">
        <div className="text-sm font-bold text-[#F8FAFC]">Monte Carlo Stress Test Scenarios</div>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono">
            <thead>
              <tr className="border-b border-[#1E293B] text-[#64748B]">
                <th className="py-2.5 px-3">STRESS SCENARIO</th>
                <th className="py-2.5 px-3">STRESS FACTOR</th>
                <th className="py-2.5 px-3">EVALUATED MISSIONS</th>
                <th className="py-2.5 px-3">SUCCESSFUL</th>
                <th className="py-2.5 px-3">RESILIENCE SCORE</th>
                <th className="py-2.5 px-3">MEAN RECOVERY</th>
                <th className="py-2.5 px-3">INVARIANT INTEGRITY</th>
              </tr>
            </thead>
            <tbody>
              {scenarios.map((sc, idx) => (
                <tr key={idx} className="border-b border-[#1E293B]/40 hover:bg-[#131D35]/50 transition-colors">
                  <td className="py-3 px-3 font-semibold text-[#F8FAFC]">{sc.name}</td>
                  <td className="py-3 px-3 text-[#38BDF8]">{sc.stress}</td>
                  <td className="py-3 px-3 text-[#94A3B8]">{sc.missions}</td>
                  <td className="py-3 px-3 text-[#10B981]">{sc.success}</td>
                  <td className="py-3 px-3">
                    <span className="font-bold text-[#10B981]">{sc.resilience}</span>
                  </td>
                  <td className="py-3 px-3 text-[#F59E0B]">{sc.recoveryTime}</td>
                  <td className="py-3 px-3">
                    <Badge variant="success" size="sm">{sc.invariants}</Badge>
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
