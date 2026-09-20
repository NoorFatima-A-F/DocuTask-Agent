import React, { useState } from 'react';
import { useWorkspace } from '../context/WorkspaceContext';
import { CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';

export const AgentInboxPanel: React.FC = () => {
  const { agentInbox, selectedAgentRole, selectAgentInbox, sendAgentDirectMessage } = useWorkspace();
  const [dmText, setDmText] = useState('');

  const activeAgent =
    agentInbox.find((a) => a.agentRole === selectedAgentRole) || agentInbox[0];

  const handleSendDm = (e: React.FormEvent) => {
    e.preventDefault();
    if (!dmText.trim() || !activeAgent) return;
    sendAgentDirectMessage(activeAgent.agentRole, dmText.trim());
    setDmText('');
  };

  return (
    <div className="w-full flex flex-col lg:flex-row h-[700px] rounded-2xl bg-[#0F172A]/90 border border-[#1E293B] shadow-2xl overflow-hidden">
      {/* Left Column: Agent Channels List (5 cols) */}
      <div className="lg:w-80 border-r border-[#1E293B] bg-[#0A0F1D]/80 flex flex-col">
        <div className="p-4 border-b border-[#1E293B]">
          <span className="text-[11px] font-bold text-[#64748B] uppercase tracking-wider block font-mono">
            Agent Inbox Channels ({agentInbox.length})
          </span>
        </div>

        <div className="flex-1 overflow-y-auto p-2 space-y-1">
          {agentInbox.map((agent) => {
            const isSelected = selectedAgentRole === agent.agentRole;

            return (
              <button
                key={agent.agentRole}
                onClick={() => selectAgentInbox(agent.agentRole)}
                className={`w-full p-3 rounded-xl text-left transition-all flex items-center justify-between ${
                  isSelected
                    ? 'bg-[#1E293B] border border-cyan-400/50 shadow-md text-[#F8FAFC]'
                    : 'hover:bg-[#131D35]/60 text-[#94A3B8]'
                }`}
              >
                <div className="flex items-center gap-2.5 min-w-0">
                  <div
                    className={`h-2.5 w-2.5 rounded-full shrink-0 ${
                      agent.status === 'EXECUTING'
                        ? 'bg-[#00D2FF] animate-pulse'
                        : agent.status === 'THINKING'
                        ? 'bg-amber-400'
                        : 'bg-[#10B981]'
                    }`}
                  />
                  <div className="truncate">
                    <span className="text-xs font-bold block truncate text-[#F8FAFC]">
                      {agent.agentName}
                    </span>
                    <span className="text-[10px] text-[#64748B] font-mono block truncate">
                      {agent.currentTask}
                    </span>
                  </div>
                </div>

                <span className="text-[10px] font-mono text-[#00D2FF] shrink-0 ml-2">
                  {(agent.confidence * 100).toFixed(0)}%
                </span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Right Column: Selected Agent Telemetry & Direct Messaging (7 cols) */}
      <div className="flex-1 flex flex-col bg-[#0F172A]">
        {activeAgent ? (
          <>
            <CardHeader className="flex flex-row items-center justify-between py-4 px-6 border-b border-[#1E293B] bg-[#131D35]/50">
              <div>
                <div className="flex items-center gap-2">
                  <Badge variant="intelligence" size="sm">
                    {activeAgent.agentRole}
                  </Badge>
                  <span className="text-xs text-[#10B981] font-mono">● {activeAgent.status}</span>
                </div>
                <CardTitle className="mt-1 text-base font-bold text-[#F8FAFC]">
                  {activeAgent.agentName}
                </CardTitle>
              </div>

              <div className="flex items-center gap-4 text-xs font-mono text-[#94A3B8]">
                <span>Artifacts: {activeAgent.producedCount}</span>
                <span>ETA: {activeAgent.etaSeconds}s</span>
              </div>
            </CardHeader>

            {/* Agent Live Status Overview */}
            <div className="p-4 bg-[#131D35]/30 border-b border-[#1E293B] grid grid-cols-2 gap-4 text-xs">
              <div>
                <span className="text-[10px] font-mono text-[#64748B] uppercase block">
                  Active Task:
                </span>
                <span className="text-[#F8FAFC] font-medium block mt-0.5">
                  {activeAgent.currentTask}
                </span>
              </div>
              <div>
                <span className="text-[10px] font-mono text-[#64748B] uppercase block">
                  Working On:
                </span>
                <span className="text-[#38BDF8] block mt-0.5">{activeAgent.workingOn}</span>
              </div>
            </div>

            {/* Direct Message Thread */}
            <CardContent className="flex-1 overflow-y-auto p-6 space-y-3">
              <span className="text-[11px] font-bold font-mono text-[#64748B] uppercase block mb-2">
                Inter-Agent & Operator Communication Thread
              </span>

              {activeAgent.recentMessages.map((msg) => (
                <div
                  key={msg.id}
                  className="p-3.5 rounded-xl bg-[#131D35] border border-[#1E293B] space-y-1 text-xs"
                >
                  <div className="flex items-center justify-between text-[11px] font-mono">
                    <span className="text-[#00D2FF] font-bold">From: {msg.fromRole}</span>
                    <span className="text-[#64748B]">{msg.timestampUtc}</span>
                  </div>
                  <p className="text-[#F8FAFC] font-mono">{msg.body}</p>
                </div>
              ))}
            </CardContent>

            {/* Direct Message Input */}
            <form
              onSubmit={handleSendDm}
              className="p-4 border-t border-[#1E293B] bg-[#131D35]/50 flex items-center gap-3"
            >
              <input
                type="text"
                value={dmText}
                onChange={(e) => setDmText(e.target.value)}
                placeholder={`Send instructions directly to ${activeAgent.agentName}...`}
                className="flex-1 bg-[#0A0F1D] border border-[#334155] rounded-xl px-4 py-2 text-xs font-mono text-[#F8FAFC] focus:outline-none focus:border-cyan-400"
              />
              <Button type="submit" variant="intelligence" size="sm" disabled={!dmText.trim()}>
                Send Message ➔
              </Button>
            </form>
          </>
        ) : (
          <div className="p-8 text-center text-xs text-[#64748B]">Select an agent from the inbox</div>
        )}
      </div>
    </div>
  );
};
