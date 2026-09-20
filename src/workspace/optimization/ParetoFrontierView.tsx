import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const ParetoFrontierView: React.FC = () => {
  const paretoPoints = [
    { id: 'P1', name: 'Ultra-Fast Wavefront', accuracy: 0.912, latencyMs: 320, costUsd: 0.002, isSelected: false },
    { id: 'P2', name: 'Balanced Hybrid Optimizer', accuracy: 0.985, latencyMs: 650, costUsd: 0.012, isSelected: true },
    { id: 'P3', name: 'High Precision Ensemble', accuracy: 0.992, latencyMs: 1400, costUsd: 0.028, isSelected: false },
    { id: 'P4', name: 'Max Reasoning Gemini Pro', accuracy: 0.998, latencyMs: 2400, costUsd: 0.045, isSelected: false },
  ];

  const dominatedPoints = [
    { id: 'D1', name: 'Greedy Heuristic Single-Pass', accuracy: 0.935, latencyMs: 1450, costUsd: 0.028 },
    { id: 'D2', name: 'Naive Retry Loop', accuracy: 0.920, latencyMs: 2100, costUsd: 0.035 },
    { id: 'D3', name: 'Uncalibrated Model Route', accuracy: 0.890, latencyMs: 980, costUsd: 0.019 },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="p-6 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-xl">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xl">📈</span>
              <h2 className="text-lg font-bold font-mono text-[#F8FAFC]">
                Pareto Frontier & Trade-off Surface
              </h2>
              <Badge variant="intelligence" size="sm">
                NON-DOMINATED SORTING
              </Badge>
            </div>
            <p className="text-xs text-[#94A3B8] mt-1">
              Visualizing the non-dominated Pareto optimal set against strictly dominated candidate execution trajectories.
            </p>
          </div>
          <div className="flex items-center gap-4">
            <div className="text-right">
              <div className="text-xs font-mono text-[#94A3B8]">Hypervolume (HV)</div>
              <div className="text-lg font-mono font-bold text-cyan-400">0.8942</div>
            </div>
            <div className="text-right border-l border-[#1E293B] pl-4">
              <div className="text-xs font-mono text-[#94A3B8]">Frontier Density</div>
              <div className="text-lg font-mono font-bold text-emerald-400">4 Points</div>
            </div>
          </div>
        </div>
      </div>

      {/* Visual Canvas Representation */}
      <Card className="p-6 bg-[#0F172A] border border-[#1E293B] space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-bold font-mono text-[#F8FAFC]">
            Trade-off Plane: Accuracy (%) vs Latency (ms) vs Cost ($)
          </h3>
          <div className="flex items-center gap-3 text-xs font-mono">
            <span className="flex items-center gap-1 text-emerald-400">
              <span className="h-2.5 w-2.5 rounded-full bg-emerald-400 inline-block" /> Pareto Optimal
            </span>
            <span className="flex items-center gap-1 text-[#64748B]">
              <span className="h-2.5 w-2.5 rounded-full bg-rose-500/60 inline-block" /> Dominated Plan
            </span>
          </div>
        </div>

        {/* 2D Tradeoff Grid Visualization */}
        <div className="relative h-64 bg-[#0A0F1D] rounded-xl border border-[#1E293B] p-4 flex flex-col justify-between">
          {/* Axis Labels */}
          <div className="text-[10px] font-mono text-[#64748B]">▲ Accuracy (Ideal: 100%)</div>
          
          {/* Simulated Scatter Plot Points */}
          <div className="relative w-full h-44">
            {/* Pareto Frontier Line */}
            <svg className="absolute inset-0 w-full h-full pointer-events-none">
              <polyline
                fill="none"
                stroke="#06b6d4"
                strokeWidth="2"
                strokeDasharray="4,4"
                points="80,140 240,40 480,24 720,12"
              />
            </svg>

            {/* Pareto Points */}
            {paretoPoints.map((p) => {
              const leftPos = `${(p.latencyMs / 2600) * 85 + 5}%`;
              const topPos = `${(1 - (p.accuracy - 0.88) / 0.12) * 75 + 10}%`;
              return (
                <div
                  key={p.id}
                  style={{ left: leftPos, top: topPos }}
                  className={`absolute -translate-x-1/2 -translate-y-1/2 group cursor-pointer`}
                >
                  <div
                    className={`h-4 w-4 rounded-full flex items-center justify-center text-[9px] font-bold font-mono text-black transition-transform group-hover:scale-125 ${
                      p.isSelected ? 'bg-emerald-400 ring-4 ring-emerald-500/30' : 'bg-cyan-400'
                    }`}
                  >
                    {p.id}
                  </div>
                  <div className="hidden group-hover:block absolute bottom-6 left-1/2 -translate-x-1/2 bg-[#0F172A] border border-[#334155] p-2 rounded-lg text-[10px] font-mono whitespace-nowrap shadow-xl z-20">
                    <div className="font-bold text-[#F8FAFC]">{p.name}</div>
                    <div className="text-emerald-400">Acc: {(p.accuracy * 100).toFixed(1)}%</div>
                    <div className="text-cyan-400">Lat: {p.latencyMs}ms | Cost: ${p.costUsd}</div>
                  </div>
                </div>
              );
            })}

            {/* Dominated Points */}
            {dominatedPoints.map((d) => {
              const leftPos = `${(d.latencyMs / 2600) * 85 + 5}%`;
              const topPos = `${(1 - (d.accuracy - 0.88) / 0.12) * 75 + 10}%`;
              return (
                <div
                  key={d.id}
                  style={{ left: leftPos, top: topPos }}
                  className="absolute -translate-x-1/2 -translate-y-1/2 group cursor-pointer"
                >
                  <div className="h-3 w-3 rounded-full bg-rose-500/70 border border-rose-400 text-[8px] flex items-center justify-center font-bold text-white group-hover:scale-125 transition-transform">
                    {d.id}
                  </div>
                  <div className="hidden group-hover:block absolute bottom-5 left-1/2 -translate-x-1/2 bg-[#0F172A] border border-rose-500/50 p-2 rounded-lg text-[10px] font-mono whitespace-nowrap shadow-xl z-20">
                    <div className="font-bold text-rose-300">{d.name} (Dominated)</div>
                    <div>Acc: {(d.accuracy * 100).toFixed(1)}% | Lat: {d.latencyMs}ms</div>
                  </div>
                </div>
              );
            })}
          </div>

          <div className="flex justify-between text-[10px] font-mono text-[#64748B]">
            <span>Fast (0ms)</span>
            <span>Execution Latency (ms) ►</span>
            <span>Slow (2600ms)</span>
          </div>
        </div>
      </Card>
    </div>
  );
};
