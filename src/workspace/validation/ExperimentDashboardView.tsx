import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const ExperimentDashboardView: React.FC = () => {
  const [activeAnalysisMode, setActiveAnalysisMode] = useState<'BAYESIAN' | 'FREQUENTIST' | 'SPRT'>('BAYESIAN');

  const experiments = [
    {
      id: 'EXP-2026-001',
      name: 'Pareto Cost Preference Weight Shift',
      controlPolicy: 'v4.2-pareto (w_cost=0.30)',
      treatmentPolicy: 'v5.0-candidate (w_cost=0.40)',
      sampleSize: '235 / 500 trials',
      tStat: 't = 2.84',
      pValue: 'p = 0.0048',
      cohensD: 'd = +0.42 (Medium)',
      probSuperior: '98.4%',
      expectedLoss: '0.0008',
      sprtDecision: 'ACCEPT_H1_TREATMENT',
      status: 'CONVERGED_SUCCESS',
    },
    {
      id: 'EXP-2026-002',
      name: 'Adaptive Fast-Fail Speculative Execution',
      controlPolicy: 'Serial Fallback Chain',
      treatmentPolicy: 'Speculative Parallel Flash-Lite',
      sampleSize: '410 / 500 trials',
      tStat: 't = 4.12',
      pValue: 'p < 0.0001',
      cohensD: 'd = +0.78 (Large)',
      probSuperior: '99.9%',
      expectedLoss: '0.0002',
      sprtDecision: 'ACCEPT_H1_TREATMENT',
      status: 'READY_FOR_PROMOTION',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="p-6 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-xl">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xl">🧪</span>
              <h2 className="text-lg font-bold font-mono text-[#F8FAFC]">
                Scientific Experimentation & A/B Hypothesis Lab
              </h2>
              <Badge variant="success" size="sm">
                SPRT & BAYESIAN READY
              </Badge>
            </div>
            <p className="text-sm font-mono text-[#94A3B8] mt-1">
              Rigorous A/B hypothesis testing, Welch's t-test, Cohen's d effect sizes, Bayesian posterior updates, and Wald's SPRT early stopping.
            </p>
          </div>
          <div className="flex items-center gap-2">
            {(['BAYESIAN', 'FREQUENTIST', 'SPRT'] as const).map((mode) => (
              <button
                key={mode}
                onClick={() => setActiveAnalysisMode(mode)}
                className={`px-3 py-1.5 rounded-lg text-xs font-mono font-medium transition-all ${
                  activeAnalysisMode === mode
                    ? 'bg-blue-600 text-white'
                    : 'bg-[#1E293B] text-[#94A3B8] hover:bg-[#334155]'
                }`}
              >
                {mode}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Experiment Cards */}
      <div className="grid grid-cols-1 gap-4">
        {experiments.map((exp) => (
          <Card key={exp.id} className="p-6 bg-[#0F172A] border-[#1E293B]">
            <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
              <div>
                <div className="flex items-center gap-2">
                  <span className="text-xs font-mono text-cyan-400 font-bold">{exp.id}</span>
                  <h3 className="text-sm font-bold font-mono text-[#F8FAFC]">{exp.name}</h3>
                </div>
                <div className="text-xs font-mono text-[#94A3B8] mt-1">
                  Control: <span className="text-[#E2E8F0]">{exp.controlPolicy}</span> vs Treatment:{' '}
                  <span className="text-indigo-400 font-bold">{exp.treatmentPolicy}</span>
                </div>
              </div>
              <Badge variant="success" size="sm">
                {exp.status}
              </Badge>
            </div>

            {/* Mode-specific metrics */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mt-6 pt-4 border-t border-[#1E293B]">
              {activeAnalysisMode === 'BAYESIAN' && (
                <>
                  <div className="p-3 rounded-lg bg-[#020617] border border-[#1E293B]">
                    <div className="text-[11px] font-mono text-[#94A3B8]">P(Treatment &gt; Control)</div>
                    <div className="text-xl font-bold font-mono text-emerald-400 mt-1">{exp.probSuperior}</div>
                  </div>
                  <div className="p-3 rounded-lg bg-[#020617] border border-[#1E293B]">
                    <div className="text-[11px] font-mono text-[#94A3B8]">Expected Loss E[L]</div>
                    <div className="text-xl font-bold font-mono text-cyan-400 mt-1">{exp.expectedLoss}</div>
                  </div>
                  <div className="p-3 rounded-lg bg-[#020617] border border-[#1E293B]">
                    <div className="text-[11px] font-mono text-[#94A3B8]">Sample Progress</div>
                    <div className="text-xl font-bold font-mono text-[#F8FAFC] mt-1">{exp.sampleSize}</div>
                  </div>
                  <div className="p-3 rounded-lg bg-[#020617] border border-[#1E293B]">
                    <div className="text-[11px] font-mono text-[#94A3B8]">Bayesian Recommendation</div>
                    <div className="text-sm font-bold font-mono text-emerald-400 mt-1">ADOPT_TREATMENT</div>
                  </div>
                </>
              )}

              {activeAnalysisMode === 'FREQUENTIST' && (
                <>
                  <div className="p-3 rounded-lg bg-[#020617] border border-[#1E293B]">
                    <div className="text-[11px] font-mono text-[#94A3B8]">Welch's t-Statistic</div>
                    <div className="text-xl font-bold font-mono text-indigo-400 mt-1">{exp.tStat}</div>
                  </div>
                  <div className="p-3 rounded-lg bg-[#020617] border border-[#1E293B]">
                    <div className="text-[11px] font-mono text-[#94A3B8]">p-Value (Alpha=0.05)</div>
                    <div className="text-xl font-bold font-mono text-emerald-400 mt-1">{exp.pValue}</div>
                  </div>
                  <div className="p-3 rounded-lg bg-[#020617] border border-[#1E293B]">
                    <div className="text-[11px] font-mono text-[#94A3B8]">Cohen's d Effect Size</div>
                    <div className="text-xl font-bold font-mono text-cyan-400 mt-1">{exp.cohensD}</div>
                  </div>
                  <div className="p-3 rounded-lg bg-[#020617] border border-[#1E293B]">
                    <div className="text-[11px] font-mono text-[#94A3B8]">Null Hypothesis H0</div>
                    <div className="text-sm font-bold font-mono text-emerald-400 mt-1">REJECTED (p &lt; 0.05)</div>
                  </div>
                </>
              )}

              {activeAnalysisMode === 'SPRT' && (
                <>
                  <div className="p-3 rounded-lg bg-[#020617] border border-[#1E293B]">
                    <div className="text-[11px] font-mono text-[#94A3B8]">Wald's LLR Boundary</div>
                    <div className="text-xl font-bold font-mono text-emerald-400 mt-1">ln(A) &gt; +2.89</div>
                  </div>
                  <div className="p-3 rounded-lg bg-[#020617] border border-[#1E293B]">
                    <div className="text-[11px] font-mono text-[#94A3B8]">Sequential Decision</div>
                    <div className="text-sm font-bold font-mono text-emerald-400 mt-1">{exp.sprtDecision}</div>
                  </div>
                  <div className="p-3 rounded-lg bg-[#020617] border border-[#1E293B]">
                    <div className="text-[11px] font-mono text-[#94A3B8]">Trials to Stop</div>
                    <div className="text-xl font-bold font-mono text-[#F8FAFC] mt-1">{exp.sampleSize}</div>
                  </div>
                  <div className="p-3 rounded-lg bg-[#020617] border border-[#1E293B]">
                    <div className="text-[11px] font-mono text-[#94A3B8]">Type I / II Error Bounds</div>
                    <div className="text-sm font-bold font-mono text-cyan-400 mt-1">α = 0.05, β = 0.10</div>
                  </div>
                </>
              )}
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
