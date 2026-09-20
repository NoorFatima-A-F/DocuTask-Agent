import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

interface IncidentItem {
  id: string;
  title: string;
  severity: string;
  status: string;
  commander: string;
  affected: string[];
  rootCause: string;
  mitigation: string;
  impact: string;
  timeline: { time: string; phase: string; action: string; actor: string }[];
  postmortem: { whys: string[]; actionItems: string[] };
}

const CANONICAL_INCIDENTS: IncidentItem[] = [
  {
    id: 'inc_2026_001',
    title: 'Transient Gemini 429 Quota Exhaustion During Batch Burst',
    severity: 'SEV2_HIGH',
    status: 'RESOLVED',
    commander: 'Chief Executive Agent',
    affected: ['Structured Extraction', 'Optical Perception'],
    rootCause: 'Upstream LLM burst exceeded 10,000 RPM concurrent token limit on single API key.',
    mitigation: 'Auto-switched extraction traffic to Gemini Flash Lite with exponential jitter backoff.',
    impact: '14 tasks delayed by 420ms; zero data loss; 100% invariant math verified.',
    timeline: [
      { time: '16:05:00Z', phase: 'DETECTED', action: 'HTTP 429 spike detected in Extraction Department.', actor: 'WorkerMonitor' },
      { time: '16:05:02Z', phase: 'TRIAGING', action: 'Incident Commander assigned; war room #incident-war-room opened.', actor: 'IncidentCommander' },
      { time: '16:05:05Z', phase: 'MITIGATING', action: 'Traffic routed to Flash Lite fallback pool; prompt compression applied.', actor: 'Lead Extraction Specialist' },
      { time: '16:05:12Z', phase: 'RESOLVED', action: 'Quota recovered; nominal queue latency restored.', actor: 'IncidentCommander' },
    ],
    postmortem: {
      whys: [
        'Why 1: Extraction tasks queued up -> upstream LLM returned HTTP 429.',
        'Why 2: Burst of 20 dense invoices arrived concurrently.',
        'Why 3: Single Gemini Pro API quota pool was shared without rate-smoothing.',
        'Why 4: Leaky-bucket token rate limiter threshold was set too loose.',
        'Why 5: Proactive prompt caching was not pre-warmed for this vendor template.',
      ],
      actionItems: [
        'Enable proactive token rate-smoothing on Extraction Department queue (COMPLETED)',
        'Pre-warm prompt caches on vendor batch ingestion (IN_PROGRESS)',
        'Add automatic Fallback-to-Flash-Lite circuit breaker rule (COMPLETED)',
      ],
    },
  },
];

export const IncidentCommandCenter: React.FC = () => {
  const [selectedIncidentId, setSelectedIncidentId] = useState('inc_2026_001');

  const inc: IncidentItem = CANONICAL_INCIDENTS.find((i) => i.id === selectedIncidentId) || CANONICAL_INCIDENTS[0]!;

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 p-5 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-xl">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-2xl">🚨</span>
            <h2 className="text-xl font-bold text-[#F8FAFC]">Enterprise Incident Command Center & War Room</h2>
            <Badge variant="error" size="sm">Automated Triage</Badge>
          </div>
          <p className="text-sm text-[#94A3B8] mt-1">
            Automated incident lifecycle: DETECTED → TRIAGING → MITIGATING → RESOLVED → POSTMORTEM with 5-Whys root cause analysis.
          </p>
        </div>

        <div className="flex items-center gap-2">
          {CANONICAL_INCIDENTS.map((i) => (
            <button
              key={i.id}
              onClick={() => setSelectedIncidentId(i.id)}
              className={`px-3 py-1.5 rounded-lg text-xs font-mono font-semibold transition-all ${
                selectedIncidentId === i.id ? 'bg-[#0066FF] text-white' : 'bg-[#1E293B] text-[#94A3B8] hover:text-white'
              }`}
            >
              {i.id}
            </button>
          ))}
        </div>
      </div>

      {/* Incident Detail Card */}
      <Card className="p-5 bg-[#0F172A] border-[#1E293B] space-y-5">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-[#1E293B] pb-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-base font-bold text-[#F8FAFC]">{inc.title}</span>
              <Badge variant="warning" size="sm">{inc.severity}</Badge>
              <Badge variant="success" size="sm">{inc.status}</Badge>
            </div>
            <div className="text-xs text-[#94A3B8] font-mono mt-1">
              Incident ID: {inc.id} | Commander: <span className="text-[#38BDF8] font-semibold">{inc.commander}</span>
            </div>
          </div>

          <div className="text-right text-xs font-mono">
            <span className="text-[#64748B] block">AFFECTED DEPARTMENTS</span>
            <span className="text-[#F8FAFC] font-semibold">{inc.affected.join(', ')}</span>
          </div>
        </div>

        {/* Impact & Mitigation */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="p-4 rounded-xl bg-[#020617] border border-[#1E293B] space-y-1">
            <div className="text-xs font-mono text-[#EF4444] font-bold">Root Cause Assessment</div>
            <p className="text-xs text-[#CBD5E1]">{inc.rootCause}</p>
          </div>

          <div className="p-4 rounded-xl bg-[#020617] border border-[#1E293B] space-y-1">
            <div className="text-xs font-mono text-[#10B981] font-bold">Mitigation Executed</div>
            <p className="text-xs text-[#CBD5E1]">{inc.mitigation}</p>
          </div>
        </div>

        {/* Triage Timeline */}
        <div className="space-y-3">
          <div className="text-xs font-mono text-[#94A3B8] uppercase">Automated Response Timeline</div>
          <div className="space-y-2">
            {inc.timeline.map((t, idx) => (
              <div key={idx} className="flex items-center justify-between p-3 rounded-lg bg-[#020617]/60 border border-[#1E293B]/60 text-xs font-mono">
                <div className="flex items-center gap-3">
                  <Badge variant={t.phase === 'RESOLVED' ? 'success' : (t.phase === 'MITIGATING' ? 'warning' : 'info')} size="sm">
                    {t.phase}
                  </Badge>
                  <span className="text-[#F8FAFC]">{t.action}</span>
                </div>
                <div className="text-[11px] text-[#64748B]">
                  Actor: <span className="text-[#38BDF8]">{t.actor}</span> | {t.time}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* 5-Whys Postmortem */}
        <div className="space-y-3 pt-2">
          <div className="text-xs font-mono text-[#94A3B8] uppercase">Blameless 5-Whys Postmortem & Action Items</div>
          <div className="p-4 rounded-xl bg-[#020617] border border-[#1E293B] space-y-3 text-xs font-mono">
            <div className="space-y-1 text-[#CBD5E1]">
              {inc.postmortem.whys.map((why, idx) => (
                <div key={idx} className="flex items-start gap-2">
                  <span className="text-[#00D2FF]">↳</span>
                  <span>{why}</span>
                </div>
              ))}
            </div>

            <div className="pt-2 border-t border-[#1E293B]/60 space-y-1">
              <div className="text-[11px] text-[#94A3B8] uppercase">Corrective Prevention Rules:</div>
              {inc.postmortem.actionItems.map((act, idx) => (
                <div key={idx} className="text-[#10B981] flex items-center gap-2">
                  <span>✓</span>
                  <span>{act}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </Card>
    </div>
  );
};
