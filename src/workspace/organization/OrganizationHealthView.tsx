import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const OrganizationHealthView: React.FC = () => {
  const healthData = [
    { dept: 'Corporate Governance', score: 100.0, utilPen: '0.0', queuePen: '0.0', errPen: '0.0', burnout: 'NOMINAL', risk: '0.00' },
    { dept: 'Mathematical Validation', score: 99.8, utilPen: '0.0', queuePen: '0.2', errPen: '0.0', burnout: 'NOMINAL', risk: '0.01' },
    { dept: 'Enterprise Memory', score: 99.5, utilPen: '0.0', queuePen: '0.3', errPen: '0.2', burnout: 'NOMINAL', risk: '0.02' },
    { dept: 'Executive Coordination', score: 99.2, utilPen: '0.0', queuePen: '0.8', errPen: '0.0', burnout: 'NOMINAL', risk: '0.02' },
    { dept: 'Quality Assurance', score: 98.9, utilPen: '0.0', queuePen: '0.7', errPen: '0.4', burnout: 'NOMINAL', risk: '0.03' },
    { dept: 'Structured Extraction', score: 98.1, utilPen: '0.0', queuePen: '0.9', errPen: '1.0', burnout: 'ELEVATED', risk: '0.05' },
    { dept: 'Research & Policy', score: 97.4, utilPen: '0.0', queuePen: '1.2', errPen: '1.4', burnout: 'NOMINAL', risk: '0.06' },
    { dept: 'Optical Perception', score: 96.5, utilPen: '0.0', queuePen: '1.9', errPen: '1.6', burnout: 'NOMINAL', risk: '0.08' },
  ];

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 p-5 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-xl">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-2xl">🩺</span>
            <h2 className="text-xl font-bold text-[#F8FAFC]">Organization Health Intelligence & Diagnostics</h2>
            <Badge variant="success" size="sm">Tier 1 Resilient</Badge>
          </div>
          <p className="text-sm text-[#94A3B8] mt-1">
            Real-time department health scores, burnout indicators, queue congestion penalties, and systemic bottleneck forecasting.
          </p>
        </div>

        <div className="text-right">
          <div className="text-xs text-[#94A3B8]">Composite Enterprise Index</div>
          <div className="text-2xl font-bold font-mono text-[#10B981]">98.7 / 100.0</div>
        </div>
      </div>

      {/* Formula & Diagnostic Alert */}
      <Card className="p-4 bg-[#0F172A] border-[#1E293B]">
        <div className="text-xs font-mono text-[#94A3B8] uppercase">Diagnostic Scoring Formula</div>
        <div className="text-xs text-[#00D2FF] font-mono mt-1">
          Health(d) = 100 - UtilizationPenalty(&gt;85%) - QueueCongestionPenalty - (ErrorRate × 20)
        </div>
      </Card>

      {/* Health Matrix Table */}
      <Card className="p-5 bg-[#0F172A] border-[#1E293B] space-y-4">
        <div className="text-sm font-bold text-[#F8FAFC]">Department Health Diagnostics Matrix</div>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono">
            <thead>
              <tr className="border-b border-[#1E293B] text-[#64748B]">
                <th className="py-2.5 px-3">DEPARTMENT</th>
                <th className="py-2.5 px-3">HEALTH SCORE</th>
                <th className="py-2.5 px-3">UTIL PENALTY</th>
                <th className="py-2.5 px-3">QUEUE PENALTY</th>
                <th className="py-2.5 px-3">ERROR PENALTY</th>
                <th className="py-2.5 px-3">BURNOUT RISK</th>
                <th className="py-2.5 px-3">SLA BREACH RISK</th>
              </tr>
            </thead>
            <tbody>
              {healthData.map((h, idx) => (
                <tr key={idx} className="border-b border-[#1E293B]/40 hover:bg-[#131D35]/50 transition-colors">
                  <td className="py-3 px-3 font-semibold text-[#F8FAFC]">{h.dept}</td>
                  <td className="py-3 px-3">
                    <span className="font-bold text-[#10B981]">{h.score}%</span>
                  </td>
                  <td className="py-3 px-3 text-[#94A3B8]">-{h.utilPen}</td>
                  <td className="py-3 px-3 text-[#F59E0B]">-{h.queuePen}</td>
                  <td className="py-3 px-3 text-[#EF4444]">-{h.errPen}</td>
                  <td className="py-3 px-3">
                    <Badge variant={h.burnout === 'NOMINAL' ? 'success' : 'warning'} size="sm">
                      {h.burnout}
                    </Badge>
                  </td>
                  <td className="py-3 px-3 text-[#38BDF8]">{h.risk}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
};
