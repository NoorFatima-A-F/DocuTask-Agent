import React from 'react';

export interface EnterpriseFooterProps {
  onOpenCommandPalette?: () => void;
}

export const EnterpriseFooter: React.FC<EnterpriseFooterProps> = ({
  onOpenCommandPalette,
}) => {
  return (
    <footer className="w-full mt-12 pt-6 pb-8 border-t border-[#1E293B] text-xs font-mono text-[#64748B] flex flex-col sm:flex-row items-center justify-between gap-4">
      {/* Left: Build & Provenance Info */}
      <div className="flex items-center gap-3">
        <span className="text-[#94A3B8]">DocuTask Agent v2.5.0-prod</span>
        <span>•</span>
        <span className="text-[#A855F7]">Build #799784cd</span>
        <span>•</span>
        <span className="text-[#10B981]">SLSA Level 3+ Verified</span>
      </div>

      {/* Center: Live Performance Telemetry */}
      <div className="flex items-center gap-3 text-[11px]">
        <span>API Latency: 18ms</span>
        <span>•</span>
        <span className="text-[#00D2FF]">Consensus: 97%</span>
        <span>•</span>
        <span className="text-[#10B981]">10/10 Agents Healthy</span>
      </div>

      {/* Right: Keyboard Shortcuts Hint */}
      <div className="flex items-center gap-2">
        <button
          onClick={onOpenCommandPalette}
          className="flex items-center gap-1.5 bg-[#131D35] px-2.5 py-1 rounded-lg border border-[#334155] hover:border-cyan-400 text-[11px] text-[#F8FAFC] transition-colors"
        >
          <span className="text-[#00D2FF]">⌘K</span>
          <span>Command Palette</span>
        </button>
      </div>
    </footer>
  );
};
