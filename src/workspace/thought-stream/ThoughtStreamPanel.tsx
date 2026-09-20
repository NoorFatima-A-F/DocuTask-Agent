import React, { useState } from 'react';
import { useMissionControl } from '../../context/MissionControlContext';
import { CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';

export const ThoughtStreamPanel: React.FC = () => {
  const { state } = useMissionControl();
  const { thoughtStream } = state;
  const [filterRole, setFilterRole] = useState<string>('ALL');

  const filtered =
    filterRole === 'ALL'
      ? thoughtStream
      : thoughtStream.filter((t) => t.agentRole === filterRole);

  return (
    <div className="w-full flex flex-col h-[700px] rounded-2xl bg-[#0F172A]/95 border border-[#1E293B] shadow-2xl overflow-hidden font-mono">
      {/* Terminal Bar Header */}
      <CardHeader className="flex flex-row items-center justify-between py-4 px-6 border-b border-[#1E293B] bg-[#0A0F1D]">
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-1.5">
            <div className="h-3 w-3 rounded-full bg-red-500/80" />
            <div className="h-3 w-3 rounded-full bg-amber-500/80" />
            <div className="h-3 w-3 rounded-full bg-emerald-500/80" />
          </div>
          <div>
            <CardTitle className="text-sm font-bold text-[#F8FAFC]">
              DocuTask Autonomous Cognition Stream
            </CardTitle>
            <span className="text-[11px] text-[#00D2FF]">
              ● LIVE DELIBERATION FEED • {filtered.length} thoughts captured
            </span>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <Button
            variant={filterRole === 'ALL' ? 'intelligence' : 'ghost'}
            size="sm"
            onClick={() => setFilterRole('ALL')}
            className="text-[11px]"
          >
            All
          </Button>
          <Button
            variant={filterRole === 'PLANNER' ? 'intelligence' : 'ghost'}
            size="sm"
            onClick={() => setFilterRole('PLANNER')}
            className="text-[11px]"
          >
            Planner
          </Button>
          <Button
            variant={filterRole === 'MEMORY' ? 'intelligence' : 'ghost'}
            size="sm"
            onClick={() => setFilterRole('MEMORY')}
            className="text-[11px]"
          >
            Memory
          </Button>
          <Button
            variant={filterRole === 'REFLECTION' ? 'intelligence' : 'ghost'}
            size="sm"
            onClick={() => setFilterRole('REFLECTION')}
            className="text-[11px]"
          >
            Reflection
          </Button>
        </div>
      </CardHeader>

      {/* Terminal Thought Body */}
      <CardContent className="flex-1 overflow-y-auto p-6 space-y-4 bg-[#0A0F1D]/70">
        {filtered.map((thought) => (
          <div
            key={thought.id}
            className="p-4 rounded-xl bg-[#131D35]/80 border border-[#1E293B] hover:border-cyan-500/40 transition-colors space-y-2"
          >
            <div className="flex items-center justify-between text-xs">
              <div className="flex items-center gap-2">
                <span className="text-[#64748B]">[{thought.timestampUtc}]</span>
                <span className="font-bold text-[#00D2FF]">{thought.agentName}</span>
                <Badge variant="intelligence" size="sm">
                  {thought.thoughtType}
                </Badge>
              </div>

              {thought.confidence !== undefined && (
                <span className="text-[#10B981] text-xs">
                  conf: {(thought.confidence * 100).toFixed(1)}%
                </span>
              )}
            </div>

            <p className="text-xs text-[#F8FAFC] leading-relaxed pl-4 border-l-2 border-cyan-500/40">
              {thought.content}
            </p>

            {thought.referencedArtifactId && (
              <div className="pt-1 text-[11px] text-[#A855F7] flex items-center gap-1.5">
                <span>🔗 Memory Reference:</span>
                <span className="underline cursor-pointer">{thought.referencedArtifactId}</span>
              </div>
            )}
          </div>
        ))}

        {/* Live Cursor Pulse */}
        <div className="flex items-center gap-2 text-xs text-[#00D2FF] pt-2">
          <span className="animate-pulse">❯❯</span>
          <span className="animate-pulse">DocuTask cognitive daemon deliberating...</span>
        </div>
      </CardContent>
    </div>
  );
};
