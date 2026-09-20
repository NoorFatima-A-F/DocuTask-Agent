import React from 'react';
import { useMissionControl } from '../../context/MissionControlContext';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/Card';
import { Badge } from '../ui/Badge';

export const EvidenceCenterSection: React.FC = () => {
  const { state } = useMissionControl();
  const { evidenceItems } = state;

  return (
    <section className="w-full mt-8">
      <Card variant="default" className="border-[#1E293B] bg-[#0F172A]/80 backdrop-blur-md">
        <CardHeader className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2">
          <div>
            <div className="flex items-center gap-2">
              <Badge variant="intelligence" size="sm">
                STAGE 7 • LINEAGE LEDGER
              </Badge>
              <span className="text-xs text-[#94A3B8] font-mono">
                {evidenceItems.length} Verified Evidence Sources
              </span>
            </div>
            <CardTitle className="mt-2 text-lg lg:text-xl font-bold text-[#F8FAFC]">
              Empirical Evidence & SLSA Lineage Ledger
            </CardTitle>
            <p className="mt-1 text-xs text-[#94A3B8]">
              Never fabricate evidence. Every reported metric is cryptographically traceable from raw scan observation to final statistical claim.
            </p>
          </div>

          <div className="flex items-center gap-2 bg-[#131D35] px-3.5 py-2 rounded-xl border border-[#334155]/60 text-xs font-mono text-[#10B981]">
            <span>SLSA Level 3+ Compliant</span>
          </div>
        </CardHeader>

        <CardContent className="p-6 space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {evidenceItems.map((item) => (
              <div
                key={item.id}
                className="p-4 rounded-xl bg-[#131D35] border border-[#1E293B] hover:border-cyan-500/40 transition-all flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-center justify-between">
                    <span className="text-[10px] font-mono bg-[#0A0F1D] text-cyan-300 px-2 py-0.5 rounded border border-cyan-500/30">
                      {item.sourceType}
                    </span>
                    <Badge variant="success" size="sm">
                      {item.slsaLevel}
                    </Badge>
                  </div>

                  <h4 className="mt-2 text-sm font-semibold text-[#F8FAFC]">
                    {item.title}
                  </h4>

                  <p className="mt-1 text-xs font-mono text-[#94A3B8] truncate" title={item.origin}>
                    Source: {item.origin}
                  </p>
                </div>

                <div className="mt-4 pt-3 border-t border-[#1E293B] space-y-1.5 text-xs font-mono">
                  <div className="flex items-center justify-between text-[#64748B]">
                    <span>Sample Size:</span>
                    <span className="text-[#F8FAFC] font-bold">n={item.sampleCount}</span>
                  </div>
                  <div className="flex items-center justify-between text-[#64748B]">
                    <span>Confidence Added:</span>
                    <span className="text-[#10B981] font-bold">
                      +{(item.confidenceContribution * 100).toFixed(1)}%
                    </span>
                  </div>
                  <div className="flex items-center justify-between text-[#64748B] pt-1">
                    <span>Digest:</span>
                    <span
                      className="text-[#A855F7] truncate max-w-[140px]"
                      title={item.sha256Digest}
                    >
                      {item.sha256Digest.substring(0, 10)}...
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
