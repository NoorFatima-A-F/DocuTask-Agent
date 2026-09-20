import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { BookOpen, Zap, Award, ArrowRight } from 'lucide-react';

export const OrganizationalLearningDashboard: React.FC = () => {
  const learningSummary = {
    totalReflections: 12,
    totalMinedLessons: 28,
    activeStrategies: 7,
    knowledgeRecords: 44,
    avgConfidence: 96.2,
    governanceApprovalRate: 92.5,
  };

  const minedLessons = [
    {
      id: 'lsn-001',
      title: 'Parallel Wavefront OCR Sharding',
      category: 'CONCURRENCY_ALLOCATION',
      confidence: 96.5,
      rulesCount: 3,
      speedup: '+34.2%',
      guidance: 'Partition document batches > 10 pages into 4 parallel worker shards with jittered retry.',
      status: 'VERIFIED',
    },
    {
      id: 'lsn-002',
      title: 'SMT Invariant Pre-Validation Gating',
      category: 'VALIDATION_STRATEGY',
      confidence: 99.1,
      rulesCount: 2,
      speedup: '100% Invariance',
      guidance: 'Enforce mathematical SMT verification before emitting confidence score to downstream subscribers.',
      status: 'VERIFIED',
    },
    {
      id: 'lsn-003',
      title: 'Exponential Backoff on Upstream Throttling',
      category: 'RESILIENCE_STRATEGY',
      confidence: 97.8,
      rulesCount: 4,
      speedup: 'Zero Dropped Tasks',
      guidance: 'Apply base 250ms backoff with exponential multiplier upon encountering HTTP 429 status codes.',
      status: 'VERIFIED',
    },
  ];

  return (
    <div className="p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-gradient-to-br from-cyan-500/20 to-blue-500/20 border border-cyan-500/30 rounded-xl text-cyan-400">
            <BookOpen className="w-5 h-5" />
          </div>
          <div>
            <h1 className="text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2">
              Organizational Learning & Knowledge Intelligence
              <Badge variant="intelligence" size="sm">Phase 13.5 Core</Badge>
            </h1>
            <p className="text-xs text-[#94A3B8] font-mono">
              Continuous institutional learning pipeline extracting verified lessons, execution strategies, and evolutionary rules
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <Badge variant="success" size="md">Self-Improving Autonomous System</Badge>
        </div>
      </div>

      {/* Top Level Metric Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
        <Card className="p-4 bg-[#0F172A] border border-[#1E293B] rounded-xl font-mono">
          <span className="text-[11px] text-[#64748B] block">Total Reflections</span>
          <span className="text-2xl font-bold text-white mt-1 block">{learningSummary.totalReflections}</span>
        </Card>
        <Card className="p-4 bg-[#0F172A] border border-[#1E293B] rounded-xl font-mono">
          <span className="text-[11px] text-[#64748B] block">Mined Lessons</span>
          <span className="text-2xl font-bold text-cyan-400 mt-1 block">{learningSummary.totalMinedLessons}</span>
        </Card>
        <Card className="p-4 bg-[#0F172A] border border-[#1E293B] rounded-xl font-mono">
          <span className="text-[11px] text-[#64748B] block">Active Strategies</span>
          <span className="text-2xl font-bold text-indigo-400 mt-1 block">{learningSummary.activeStrategies}</span>
        </Card>
        <Card className="p-4 bg-[#0F172A] border border-[#1E293B] rounded-xl font-mono">
          <span className="text-[11px] text-[#64748B] block">Knowledge Records</span>
          <span className="text-2xl font-bold text-purple-400 mt-1 block">{learningSummary.knowledgeRecords}</span>
        </Card>
        <Card className="p-4 bg-[#0F172A] border border-[#1E293B] rounded-xl font-mono">
          <span className="text-[11px] text-[#64748B] block">Mean Confidence</span>
          <span className="text-2xl font-bold text-emerald-400 mt-1 block">{learningSummary.avgConfidence}%</span>
        </Card>
        <Card className="p-4 bg-[#0F172A] border border-[#1E293B] rounded-xl font-mono">
          <span className="text-[11px] text-[#64748B] block">Gov Approval Rate</span>
          <span className="text-2xl font-bold text-teal-400 mt-1 block">{learningSummary.governanceApprovalRate}%</span>
        </Card>
      </div>

      {/* Autonomous Learning Pipeline Visualizer */}
      <Card className="p-6 rounded-2xl border border-[#1E293B] bg-gradient-to-br from-[#0F172A] to-[#121B2F] font-mono space-y-4">
        <div className="flex items-center justify-between border-b border-[#1E293B] pb-3">
          <span className="text-xs font-bold text-white flex items-center gap-2">
            <Zap className="w-4 h-4 text-amber-400" />
            Autonomous Scientific Learning Cycle
          </span>
          <span className="text-[11px] text-[#94A3B8]">Hypothesis &rarr; Replay Validation &rarr; Promotion</span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-5 gap-3 pt-2 text-center text-xs">
          <div className="p-3 bg-[#0B1120] border border-[#1E293B] rounded-xl space-y-1">
            <div className="w-6 h-6 rounded-full bg-indigo-500/20 text-indigo-400 flex items-center justify-center mx-auto text-[11px] font-bold">1</div>
            <span className="font-bold text-white block">Mission Replay</span>
            <span className="text-[10px] text-[#64748B] block">Immutable event traces</span>
          </div>
          <div className="p-3 bg-[#0B1120] border border-[#1E293B] rounded-xl space-y-1">
            <div className="w-6 h-6 rounded-full bg-cyan-500/20 text-cyan-400 flex items-center justify-center mx-auto text-[11px] font-bold">2</div>
            <span className="font-bold text-white block">Reflection</span>
            <span className="text-[10px] text-[#64748B] block">Macro & Micro KPIs</span>
          </div>
          <div className="p-3 bg-[#0B1120] border border-[#1E293B] rounded-xl space-y-1">
            <div className="w-6 h-6 rounded-full bg-purple-500/20 text-purple-400 flex items-center justify-center mx-auto text-[11px] font-bold">3</div>
            <span className="font-bold text-white block">Pattern Mining</span>
            <span className="text-[10px] text-[#64748B] block">Rule extraction</span>
          </div>
          <div className="p-3 bg-[#0B1120] border border-[#1E293B] rounded-xl space-y-1">
            <div className="w-6 h-6 rounded-full bg-amber-500/20 text-amber-400 flex items-center justify-center mx-auto text-[11px] font-bold">4</div>
            <span className="font-bold text-white block">Counterfactual Sim</span>
            <span className="text-[10px] text-[#64748B] block">Monte-Carlo replays</span>
          </div>
          <div className="p-3 bg-[#0B1120] border border-[#1E293B] rounded-xl space-y-1">
            <div className="w-6 h-6 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center mx-auto text-[11px] font-bold">5</div>
            <span className="font-bold text-white block">Governance Gate</span>
            <span className="text-[10px] text-[#64748B] block">Automated promotion</span>
          </div>
        </div>
      </Card>

      {/* Institutional Mined Lessons Section */}
      <div className="space-y-4 font-mono">
        <div className="flex items-center justify-between">
          <h2 className="text-sm font-bold text-white flex items-center gap-2">
            <Award className="w-4 h-4 text-cyan-400" />
            Recently Mined Institutional Lessons
          </h2>
          <span className="text-xs text-[#94A3B8]">Total Lessons: {minedLessons.length}</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {minedLessons.map((lesson) => (
            <Card key={lesson.id} className="p-5 rounded-xl border border-[#1E293B] bg-[#0F172A] space-y-3 flex flex-col justify-between">
              <div className="space-y-2">
                <div className="flex items-start justify-between gap-2">
                  <Badge variant="intelligence" size="sm">{lesson.category}</Badge>
                  <span className="text-xs font-bold text-emerald-400">{lesson.confidence}% Conf</span>
                </div>
                <h3 className="text-sm font-bold text-white">{lesson.title}</h3>
                <p className="text-xs text-[#94A3B8] leading-relaxed">{lesson.guidance}</p>
              </div>

              <div className="pt-3 border-t border-[#1E293B] flex items-center justify-between text-xs">
                <span className="text-cyan-400 font-bold flex items-center gap-1">
                  <Zap className="w-3.5 h-3.5" />
                  {lesson.speedup}
                </span>
                <span className="text-[#64748B] flex items-center gap-1">
                  {lesson.rulesCount} Rules <ArrowRight className="w-3 h-3 text-[#94A3B8]" />
                </span>
              </div>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
};
