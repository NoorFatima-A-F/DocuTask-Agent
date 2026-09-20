import React from 'react';
import { useWorkspace } from '../context/WorkspaceContext';
import { CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';

export const ConfidenceExplorerPanel: React.FC = () => {
  const { confidenceConstituents } = useWorkspace();

  return (
    <div className="w-full flex flex-col h-[700px] rounded-2xl bg-[#0F172A]/90 border border-[#1E293B] shadow-2xl overflow-hidden">
      <CardHeader className="flex flex-row items-center justify-between py-4 px-6 border-b border-[#1E293B] bg-[#131D35]/50">
        <div>
          <div className="flex items-center gap-2">
            <Badge variant="intelligence" size="sm">
              CONFIDENCE DECOMPOSITION
            </Badge>
            <span className="text-xs text-[#94A3B8] font-mono">
              6 Constituent Pillars
            </span>
          </div>
          <CardTitle className="mt-1 text-base font-bold text-[#F8FAFC]">
            Mathematical Confidence & Evidence Contribution
          </CardTitle>
        </div>

        <div className="text-xs font-mono text-[#00D2FF] bg-[#0A0F1D] px-3.5 py-1.5 rounded-lg border border-cyan-500/30 font-bold">
          Total Composite: 97.2%
        </div>
      </CardHeader>

      <CardContent className="flex-1 overflow-y-auto p-6 space-y-4">
        <p className="text-xs text-[#94A3B8] leading-relaxed">
          Instead of opaque single numbers, DocuTask Agent decomposes confidence into independently verifiable empirical contributions:
        </p>

        <div className="space-y-4 mt-4">
          {confidenceConstituents.map((item) => (
            <div
              key={item.name}
              className="p-4 rounded-xl bg-[#131D35] border border-[#1E293B] space-y-2 hover:border-cyan-500/40 transition-colors"
            >
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1 text-xs">
                <div className="flex items-center gap-2">
                  <span className="font-bold text-[#F8FAFC]">{item.name}</span>
                  <Badge variant="default" size="sm" className="font-mono text-[10px]">
                    {item.category}
                  </Badge>
                </div>

                <div className="flex items-center gap-3 font-mono">
                  {item.sampleSize && (
                    <span className="text-[#64748B] text-[11px]">n={item.sampleSize}</span>
                  )}
                  <span className="text-[#00D2FF] font-bold">
                    {item.contributionPercentage}% contribution
                  </span>
                  <span className="text-[#10B981]">
                    (Score: {(item.confidenceScore * 100).toFixed(1)}%)
                  </span>
                </div>
              </div>

              {/* Visual Contribution Bar */}
              <div className="h-2 w-full bg-[#0A0F1D] rounded-full overflow-hidden">
                <div
                  className="h-full bg-gradient-to-r from-[#0066FF] to-[#00D2FF] rounded-full"
                  style={{ width: `${item.contributionPercentage * 2.5}%` }}
                />
              </div>

              <p className="text-[11px] text-[#94A3B8] leading-relaxed">
                {item.description}
              </p>
            </div>
          ))}
        </div>
      </CardContent>
    </div>
  );
};
