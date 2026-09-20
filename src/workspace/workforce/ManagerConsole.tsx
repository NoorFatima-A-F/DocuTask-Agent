import React, { useState, useEffect } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { ManagerReviewRecord } from '../../types/workforce';

export const ManagerConsole: React.FC = () => {
  const [reviews, setReviews] = useState<ManagerReviewRecord[]>([]);

  useEffect(() => {
    // Seed default review display
    setReviews([
      {
        id: 'rev-q1-doc-spec',
        tenant_id: 'default-tenant',
        employee_id: 'emp-doc-spec-01',
        manager_id: 'emp-eng-vp',
        review_period: '2026-Q1',
        performance_rating: 4.9,
        strengths: ['Zero error rate in table extraction', 'High reuse of experience memory'],
        areas_for_growth: ['Can mentor junior parser agents'],
        workload_balance_action: 'OPTIMAL',
        promotion_recommended: true,
        created_at: new Date().toISOString()
      }
    ]);
  }, []);

  return (
    <div className="space-y-6">
      <div className="bg-slate-900/60 p-5 rounded-2xl border border-slate-800">
        <h1 className="text-2xl font-bold text-white flex items-center gap-3">
          <span className="p-2 bg-blue-500/20 text-blue-400 rounded-xl">👔</span>
          Manager Console & Review Studio
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          Departmental Coaching, Workload Leveling, and Performance Appraisals
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {reviews.map((r) => (
          <Card key={r.id} className="p-5 bg-slate-900/50 border-slate-800">
            <div className="flex justify-between items-start mb-3">
              <div>
                <div className="text-base font-bold text-white">Employee: {r.employee_id}</div>
                <div className="text-xs text-slate-400">Manager: {r.manager_id} • Period: {r.review_period}</div>
              </div>
              <Badge variant="default">Rating: {r.performance_rating} / 5.0</Badge>
            </div>

            <div className="space-y-3 my-4 text-xs">
              <div>
                <div className="font-semibold text-emerald-400 mb-1">Key Strengths:</div>
                <ul className="list-disc list-inside text-slate-300 space-y-0.5">
                  {r.strengths.map((s, idx) => <li key={idx}>{s}</li>)}
                </ul>
              </div>
              <div>
                <div className="font-semibold text-amber-400 mb-1">Growth Opportunities:</div>
                <ul className="list-disc list-inside text-slate-300 space-y-0.5">
                  {r.areas_for_growth.map((g, idx) => <li key={idx}>{g}</li>)}
                </ul>
              </div>
            </div>

            <div className="border-t border-slate-800 pt-3 flex justify-between items-center text-xs">
              <span className="text-slate-400">Action: <strong className="text-white">{r.workload_balance_action}</strong></span>
              {r.promotion_recommended && (
                <Badge variant="default">★ Promotion Recommended</Badge>
              )}
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
