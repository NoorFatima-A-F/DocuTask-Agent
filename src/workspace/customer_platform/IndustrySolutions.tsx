import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';

export const IndustrySolutions: React.FC = () => {
  const [selectedIndustry, setSelectedIndustry] = useState<'FINANCE' | 'HR' | 'LEGAL' | 'HEALTHCARE'>('FINANCE');

  const content = {
    FINANCE: {
      title: 'Autonomous Accounts Payable & Invoice Intelligence',
      problem: 'Enterprise finance departments spend $2.4M+ annually on manual data entry, suffering from 3-week payment backlogs and vendor duplicate errors.',
      solution: 'DocuTask Agent provides zero-config mailbox ingestion, multimodal layout parsing, automated 3-way PO matching, and instant ERP sync.',
      impact: ['$2.28M Net Annual Savings', '92.8% Unit Cost Reduction ($0.025/doc)', '4.5s End-to-End Processing Duration', '91.5% Straight-Through Processing (STP)'],
    },
    HR: {
      title: 'AI Resume Screening & Competency Vector Matcher',
      problem: 'Recruiting teams spend hundreds of hours manually screening thousands of unstructured resumes, leading to candidate drop-off and subjective bias.',
      solution: 'Ingests PDF/DOCX resumes, ranks candidates by technical competency match, anonymizes PII, and triggers calendar bookings.',
      impact: ['99.3% Faster Time-to-Shortlist', '96.5% Semantic Competency Match Precision', '100% Bias-Free Blind Evaluation', '4,800 Recruiter Hours Saved Annually'],
    },
    LEGAL: {
      title: 'Commercial Contract Clause Risk & M&A Intelligence',
      problem: 'Legal review of complex Master Services Agreements takes 4+ business days, stalling sales cycles and risking hidden liability exposure.',
      solution: 'Extracts non-standard indemnification clauses, liability caps, and compliance obligations with instant redline generation.',
      impact: ['99.0% Reduction in Review Cycle (45s)', '98.5% Non-Standard Clause Risk Detection', 'Full Legal Citation Provenance', '100% Attorney-Client Isolation'],
    },
    HEALTHCARE: {
      title: 'Clinical Prior Authorization & Claims Triage',
      problem: 'Clinical chart notes take 72+ hours to verify against ICD-10/CPT guidelines, causing critical patient care delays and high administrative appeal costs.',
      solution: 'Evaluates clinical notes against medical necessity criteria with HIPAA-compliant cryptographic partitioning and EHR gateway integration.',
      impact: ['Turnaround Reduced from 72h to 12s', '97.8% Clinical Guideline Compliance', '28,400 Staff Hours Liberated', 'Zero ePHI Data Retention on LLM'],
    },
  };

  const current = content[selectedIndustry];

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-6 rounded-2xl bg-gradient-to-r from-[#0F172A] to-[#1E293B] border border-[#334155]/60 shadow-xl">
        <div>
          <Badge variant="intelligence" size="sm">INDUSTRY VALUE SHOWCASE</Badge>
          <h1 className="text-2xl font-black text-white mt-1">Enterprise Automation Solutions</h1>
          <p className="text-sm text-[#94A3B8]">
            Explore how DocuTask solves specific business challenges across major industry verticals.
          </p>
        </div>
        <div className="flex gap-2">
          {(['FINANCE', 'HR', 'LEGAL', 'HEALTHCARE'] as const).map((ind) => (
            <button
              key={ind}
              onClick={() => setSelectedIndustry(ind)}
              className={`px-3.5 py-2 rounded-xl text-xs font-bold transition-all ${
                selectedIndustry === ind
                  ? 'bg-[#0066FF] text-white shadow-lg shadow-[#0066FF]/25'
                  : 'bg-[#0A0F1D] text-[#94A3B8] hover:text-white border border-[#1E293B]'
              }`}
            >
              {ind}
            </button>
          ))}
        </div>
      </div>

      <div className="p-8 rounded-2xl bg-[#0F172A]/80 border border-[#1E293B] shadow-2xl space-y-6">
        <h2 className="text-xl font-bold text-white">{current.title}</h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="p-5 rounded-xl bg-[#0A0F1D] border border-rose-900/30 space-y-2">
            <span className="text-xs font-bold text-rose-400 uppercase font-mono">The Business Problem</span>
            <p className="text-xs text-[#CBD5E1] leading-relaxed">{current.problem}</p>
          </div>

          <div className="p-5 rounded-xl bg-[#0A0F1D] border border-blue-900/30 space-y-2">
            <span className="text-xs font-bold text-cyan-400 uppercase font-mono">The Autonomous AI Solution</span>
            <p className="text-xs text-[#CBD5E1] leading-relaxed">{current.solution}</p>
          </div>
        </div>

        <div className="space-y-3">
          <span className="text-xs font-bold text-[#94A3B8] uppercase tracking-wider font-mono">
            Quantified Business Impact
          </span>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {current.impact.map((imp, idx) => (
              <div key={idx} className="p-4 rounded-xl bg-emerald-950/20 border border-emerald-500/30 flex items-center gap-3">
                <span className="text-emerald-400 text-lg">⚡</span>
                <span className="text-xs font-bold text-white">{imp}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
