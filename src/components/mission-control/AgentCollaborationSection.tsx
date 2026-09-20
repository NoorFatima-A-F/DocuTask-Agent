import React, { useState } from 'react';
import { useMissionControl } from '../../context/MissionControlContext';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/Card';
import { Badge } from '../ui/Badge';
import { StatusIndicator } from '../ui/StatusIndicator';

export const AgentCollaborationSection: React.FC = () => {
  const { state } = useMissionControl();
  const { agentTeam, thoughtStream } = state;
  const [filterRole, setFilterRole] = useState<string>('ALL');

  const filteredThoughts =
    filterRole === 'ALL'
      ? thoughtStream
      : thoughtStream.filter((t) => t.agentRole === filterRole);

  const getAgentStatusType = (
    stateVal: string
  ): 'idle' | 'thinking' | 'executing' | 'verifying' | 'learning' | 'waiting' => {
    switch (stateVal) {
      case 'THINKING':
      case 'OBSERVING':
      case 'PLANNING':
        return 'thinking';
      case 'EXECUTING':
        return 'executing';
      case 'VERIFYING':
        return 'verifying';
      case 'LEARNING':
        return 'learning';
      case 'WAITING_FOR_HITL':
        return 'waiting';
      case 'IDLE':
      default:
        return 'idle';
    }
  };

  return (
    <section className="w-full mt-8">
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* LEFT: 10-Agent Team Grid (7 cols) */}
        <div className="lg:col-span-7">
          <Card variant="default" className="border-[#1E293B] bg-[#0F172A]/80 backdrop-blur-md h-full">
            <CardHeader className="flex flex-row items-center justify-between pb-3">
              <div>
                <div className="flex items-center gap-2">
                  <Badge variant="intelligence" size="sm">
                    MULTI-AGENT FLEET
                  </Badge>
                  <span className="text-xs text-[#94A3B8] font-mono">10 Specialized Roles</span>
                </div>
                <CardTitle className="mt-2 text-lg font-bold text-[#F8FAFC]">
                  Autonomous Agent Team
                </CardTitle>
              </div>

              <div className="flex items-center gap-2 text-xs font-mono text-[#10B981] bg-[#131D35] px-3 py-1.5 rounded-lg border border-[#334155]/60">
                <span>Fleet Health: 100% OK</span>
              </div>
            </CardHeader>

            <CardContent className="p-4 grid grid-cols-1 sm:grid-cols-2 gap-3 max-h-[560px] overflow-y-auto">
              {agentTeam.map((agent) => (
                <div
                  key={agent.agentId}
                  onClick={() => setFilterRole(filterRole === agent.role ? 'ALL' : agent.role)}
                  className={`p-3.5 rounded-xl border transition-all cursor-pointer ${
                    filterRole === agent.role
                      ? 'bg-[#1E293B] border-cyan-400 shadow-[0_0_15px_rgba(0,210,255,0.25)]'
                      : 'bg-[#131D35]/70 border-[#1E293B] hover:border-[#334155] hover:bg-[#1E293B]/40'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold text-[#F8FAFC]">{agent.name}</span>
                    <StatusIndicator
                      status={getAgentStatusType(agent.state)}
                      showPulse={agent.state !== 'IDLE'}
                      size="sm"
                    />
                  </div>

                  <p className="mt-2 text-[11px] text-[#94A3B8] line-clamp-1">
                    🎯 {agent.currentGoal}
                  </p>

                  <div className="mt-3 pt-2 border-t border-[#1E293B]/80 flex items-center justify-between text-[10px] font-mono text-[#64748B]">
                    <span>{(agent.confidence * 100).toFixed(0)}% conf</span>
                    <span>{agent.thinkingDurationMs}ms</span>
                    <span>Q: {agent.queueSize}</span>
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>
        </div>

        {/* RIGHT: Live Thought Stream & Message Passing Bus (5 cols) */}
        <div className="lg:col-span-5">
          <Card variant="default" className="border-[#1E293B] bg-[#0F172A]/80 backdrop-blur-md h-full flex flex-col">
            <CardHeader className="flex flex-row items-center justify-between pb-3">
              <div>
                <div className="flex items-center gap-2">
                  <span className="relative flex h-2 w-2">
                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75" />
                    <span className="relative inline-flex rounded-full h-2 w-2 bg-[#00D2FF]" />
                  </span>
                  <Badge variant="intelligence" size="sm">
                    LIVE AGENT THOUGHTS
                  </Badge>
                </div>
                <CardTitle className="mt-2 text-lg font-bold text-[#F8FAFC]">
                  Cognition Thought Stream
                </CardTitle>
              </div>

              {filterRole !== 'ALL' && (
                <button
                  onClick={() => setFilterRole('ALL')}
                  className="text-[11px] text-[#00D2FF] hover:underline font-mono"
                >
                  Clear ({filterRole})
                </button>
              )}
            </CardHeader>

            <CardContent className="p-4 flex-1 overflow-y-auto max-h-[560px] space-y-3">
              {filteredThoughts.map((msg) => (
                <div
                  key={msg.id}
                  className="p-3 rounded-xl bg-[#131D35]/90 border border-[#1E293B] hover:border-cyan-500/40 transition-colors"
                >
                  <div className="flex items-center justify-between text-[11px]">
                    <div className="flex items-center gap-2">
                      <span className="font-bold text-[#00D2FF]">{msg.agentName}</span>
                      <span className="text-[10px] font-mono bg-[#0A0F1D] text-[#94A3B8] px-1.5 py-0.5 rounded border border-[#1E293B]">
                        {msg.thoughtType}
                      </span>
                    </div>
                    <span className="text-[10px] font-mono text-[#64748B]">{msg.timestampUtc}</span>
                  </div>

                  <p className="mt-1.5 text-xs text-[#F8FAFC] leading-relaxed font-mono">
                    "{msg.content}"
                  </p>

                  {msg.confidence !== undefined && (
                    <div className="mt-2 flex items-center justify-end text-[10px] font-mono text-[#10B981]">
                      <span>Confidence: {(msg.confidence * 100).toFixed(1)}%</span>
                    </div>
                  )}
                </div>
              ))}
            </CardContent>
          </Card>
        </div>
      </div>
    </section>
  );
};
