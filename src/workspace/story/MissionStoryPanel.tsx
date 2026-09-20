import React from 'react';
import { CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { TrustIndicator } from '../../components/ui/TrustIndicator';

export const MissionStoryPanel: React.FC = () => {
  const storyChapters = [
    {
      chapterNumber: '01',
      title: 'The Challenge: Degraded Thermal Receipts',
      time: '09:15:00 UTC',
      narrative:
        'The operator requested processing for high-volume enterprise utility invoices. Thermal scan sensor noise and uneven background gradient posed severe risk of losing decimal amounts and tax identifiers under standard OCR pipelines.',
      trustState: 'EMPIRICAL' as const,
      highlightMetric: 'Initial Risk: 14.2% CER',
    },
    {
      chapterNumber: '02',
      title: 'Memory Recall: Extracting Past Lessons',
      time: '09:15:05 UTC',
      narrative:
        'Memory Agent audited historical runs across 18 previous invoice missions. It identified that global Otsu thresholding repeatedly destroyed bottom-left watermarks and recommended injecting an Adaptive Local Contrast Filter.',
      trustState: 'VERIFIED' as const,
      highlightMetric: 'Memory Retention: R=0.98',
    },
    {
      chapterNumber: '03',
      title: 'Autonomous Multi-Agent Consensus',
      time: '09:15:10 UTC',
      narrative:
        'Planner, Governance, Evidence, and Reviewer agents deliberated on computational cost vs accuracy. A consensus score of 97% was achieved, and the compiled 6-node DAG was dispatched to the execution runtime.',
      trustState: 'VERIFIED' as const,
      highlightMetric: 'Consensus: 97%',
    },
    {
      chapterNumber: '04',
      title: 'Execution: Closed-Loop Bayesian Optimization',
      time: '09:22:40 UTC',
      narrative:
        'Execution Agent ran 10 hyperparameter trials on GPU instances. The Gaussian Process surrogate model converged at optimal contrast parameter x*=0.6800, achieving macro F1=0.9796 across 53 holdout observations.',
      trustState: 'EMPIRICAL' as const,
      highlightMetric: 'Optimal x* = 0.6800',
    },
    {
      chapterNumber: '05',
      title: 'Statistical Certification & Mission Success',
      time: '09:22:45 UTC',
      narrative:
        'Statistics Agent verified sample power threshold (n=53 >= 48, Power=0.84, p=0.0012). Final confidence reached 97.2%, surpassing the 95.0% stopping threshold. Provenance was signed with SLSA Level 3+ digital certificates.',
      trustState: 'VERIFIED' as const,
      highlightMetric: 'Target Reached: 97.2%',
    },
  ];

  return (
    <div className="w-full flex flex-col h-[700px] rounded-2xl bg-[#0F172A]/90 border border-[#1E293B] shadow-2xl overflow-hidden">
      <CardHeader className="flex flex-row items-center justify-between py-4 px-6 border-b border-[#1E293B] bg-[#131D35]/50">
        <div>
          <div className="flex items-center gap-2">
            <Badge variant="intelligence" size="sm">
              DOCUMENTARY STORYTELLING
            </Badge>
            <span className="text-xs text-[#94A3B8] font-mono">
              Mission Narrative Mode
            </span>
          </div>
          <CardTitle className="mt-1 text-base font-bold text-[#F8FAFC]">
            The Journey of Autonomous Discovery
          </CardTitle>
        </div>

        <div className="text-xs font-mono text-[#10B981] bg-[#0A0F1D] px-3.5 py-1.5 rounded-lg border border-emerald-500/30">
          Status: Mission Goal Satisfied
        </div>
      </CardHeader>

      <CardContent className="flex-1 overflow-y-auto p-6 space-y-6">
        <div className="space-y-6">
          {storyChapters.map((ch) => (
            <div
              key={ch.chapterNumber}
              className="p-6 rounded-2xl bg-[#131D35] border border-[#1E293B] hover:border-cyan-500/40 transition-all space-y-3"
            >
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-[#1E293B] pb-3">
                <div className="flex items-center gap-3">
                  <span className="h-7 w-7 rounded-lg bg-gradient-to-tr from-[#0066FF] to-[#00D2FF] text-white flex items-center justify-center text-xs font-mono font-bold">
                    {ch.chapterNumber}
                  </span>
                  <h3 className="text-sm font-bold text-[#F8FAFC]">{ch.title}</h3>
                </div>

                <div className="flex items-center gap-3">
                  <TrustIndicator state={ch.trustState} />
                  <span className="text-xs font-mono text-[#64748B]">{ch.time}</span>
                </div>
              </div>

              <p className="text-xs sm:text-sm text-[#94A3B8] leading-relaxed">
                {ch.narrative}
              </p>

              <div className="pt-2 flex items-center justify-between text-xs font-mono">
                <span className="text-[#00D2FF] font-bold">★ {ch.highlightMetric}</span>
                <span className="text-[#64748B]">Audited by Coordinator Agent</span>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </div>
  );
};
