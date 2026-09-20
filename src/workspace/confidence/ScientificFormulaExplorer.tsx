import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Calculator } from 'lucide-react';

export const ScientificFormulaExplorer: React.FC = () => {
  const formulas = [
    {
      name: 'WeightedEnsemble (v1.3.0)',
      type: 'LINEAR_ENSEMBLE',
      mathExpr: 'C(\\vec{f}) = \\frac{\\sum_{i=1}^n w_i \\cdot f_i}{\\sum_{i=1}^n w_i}',
      calibratedExpr: 'C_{calibrated} = \\sigma\\left(\\frac{\\text{logit}(C(\\vec{f}))}{T}\\right)',
      variables: ['f_i: Feature values in [0, 1]', 'w_i: Policy importance weight', 'T = 1.05: Temperature scaling parameter'],
      status: 'ACTIVE_DEFAULT',
    },
    {
      name: 'BayesianInference (v2.0.0)',
      type: 'PROBABILISTIC_PRIOR_POSTERIOR',
      mathExpr: 'P(H|E) = \\frac{P(E|H) \\cdot P(H)}{P(E|H) \\cdot P(H) + P(E|\\neg H) \\cdot P(\\neg H)}',
      calibratedExpr: 'P_{calibrated} = \\text{Isotonic}(P(H|E))',
      variables: ['P(H): Prior historical success rate', 'P(E|H): Likelihood given verified evidence', 'P(E|¬H): False positive likelihood'],
      status: 'SUPPORTED',
    },
    {
      name: 'ReliabilityMultiplication (v1.1.0)',
      type: 'STOCHASTIC_SERIES_PIPELINE',
      mathExpr: 'R_{total} = \\prod_{i=1}^m R_i',
      calibratedExpr: 'R_{calibrated} = \\min(1.0, R_{total} \\cdot (1.0 + \\epsilon))',
      variables: ['R_i: Independent stage reliability bounds'],
      status: 'SUPPORTED',
    },
  ];

  return (
    <div className="p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6">
        <div className="space-y-1">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-gradient-to-br from-purple-500/20 to-cyan-500/20 border border-purple-500/30 rounded-xl text-purple-400">
              <Calculator className="w-5 h-5" />
            </div>
            <div>
              <h1 className="text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2">
                Scientific Formula Explorer & Mathematical Foundations
                <Badge variant="success" size="sm">LaTeX Validated</Badge>
              </h1>
              <p className="text-xs text-[#94A3B8] font-mono">
                Inspect transparent mathematical formulas, intermediate sensitivity, and calibration transformations
              </p>
            </div>
          </div>
        </div>

        <Badge variant="intelligence" size="md">Zero Hidden Formulas</Badge>
      </div>

      {/* Formula Cards */}
      <div className="space-y-4 font-mono">
        {formulas.map(f => (
          <Card key={f.name} className="p-5 rounded-2xl border border-[#1E293B] bg-[#0F172A] space-y-4">
            <div className="flex flex-wrap items-center justify-between gap-2 border-b border-[#1E293B] pb-3">
              <div>
                <h3 className="text-sm font-bold text-white">{f.name}</h3>
                <span className="text-[10px] text-[#64748B]">{f.type}</span>
              </div>
              <Badge variant={f.status === 'ACTIVE_DEFAULT' ? 'success' : 'outline'} size="sm">
                {f.status}
              </Badge>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 text-xs">
              <div className="p-4 bg-[#131D35] rounded-xl border border-[#1E293B] space-y-2">
                <span className="text-[10px] text-[#64748B] block">MATHEMATICAL EXPRESSION</span>
                <code className="text-cyan-400 font-bold text-sm block py-1">{f.mathExpr}</code>
                <span className="text-[10px] text-[#94A3B8] block">Post-Calibration: {f.calibratedExpr}</span>
              </div>

              <div className="p-4 bg-[#131D35] rounded-xl border border-[#1E293B] space-y-2">
                <span className="text-[10px] text-[#64748B] block">VARIABLES & ATTRIBUTES</span>
                <ul className="space-y-1 text-[#F8FAFC] text-[11px]">
                  {f.variables.map((v, i) => (
                    <li key={i} className="flex items-center gap-2">
                      <span className="w-1.5 h-1.5 rounded-full bg-cyan-400" />
                      <span>{v}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
