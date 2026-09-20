import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const SLAIntelligenceView: React.FC = () => {
  const slaReports = [
    { dept: 'Corporate Governance', target: '75 ms', p95: '42.0 ms', p99: '68.0 ms', avail: '100.0%', mttr: '5.0s', mtbf: '1200h', slo: '100.0%' },
    { dept: 'Mathematical Validation', target: '80 ms', p95: '52.0 ms', p99: '74.0 ms', avail: '99.99%', mttr: '8.0s', mtbf: '950h', slo: '100.0%' },
    { dept: 'Enterprise Memory', target: '50 ms', p95: '34.0 ms', p99: '48.0 ms', avail: '99.99%', mttr: '10.0s', mtbf: '850h', slo: '99.9%' },
    { dept: 'Executive Coordination', target: '100 ms', p95: '42.0 ms', p99: '65.0 ms', avail: '99.99%', mttr: '12.0s', mtbf: '720h', slo: '100.0%' },
    { dept: 'Quality Assurance', target: '150 ms', p95: '115.0 ms', p99: '142.0 ms', avail: '99.95%', mttr: '25.0s', mtbf: '400h', slo: '99.5%' },
    { dept: 'Optical Perception', target: '250 ms', p95: '210.0 ms', p99: '245.0 ms', avail: '99.92%', mttr: '45.0s', mtbf: '180h', slo: '99.1%' },
    { dept: 'Structured Extraction', target: '600 ms', p95: '480.0 ms', p99: '585.0 ms', avail: '99.90%', mttr: '60.0s', mtbf: '140h', slo: '98.9%' },
    { dept: 'Research & Policy', target: '1200 ms', p95: '920.0 ms', p99: '1150.0 ms', avail: '99.85%', mttr: '90.0s', mtbf: '96h', slo: '98.2%' },
  ];

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 p-5 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-xl">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-2xl">⏱️</span>
            <h2 className="text-xl font-bold text-[#F8FAFC]">Enterprise SLA, SLO & SRE Error Budget Intelligence</h2>
            <Badge variant="success" size="sm">Tier 1 High Availability</Badge>
          </div>
          <p className="text-sm text-[#94A3B8] mt-1">
            MTTR (Mean Time to Recovery), MTBF (Mean Time Between Failures), 99.9%+ availability, and multi-window burn rate telemetry.
          </p>
        </div>

        <div className="text-right">
          <div className="text-xs text-[#94A3B8]">Macro System Availability</div>
          <div className="text-2xl font-bold font-mono text-[#10B981]">99.95% (4 Nines)</div>
        </div>
      </div>

      {/* SRE Metrics Strip */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card className="p-4 bg-[#0F172A]/80 border-[#1E293B]">
          <div className="text-xs font-mono text-[#94A3B8] uppercase">Macro MTTR</div>
          <div className="text-2xl font-bold font-mono text-[#00D2FF] mt-1">31.9 sec</div>
          <div className="text-[11px] text-[#64748B] mt-1">Mean Time to Recovery</div>
        </Card>
        <Card className="p-4 bg-[#0F172A]/80 border-[#1E293B]">
          <div className="text-xs font-mono text-[#94A3B8] uppercase">Macro MTBF</div>
          <div className="text-2xl font-bold font-mono text-[#10B981] mt-1">567 hours</div>
          <div className="text-[11px] text-[#64748B] mt-1">Mean Time Between Failures</div>
        </Card>
        <Card className="p-4 bg-[#0F172A]/80 border-[#1E293B]">
          <div className="text-xs font-mono text-[#94A3B8] uppercase">Error Budget Remaining</div>
          <div className="text-2xl font-bold font-mono text-[#F59E0B] mt-1">91.2%</div>
          <div className="text-[11px] text-[#64748B] mt-1">Burn Rate: 0.95x (Nominal)</div>
        </Card>
        <Card className="p-4 bg-[#0F172A]/80 border-[#1E293B]">
          <div className="text-xs font-mono text-[#94A3B8] uppercase">Active SLA Breaches</div>
          <div className="text-2xl font-bold font-mono text-[#10B981] mt-1">0 Breaches</div>
          <div className="text-[11px] text-[#64748B] mt-1">100% contracts compliant</div>
        </Card>
      </div>

      {/* SLA Table */}
      <Card className="p-5 bg-[#0F172A] border-[#1E293B] space-y-4">
        <div className="text-sm font-bold text-[#F8FAFC]">Department SLA & Latency Percentiles</div>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono">
            <thead>
              <tr className="border-b border-[#1E293B] text-[#64748B]">
                <th className="py-2.5 px-3">DEPARTMENT</th>
                <th className="py-2.5 px-3">SLA TARGET</th>
                <th className="py-2.5 px-3">P95 LATENCY</th>
                <th className="py-2.5 px-3">P99 LATENCY</th>
                <th className="py-2.5 px-3">AVAILABILITY</th>
                <th className="py-2.5 px-3">MTTR</th>
                <th className="py-2.5 px-3">MTBF</th>
                <th className="py-2.5 px-3">SLO SCORE</th>
              </tr>
            </thead>
            <tbody>
              {slaReports.map((r, idx) => (
                <tr key={idx} className="border-b border-[#1E293B]/40 hover:bg-[#131D35]/50 transition-colors">
                  <td className="py-3 px-3 font-semibold text-[#F8FAFC]">{r.dept}</td>
                  <td className="py-3 px-3 text-[#94A3B8]">{r.target}</td>
                  <td className="py-3 px-3 text-[#10B981] font-bold">{r.p95}</td>
                  <td className="py-3 px-3 text-[#38BDF8]">{r.p99}</td>
                  <td className="py-3 px-3 text-[#F8FAFC]">{r.avail}</td>
                  <td className="py-3 px-3 text-[#94A3B8]">{r.mttr}</td>
                  <td className="py-3 px-3 text-[#F59E0B]">{r.mtbf}</td>
                  <td className="py-3 px-3">
                    <Badge variant="success" size="sm">{r.slo}</Badge>
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
