import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const DriftDetectionCenterView: React.FC = () => {
  const monitoredFeatures = [
    {
      featureName: 'Latency Distribution (ms)',
      psi: 0.042,
      klDivergence: 0.018,
      wasserstein: 14.5,
      sequentialAlarm: 'NO_ALARM',
      status: 'NEGLIGIBLE_DRIFT',
      mitigation: 'Distribution stable. No recalibration needed.',
    },
    {
      featureName: 'Extraction Accuracy (Exact Match)',
      psi: 0.028,
      klDivergence: 0.011,
      wasserstein: 0.008,
      sequentialAlarm: 'NO_ALARM',
      status: 'NEGLIGIBLE_DRIFT',
      mitigation: 'Ground-truth accuracy remains calibrated.',
    },
    {
      featureName: 'Document OCR Noise Level',
      psi: 0.142,
      klDivergence: 0.089,
      wasserstein: 0.045,
      sequentialAlarm: 'WARNING_ADWIN',
      status: 'DRIFT_WARNING',
      mitigation: 'Increase shadow sampling rate; monitor residual autocorrelation.',
    },
    {
      featureName: 'API Token Consumption',
      psi: 0.065,
      klDivergence: 0.032,
      wasserstein: 22.0,
      sequentialAlarm: 'NO_ALARM',
      status: 'NEGLIGIBLE_DRIFT',
      mitigation: 'Token budget within ±5% bounds.',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="p-6 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-xl">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xl">🌊</span>
              <h2 className="text-lg font-bold font-mono text-[#F8FAFC]">
                Online Statistical Drift Detection Center
              </h2>
              <Badge variant="success" size="sm">
                ADWIN & PSI ACTIVE
              </Badge>
            </div>
            <p className="text-sm font-mono text-[#94A3B8] mt-1">
              Streaming distribution divergence tracking (PSI, KL, Wasserstein) and sequential change-point alarms (ADWIN, CUSUM).
            </p>
          </div>
        </div>
      </div>

      {/* Metric Breakdown Table */}
      <Card className="p-6 bg-[#0F172A] border-[#1E293B]">
        <h3 className="text-sm font-bold font-mono text-[#F8FAFC] mb-4">
          Feature Distribution Divergence & Sequential Alarms
        </h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left font-mono text-xs">
            <thead>
              <tr className="border-b border-[#1E293B] text-[#94A3B8]">
                <th className="pb-3">Monitored Feature</th>
                <th className="pb-3">PSI (Pop. Stability)</th>
                <th className="pb-3">KL Divergence</th>
                <th className="pb-3">Wasserstein (EMD)</th>
                <th className="pb-3">Sequential Alarm</th>
                <th className="pb-3">Severity</th>
                <th className="pb-3">Prescribed Mitigation</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#1E293B]">
              {monitoredFeatures.map((m, idx) => (
                <tr key={idx} className="hover:bg-[#1E293B]/40 transition-colors">
                  <td className="py-3 font-bold text-[#F8FAFC]">{m.featureName}</td>
                  <td className="py-3">
                    <span className={m.psi < 0.1 ? 'text-emerald-400' : 'text-amber-400 font-bold'}>
                      {m.psi.toFixed(3)}
                    </span>
                    <span className="text-[#64748B] text-[10px] ml-1">(&lt;0.10)</span>
                  </td>
                  <td className="py-3 text-cyan-400">{m.klDivergence.toFixed(3)}</td>
                  <td className="py-3 text-indigo-400">{m.wasserstein.toFixed(2)}</td>
                  <td className="py-3">
                    <Badge variant={m.sequentialAlarm === 'NO_ALARM' ? 'default' : 'warning'} size="sm">
                      {m.sequentialAlarm}
                    </Badge>
                  </td>
                  <td className="py-3">
                    <Badge variant={m.status === 'NEGLIGIBLE_DRIFT' ? 'success' : 'warning'} size="sm">
                      {m.status}
                    </Badge>
                  </td>
                  <td className="py-3 text-[#94A3B8] text-[11px]">{m.mitigation}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
};
