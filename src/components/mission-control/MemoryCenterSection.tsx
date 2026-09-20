import React from 'react';
import { useMissionControl } from '../../context/MissionControlContext';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/Card';
import { Badge } from '../ui/Badge';

export const MemoryCenterSection: React.FC = () => {
  const { state } = useMissionControl();
  const { memoryEntries } = state;

  return (
    <section className="w-full mt-8">
      <Card variant="default" className="border-[#1E293B] bg-[#0F172A]/80 backdrop-blur-md">
        <CardHeader className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2">
          <div>
            <div className="flex items-center gap-2">
              <Badge variant="intelligence" size="sm">
                STAGE 8 • SCIENTIFIC MEMORY
              </Badge>
              <span className="text-xs text-[#94A3B8] font-mono">
                {memoryEntries.length} Active Memory Traces
              </span>
            </div>
            <CardTitle className="mt-2 text-lg lg:text-xl font-bold text-[#F8FAFC]">
              Long-Term Memory & Exponential Retention Decay
            </CardTitle>
            <p className="mt-1 text-xs text-[#94A3B8]">
              The autonomous employee learns from previous missions, recalling optimal binarization parameters and avoiding historical failure patterns using mathematical retention decay (R = e^(-&lambda;&Delta;t)).
            </p>
          </div>
        </CardHeader>

        <CardContent className="p-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {memoryEntries.map((mem) => (
              <div
                key={mem.id}
                className="p-4 rounded-xl bg-[#131D35] border border-[#1E293B] hover:border-cyan-500/40 transition-all flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-center justify-between">
                    <span className="text-[10px] font-mono bg-[#0A0F1D] text-pink-300 px-2 py-0.5 rounded border border-pink-500/30">
                      {mem.store}
                    </span>
                    <span className="text-[10px] font-mono text-[#10B981] bg-[#0A0F1D] px-2 py-0.5 rounded">
                      Recalled {mem.recallCount}x
                    </span>
                  </div>

                  <h4 className="mt-2 text-sm font-semibold text-[#F8FAFC]">
                    {mem.title}
                  </h4>

                  <p className="mt-1 text-xs text-[#94A3B8] leading-relaxed">
                    {mem.summary}
                  </p>
                </div>

                <div className="mt-4 pt-3 border-t border-[#1E293B] space-y-1.5 text-xs font-mono">
                  <div className="flex items-center justify-between text-[#64748B]">
                    <span>Retention Weight (R):</span>
                    <span className="text-[#00D2FF] font-bold">
                      {(mem.retentionWeight * 100).toFixed(0)}%
                    </span>
                  </div>

                  <div className="flex items-center justify-between text-[#64748B]">
                    <span>Relevance Similarity:</span>
                    <span className="text-[#F8FAFC] font-bold">
                      {(mem.similarityScore * 100).toFixed(0)}%
                    </span>
                  </div>

                  <div className="flex items-center justify-between text-[#64748B]">
                    <span>Half-Life:</span>
                    <span className="text-[#94A3B8]">{mem.decayHalfLifeDays} days</span>
                  </div>

                  <div className="pt-2 border-t border-[#1E293B]/60 flex items-center justify-between text-[10px] text-[#64748B]">
                    <span>Proof:</span>
                    <span className="text-[#A855F7] truncate max-w-[120px]" title={mem.sha256Proof}>
                      {mem.sha256Proof.substring(0, 10)}...
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </section>
  );
};
