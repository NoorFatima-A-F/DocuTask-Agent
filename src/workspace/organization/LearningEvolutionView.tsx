import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const LearningEvolutionView: React.FC = () => {
  const knowledgeItems = [
    {
      dept: 'Optical Perception (dept_ocr)',
      category: 'HEURISTIC',
      title: 'Bilateral Filtering for Thermal Receipts',
      content: 'Apply bilateral filter with diameter 9 and sigmaColor 75 when document luminance variance is < 12.0.',
      gain: '+3.8% Accuracy Boost',
      confidence: '96.0%',
    },
    {
      dept: 'Structured Extraction (dept_extraction)',
      category: 'PROMPT_TEMPLATE',
      title: 'European VAT Multi-Rate Extraction Anchor',
      content: 'Explicitly prompt Gemini 2.5 Flash with table line-item VAT rate mapping when vendor country is EU.',
      gain: '+4.5% Accuracy Boost',
      confidence: '98.0%',
    },
    {
      dept: 'Mathematical Validation (dept_validation)',
      category: 'SCHEMA_RULE',
      title: 'Dynamic Currency Symbol Normalization',
      content: 'Strip non-breaking currency whitespace characters prior to decimal invariant arithmetic evaluation.',
      gain: '+1.2% Accuracy Boost',
      confidence: '99.0%',
    },
  ];

  const retrospectives = [
    {
      dept: 'Optical Perception',
      score: '0.94',
      gain: '+4.2% projected speedup',
      bottleneck: 'Multi-column skewed tables caused 15ms latency tail in LayoutLM bounding box assignment.',
      action: 'Synthesize pre-rotation OpenCV affine transform before LayoutLM tokenization.',
    },
    {
      dept: 'Structured Extraction',
      score: '0.96',
      gain: '+6.5% projected speedup',
      bottleneck: 'Nested invoice line-item sub-tables required single retry due to trailing semicolon.',
      action: 'Update extraction prompt with explicit JSON schema regex validator.',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 p-5 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-xl">
        <div>
          <div className="flex items-center gap-2">
            <span className="text-2xl">🧠</span>
            <h2 className="text-xl font-bold text-[#F8FAFC]">Organizational Learning & Cognitive Evolution</h2>
            <Badge variant="intelligence" size="sm">Self-Improving Enterprise</Badge>
          </div>
          <p className="text-sm text-[#94A3B8] mt-1">
            Independent departmental retrospectives, procedural memory accumulation, and organization-wide policy synthesis.
          </p>
        </div>

        <div className="text-right">
          <div className="text-xs text-[#94A3B8]">Cumulative Accuracy Gain</div>
          <div className="text-2xl font-bold font-mono text-[#10B981]">+9.5% Macro Boost</div>
        </div>
      </div>

      {/* Department Knowledge Base */}
      <Card className="p-5 bg-[#0F172A] border-[#1E293B] space-y-4">
        <div className="text-sm font-bold text-[#F8FAFC]">Active Department Procedural Memories</div>
        <div className="space-y-3">
          {knowledgeItems.map((item, idx) => (
            <div key={idx} className="p-4 rounded-xl bg-[#020617] border border-[#1E293B] space-y-2">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <span className="text-xs font-bold font-mono text-[#38BDF8]">{item.dept}</span>
                  <Badge variant="intelligence" size="sm">{item.category}</Badge>
                </div>
                <div className="flex items-center gap-2">
                  <Badge variant="success" size="sm">{item.gain}</Badge>
                  <span className="text-xs font-mono text-[#64748B]">Conf: {item.confidence}</span>
                </div>
              </div>

              <div className="text-sm font-semibold text-[#F8FAFC]">{item.title}</div>
              <p className="text-xs text-[#94A3B8] font-mono">{item.content}</p>
            </div>
          ))}
        </div>
      </Card>

      {/* Retrospectives */}
      <Card className="p-5 bg-[#0F172A] border-[#1E293B] space-y-4">
        <div className="text-sm font-bold text-[#F8FAFC]">Recent Post-Mission Departmental Retrospectives</div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {retrospectives.map((r, idx) => (
            <div key={idx} className="p-4 rounded-xl bg-[#020617] border border-[#1E293B] space-y-2 text-xs font-mono">
              <div className="flex items-center justify-between">
                <span className="font-bold text-[#F8FAFC]">{r.dept}</span>
                <span className="text-[#10B981]">{r.gain}</span>
              </div>
              <div className="text-[#EF4444] pt-1">
                <span className="text-[#64748B] block text-[10px]">IDENTIFIED BOTTLENECK:</span>
                {r.bottleneck}
              </div>
              <div className="text-[#00D2FF] pt-1">
                <span className="text-[#64748B] block text-[10px]">SYNTHESIZED ACTION:</span>
                {r.action}
              </div>
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
};
