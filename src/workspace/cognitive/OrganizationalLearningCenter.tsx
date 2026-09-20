import React, { useState, useEffect } from 'react';
import { BookOpen, RefreshCw } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';

export const OrganizationalLearningCenter: React.FC = () => {
  const [insights, setInsights] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  const loadData = async () => {
    setLoading(true);
    try {
      const res = await fetch('/api/v1/cognitive/learning/insights?tenant_id=default-tenant');
      if (res.ok) setInsights(await res.json());
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-slate-100 flex items-center gap-2">
            <BookOpen className="w-7 h-7 text-indigo-400" />
            Autonomous Organizational Learning Center
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Continuous distillation of cross-agent best practices, pattern mining, and emergent operational policies.
          </p>
        </div>
        <Button variant="outline" onClick={loadData}>
          <span className="flex items-center gap-2">
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            Refresh
          </span>
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {insights.map((item, idx) => (
          <Card key={idx} className="p-5 bg-slate-900/60 border-slate-800 space-y-3">
            <div className="flex justify-between items-center">
              <Badge variant="outline" className="text-indigo-400 border-indigo-500/30">
                {item.action || 'BEST_PRACTICE_DISTILLED'}
              </Badge>
              <span className="text-[10px] text-slate-500 font-mono">{item.discovered_at?.slice(0, 16)}</span>
            </div>
            <h3 className="text-base font-semibold text-slate-200">{item.topic}</h3>
            <p className="text-xs text-slate-300 bg-slate-800/40 p-3 rounded border border-slate-700/50">
              {item.observation}
            </p>
            <div className="pt-2 border-t border-slate-800 flex justify-between items-center text-xs text-emerald-400">
              <span>Policy: {item.recommended_policy}</span>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
