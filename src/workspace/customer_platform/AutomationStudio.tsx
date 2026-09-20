import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';

export const AutomationStudio: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'ACTIVE' | 'DRAFT' | 'MARKETPLACE'>('ACTIVE');

  const pipelines = [
    {
      id: 'PIPE-01',
      name: 'AP Autonomous Invoice Ingestion & ERP Posting',
      industry: 'Finance',
      status: 'LIVE',
      processedToday: 1420,
      accuracy: '99.4%',
      avgSpeed: '4.5s',
      guardrails: 'Confidence > 95%',
    },
    {
      id: 'PIPE-02',
      name: 'Technical Candidate Screening & Vector Ranking',
      industry: 'Human Resources',
      status: 'LIVE',
      processedToday: 240,
      accuracy: '96.5%',
      avgSpeed: '3.2s',
      guardrails: 'Strict Anonymization',
    },
    {
      id: 'PIPE-03',
      name: 'Commercial Contract Clause Risk Review',
      industry: 'Legal',
      status: 'PAUSED',
      processedToday: 45,
      accuracy: '98.5%',
      avgSpeed: '12.0s',
      guardrails: 'Legal Counsel Signoff',
    },
  ];

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-6 rounded-2xl bg-gradient-to-r from-[#0F172A] to-[#1E293B] border border-[#334155]/60 shadow-xl">
        <div>
          <Badge variant="intelligence" size="sm">ENTERPRISE AUTOMATION STUDIO</Badge>
          <h1 className="text-2xl font-black text-white mt-1">Autonomous AI Pipelines</h1>
          <p className="text-sm text-[#94A3B8]">
            Configure, deploy, and govern end-to-end multi-agent document intelligence workflows.
          </p>
        </div>
        <div className="flex gap-3">
          <Button variant="secondary" size="md">+ Import Template</Button>
          <Button variant="primary" size="md">+ Create Workflow</Button>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex gap-2 border-b border-[#1E293B] pb-3">
        {(['ACTIVE', 'DRAFT', 'MARKETPLACE'] as const).map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`px-4 py-2 rounded-xl text-xs font-bold transition-all ${
              activeTab === tab
                ? 'bg-[#0066FF] text-white shadow-lg shadow-[#0066FF]/25'
                : 'bg-[#0F172A] text-[#94A3B8] hover:text-white border border-[#1E293B]'
            }`}
          >
            {tab === 'ACTIVE' && 'Active Pipelines (3)'}
            {tab === 'DRAFT' && 'Drafts & Revisions (2)'}
            {tab === 'MARKETPLACE' && 'Template Library (5)'}
          </button>
        ))}
      </div>

      {/* Pipeline Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {pipelines.map((pipe) => (
          <div key={pipe.id} className="p-6 rounded-2xl bg-[#0F172A]/80 border border-[#1E293B] shadow-xl hover:border-[#00D2FF]/40 transition-all flex flex-col justify-between space-y-4">
            <div>
              <div className="flex items-center justify-between mb-2">
                <Badge variant="default" size="sm">{pipe.industry}</Badge>
                <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                  pipe.status === 'LIVE' ? 'bg-emerald-950 text-emerald-400 border border-emerald-800/40' : 'bg-gray-800 text-gray-400'
                }`}>
                  {pipe.status}
                </span>
              </div>
              <h3 className="text-base font-bold text-white mb-2">{pipe.name}</h3>
              <p className="text-xs text-[#94A3B8] font-mono">Guardrails: {pipe.guardrails}</p>
            </div>

            <div className="grid grid-cols-3 gap-2 py-3 border-y border-[#1E293B] text-center">
              <div>
                <span className="text-[10px] text-[#94A3B8] block">Today</span>
                <span className="text-xs font-bold text-white">{pipe.processedToday}</span>
              </div>
              <div>
                <span className="text-[10px] text-[#94A3B8] block">Accuracy</span>
                <span className="text-xs font-bold text-emerald-400">{pipe.accuracy}</span>
              </div>
              <div>
                <span className="text-[10px] text-[#94A3B8] block">Latency</span>
                <span className="text-xs font-bold text-cyan-400">{pipe.avgSpeed}</span>
              </div>
            </div>

            <div className="flex gap-2">
              <Button variant="secondary" size="sm" className="w-full">Edit DAG</Button>
              <Button variant="outline" size="sm" className="w-full">Analytics</Button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
