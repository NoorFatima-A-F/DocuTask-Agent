import React from 'react';
import { useWorkspace } from '../context/WorkspaceContext';
import { useRuntimeTelemetry } from '../../context/RuntimeTelemetryContext';
import { CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import type { RuntimeEvent } from '../../types/runtimeTelemetry';

export const LiveTimelinePanel: React.FC = () => {
  const { timelineEvents } = useWorkspace();
  const { events: runtimeEvents, isConnected, setSelectedEventForInspector } = useRuntimeTelemetry();

  const hasRealEvents = runtimeEvents.length > 0;

  const handleInspectRealEvent = (evt: RuntimeEvent) => {
    setSelectedEventForInspector(evt);
  };

  const handleInspectMockEvent = (evt: typeof timelineEvents[0]) => {
    // Synthesize a structured RuntimeEvent for inspector viewing
    const syntheticEvent: RuntimeEvent = {
      event_id: evt.id,
      mission_id: 'mission_doc_audit_9042',
      parent_event_id: null,
      timestamp: evt.timestampUtc,
      sequence_number: 1,
      agent_id: evt.agentRole,
      worker_id: evt.agentName,
      event_type: evt.eventTitle,
      payload: {
        description: evt.eventDescription,
        stage: evt.stageName,
        confidence: evt.confidenceScore,
        producedArtifact: evt.producedArtifact,
      },
      metadata: {
        source: 'SYNTHESIZED_TRACE_EVENT',
        isReplanned: evt.isReplanned || false,
        isCritiqueFlag: evt.isCritiqueFlag || false,
      },
      correlation_id: 'corr_' + evt.id,
      causation_id: null,
      trace_id: '4bf92f3577b34da6a3ce929d0e0e4736',
      span_id: '00f067aa0ba902b7',
      duration_ms: 142.5,
      status: 'COMPLETED',
      version: '1.0.0',
    };
    setSelectedEventForInspector(syntheticEvent);
  };

  return (
    <div className="w-full flex flex-col h-[700px] rounded-2xl bg-[#0F172A]/90 border border-[#1E293B] shadow-2xl overflow-hidden">
      <CardHeader className="flex flex-row items-center justify-between py-4 px-6 border-b border-[#1E293B] bg-[#131D35]/50">
        <div>
          <div className="flex items-center gap-2">
            <Badge variant="intelligence" size="sm" hasDot={isConnected} isPulsing={isConnected}>
              {isConnected ? 'LIVE EXECUTION STREAM' : 'CHRONOLOGICAL TRACE'}
            </Badge>
            <span className="text-xs text-[#94A3B8] font-mono">
              {hasRealEvents ? runtimeEvents.length : timelineEvents.length} Execution Checkpoints
            </span>
          </div>
          <CardTitle className="mt-1 text-base font-bold text-[#F8FAFC]">
            Live Mission Execution Timeline
          </CardTitle>
        </div>

        <div className="flex items-center gap-2 text-xs font-mono text-[#38BDF8] bg-[#0A0F1D] px-3 py-1.5 rounded-lg border border-cyan-500/30">
          <span>{isConnected ? 'SSE: Connected' : 'Telemetry: Ready'}</span>
        </div>
      </CardHeader>

      <CardContent className="flex-1 overflow-y-auto p-6 space-y-6">
        <div className="relative border-l-2 border-[#1E293B] ml-4 pl-6 space-y-6">
          {hasRealEvents
            ? runtimeEvents.map((evt, idx) => {
                const timeStr = new Date(evt.timestamp).toLocaleTimeString();
                return (
                  <div key={evt.event_id} className="relative group cursor-pointer" onClick={() => handleInspectRealEvent(evt)}>
                    {/* Timeline Dot */}
                    <div
                      className={`absolute -left-[31px] top-1 h-3.5 w-3.5 rounded-full ring-4 ring-[#0F172A] ${
                        idx === 0
                          ? 'bg-[#00D2FF] animate-pulse shadow-[0_0_10px_rgba(0,210,255,0.7)]'
                          : evt.status === 'FAILED'
                          ? 'bg-[#EF4444]'
                          : 'bg-[#10B981]'
                      }`}
                    />

                    <div className="p-4 rounded-xl bg-[#131D35] border border-[#1E293B] group-hover:border-cyan-500/50 group-hover:bg-[#16223f] transition-all space-y-2">
                      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                        <div className="flex items-center gap-2">
                          <span className="text-xs font-mono font-bold text-[#00D2FF]">
                            [{timeStr}]
                          </span>
                          <Badge variant="intelligence" size="sm">
                            {evt.agent_id || evt.worker_id || 'ENGINE'}
                          </Badge>
                          <Badge variant="default" size="sm" className="font-mono text-[10px]">
                            #{evt.sequence_number}
                          </Badge>
                        </div>

                        {evt.duration_ms != null && (
                          <span className="text-xs font-mono text-[#10B981]">
                            {evt.duration_ms.toFixed(1)} ms
                          </span>
                        )}
                      </div>

                      <h4 className="text-sm font-semibold text-[#F8FAFC] flex items-center justify-between">
                        <span>{evt.event_type}</span>
                        <span className="text-[11px] font-mono text-cyan-400 opacity-0 group-hover:opacity-100 transition-opacity">
                          Inspect Trace ↗
                        </span>
                      </h4>

                      <p className="text-xs text-[#94A3B8] leading-relaxed">
                        {evt.payload?.thought_text ||
                          evt.payload?.action_title ||
                          evt.payload?.task_title ||
                          evt.payload?.summary ||
                          JSON.stringify(evt.payload).substring(0, 120)}
                      </p>

                      <div className="pt-2 border-t border-[#1E293B]/60 text-[10px] font-mono text-slate-400 flex items-center justify-between">
                        <span>Trace: {evt.trace_id.substring(0, 8)}...</span>
                        <span className="text-emerald-400 font-semibold">{evt.status}</span>
                      </div>
                    </div>
                  </div>
                );
              })
            : timelineEvents.map((evt, idx) => (
                <div key={evt.id} className="relative group cursor-pointer" onClick={() => handleInspectMockEvent(evt)}>
                  {/* Timeline Dot */}
                  <div
                    className={`absolute -left-[31px] top-1 h-3.5 w-3.5 rounded-full ring-4 ring-[#0F172A] ${
                      idx === 0
                        ? 'bg-[#00D2FF] animate-pulse shadow-[0_0_10px_rgba(0,210,255,0.7)]'
                        : 'bg-[#10B981]'
                    }`}
                  />

                  <div className="p-4 rounded-xl bg-[#131D35] border border-[#1E293B] group-hover:border-cyan-500/50 group-hover:bg-[#16223f] transition-all space-y-2">
                    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                      <div className="flex items-center gap-2">
                        <span className="text-xs font-mono font-bold text-[#00D2FF]">
                          [{evt.timeDisplay}]
                        </span>
                        <Badge variant="intelligence" size="sm">
                          {evt.agentRole}
                        </Badge>
                        <Badge variant="default" size="sm" className="font-mono text-[10px]">
                          {evt.stageName}
                        </Badge>
                      </div>

                      {evt.confidenceScore !== undefined && (
                        <span className="text-xs font-mono text-[#10B981]">
                          conf: {(evt.confidenceScore * 100).toFixed(1)}%
                        </span>
                      )}
                    </div>

                    <h4 className="text-sm font-semibold text-[#F8FAFC] flex items-center justify-between">
                      <span>{evt.eventTitle}</span>
                      <span className="text-[11px] font-mono text-cyan-400 opacity-0 group-hover:opacity-100 transition-opacity">
                        Inspect Trace ↗
                      </span>
                    </h4>

                    <p className="text-xs text-[#94A3B8] leading-relaxed">
                      {evt.eventDescription}
                    </p>

                    {evt.producedArtifact && (
                      <div className="pt-2 border-t border-[#1E293B]/60 text-[11px] font-mono text-[#A855F7] flex items-center gap-1.5">
                        <span>📄 Artifact:</span>
                        <span className="underline">{evt.producedArtifact}</span>
                      </div>
                    )}
                  </div>
                </div>
              ))}
        </div>
      </CardContent>
    </div>
  );
};
