import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { LineChart, CheckCircle2 } from 'lucide-react';

export const ReliabilityDiagramViewer: React.FC = () => {
  const points = [
    { x: 10, conf: 0.1, acc: 0.11 },
    { x: 30, conf: 0.3, acc: 0.29 },
    { x: 50, conf: 0.5, acc: 0.49 },
    { x: 70, conf: 0.7, acc: 0.71 },
    { x: 90, conf: 0.9, acc: 0.89 },
    { x: 98, conf: 0.98, acc: 0.982 },
  ];

  return (
    <div className="p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6">
        <div className="space-y-1">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-gradient-to-br from-blue-500/20 to-indigo-500/20 border border-blue-500/30 rounded-xl text-blue-400">
              <LineChart className="w-5 h-5" />
            </div>
            <div>
              <h1 className="text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2">
                Reliability Diagram Viewer
                <Badge variant="success" size="sm">Diagonal Alignment (y=x)</Badge>
              </h1>
              <p className="text-xs text-slate-400">
                Visualizing empirical probability calibration curves vs ideal theoretical confidence line.
              </p>
            </div>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <Badge variant="intelligence" size="sm">Calibration Index: 0.989</Badge>
        </div>
      </div>

      {/* SVG Reliability Diagram */}
      <Card className="p-6 bg-[#0F172A] border-[#1E293B]">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-sm font-bold font-mono text-slate-200">
            Calibration Curve (P_true vs P_conf)
          </h2>
          <div className="flex items-center gap-4 text-xs font-mono">
            <span className="flex items-center gap-1.5 text-slate-400">
              <span className="w-3 h-0.5 bg-slate-500 inline-block border-dashed border-b"></span> Ideal (y = x)
            </span>
            <span className="flex items-center gap-1.5 text-cyan-400">
              <span className="w-3 h-1 bg-cyan-400 rounded-full inline-block"></span> Empirical Curve
            </span>
          </div>
        </div>

        <div className="relative w-full h-80 bg-slate-950/60 rounded-xl border border-slate-800 p-6 flex flex-col justify-between">
          <svg className="w-full h-full" viewBox="0 0 400 200" preserveAspectRatio="none">
            {/* Grid lines */}
            <line x1="0" y1="200" x2="400" y2="200" stroke="#334155" strokeWidth="1" />
            <line x1="0" y1="150" x2="400" y2="150" stroke="#1E293B" strokeWidth="1" strokeDasharray="4 4" />
            <line x1="0" y1="100" x2="400" y2="100" stroke="#1E293B" strokeWidth="1" strokeDasharray="4 4" />
            <line x1="0" y1="50" x2="400" y2="50" stroke="#1E293B" strokeWidth="1" strokeDasharray="4 4" />
            <line x1="0" y1="0" x2="400" y2="0" stroke="#1E293B" strokeWidth="1" strokeDasharray="4 4" />

            {/* Ideal y=x line */}
            <line x1="0" y1="200" x2="400" y2="0" stroke="#64748B" strokeWidth="2" strokeDasharray="6 6" />

            {/* Calibration empirical line */}
            <polyline
              fill="none"
              stroke="#22D3EE"
              strokeWidth="3"
              points="0,200 40,178 120,142 200,102 280,58 360,22 400,3.6"
            />

            {/* Points */}
            <circle cx="40" cy="178" r="4" fill="#22D3EE" />
            <circle cx="120" cy="142" r="4" fill="#22D3EE" />
            <circle cx="200" cy="102" r="4" fill="#22D3EE" />
            <circle cx="280" cy="58" r="4" fill="#22D3EE" />
            <circle cx="360" cy="22" r="4" fill="#22D3EE" />
            <circle cx="400" cy="3.6" r="4" fill="#10B981" />
          </svg>

          <div className="flex justify-between text-[10px] font-mono text-slate-500 pt-2 border-t border-slate-800">
            <span>0.0 (Low Conf)</span>
            <span>0.25</span>
            <span>0.50</span>
            <span>0.75</span>
            <span>1.0 (High Conf)</span>
          </div>
        </div>
      </Card>

      {/* Point details */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
        {points.map((p, idx) => (
          <Card key={idx} className="p-3 bg-[#0F172A] border-[#1E293B] text-center font-mono">
            <div className="text-[11px] text-slate-400">Target #{idx + 1}</div>
            <div className="text-sm font-bold text-cyan-400 mt-1">{(p.conf * 100).toFixed(0)}% Conf</div>
            <div className="text-xs text-slate-300 mt-0.5">{(p.acc * 100).toFixed(1)}% Acc</div>
            <Badge variant="success" size="sm" className="mt-2 text-[10px]">
              <CheckCircle2 className="w-2.5 h-2.5 inline mr-1" />
              Calibrated
            </Badge>
          </Card>
        ))}
      </div>
    </div>
  );
};
