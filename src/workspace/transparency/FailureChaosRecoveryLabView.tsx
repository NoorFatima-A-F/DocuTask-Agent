import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const FailureChaosRecoveryLabView: React.FC = () => {
  const [injectedHistory, setInjectedHistory] = useState([
    {
      faultId: 'fault_ocr_crash',
      target: 'OCR_INGEST',
      type: 'PROCESS_CRASH',
      actionTaken: 'ALTERNATE_OCR_FALLBACK',
      replannedNodes: ['task_ocr_tesseract_fallback', 'task_dewarp_repair'],
      recoveryMs: 38.2,
      status: 'AUTONOMOUSLY_RECOVERED',
      timestamp: '5 mins ago',
    },
    {
      faultId: 'fault_gemini_429',
      target: 'LLM_EXTRACT',
      type: 'HTTP_429_RATE_LIMIT',
      actionTaken: 'EXPONENTIAL_BACKOFF_RETRY',
      replannedNodes: ['task_llm_backoff_jitter', 'task_flash_lite_route'],
      recoveryMs: 42.5,
      status: 'AUTONOMOUSLY_RECOVERED',
      timestamp: '12 mins ago',
    },
  ]);

  const handleInjectFault = (faultType: string) => {
    const newEvent = {
      faultId: `fault_${Date.now()}`,
      target: 'LLM_EXTRACT',
      type: faultType,
      actionTaken: 'DYNAMIC_REPLAN_FALLBACK',
      replannedNodes: ['task_speculative_fallback', 'task_schema_patch'],
      recoveryMs: 35.0,
      status: 'AUTONOMOUSLY_RECOVERED',
      timestamp: 'Just now',
    };
    setInjectedHistory([newEvent, ...injectedHistory]);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="p-6 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-xl">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xl">⚡</span>
              <h2 className="text-lg font-bold font-mono text-[#F8FAFC]">
                Failure Recovery & Chaos Fault Injection Lab
              </h2>
              <Badge variant="success" size="sm">
                SELF-HEALING ACTIVE
              </Badge>
            </div>
            <p className="text-sm font-mono text-[#94A3B8] mt-1">
              Test autonomous resilience by injecting simulated worker crashes, API rate-limits, and schema drift.
            </p>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={() => handleInjectFault('PROCESS_CRASH')}
              className="px-3 py-1.5 rounded-lg text-xs font-mono font-bold bg-rose-600/20 border border-rose-500 text-rose-300 hover:bg-rose-600 hover:text-white transition-all"
            >
              💥 Inject OCR Crash
            </button>
            <button
              onClick={() => handleInjectFault('HTTP_429_RATE_LIMIT')}
              className="px-3 py-1.5 rounded-lg text-xs font-mono font-bold bg-amber-600/20 border border-amber-500 text-amber-300 hover:bg-amber-600 hover:text-white transition-all"
            >
              ⚠️ Inject HTTP 429 Quota
            </button>
          </div>
        </div>
      </div>

      {/* Recovery History */}
      <Card className="p-6 bg-[#0F172A] border-[#1E293B]">
        <h3 className="text-sm font-bold font-mono text-[#F8FAFC] mb-4">
          Autonomous Replanning & Fault Mitigation Stream
        </h3>
        <div className="space-y-3">
          {injectedHistory.map((item, idx) => (
            <div key={idx} className="p-4 rounded-xl bg-[#020617] border border-[#1E293B]">
              <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-2">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-mono text-rose-400 font-bold">{item.type}</span>
                    <span className="text-xs font-mono text-[#94A3B8]">on {item.target}</span>
                  </div>
                  <div className="text-xs font-mono text-[#F8FAFC] mt-1">
                    Mitigation: <span className="text-cyan-400 font-bold">{item.actionTaken}</span>
                  </div>
                  <div className="text-[11px] font-mono text-[#64748B] mt-0.5">
                    Synthesized Subgraph: {item.replannedNodes.join(' → ')} • Recovery Time: {item.recoveryMs} ms
                  </div>
                </div>
                <Badge variant="success" size="sm">
                  {item.status}
                </Badge>
              </div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
};
