import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Target, CheckCircle2 } from 'lucide-react';

export const GoalAnalysisView: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'OBJECTIVES' | 'CONSTRAINTS' | 'RESOURCES'>('OBJECTIVES');

  const goalData = {
    goalId: 'goal-m01-fin-audit',
    title: 'Process and validate 2026 Q3 vendor audit invoices with arithmetic invariant checks',
    priority: 'HIGH',
    deadline: '30.0s SLA',
    estimatedCostUsd: 0.0032,
    confidence: 0.985,
    objectives: [
      { id: 'obj-1', name: 'Rasterize & Segment Invoices', worker: 'OCR Workers', latency: '320ms', status: 'COMPLETED' },
      { id: 'obj-2', name: 'Extract Structured Vendor Line Items', worker: 'Extract Worker', latency: '250ms', status: 'RUNNING' },
      { id: 'obj-3', name: 'Verify Mathematical Arithmetic Invariant', worker: 'Scientific Validator', latency: '180ms', status: 'PENDING' },
      { id: 'obj-4', name: 'Commit Merkle Proof to Truth Ledger', worker: 'Truth Authenticator', latency: '110ms', status: 'PENDING' },
    ],
    constraints: [
      'Total mission latency must remain strictly below 30.0 seconds.',
      'Arithmetic invariant: sum(item_subtotals) + tax == total_amount_due.',
      'Zero hallucinations: Confidence score >= 0.95 across invoice tax IDs.',
      'Immutable cryptographic hash chain must link raw document to final extracted JSON.',
    ],
    resources: [
      { name: 'Google Cloud Document AI (Primary)', type: 'CLOUD_OCR', quota: '50 req/min' },
      { name: 'Tesseract OCR Fallback (Edge Engine)', type: 'LOCAL_FALLBACK', quota: 'Unlimited' },
      { name: 'Deterministic Schema Regex Engine', type: 'SCHEMA_NORMALIZER', quota: 'In-Memory' },
      { name: 'Hardware Merkle Hash Ring', type: 'LEDGER_SIGNER', quota: '1000 ops/sec' },
    ],
  };

  return (
    <div className="p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6">
        <div className="space-y-1">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-gradient-to-br from-cyan-500/20 to-blue-500/20 border border-cyan-500/30 rounded-xl text-cyan-400">
              <Target className="w-5 h-5" />
            </div>
            <div>
              <h1 className="text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2">
                Autonomous Goal Analysis & Constraint Extractor
                <Badge variant="success" size="sm">Decomposed</Badge>
              </h1>
              <p className="text-xs text-[#94A3B8] font-mono">
                Inspect structured objectives, deterministic constraints, and discovered capabilities
              </p>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <Badge variant="intelligence" size="md">Confidence 98.5%</Badge>
          <Badge variant="outline" size="md">SLA: 30.0s</Badge>
        </div>
      </div>

      {/* Goal Summary Card */}
      <Card className="p-5 rounded-2xl border border-[#1E293B] bg-[#0F172A] space-y-3 font-mono">
        <div className="flex items-center justify-between">
          <span className="text-xs text-[#64748B]">MISSION GOAL IDENTIFIER: {goalData.goalId}</span>
          <Badge variant="info" size="sm">Priority: {goalData.priority}</Badge>
        </div>
        <p className="text-sm font-semibold text-white">{goalData.title}</p>
        <div className="flex flex-wrap gap-4 text-xs text-[#94A3B8] pt-2 border-t border-[#1E293B]">
          <span>Estimated Cost: <strong className="text-emerald-400">${goalData.estimatedCostUsd}</strong></span>
          <span>Target SLA: <strong className="text-cyan-400">{goalData.deadline}</strong></span>
          <span>Decomposed Sub-Tasks: <strong className="text-purple-400">{goalData.objectives.length}</strong></span>
        </div>
      </Card>

      {/* Tabs */}
      <div className="flex gap-2 border-b border-[#1E293B] pb-2 font-mono text-xs">
        {(['OBJECTIVES', 'CONSTRAINTS', 'RESOURCES'] as const).map(tab => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`px-4 py-2 rounded-xl transition-all font-semibold ${
              activeTab === tab ? 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/30' : 'text-[#94A3B8] hover:bg-[#131D35]'
            }`}
          >
            {tab}
          </button>
        ))}
      </div>

      {/* Tab Panels */}
      {activeTab === 'OBJECTIVES' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {goalData.objectives.map((obj, i) => (
            <Card key={obj.id} className="p-4 rounded-xl border border-[#1E293B] bg-[#0F172A] space-y-2 font-mono">
              <div className="flex items-center justify-between">
                <span className="text-[10px] text-[#64748B]">OBJECTIVE #{i + 1}</span>
                <Badge variant={obj.status === 'COMPLETED' ? 'success' : obj.status === 'RUNNING' ? 'intelligence' : 'outline'} size="sm">
                  {obj.status}
                </Badge>
              </div>
              <h3 className="text-xs font-bold text-white">{obj.name}</h3>
              <div className="flex items-center justify-between text-[11px] text-[#94A3B8] pt-2 border-t border-[#1E293B]">
                <span>Target: {obj.worker}</span>
                <span>Latency Est: {obj.latency}</span>
              </div>
            </Card>
          ))}
        </div>
      )}

      {activeTab === 'CONSTRAINTS' && (
        <div className="space-y-3 font-mono">
          {goalData.constraints.map((c, i) => (
            <Card key={i} className="p-4 rounded-xl border border-[#1E293B] bg-[#0F172A] flex items-center gap-3">
              <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0" />
              <div className="text-xs text-[#F8FAFC]">{c}</div>
            </Card>
          ))}
        </div>
      )}

      {activeTab === 'RESOURCES' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 font-mono">
          {goalData.resources.map((r, i) => (
            <Card key={i} className="p-4 rounded-xl border border-[#1E293B] bg-[#0F172A] space-y-2">
              <div className="flex items-center justify-between">
                <Badge variant="info" size="sm">{r.type}</Badge>
                <span className="text-[10px] text-[#64748B]">Quota: {r.quota}</span>
              </div>
              <h3 className="text-xs font-bold text-white">{r.name}</h3>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};
