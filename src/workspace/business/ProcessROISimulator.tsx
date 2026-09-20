import React, { useState } from 'react';
import {
  Calculator,
  Play,
  RefreshCw,
} from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { BusinessApiClient } from '../../services/businessApiClient';
import { SimulationResult } from '../../types/businessPlatform';

export const ProcessROISimulator: React.FC = () => {
  const [txCount, setTxCount] = useState<number>(1000);
  const [running, setRunning] = useState(false);
  const [result, setResult] = useState<SimulationResult | null>(null);

  const handleSimulate = async () => {
    try {
      setRunning(true);
      const res = await BusinessApiClient.runSimulation({
        process_id: 'proc_invoice_enterprise_01',
        simulated_transactions_count: txCount,
      });
      setResult(res);
    } catch (err) {
      console.error('Failed to run simulation:', err);
    } finally {
      setRunning(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/60 p-6 rounded-2xl border border-slate-800 backdrop-blur-md">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-indigo-500/10 rounded-xl border border-indigo-500/20 text-indigo-400">
            <Calculator className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white">What-If Process Simulation & ROI Forecaster</h1>
            <p className="text-sm text-slate-400">
              Monte Carlo discrete-event simulation forecasting cost, cycle time, and ROI before production deployment
            </p>
          </div>
        </div>
      </div>

      {/* Simulation Form & Results */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Simulation Controls */}
        <Card className="lg:col-span-1 p-6 bg-slate-900/60 border-slate-800 space-y-4">
          <h2 className="text-base font-bold text-white border-b border-slate-800 pb-3">
            Simulation Parameters
          </h2>

          <div className="space-y-3 text-xs">
            <div>
              <label className="block text-slate-400 mb-1">Simulated Transaction Volume</label>
              <input
                type="number"
                value={txCount}
                onChange={(e) => setTxCount(Number(e.target.value))}
                className="w-full bg-slate-800 border border-slate-700 text-white rounded-lg p-2.5 text-xs"
              />
            </div>

            <div>
              <label className="block text-slate-400 mb-1">Target Process Workflow</label>
              <select className="w-full bg-slate-800 border border-slate-700 text-white rounded-lg p-2.5 text-xs">
                <option value="proc_invoice_enterprise_01">End-to-End Enterprise Invoicing</option>
                <option value="proc_vendor_onboarding">Global Vendor Onboarding</option>
              </select>
            </div>

            <Button
              variant="intelligence"
              className="w-full"
              onClick={handleSimulate}
              disabled={running}
            >
              <span className="flex items-center justify-center gap-2">
                {running ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Play className="w-4 h-4" />}
                Run Monte Carlo Simulation
              </span>
            </Button>
          </div>
        </Card>

        {/* Forecasted Results */}
        <Card className="lg:col-span-2 p-6 bg-slate-900/40 border-slate-800 space-y-5">
          <div className="flex justify-between items-center border-b border-slate-800 pb-3">
            <h2 className="text-base font-semibold text-white">Projected Business Impact & ROI</h2>
            {result && <Badge variant="success">Simulated ({txCount} Transactions)</Badge>}
          </div>

          {result ? (
            <div className="space-y-4">
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/60">
                  <span className="text-slate-400 text-xs block mb-1">Net Cost Savings</span>
                  <span className="text-2xl font-bold text-emerald-400 font-mono">
                    ${result.cost_reduction_usd.toLocaleString()}
                  </span>
                </div>

                <div className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/60">
                  <span className="text-slate-400 text-xs block mb-1">Cycle Time Reduction</span>
                  <span className="text-2xl font-bold text-indigo-300 font-mono">
                    {((result.baseline_cycle_time_sec - result.optimized_cycle_time_sec) / 60).toFixed(0)} mins
                  </span>
                </div>

                <div className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/60">
                  <span className="text-slate-400 text-xs block mb-1">Throughput Boost</span>
                  <span className="text-2xl font-bold text-cyan-300 font-mono">
                    +{result.throughput_increase_pct.toFixed(0)}%
                  </span>
                </div>
              </div>

              <div className="space-y-2 pt-2 border-t border-slate-800 text-xs font-mono text-slate-300">
                <div className="flex justify-between">
                  <span className="text-slate-400">Baseline Legacy Process Cost:</span>
                  <span className="text-white">${result.baseline_cost_usd.toLocaleString()}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">AI-Optimized Autonomous Cost:</span>
                  <span className="text-emerald-400 font-bold">${result.optimized_cost_usd.toLocaleString()}</span>
                </div>
              </div>
            </div>
          ) : (
            <p className="text-slate-500 italic text-sm py-8 text-center">
              Configure parameters and click "Run Monte Carlo Simulation" to forecast process ROI.
            </p>
          )}
        </Card>
      </div>
    </div>
  );
};
