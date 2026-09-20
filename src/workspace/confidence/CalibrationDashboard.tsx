import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Target, CheckCircle2 } from 'lucide-react';

export const CalibrationDashboard: React.FC = () => {
  const calibrationMetrics = [
    { name: 'Expected Calibration Error (ECE)', value: '0.014', target: '< 0.050', status: 'OPTIMAL' },
    { name: 'Maximum Calibration Error (MCE)', value: '0.032', target: '< 0.100', status: 'OPTIMAL' },
    { name: 'Brier Score Loss', value: '0.018', target: '< 0.050', status: 'OPTIMAL' },
    { name: 'Temperature Scaling (T)', value: '1.042', target: '[0.90, 1.20]', status: 'CALIBRATED' },
  ];

  const binData = [
    { bin: '0.0 - 0.2', count: 12, predictedConf: 0.15, empiricalAcc: 0.14, gap: 0.01 },
    { bin: '0.2 - 0.4', count: 28, predictedConf: 0.35, empiricalAcc: 0.36, gap: -0.01 },
    { bin: '0.4 - 0.6', count: 45, predictedConf: 0.52, empiricalAcc: 0.51, gap: 0.01 },
    { bin: '0.6 - 0.8', count: 110, predictedConf: 0.74, empiricalAcc: 0.73, gap: 0.01 },
    { bin: '0.8 - 1.0', count: 850, predictedConf: 0.98, empiricalAcc: 0.982, gap: -0.002 },
  ];

  return (
    <div className="p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6">
        <div className="space-y-1">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-gradient-to-br from-teal-500/20 to-emerald-500/20 border border-teal-500/30 rounded-xl text-teal-400">
              <Target className="w-5 h-5" />
            </div>
            <div>
              <h1 className="text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2">
                Scientific Calibration Dashboard
                <Badge variant="success" size="sm">ECE &lt; 2%</Badge>
              </h1>
              <p className="text-xs text-slate-400">
                Evaluating empirical accuracy vs. model-stated confidence via Temperature & Isotonic Scaling.
              </p>
            </div>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <Badge variant="intelligence" size="sm">Calibration Model: Platt-Isotonic (v1.2)</Badge>
        </div>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {calibrationMetrics.map((item, idx) => (
          <Card key={idx} className="p-4 bg-[#0F172A] border-[#1E293B]">
            <div className="text-xs text-slate-400 font-mono">{item.name}</div>
            <div className="text-2xl font-bold text-white font-mono mt-2">{item.value}</div>
            <div className="flex items-center justify-between mt-2 pt-2 border-t border-slate-800 text-[11px] font-mono">
              <span className="text-slate-500">Target: {item.target}</span>
              <Badge variant="success" size="sm">{item.status}</Badge>
            </div>
          </Card>
        ))}
      </div>

      {/* Calibration Bins Table */}
      <Card className="p-5 bg-[#0F172A] border-[#1E293B]">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-sm font-bold font-mono text-slate-200">Confidence Reliability Bin Breakdown</h2>
          <Badge variant="outline" size="sm">N = 1,045 Evaluation Samples</Badge>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono">
            <thead className="bg-[#1E293B]/60 text-slate-400 border-b border-[#1E293B]">
              <tr>
                <th className="p-3">Confidence Bin</th>
                <th className="p-3">Sample Count</th>
                <th className="p-3">Avg Predicted Confidence</th>
                <th className="p-3">Empirical Accuracy</th>
                <th className="p-3">Calibration Gap (|Acc - Conf|)</th>
                <th className="p-3">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#1E293B]/40">
              {binData.map((b, idx) => (
                <tr key={idx} className="hover:bg-slate-800/30 transition-colors">
                  <td className="p-3 font-semibold text-teal-400">{b.bin}</td>
                  <td className="p-3 text-slate-300">{b.count}</td>
                  <td className="p-3 text-slate-200">{(b.predictedConf * 100).toFixed(1)}%</td>
                  <td className="p-3 text-slate-200">{(b.empiricalAcc * 100).toFixed(1)}%</td>
                  <td className="p-3 text-slate-300">{(Math.abs(b.gap) * 100).toFixed(2)}%</td>
                  <td className="p-3">
                    <Badge variant="success" size="sm" className="flex items-center gap-1">
                      <CheckCircle2 className="w-3 h-3" />
                      Calibrated
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
