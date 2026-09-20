/**
 * Planner Self-Evaluation & Calibration Card Component.
 * Displays predicted vs actual execution metrics, calibration scores, and automated feedback tuning loops.
 */

import React, { useState, useEffect } from 'react';
import { PlanCalibrationMetric } from '../../types/autonomousPlanning';
import { PlanningApiClient } from '../../services/planningApiClient';

interface PlannerCalibrationCardProps {
  missionId?: string;
}

export const PlannerCalibrationCardView: React.FC<PlannerCalibrationCardProps> = ({
  missionId = 'mission_active_001',
}) => {
  const [metric, setMetric] = useState<PlanCalibrationMetric | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    loadCalibration();
  }, [missionId]);

  const loadCalibration = async () => {
    setLoading(true);
    try {
      const data = await PlanningApiClient.evaluateMission(missionId, 1920.0, 0.0039, 0.99);
      setMetric(data);
    } catch (err) {
      console.error('Failed to load calibration', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading || !metric) {
    return (
      <div className="flex items-center justify-center p-8 text-slate-400">
        <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-indigo-500 mr-2"></div>
        <span>Calculating Calibration Errors...</span>
      </div>
    );
  }

  const comp = metric.comparison;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 text-slate-100 shadow-2xl space-y-5">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between border-b border-slate-800 pb-3 gap-3">
        <div>
          <div className="flex items-center space-x-2">
            <span className="px-2 py-0.5 text-[10px] font-bold uppercase tracking-wider bg-indigo-500/20 text-indigo-400 border border-indigo-500/30 rounded">
              Self-Evaluation Loop
            </span>
            <span className="text-xs text-slate-400 font-mono">Mission: {metric.mission_id}</span>
          </div>
          <h3 className="text-lg font-bold text-white mt-1">Planner Calibration & Drift Analysis</h3>
        </div>

        <div className="bg-emerald-950/40 border border-emerald-500/40 px-3 py-1.5 rounded-lg text-right">
          <span className="text-[10px] uppercase text-emerald-300 font-semibold block">Model Calibration</span>
          <span className="text-sm font-bold text-emerald-400 font-mono">
            {(metric.overall_calibration_score * 100).toFixed(1)}%
          </span>
        </div>
      </div>

      {/* Expected vs Actual Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs font-mono">
        <div className="bg-slate-950/60 p-3 rounded-lg border border-slate-800">
          <span className="text-slate-400 block text-[10px] uppercase">Execution Latency</span>
          <div className="flex justify-between mt-1 text-slate-200">
            <span>Pred: {comp.predicted_latency_ms.toFixed(0)}ms</span>
            <span>Act: {comp.actual_latency_ms.toFixed(0)}ms</span>
          </div>
          <div className="text-emerald-400 text-[11px] mt-1">
            Delta: {comp.latency_delta_ms > 0 ? `+${comp.latency_delta_ms.toFixed(0)}ms` : `${comp.latency_delta_ms.toFixed(0)}ms`} (err: {comp.latency_error_pct.toFixed(1)}%)
          </div>
        </div>

        <div className="bg-slate-950/60 p-3 rounded-lg border border-slate-800">
          <span className="text-slate-400 block text-[10px] uppercase">Cost Consumption</span>
          <div className="flex justify-between mt-1 text-slate-200">
            <span>Pred: ${comp.predicted_cost_usd.toFixed(4)}</span>
            <span>Act: ${comp.actual_cost_usd.toFixed(4)}</span>
          </div>
          <div className="text-emerald-400 text-[11px] mt-1">
            Delta: ${comp.cost_delta_usd.toFixed(4)} (err: {comp.cost_error_pct.toFixed(1)}%)
          </div>
        </div>

        <div className="bg-slate-950/60 p-3 rounded-lg border border-slate-800">
          <span className="text-slate-400 block text-[10px] uppercase">Validation Accuracy</span>
          <div className="flex justify-between mt-1 text-slate-200">
            <span>Pred: {(comp.predicted_accuracy * 100).toFixed(1)}%</span>
            <span>Act: {(comp.actual_accuracy * 100).toFixed(1)}%</span>
          </div>
          <div className="text-emerald-400 text-[11px] mt-1">
            Gain: +{(comp.accuracy_delta * 100).toFixed(2)}%
          </div>
        </div>
      </div>

      {/* Root Cause & Tuning Recommendations */}
      <div className="bg-slate-950/40 p-3.5 rounded-lg border border-slate-800/80 space-y-2 text-xs">
        <div className="font-bold text-slate-300 uppercase tracking-wider text-[11px]">
          Root Cause & Automated Tuning
        </div>
        <div className="text-slate-400">
          {metric.root_causes.map((rc, i) => (
            <p key={i} className="font-sans leading-relaxed text-slate-300">
              • {rc}
            </p>
          ))}
        </div>
        {Object.keys(metric.tuning_recommendations).length > 0 && (
          <div className="pt-2 border-t border-slate-800/60 font-mono text-[11px] text-indigo-300">
            {Object.entries(metric.tuning_recommendations).map(([k, v]) => (
              <div key={k} className="flex space-x-2">
                <span className="text-slate-500 uppercase">{k}:</span>
                <span>{v}</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
