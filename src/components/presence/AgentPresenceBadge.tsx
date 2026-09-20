import React from 'react';
import { polishTokens } from '../../design-system/tokens/polish';
import type { AgentRoleType } from '../agent';

export interface AgentPresenceBadgeProps {
  role: AgentRoleType;
  name: string;
  status: 'ONLINE' | 'THINKING' | 'EXECUTING' | 'WAITING' | 'PAUSED';
  currentThought?: string;
  confidence?: number;
  size?: 'sm' | 'md' | 'lg';
}

export const AgentPresenceBadge: React.FC<AgentPresenceBadgeProps> = ({
  role,
  name,
  status,
  currentThought,
  confidence,
  size = 'md',
}) => {
  const avatar =
    polishTokens.agentAvatars[role as keyof typeof polishTokens.agentAvatars] || {
      avatarBg: 'from-blue-600 to-cyan-600',
      tagline: 'Autonomous deliberation',
      icon: '🤖',
    };

  const isThinking = status === 'THINKING' || status === 'EXECUTING';

  return (
    <div className="flex items-center gap-3 p-3 rounded-2xl bg-[#131D35] border border-[#1E293B] shadow-md hover:border-cyan-500/40 transition-all">
      {/* Avatar with Pulse Rings */}
      <div className="relative shrink-0">
        {isThinking && (
          <span className="absolute -inset-1 rounded-2xl bg-cyan-400 opacity-40 animate-ping" />
        )}
        <div
          className={`relative rounded-xl bg-gradient-to-tr ${avatar.avatarBg} flex items-center justify-center text-white font-bold shadow-md ${
            size === 'sm'
              ? 'h-8 w-8 text-xs'
              : size === 'lg'
              ? 'h-12 w-12 text-lg'
              : 'h-10 w-10 text-sm'
          }`}
        >
          <span>{avatar.icon}</span>
        </div>

        {/* Live Dot */}
        <span
          className={`absolute -bottom-1 -right-1 h-3 w-3 rounded-full border-2 border-[#0F172A] ${
            status === 'EXECUTING'
              ? 'bg-[#00D2FF] animate-pulse'
              : status === 'THINKING'
              ? 'bg-amber-400 animate-pulse'
              : 'bg-[#10B981]'
          }`}
        />
      </div>

      {/* Agent Identity & Live Personality Blurb */}
      <div className="min-w-0 flex-1">
        <div className="flex items-center justify-between gap-2">
          <span className="text-xs font-bold text-[#F8FAFC] truncate">{name}</span>
          {confidence !== undefined && (
            <span className="text-[10px] font-mono text-[#00D2FF] font-bold shrink-0">
              {(confidence * 100).toFixed(0)}%
            </span>
          )}
        </div>

        <p className="text-[11px] text-[#94A3B8] font-mono truncate mt-0.5">
          {currentThought ? `"${currentThought}"` : avatar.tagline}
        </p>
      </div>
    </div>
  );
};
