import React from 'react';
import { useWorkspace } from '../context/WorkspaceContext';
import { CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { CommandInput } from './CommandInput';

export const ConversationPanel: React.FC = () => {
  const { chatMessages, sendUserCommand, isDemoRunning } = useWorkspace();

  return (
    <div className="w-full flex flex-col h-[700px] rounded-2xl bg-[#0F172A]/90 border border-[#1E293B] shadow-2xl overflow-hidden">
      {/* Header */}
      <CardHeader className="flex flex-row items-center justify-between py-4 px-6 border-b border-[#1E293B] bg-[#131D35]/50">
        <div>
          <div className="flex items-center gap-2">
            <Badge variant="intelligence" size="sm" hasDot isPulsing>
              AI COWORKER ACTIVE
            </Badge>
            <span className="text-xs text-[#94A3B8] font-mono">
              Natural Language Intent Engine
            </span>
          </div>
          <CardTitle className="mt-1 text-base font-bold text-[#F8FAFC]">
            Interactive Collaboration Stream
          </CardTitle>
        </div>

        <div className="flex items-center gap-2 text-xs font-mono text-[#38BDF8] bg-[#0A0F1D] px-3 py-1.5 rounded-lg border border-cyan-500/30">
          <span>Zero-Fabrication Guard: ON</span>
        </div>
      </CardHeader>

      {/* Message Stream */}
      <CardContent className="flex-1 overflow-y-auto p-6 space-y-4">
        {chatMessages.map((msg) => {
          const isUser = msg.sender === 'HUMAN';

          return (
            <div
              key={msg.id}
              className={`flex flex-col ${isUser ? 'items-end' : 'items-start'}`}
            >
              <div className="flex items-center gap-2 mb-1 text-[11px] font-mono">
                {isUser ? (
                  <span className="text-[#94A3B8]">You (Operator) • {msg.timestampUtc}</span>
                ) : (
                  <div className="flex items-center gap-1.5">
                    <span className="font-bold text-[#00D2FF]">DocuTask Agent</span>
                    {msg.agentRole && (
                      <Badge variant="intelligence" size="sm">
                        {msg.agentRole}
                      </Badge>
                    )}
                    <span className="text-[#64748B]">• {msg.timestampUtc}</span>
                  </div>
                )}
              </div>

              <div
                className={`max-w-2xl p-4 rounded-2xl text-xs sm:text-sm leading-relaxed ${
                  isUser
                    ? 'bg-[#0066FF] text-white rounded-tr-none shadow-[0_0_15px_rgba(0,102,255,0.3)]'
                    : 'bg-[#131D35] border border-[#334155] text-[#F8FAFC] rounded-tl-none shadow-lg'
                }`}
              >
                <p className="whitespace-pre-wrap">{msg.text}</p>

                {/* AI Proposed Plan Adaptation */}
                {msg.proposedPlanUpdate && msg.proposedPlanUpdate.length > 0 && (
                  <div className="mt-3 p-3 rounded-xl bg-[#0A0F1D]/80 border border-cyan-500/30 space-y-1.5 font-mono text-xs">
                    <span className="text-[10px] font-bold text-[#00D2FF] uppercase tracking-wider block">
                      Proposed DAG Adaptation:
                    </span>
                    {msg.proposedPlanUpdate.map((step, i) => (
                      <div key={i} className="flex items-start gap-2 text-[#94A3B8]">
                        <span className="text-[#10B981]">➔</span>
                        <span>{step}</span>
                      </div>
                    ))}
                  </div>
                )}

                {/* Action Taken Badge */}
                {msg.actionTaken && (
                  <div className="mt-2 pt-2 border-t border-[#1E293B] flex items-center justify-between text-[11px] font-mono">
                    <span className="text-[#10B981]">⚡ {msg.actionTaken}</span>
                    {msg.confidenceScore && (
                      <span className="text-[#00D2FF]">
                        Confidence: {(msg.confidenceScore * 100).toFixed(1)}%
                      </span>
                    )}
                  </div>
                )}
              </div>

              {/* Suggested Quick Actions */}
              {msg.suggestedQuickActions && msg.suggestedQuickActions.length > 0 && (
                <div className="flex flex-wrap gap-2 mt-2">
                  {msg.suggestedQuickActions.map((qa) => (
                    <Button
                      key={qa}
                      variant="ghost"
                      size="sm"
                      onClick={() => sendUserCommand(qa)}
                      className="text-[11px] bg-[#131D35] border border-[#1E293B] hover:border-cyan-400 hover:text-[#00D2FF]"
                    >
                      💬 {qa}
                    </Button>
                  ))}
                </div>
              )}
            </div>
          );
        })}
      </CardContent>

      {/* Bottom Command Input */}
      <div className="p-4 border-t border-[#1E293B] bg-[#131D35]/70">
        <CommandInput onSendCommand={sendUserCommand} disabled={isDemoRunning} />
      </div>
    </div>
  );
};
